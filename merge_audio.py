import os
import subprocess
import re
import json

def extract_season_episode(file_name):
    # Extract season and episode number from the file name
    match = re.search(r'S(\d{1,2}) E(\d{1,2})', file_name)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        return season, episode
    else:
        print(f"Warning: Could not extract season and episode from '{file_name}'.")
        return None, None

def get_episode_files(root_path, ignore_folders=None):
    if ignore_folders is None:
        ignore_folders = []
    episode_dict = {}
    for root, dirs, files in os.walk(root_path):
        # Ignore specified folders
        dirs[:] = [d for d in dirs if d not in ignore_folders]
        for file in files:
            if file.endswith(('.mkv', '.mp4', '.avi')):
                file_path = os.path.join(root, file)
                season, episode = extract_season_episode(file)
                if season is not None and episode is not None:
                    key = f"S{season:02d}E{episode:02d}"
                    episode_dict[key] = file_path
    return episode_dict

def match_episodes(source1_dict, source2_dict):
    # Create a list of common episode keys
    common_keys = set(source1_dict.keys()) & set(source2_dict.keys())
    matched_episodes = []
    for key in sorted(common_keys):
        source1_file = source1_dict[key]
        source2_file = source2_dict[key]
        matched_episodes.append((key, source1_file, source2_file))
    if not matched_episodes:
        print("No matching episodes found.")
    else:
        print(f"{len(matched_episodes)} matching episodes found.")
    return matched_episodes

def extract_english_audio_index(source2_file):
    print(f"Extracting audio stream information from '{source2_file}'...")
    # Use ffprobe in JSON format
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream',
        '-of', 'json', source2_file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running ffprobe on '{source2_file}'.")
        print(result.stderr)
        return None
    try:
        ffprobe_output = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing ffprobe output: {e}")
        return None
    streams = ffprobe_output.get('streams', [])
    if not streams:
        print(f"No streams found in '{source2_file}'.")
        return None
    print(f"Streams found in '{source2_file}':")
    for stream in streams:
        index = stream.get('index')
        codec_type = stream.get('codec_type')
        tags = stream.get('tags', {})
        language = tags.get('language', 'unknown')
        title = tags.get('title', 'no title')
        print(f"  Stream #{index}: Type={codec_type}, Language={language}, Title={title}")
    english_stream_index = None
    for stream in streams:
        index = stream.get('index')
        codec_type = stream.get('codec_type')
        if codec_type != 'audio':
            continue
        tags = stream.get('tags', {})
        language = tags.get('language', '').lower()
        title = tags.get('title', '').lower()
        if 'eng' in language or 'english' in title:
            english_stream_index = index
            print(f"English audio stream found: Stream #{english_stream_index}")
            break
    if english_stream_index is None:
        print(f"Error: No English audio stream found in '{source2_file}'.")
        return None
    return english_stream_index

def get_stream_indices(file_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream',
        '-of', 'json', file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running ffprobe on '{file_path}'.")
        print(result.stderr)
        return None
    try:
        ffprobe_output = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing ffprobe output: {e}")
        return None
    streams = ffprobe_output.get('streams', [])
    if not streams:
        print(f"No streams found in '{file_path}'.")
        return None
    video_index = None
    audio_indices = []
    print(f"Streams in '{file_path}':")
    for stream in streams:
        index = stream.get('index')
        codec_type = stream.get('codec_type')
        codec_name = stream.get('codec_name')
        tags = stream.get('tags', {})
        language = tags.get('language', 'unknown')
        print(f"  Stream #{index}: Type={codec_type}, Codec={codec_name}, Language={language}")
        if codec_type == 'video' and video_index is None:
            video_index = index
        elif codec_type == 'audio':
            audio_indices.append((index, language))
    return video_index, audio_indices

def merge_audio_video(source1_file, english_audio_index, source2_file, output_file):
    print(f"Adding audio stream to '{source1_file}'...")
    # Get indices of video and audio streams in source1_file
    video_index, source1_audio_indices = get_stream_indices(source1_file)
    if video_index is None or not source1_audio_indices:
        print(f"Error: Could not find video or audio streams in '{source1_file}'.")
        return False
    # Assume the first audio stream is Japanese
    japanese_audio_index = source1_audio_indices[0][0]
    print(f"Video index in '{source1_file}': {video_index}")
    print(f"Japanese audio stream index in '{source1_file}': {japanese_audio_index}")
    # Get the language of the audio stream from source1_file
    japanese_audio_language = source1_audio_indices[0][1]
    # Execute ffmpeg command to merge
    cmd = [
        'ffmpeg', '-y',
        '-i', source1_file,
        '-i', source2_file,
        '-map', f'0:{video_index}',          # Video from source1_file
        '-map', f'0:{japanese_audio_index}', # Japanese audio from source1_file
        '-map', f'1:{english_audio_index}',  # English audio from source2_file
        '-metadata:s:a:0', f'language={japanese_audio_language}',
        '-metadata:s:a:1', 'language=eng',
        '-c', 'copy', output_file
    ]
    print(f"Executing ffmpeg with the following command:\n{' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error merging '{source1_file}' with the English audio stream.")
        return False
    return True

def process_episodes(matched_episodes, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for key, source1_file, source2_file in matched_episodes:
        print(f"\nProcessing episode: {key}")
        output_file = os.path.join(output_folder, os.path.basename(source1_file))
        # Extract the index of the English audio stream
        english_audio_index = extract_english_audio_index(source2_file)
        if english_audio_index is None:
            continue
        # Merge the audio stream
        success = merge_audio_video(source1_file, english_audio_index, source2_file, output_file)
        if not success:
            continue
        print(f"Episode '{key}' processed successfully.")
    print("\nProcessing completed.")

if __name__ == "__main__":
    # Paths to the folders
    source1_path = "/path/to/Source1"
    source2_path = "/path/to/Source2"
    output_folder = "/path/to/Output"

    # Ignore specific folders in the source2 path
    ignore_folders = ['OVAs']

    # Get the episode files
    print("Searching for episodes in the Source1 folder...")
    source1_episodes = get_episode_files(source1_path)
    print(f"{len(source1_episodes)} episodes found in the Source1 folder.")

    print("\nSearching for episodes in the Source2 folder...")
    source2_episodes = get_episode_files(source2_path, ignore_folders)
    print(f"{len(source2_episodes)} episodes found in the Source2 folder.")

    # Find matching episodes
    print("\nMatching episodes...")
    matched_episodes = match_episodes(source1_episodes, source2_episodes)

    if matched_episodes:
        # Process the episodes
        process_episodes(matched_episodes, output_folder)
    else:
        print("No episodes to process.")
