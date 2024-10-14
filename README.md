# 📼 Video Audio and Subtitle Merger Scripts 🎬

This repository contains three Python scripts designed to automate the process of merging audio tracks 🎧 and subtitles 📝 between video files from different sources. The scripts utilize `ffmpeg` and `ffprobe` to manipulate media files without re-encoding, ensuring fast processing ⚡ and preserving original quality 🎥.

## 📚 Table of Contents

- [Description](#-description)
- [Use Case](#-use-case)
- [Prerequisites](#-prerequisites)
- [Scripts Overview](#-scripts-overview)
  - [1. merge_audio.py](#1-merge_audiopy-)
  - [2. add_subtitles.py](#2-add_subtitlespy-)
  - [3. remove_french_subtitles.py](#3-remove_french_subtitlespy-)
- [Usage](#-usage)
  - [Customizing the Scripts](#-customizing-the-scripts)
  - [1. Merging Audio](#1-merging-audio-)
  - [2. Adding Subtitles](#2-adding-subtitles-)
  - [3. Removing French Subtitles](#3-removing-french-subtitles-)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## 📝 Description

These scripts serve as a foundational base 🛠️ and can be adapted for various use cases. They were developed to combine audio and subtitle tracks from different video sources to create a final product that incorporates the best elements from each source 🌟.

## 🎯 Use Case

In my specific use case, I wanted to manage episodes of **Attack on Titan** 🗡️🛡️. I had different providers from which I downloaded the episodes, resulting in the following situation:

- **Source 1**: High-resolution videos 📺 with poor subtitles 📝❌ and audio 🎧❌.
- **Source 2**: Low-resolution videos 📺🔽 with good subtitles 📝✅ and high-quality audio 🎧✅.

My goal was to combine the best of both sources to obtain high-resolution videos with the best available subtitles and audio tracks 🚀. Additionally, I removed French subtitles 🇫🇷❌ because I do not speak French, and in my case, there were French subtitles present. Of course, you can adjust the scripts according to your own needs.

These scripts automate this process 🤖 and can be customized to perform similar tasks for other projects or media 🎥.

## ⚙️ Prerequisites

- **Python 3.x** 🐍: Ensure you have Python 3 installed on your system.
- **ffmpeg and ffprobe** 🎞️: These must be installed and accessible via the command line.
  - [Download ffmpeg](https://ffmpeg.org/download.html)
- **Basic command-line knowledge** 💻.
- **Backup your data** 💾: Always create backups of your original files to prevent data loss.

## 🛠️ Scripts Overview

### 1. `merge_audio.py` 🎧➕

**Purpose**: Combines audio tracks from two different video sources.

- **Input Folders**:
  - `Source1`: Contains video files with, for example, poor audio quality 🎧❌.
  - `Source2`: Contains video files with better audio quality 🎧✅.
- **Output Folder**:
  - `Output`: Where the combined video files will be saved 💾.

**Functionality**:

- Scans both input folders for video files 🔍.
- Matches episodes based on season and episode numbers extracted from filenames (e.g., `S01 E01`) 🔢.
- Extracts the desired audio track from each `Source2` file 🎧.
- Merges the extracted audio track into the corresponding `Source1` file without re-encoding ⚡.

### 2. `add_subtitles.py` 📝➕

**Purpose**: Adds subtitles from the `Source2` files to the combined output files.

- **Input Folders**:
  - `Output`: Contains the combined video files from the previous step 🎬.
  - `Source2`: Contains the original files with the desired subtitles 📝.
- **Functionality**:
  - Matches files between the `Output` and `Source2` folders 🔄.
  - Adds all subtitle streams from the `Source2` files to the corresponding files in the `Output` folder 🗂️.

### 3. `remove_french_subtitles.py` 🇫🇷❌

**Purpose**: Removes unwanted French subtitles from the video files in the `Output` folder.

- **Input Folder**:
  - `Output`: Contains video files that may have unwanted French subtitles 📝🇫🇷.
- **Functionality**:
  - Scans the `Output` folder for video files 🔍.
  - Removes subtitle streams with language codes `fre` or `fra` 🗑️.
  - Overwrites the original files with the cleaned versions ♻️.

## 🚀 Usage

### 🛠️ Customizing the Scripts

These scripts serve as a base and can be adjusted to fit individual needs ✏️. Depending on your specific requirements, you may need to modify file paths, criteria for matching episodes, or other parameters ⚙️.

### 1. Merging Audio 🎧➕

**Step 1**: Adjust paths in `merge_audio.py`.

- Open `merge_audio.py` in a text editor 📝.
- Modify the following variables to match your folder paths:

  ```python
  source1_path = "/path/to/Source1"
  source2_path = "/path/to/Source2"
  output_folder = "/path/to/Output"
  ```

**Step 2**: Run the script.

```bash
python3 merge_audio.py
```

**Expected Outcome**:

- Combined video files will be saved in the `Output` folder 💾.
- Console output will indicate progress and any errors 🖥️.

### 2. Adding Subtitles 📝➕

**Step 1**: Adjust paths in `add_subtitles.py`.

- Open `add_subtitles.py` in a text editor 📝.
- Modify the following variables:

  ```python
  output_folder = "/path/to/Output"
  source2_folder = "/path/to/Source2"
  ```

**Step 2**: Run the script.

```bash
python3 add_subtitles.py
```

**Expected Outcome**:

- Subtitles from the `Source2` files will be added to the videos in the `Output` folder 🗂️.
- Console output will indicate progress and any errors 🖥️.

### 3. Removing French Subtitles 🇫🇷❌

**Step 1**: Adjust path in `remove_french_subtitles.py`.

- Open `remove_french_subtitles.py` in a text editor 📝.
- Modify the following variable:

  ```python
  output_folder = "/path/to/Output"
  ```

**Step 2**: Run the script.

```bash
python3 remove_french_subtitles.py
```

**Expected Outcome**:

- French subtitles will be removed from the videos in the `Output` folder 🗑️.
- Console output will indicate progress and any errors 🖥️.

## 📄 License

This project is licensed under the MIT License 📜. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ffmpeg** 🎞️: A complete, cross-platform solution to record, convert, and stream audio and video.
- **Python** 🐍: A powerful programming language that simplifies working with media files.
- Special thanks to the original sources of the video files used with these scripts 🌟.

---

**Note**: These scripts are intended for personal use and should be used in compliance with all applicable laws and regulations ⚖️. They serve as a foundation and can be customized according to individual requirements 🛠️. The author is not responsible for any misuse of these scripts.

---

**Enjoy using the scripts!** 🎉
