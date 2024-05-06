import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from slugify import slugify
from pytube import YouTube
import moviepy.editor as mymovie

Foldername = ""

def openloc():
    global Foldername
    Foldername = filedialog.askdirectory()
    if len(Foldername) > 1:
        locationnerror.config(text=Foldername, fg="green")
    else:
        locationnerror.config(text="Choose Directory", fg="red")

def Download_vid():
    choice = ytdchoices.get()
    url = ytdentry.get()

    if len(url) > 1:
        ytderror.config(text="")
        yt = YouTube(url)

        if choice == choices[0]:
            filenamee = slugify(yt.title)
            video = yt.streams.filter(adaptive=True).first()
            size = video.filesize

            try:
                get = messagebox.askyesno("Do You Want To Download", f"File Size: {round(size * 0.000001, 2)} MB")
                if get:
                    video.download(Foldername, filenamee + ".mp4")
                    ytderror.config(text="Download Completed", fg="green")
            except Exception as e:
                messagebox.showerror("Error", "Check Your Internet Connection!")

        elif choice == choices[1]:
            filenamee = slugify(yt.title)
            audio = yt.streams.filter(only_audio=True).last().download(Foldername, filenamee + ".webm")
            clip = mymovie.AudioFileClip(os.path.join(Foldername, filenamee + ".webm"))
            clip.write_audiofile(os.path.join(Foldername, filenamee + ".mp3"))
            clip.close()
            os.remove(os.path.join(Foldername, filenamee + ".webm"))
            ytderror.config(text="Download Completed", fg="green")

        elif choice == choices[2]:
            filenamee = slugify(yt.title)
            videofolder = os.path.join(Foldername, filenamee + ".mp4")
            audiofolder = os.path.join(Foldername, filenamee + ".mp3")

            yt.streams.filter(adaptive=True).first().download(Foldername, filenamee + ".mp4")
            yt.streams.filter(only_audio=True).last().download(Foldername, filenamee + ".mp3")

            inputvideo = videofolder
            inputaudio = audiofolder
            outputvideo = os.path.join(Foldername, filenamee + "_final" + ".mp4")

            videoclip = mymovie.VideoFileClip(inputvideo)
            audioclip = mymovie.AudioFileClip(inputaudio)
            finalclip = videoclip.set_audio(audioclip)
            finalclip.write_videofile(outputvideo, fps=60)

            os.remove(videofolder)
            os.remove(audiofolder)
            ytderror.config(text="Download Completed", fg="green")

    else:
        ytderror.config(text="Paste the link again", fg="red")

root = Tk()
root.title("Youtube Video and Sound Converter")
root.geometry("350x400")
root.columnconfigure(0, weight=1)

ytdlabel = Label(root, text="Enter URL:", font=("bahnschrift semilight", 15))
ytdlabel.grid()

ytdentryvar = StringVar()
ytdentry = Entry(root, width=50, textvariable=ytdentryvar)
ytdentry.grid()

ytderror = Label(root, text="", fg="red", font=("bahnschrift semilight", 13))
ytderror.grid()

savelabel = Label(root, text="Save the Video", font=("bahnschrift semilight", 15))
savelabel.grid()

saveEntry = Button(root, width=13, bg="red", fg="white", text="Choose Directory", command=openloc)
saveEntry.grid()

locationnerror = Label(root, text="", fg="red", font=("bahnschrift semilight", 13))
locationnerror.grid()

choices = ["1080p", "Audio", "Combine"]
ytdchoices = ttk.Combobox(root, values=choices)
ytdchoices.grid()

downloadbtn = Button(root, width=10, text="Apply", bg="green", fg="lightyellow",
                     font=("bahnschrift semilight", 15), command=Download_vid)
downloadbtn.grid()

root.mainloop()
