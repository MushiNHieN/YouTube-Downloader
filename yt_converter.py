from pytube import YouTube, Playlist
from pytube.exceptions import AgeRestrictedError
import customtkinter as ctk
import re
import threading
from time import sleep


def replace_invalid_chars(filename):
    invalid_chars_regex = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars_regex, ' ', filename)


def convert(path, link):
    if 'list' in link:
        dl_playlist(path, link)
    else:
        dl_single(path, link)


def dl_single(path, link):
    if mp3_checked.get() == 'on':
        video = YouTube(link)
        stream = video.streams.get_audio_only()
        complete_label.configure(
            text=f'Downloading: "{stream.title}"...', text_color='cyan')
        try:
            stream.download(output_path=path,
                            filename=f'{replace_invalid_chars(stream.title)}.mp3', timeout=20)
            complete_label.configure(
                text=f'"{stream.title}" download complete.', text_color='green')
        except Exception as e:
            complete_label.configure(
                text=f"'{stream.title}' {e}.", text_color='orange')

    if mp4_checked.get() == 'on':
        video = YouTube(link)
        stream = video.streams.filter(progressive=True, res='720p').first()
        complete_label.configure(
            text=f'Downloading: "{stream.title}"...', text_color='cyan')
        try:
            stream.download(output_path=path,
                            filename=f'{replace_invalid_chars(stream.title)}.mp4', timeout=20)
            complete_label.configure(
                text=f'"{stream.title}" download complete.', text_color='green')
        except Exception as e:
            complete_label.configure(
                text=f'"{stream.title}" {e}.', text_color='orange')


def dl_playlist(path, link):
    playlist = Playlist(link)
    if mp3_checked.get() == 'on':
        for i, video in enumerate(playlist.videos):
            playlist_label.configure(
                text=f'Downloading: {playlist.title} playlist')
            complete_label.configure(
                text=video.title, text_color='cyan')
            count_label.configure(text=f'( {i+1} / {len(playlist.videos)} )')
            try:
                stream = video.streams.get_audio_only()
                stream.download(output_path=f'{path}/{playlist.title}',
                                filename=f'{replace_invalid_chars(stream.title)}.mp3', timeout=20)
            except Exception as e:
                complete_label.configure(
                    text=f'{playlist.title} {e}.', text_color='orange')
                sleep(2)
                continue
        complete_label.configure(
            text=f'{playlist.title} playlist download complete.', text_color='green')
        playlist_label.configure(text='')
        count_label.configure(text='')

    if mp4_checked.get() == 'on':
        for i, video in enumerate(playlist.videos):
            playlist_label.configure(
                text=f'Downloading: {playlist.title} playlist')
            complete_label.configure(
                text=video.title, text_color='cyan')
            count_label.configure(text=f'( {i+1} / {len(playlist.videos)} )')
            try:
                stream = video.streams.filter(
                    progressive=True, res='720p').first()
            except:
                stream = video.streams.filter(progressive=True).first()
            try:
                stream.download(output_path=f'{path}/{playlist.title}',
                                filename=f'{replace_invalid_chars(stream.title)}.mp4', timeout=20)
            except Exception as e:
                complete_label.configure(
                    text=f'{playlist.title} {e}.', text_color='orange')
                sleep(2)
                continue
        complete_label.configure(
            text=f'{playlist.title} playlist download complete.', text_color='green')
        playlist_label.configure(text='')
        count_label.configure(text='')


def open_file_dialog():
    global file_path
    file_path = ctk.filedialog.askdirectory()
    if file_path:
        output_label.configure(text=f'Download will be stored at: {file_path}')


# tk window settings
root = ctk.CTk()
root.title('Youtube Converter')
root.geometry('700x500')
root.iconbitmap('youtube.ico')


mp3_checked = ctk.StringVar(value="off")
mp4_checked = ctk.StringVar(value="off")


youtube_link_entry = ctk.CTkEntry(
    root, width=600, placeholder_text='Youtube link or playlist to convert')
youtube_link_entry.pack(pady=50)


output_path_button = ctk.CTkButton(
    root, text='Output directory', command=open_file_dialog)
output_path_button.pack()
output_label = ctk.CTkLabel(root, text='', text_color='cyan')
output_label.pack()

mp3_checkbox = ctk.CTkCheckBox(
    master=root, text='.mp3', variable=mp3_checked, onvalue='on', offvalue='off')
mp3_checkbox.pack(pady=10)

mp4_checkbox = ctk.CTkCheckBox(
    master=root, text='.mp4', variable=mp4_checked, onvalue='on', offvalue='off')
mp4_checkbox.pack(pady=10)


convert_single = ctk.CTkButton(
    root, text='Download', command=lambda: threading.Thread(target=convert, args=(file_path, youtube_link_entry.get())).start())
convert_single.pack(pady=10)


# convert_single = ctk.CTkButton(
#     root, text='Convert single', command=lambda: threading.Thread(target=dl_single, args=(file_path, youtube_link_entry.get())).start())
# convert_single.pack(pady=10)

# convert_playlist = ctk.CTkButton(
#     root, text='Convert playlist', command=lambda: threading.Thread(target=dl_playlist, args=(file_path, youtube_link_entry.get())).start())
# convert_playlist.pack(pady=10)

playlist_label = ctk.CTkLabel(root, text='', wraplength=400, text_color='cyan')
playlist_label.pack()

complete_label = ctk.CTkLabel(root, text='', wraplength=400)
complete_label.pack()

count_label = ctk.CTkLabel(root, text='', text_color='cyan')
count_label.pack()

# center window on screen
root.update_idletasks()  # Update geometry
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) // 2
root.geometry("+{}+{}".format(x, y))

root.mainloop()
