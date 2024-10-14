import os
import subprocess

def get_output_files(output_folder):
    output_files = {}
    for file in os.listdir(output_folder):
        if file.endswith('.mkv'):
            key = file  # e.g., "Episode S01 E01.mkv"
            output_files[key] = os.path.join(output_folder, file)
    return output_files

def get_source2_files(source2_folder):
    source2_files = {}
    for file in os.listdir(source2_folder):
        if file.endswith('.mkv') and 'English Dub' in file:
            key = file.replace(' English Dub', '')  # Remove " English Dub" from the filename
            source2_files[key] = os.path.join(source2_folder, file)
    return source2_files

def add_subtitles_to_output(output_files, source2_files):
    for key in output_files:
        output_file = output_files[key]
        source2_file = source2_files.get(key)
        if source2_file:
            print(f"Adding subtitles to '{output_file}'...")
            # Create a temporary file for the new output
            temp_output = output_file + '.temp.mkv'
            # ffmpeg command to add subtitles
            cmd = [
                'ffmpeg', '-y',
                '-i', output_file,
                '-i', source2_file,
                '-map', '0',
                '-map', '1:s',  # All subtitle streams from source2_file
                '-c', 'copy',
                temp_output
            ]
            print(f"Executing ffmpeg with the following command:\n{' '.join(cmd)}")
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"Error adding subtitles to '{output_file}'.")
                continue
            # Replace the original file with the new file
            os.replace(temp_output, output_file)
            print(f"Subtitles added successfully to '{output_file}'.")
        else:
            print(f"No corresponding source file found for '{output_file}'.")

if __name__ == "__main__":
    # Paths to the folders
    output_folder = "/path/to/Output"
    source2_folder = "/path/to/Source2"

    # Get the files in the folders
    output_files = get_output_files(output_folder)
    source2_files = get_source2_files(source2_folder)

    # Add the subtitles
    add_subtitles_to_output(output_files, source2_files)
