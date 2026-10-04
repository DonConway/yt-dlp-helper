# YT-DLP Helper

A simple Windows application that provides an easy command-line interface for downloading video and audio using **yt-dlp**.

YT-DLP Helper handles the yt-dlp commands for you, allowing you to choose the media format, quality, playlist behavior, and download location without needing to know yt-dlp's command-line syntax.

## Features

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
- Validates URLs before continuing
- Animated validation indicator
- Graphical folder picker for choosing the download destination
- Bundled yt-dlp and FFmpeg support
- Standalone Windows application — Python does not need to be installed

## Installation

Download `YT-DLP-Helper-Setup.exe` from the project's Releases page and run the installer.

The installer creates a Start Menu shortcut and optionally a Desktop shortcut.

## Usage

1. Launch **YT-DLP Helper**.
2. Paste the URL of the media you want to download.
3. Choose Video or Audio.
4. Select the desired quality.
5. Choose whether to download the entire playlist.
6. Select a destination folder.
7. YT-DLP Helper will run the download and display its progress.

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