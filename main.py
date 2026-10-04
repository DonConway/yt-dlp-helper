import subprocess
import tkinter as tk
from tkinter import filedialog
import threading
import time


#Get URL input and check validity first:
def get_url():
    while True:
        link = input("Media URL: ")
        stop_event = threading.Event()
        loader = threading.Thread(target=loading_message, args=(stop_event,)
        )
        loader.start()
        result = subprocess.run(
            ["yt-dlp", "--simulate", "--no-playlist", link],
                capture_output=True, text=True)
        stop_event.set()
        loader.join()
        if result.returncode == 0:
            return link
        print("Invalid URL")


# Get desired format (Video or Audio):
def get_format():
    download_type = 0
    while download_type not in [1, 2]:
        download_type = input("Video.mp4 (1) or Audio.mp3 (2) [1/2]: ")
        try:
            download_type = int(download_type)
            if download_type not in [1, 2]:
                print("Only the entries '1' or '2' are allowed.")
        except ValueError:
            print("Invalid entry. Please enter 1 for Video,"
                                  "or 2 for Audio.")
    return download_type


# Get desired Quality:
def get_quality(download_type):
    quality = ""
    while quality not in [1, 2, 3, 4]:
        if download_type == 1:
            print("1. Best available")
            print("2. 1080P")
            print("3. 720P")
            print("4. 480P")
        elif download_type == 2:
            print("1. Best available")
            print("2. 320 kbps")
            print("3. 192 kbps")
            print("4. 128 kbps")
        quality = input("Quality [1-4]: ")
        try:
            quality = int(quality)
        except ValueError:
            print("Invalid entry. 1, 2, 3, or 4 only.")
            continue
        if quality not in [1, 2, 3, 4]:
            print("Invalid entry. 1, 2, 3, or 4 only.")
    return quality


# Choose single video or entire playlist (single vid default):
def get_playlist():
    playlist = input("Download the playlist? (y/N): ").lower()
    while playlist not in ['y', 'n', '']:
        print("Invalid Entry. y for yes or N for no. Empty defaults to no.")
        playlist = input("Download the playlist? (y/N): ").lower()
    return playlist == "y"


#Now we determine the download's destination:
def get_destination():
    while True:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        destination = filedialog.askdirectory(
            parent=root,
            title="Choose where to save your download:"
        )

        root.destroy()

        if destination:
            return destination

        input("No directory selected. Press Enter to try again.")


#Now we build the command for the console to begin the download:
def build_command(media, download_type, quality, playlist, destination):
    command = ["yt-dlp"]
    if not playlist:
        command.append("--no-playlist")
    if download_type == 1:
        command.append("-f")
        if quality == 1:
            command.append("bv*+ba/b")
        elif quality == 2:
            command.append("bv*[height<=1080]+ba/b[height<=1080]")
        elif quality == 3:
            command.append("bv*[height<=720]+ba/b[height<=720]")
        elif quality  == 4:
            command.append("bv*[height<=480]+ba/b[height<=480]")
    elif download_type == 2:
        command.extend(["-x", "--audio-format", "mp3", "--audio-quality"])
        if quality == 1:
            command.append("0")
        elif quality == 2:
            command.append("320K")
        elif quality == 3:
            command.append("192K")
        elif quality == 4:
            command.append("128K")
    command.extend(["-P", destination])
    command.append(media)
    return command

#This makes a "Validating..." loading bar for URL Validation
def loading_message(stop_event):
    dots = 1

    while not stop_event.is_set():
        print(f"\rValidating{'.' * dots}  ", end="", flush=True)
        dots = dots % 3 + 1
        time.sleep(0.4)

    print("\r" + " " * 30 + "\r", end="", flush=True)


def main():
    media = get_url()
    download_type = get_format()
    quality = get_quality(download_type)
    playlist = get_playlist()
    destination = get_destination()
    command = build_command(media, download_type, quality, playlist, destination)

    result = subprocess.run(command)

    if result.returncode == 0:
        input("\nDownload Successful! Press Enter to Exit.")
    else:
        input(
            "\nDownload Unsuccessful. See the error above. Press Enter to Exit.")






if __name__ == "__main__":
    main()


