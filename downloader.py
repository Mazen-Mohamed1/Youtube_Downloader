from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import threading   # to make the app lighter
import customtkinter as ctk
from tkinter import ttk
import moviepy.editor as mp
import os


root = ctk.CTk()
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


root.title('Youtube Downloader')   # for title
root.geometry("800x600")   # for the size
root.minsize(800, 600)
root.maxsize(1080, 720)

# status bar

status = Label(root, text="STATUS: Ready", font=("Arial", 20), fg="white", bg="#b32136", anchor="w")
status.place(rely=1, anchor="sw", relwidth=1)


# function for browse

def browse():
    try:
        directory = filedialog.askdirectory(title="Save Video")
        folderLink.delete(0, "end")
        folderLink.insert(0, directory)

    # video title

        video_title = ytLink.get()
        title = YouTube(video_title).title
        btit.config(text=title)
        tit = Label(root, text=title, font=("Arial", 20), fg="#b32136")
        tit.place(x=200, y=100)
    except:
        status.config(text="STATUS: Invalid Link")

yttile = Label(root, text="TITLE:", font=("Arial", 20))
yttile.place(x=25, y=100)

btit = Label(root, text="Enter the link", font=("Arial", 20), fg="#b32136")
btit.place(x=200, y=100)


def finish(stream=None, chunk=None, file_handle=None, remaining=None):
    status.config(text="STATUS: Downloaded Successfully")



# youtube link

ytLabel = Label(root, text="Youtube Link", font=("Arial", 20))
ytLabel.place(x = 25, y = 150)

ytLink = Entry(root, width=60, font=("Arial", 12))
ytLink.place(x = 200, y = 150)
ytLink.config(highlightthickness=9)

# download folder

folderLabel = Label(root, text="Download folder",font=("Arial", 20))
folderLabel.place(x = 25, y = 200)


folderLink = Entry(root, width=50,font=("Arial", 12))
folderLink.place(x = 230, y = 200)
folderLink.config(highlightthickness=9)






# browse button

browse = Button(root, text="Browse", command=browse, font=("Arial", 14),bg="#b32136", fg="white")
browse.place(x = 700, y = 200)


# create resolution combo box
resolution_combobox = None

def get_resolutions():
    try:
        global resolution_combobox
        link = ytLink.get()
        yt = YouTube(link)
        resolutions = []
        for stream in yt.streams:
            res = stream.resolution
            if res not in resolutions and res != None:
                resolutions.append(res)
        style = ttk.Style()
        style.configure('TCombobox', width=15, font=('Arial', 14))

        resolution_combobox = ttk.Combobox(root, values=sorted(resolutions), font=("Arial", 14))
        resolution_combobox.place(x = 320, y = 283)
    except:
        status.config(text="STATUS: Invalid Link")

res_button = Button(root, text="Available Resolution", command=get_resolutions,font=("Arial", 14),bg="#b32136", fg="white")
res_button.place(x = 600, y = 280)

# Download as audio
def audio():
    try:
        status.config(text="STATUS: Downloading....")
        audio_link = ytLink.get()
        audio_folder = folderLink.get()
        audio = YouTube(audio_link, on_complete_callback=finish).streams.filter(only_audio=True).first().download(audio_folder)
    except:
        status.config(text="STATUS: Something went wrong restart the app")

audio_btn = Button(root, text="Download Audio", command=threading.Thread(target=audio).start,font=("Arial", 20),bg="#b32136", fg="white")
audio_btn.place(x = 550, y = 400)
audio_btn.config(highlightthickness=5)

# download function
def down_yt():
        try:
            status.config(text="STATUS: Downloading....")
            current_dir = os.chdir(os.path.dirname(os.path.abspath(__file__)))
            link = ytLink.get()
            folder = folderLink.get()
            resolution = resolution_combobox.get()
            if resolution in ["144p", "360p", "480p","720p"]:
                YouTube(link, on_complete_callback=finish).streams.filter(res=resolution, progressive=True).order_by("resolution").desc().first().download(folder)
            else:
                dvideo = YouTube(link).streams.filter(res=resolution).order_by("resolution").desc().first().download(current_dir)
                daudio = YouTube(link).streams.filter(only_audio=True).first().download(current_dir)
                dtitle = YouTube(link).title
            # combine them


                videoclip = mp.VideoFileClip(dvideo)
                audioclip = mp.AudioFileClip(daudio)

                final_clip = videoclip.set_audio(audioclip)


                output_path = os.path.join(fr'{folder}\{dtitle}.mp4')
                final_clip.write_videofile(output_path, codec='libx264')


                os.remove(dvideo)
                os.remove(daudio)

                status.config(text="STATUS: Downloaded Successfully")

        except:
                status.config(text="STATUS: Something went wrong restart the app")





# download button

download = Button(root, text="Download Video", command=threading.Thread(target=down_yt).start,font=("Arial", 20),bg="#b32136", fg="white")
download.place(x = 150, y = 400)
download.config(highlightthickness=5)




root.mainloop()

