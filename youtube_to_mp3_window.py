
from tkinter import *
from tkinter import messagebox
from pytube import YouTube
import os
import time

root = Tk()
root.title("Convert YouTube to .MP4")
root.configure(border=5, bg="#1e1e1e")
root.resizable(False, False)

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight-300, positionDown-100))

def clearBtn():
    urlTextbox.delete(0, END)

def downloadAsAudio():
    enteredString = urlTextbox.get().strip()
    if enteredString == "":
        messagebox.showerror("Required Field", "You did not enter anything in the box.")
    elif "www.youtube.com/" not in enteredString:
        messagebox.showerror("Invalid URL", "You have entered an invalid URL.")
    else:
        # get url input from user
        yt = YouTube(urlTextbox.get().strip())

        downloadsFolder = file_path()
        audio = yt.streams.filter(only_audio=True).first().download(downloadsFolder)

        # download only audio
        try:
            downloadsFolder = file_path()
            audio = yt.streams.filter(only_audio=True).first().download(downloadsFolder)
        except:
            messagebox.showerror("Error", "Something wrong occurred. Application will close...")
            time.sleep(1)
            closeApp()

        # result of success
        downloadedList.insert(END, f"\"{yt.title}\" Audio has been successfully downloaded.\n")

def downloadAsVideo():
    enteredString = urlTextbox.get().strip()
    if enteredString == "":
        messagebox.showerror("Required Field", "You did not enter anything in the box.")
    elif "www." not in enteredString:
        messagebox.showerror("Required Field", "You have entered an invalid URL.")
    else:
        # get url input from user
        yt = YouTube(urlTextbox.get().strip())

        # download the entire video
        try:
            downloadsFolder = file_path()
            yt.streams.get_highest_resolution().download(downloadsFolder)
        except:
            messagebox.showerror("Error", "Something wrong occurred. Application is closing...")
            time.sleep(1)
            closeApp()

        # result of success
        downloadedList.insert(END, f"\"{yt.title}\" Video has been successfully downloaded.\n")

def file_path():
    home = os.path.expanduser('~')
    download_path = os.path.join(home, 'Downloads')
    return download_path

def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

def paste_func(e, urlTextbox):
    if root.clipboard_get() != '':
        try:
            cursorPosition = urlTextbox.index(INSERT)
            urlTextbox.insert(cursorPosition, root.clipboard_get())
        except TclError:
            pass

def closeApp():
    root.quit()

# create the label
label = Label(root, text="Enter the URL of the video you want to download in the box below:", font=("Helvetica", 14), bg="#1e1e1e", fg="#ffffff")
label.grid(row=0, column=0, columnspan=3, sticky=W, padx=20, pady=0)

# create the Entry Textbox
urlTextbox = Entry(root, width=100, highlightthickness=1)
urlTextbox.config(highlightbackground="#4eab70", highlightcolor="#4eab70")
urlTextbox.grid(row=1, column=0, columnspan=3, sticky=NSEW, padx=20, pady=5)
urlTextbox.focus()

# create the Clear Button
clearButton = Button(root, text="CLEAR", command=clearBtn, bg="#ffffff", fg="#4eab70", font=("Helvetica", 12, "bold"))
clearButton.grid(row=0, column=2, sticky=E, padx=20, pady=10)

# create the Download As Audio button
convertButton1 = Button(root, text="Download Audio (MP4)", command=downloadAsAudio, bg="#4eab70", fg="#ffffff", font=("Helvetica", 12, "bold"), height=2, width=30)
convertButton1.grid(row=2, column=0, padx=20, pady=10, sticky=E)

# create the Download As Video button
convertButton2 = Button(root, text="Download Video (MP4)", command=downloadAsVideo, bg="#4eab70", fg="#ffffff", font=("Helvetica", 12, "bold"), height=2, width=30)
convertButton2.grid(row=2, column=2, padx=20, pady=10, sticky=W)

# # create the Progress Bar
# downloadProgress = Progressbar(root, orient=HORIZONTAL, length=300, mode="determinate")
# downloadProgress.grid(row=3, column=0)

# create Downloaded List (Listbox)
downloadedList = Listbox(root, width=100, bg="#1e1e1e", fg="#ffffff")
downloadedList.config(highlightbackground="#4eab70", highlightcolor="#4eab70")
downloadedList.grid(row=5, column=0, columnspan=3, sticky=NSEW, padx=20, pady=20)

# create Scrollbar Horizontal
scrollbarX = Scrollbar(root, orient=HORIZONTAL)
scrollbarX.grid(row=5, column=0, columnspan=3, sticky=S, pady=2)
downloadedList.configure(xscrollcommand=scrollbarX.set)
scrollbarX.configure(command=downloadedList.xview)

# create Scrollbar Vertical
scrollbarY = Scrollbar(root)
scrollbarY.grid(row=5, column=2, sticky=E, padx=2)
downloadedList.configure(yscrollcommand=scrollbarY.set)
scrollbarY.configure(command=downloadedList.yview, activerelief="groove")

# add the right click menu popup
m = Menu(root, tearoff = 0)
m.add_command(label="Paste", command= lambda: paste_func(False, urlTextbox))

urlTextbox.bind("<Button-3>", do_popup)

# start program
root.mainloop()
