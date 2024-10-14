import os
import subprocess

def remove_french_subtitles(output_folder):
    for file in os.listdir(output_folder):
        if file.endswith('.mkv'):
            file_path = os.path.join(output_folder, file)
            temp_output = file_path + '.temp.mkv'
            print(f"Removing French subtitles from '{file_path}'...")
            # ffmpeg command to remove French subtitles
            cmd = [
                'ffmpeg', '-y',
                '-i', file_path,
                '-map', '0',
                '-map', '-0:s:m:language:fre',  # Remove subtitles with language 'fre'
                '-map', '-0:s:m:language:fra',  # Remove subtitles with language 'fra'
                '-c', 'copy',
                temp_output
            ]
            print(f"Executing ffmpeg with the following command:\n{' '.join(cmd)}")
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"Error removing French subtitles from '{file_path}'.")
                continue
            # Replace the original file with the new file
            os.replace(temp_output, file_path)
            print(f"French subtitles removed successfully from '{file_path}'.")

if __name__ == "__main__":
    # Path to the Output folder
    output_folder = "/path/to/Output"

    # Remove French subtitles
    remove_french_subtitles(output_folder)
