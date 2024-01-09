from pytube import YouTube
import tkinter
import customtkinter
import ffmpeg


def download():
    try:
        ytLink = link.get()
        finishLabel.configure(text="", text_color="white")
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)

        if check.get() == "on":
            audio = ytObject.streams.get_audio_only()
            audio.download("C:\D\PyTube\Musik")

        elif check.get() == "off":
            # Audio und Video Streams
            highest_res_video = ytObject.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc().first()
            # Check for Quality
            print(ytObject.streams.filter(only_video=True).order_by('resolution').desc())
            print(highest_res_video)
            highest_res_video.download("C:\D\PyTube\merge", ytObject.title + "_video.mp4")
            ytObject.streams.get_audio_only().download("C:\D\PyTube\merge", ytObject.title + "_audio.mp4")

            # Merging with ffmpeg
            video_stream = ffmpeg.input("C:\D\PyTube\merge\\" + ytObject.title + "_video.mp4")
            audio_stream = ffmpeg.input("C:\D\PyTube\merge\\" + ytObject.title + "_audio.mp4")
            ffmpeg.output(audio_stream, video_stream, "C:\D\PyTube\Videos\\" + ytObject.title + ".mp4").run()

        finishLabel.configure(text="Downloaded!")

        progressBar.set(0)
        finishLabel.configure(text="", text_color="white")

    except:
        finishLabel.configure(text="Download Error", text_color="red")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    percentage.configure(text=per + '%')
    percentage.update()

    progressBar.set(float(percentage_of_completion) / 100)


# GUI

# System Settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# App Frame
app = customtkinter.CTk()
app.geometry("1200x700")
app.title("PyTube")

# UI Elements
title = customtkinter.CTkLabel(app, text="Insert a YouTube Link")
title.pack(padx=10, pady=10,)

# Link Input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Audio only Checkbox
check_var = customtkinter.StringVar(value="on")
check = customtkinter.CTkCheckBox(app, text="Only Audio", onvalue="on", offvalue="off")
check.pack(padx=10, pady=10)

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=download)
download.pack(padx=10, pady=30, side="bottom")

# Progress Bar
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10, side="bottom")

percentage = customtkinter.CTkLabel(app, text="0%")
percentage.pack(side="bottom")

# Run App
app.mainloop()