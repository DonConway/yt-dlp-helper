import queue
import re
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import json
import os

BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
YT_DLP = BASE_DIR / 'bin' / 'yt-dlp.exe'
FFMPEG_DIR = BASE_DIR / 'bin'

VIDEO_QUALITIES = ('Best available', '1080p', '720p', '480p')
AUDIO_QUALITIES = ('Best available', '320 kbps', '192 kbps', '128 kbps')
VIDEO_FORMATS = {
    'Best available': 'bv*+ba/b',
    '1080p': 'bv*[height<=1080]+ba/b[height<=1080]',
    '720p': 'bv*[height<=720]+ba/b[height<=720]',
    '480p': 'bv*[height<=480]+ba/b[height<=480]',
}
AUDIO_BITRATES = {'Best available': '0', '320 kbps': '320K', '192 kbps': '192K', '128 kbps': '128K'}
PROGRESS_PATTERN = re.compile(r'\[download\]\s+(\d+(?:\.\d+)?)%')

SETTINGS_DIR = Path(os.getenv("APPDATA", str(Path.home()))) / "YT-DLP Helper"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"


def load_download_folder():
    default = str(Path.home() / "Downloads")

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        folder = settings.get("download_folder", default)

        if Path(folder).is_dir():
            return folder

    except (OSError, ValueError, TypeError):
        pass

    return default


def save_download_folder(folder):
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump({"download_folder": folder}, file, indent=4)

def build_command(url, media_type, quality, playlist, destination):
    command = [str(YT_DLP), '--ffmpeg-location', str(FFMPEG_DIR), '--newline', '--no-colors']

    # Set output filename based on video resolution or audio quality
    if media_type == 'Video':
        command.extend(['-o', '%(title)s [%(height)sp].%(ext)s'])
    else:
        command.extend(['-o', '%(title)s [%(abr)skbps].%(ext)s'])

    # Download single video unless playlist is selected
    if not playlist:
        command.append('--no-playlist')

    # Video settings
    if media_type == 'Video':
        command.extend(['--remux-video', 'mp4', '-f', VIDEO_FORMATS[quality]])

    # Audio settings
    else:
        command.extend([
            '-x',
            '--audio-format', 'mp3',
            '--audio-quality', AUDIO_BITRATES[quality]
        ])

    # Destination and URL
    command.extend(['-P', destination, url])

    return command



class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title('YT-DLP Helper')
        self.root.geometry('580x485')
        self.root.minsize(510, 430)
        self.root.configure(bg='#f5f7fb')
        self.events = queue.Queue()
        self.working = False
        self.url = tk.StringVar()
        self.media_type = tk.StringVar(value='Video')
        self.quality = tk.StringVar(value='Best available')
        self.playlist = tk.BooleanVar(value=False)
        self.destination = tk.StringVar(value=load_download_folder())
        self.status = tk.StringVar(value='Ready')
        self.percent = tk.StringVar(value='0%')
        self.progress = tk.DoubleVar(value=0)
        self._create_widgets()
        self.root.after(100, self._process_events)

    def _create_widgets(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('TFrame', background='#f5f7fb')
        style.configure('TLabel', background='#f5f7fb', foreground='#243047', font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI Semibold', 19), foreground='#16243b')
        style.configure('Sub.TLabel', foreground='#65758d', font=('Segoe UI', 9))
        style.configure('TCombobox', padding=6)
        style.configure('TEntry', padding=6)
        style.configure('Accent.TButton', font=('Segoe UI Semibold', 11), padding=11,
                        background='#2563eb', foreground='white', borderwidth=0)
        style.map('Accent.TButton', background=[('active', '#1d4ed8'), ('disabled', '#a9b9d6')])
        style.configure('Horizontal.TProgressbar', background='#2563eb', troughcolor='#e1e7f0', thickness=10)

        frame = ttk.Frame(self.root, padding=25)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='YT-DLP Helper', style='Title.TLabel').pack(anchor='w')
        ttk.Label(frame, text='Download video or audio in a few clicks', style='Sub.TLabel').pack(anchor='w', pady=(0, 20))
        ttk.Label(frame, text='Media URL').pack(anchor='w')
        self.url_entry = ttk.Entry(frame, textvariable=self.url)
        self.url_entry.pack(fill='x', pady=(5, 15))

        row = ttk.Frame(frame)
        row.pack(fill='x', pady=(0, 15))
        left = ttk.Frame(row)
        left.pack(side='left', fill='x', expand=True, padx=(0, 8))
        right = ttk.Frame(row)
        right.pack(side='left', fill='x', expand=True, padx=(8, 0))
        ttk.Label(left, text='Format').pack(anchor='w')
        self.format_combo = ttk.Combobox(left, textvariable=self.media_type, state='readonly', values=('Video', 'Audio'))
        self.format_combo.pack(fill='x', pady=(5, 0))
        self.format_combo.bind('<<ComboboxSelected>>', self._format_changed)
        ttk.Label(right, text='Quality').pack(anchor='w')
        self.quality_combo = ttk.Combobox(right, textvariable=self.quality, state='readonly', values=VIDEO_QUALITIES)
        self.quality_combo.pack(fill='x', pady=(5, 0))
        self.playlist_check = ttk.Checkbutton(frame, text='Download entire playlist', variable=self.playlist)
        self.playlist_check.pack(anchor='w', pady=(0, 15))

        ttk.Label(frame, text='Save to').pack(anchor='w')
        dest_row = ttk.Frame(frame)
        dest_row.pack(fill='x', pady=(5, 20))
        self.dest_entry = ttk.Entry(dest_row, textvariable=self.destination)
        self.dest_entry.pack(side='left', fill='x', expand=True, padx=(0, 8))
        self.browse_button = ttk.Button(dest_row, text='Browse...', command=self._browse)
        self.browse_button.pack(side='left')

        self.bar = ttk.Progressbar(frame, variable=self.progress, maximum=100)
        self.bar.pack(fill='x', pady=(0, 7))
        status_row = ttk.Frame(frame)
        status_row.pack(fill='x', pady=(0, 16))
        ttk.Label(status_row, textvariable=self.status, style='Sub.TLabel').pack(side='left')
        ttk.Label(status_row, textvariable=self.percent, style='Sub.TLabel').pack(side='right')
        self.download_button = ttk.Button(frame, text='Download', style='Accent.TButton', command=self._start)
        self.download_button.pack(fill='x')
        self.url_entry.focus_set()

    def _format_changed(self, _event=None):
        self.quality_combo.configure(values=VIDEO_QUALITIES if self.media_type.get() == 'Video' else AUDIO_QUALITIES)
        self.quality.set('Best available')

    def _browse(self):
        path = filedialog.askdirectory(
            parent=self.root,
            title='Choose download folder',
            initialdir=self.destination.get()
        )
        if path:
            self.destination.set(path)
            save_download_folder(path)

    def _set_working(self, working):
        self.working = working
        self.download_button.configure(state='disabled' if working else 'normal')
        self.url_entry.configure(state='disabled' if working else 'normal')
        self.format_combo.configure(state='disabled' if working else 'readonly')
        self.quality_combo.configure(state='disabled' if working else 'readonly')
        self.playlist_check.configure(state='disabled' if working else 'normal')
        self.dest_entry.configure(state='disabled' if working else 'normal')
        self.browse_button.configure(state='disabled' if working else 'normal')

    def _start(self):
        if self.working:
            return
        url = self.url.get().strip()
        destination = Path(self.destination.get().strip())
        if not url.startswith(('https://', 'http://')):
            messagebox.showwarning('Invalid URL', 'Enter a complete http:// or https:// media URL.', parent=self.root)
            return
        if not destination.is_dir():
            messagebox.showwarning('Invalid folder', 'Please choose an existing download folder.', parent=self.root)
            return
        if not YT_DLP.is_file():
            messagebox.showerror('Missing yt-dlp', f'Cannot find yt-dlp at:\n{YT_DLP}', parent=self.root)
            return
        if not (FFMPEG_DIR / 'ffmpeg.exe').is_file():
            messagebox.showerror('Missing FFmpeg', f'Cannot find ffmpeg.exe in:\n{FFMPEG_DIR}', parent=self.root)
            return
        save_download_folder(str(destination))
        command = build_command(url, self.media_type.get(), self.quality.get(), self.playlist.get(), str(destination))
        self.progress.set(0)
        self.percent.set('0%')
        self.status.set('Connecting...')
        self._set_working(True)
        threading.Thread(target=self._run_download, args=(command,), daemon=True).start()

    def _run_download(self, command):
        recent_lines = []
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  text=True, encoding='utf-8', errors='replace', bufsize=1,
                                  creationflags=creationflags) as process:
                for line in process.stdout:
                    line = line.strip()
                    if not line:
                        continue
                    recent_lines.append(line)
                    recent_lines = recent_lines[-15:]
                    match = PROGRESS_PATTERN.search(line)
                    if match:
                        self.events.put(('progress', float(match.group(1))))
                    elif line.startswith('[Merger]') or line.startswith('[VideoRemuxer]') or line.startswith('[ExtractAudio]'):
                        self.events.put(('status', 'Processing media...'))
                    elif line.startswith('ERROR:'):
                        self.events.put(('status', 'Download error'))
                    elif line.startswith('[youtube]') or line.startswith('[download] Destination'):
                        self.events.put(('status', 'Downloading...'))
                code = process.wait()
            self.events.put(('done', code, '\n'.join(recent_lines)))
        except Exception as exc:
            self.events.put(('done', -1, str(exc)))

    def _process_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                kind = event[0]
                if kind == 'progress':
                    self.progress.set(event[1])
                    self.percent.set(f'{event[1]:.0f}%')
                    self.status.set('Downloading...')
                elif kind == 'status':
                    self.status.set(event[1])
                elif kind == 'done':
                    self._set_working(False)
                    if event[1] == 0:
                        self.progress.set(100)
                        self.percent.set('100%')
                        self.status.set('Download complete!')
                        messagebox.showinfo('Success', 'Download completed successfully.', parent=self.root)
                    else:
                        self.status.set('Download failed')
                        messagebox.showerror('Download failed', 'yt-dlp reported an error:\n\n' + event[2][-1600:], parent=self.root)
        except queue.Empty:
            pass
        self.root.after(100, self._process_events)


if __name__ == '__main__':
    root = tk.Tk()
    DownloadApp(root)
    root.mainloop()
