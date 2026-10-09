# YT-DLP Helper

A simple Windows desktop application for downloading video and audio using **yt-dlp**, with a graphical interface (no command line usage).

YT-DLP Helper handles the yt-dlp commands for you, allowing you to choose the media format, quality, playlist behavior, and download location without needing to know yt-dlp's command-line syntax.

## Features
- Graphical interface
- Download video as MP4
- Extract audio as MP3
- Choose video quality:
  - Best available
  - 1080p
  - 720p
  - 480p
- Choose MP3 quality:
  - Best available
  - 320 kbps
  - 192 kbps
  - 128 kbps
- Download individual media or playlists
- Chosen download path becomes new default
- Bundled yt-dlp and FFmpeg support
- Standalone Windows application — Python does not need to be installed
- Live download progress and percentage
- Download speed and estimated time remaining
- Playlist item tracking and estimated completion time
- Automatically remembers the last download folder
- Windows-compatible filenames

## Installation

Download `YT-DLP-Helper-v1.0.1-Setup.exe` (or newer version) from the project's
Releases page and run the installer.

The installer creates a Start Menu shortcut and optionally a Desktop shortcut.

## Usage

1. Launch **YT-DLP Helper**.
2. Paste the URL of the media you want to download.
3. Choose Video or Audio.
4. Select the desired quality.
5. Tick whether to download the entire playlist.
6. Select a destination folder.
7. Click **Download**. The application displays download progress, speed, and estimated time remaining.

## Built With

- Python
- yt-dlp
- FFmpeg
- Tkinter
- PyInstaller
- Inno Setup

## Development

The application uses a bundled copy of yt-dlp and FFmpeg rather than relying on them being installed globally on the user's computer.

The Python application is packaged for Windows using PyInstaller, and the resulting application is distributed using an Inno Setup installer.

## Disclaimer

YT-DLP Helper is a convenience interface for yt-dlp. Users are responsible for ensuring that their use of the application complies with applicable laws, website terms, and the rights of content owners.

## Acknowledgments

This project uses **yt-dlp** for media downloading and **FFmpeg** for media processing and conversion.

YT-DLP Helper is an independent project and is not affiliated with the yt-dlp or FFmpeg projects.

YT-DLP Helper was developed with substantial assistance from OpenAI's ChatGPT, which helped with code generation, debugging, GUI development, and application packaging.

Project direction, feature decisions, testing, and release management were handled by the project maintainer.