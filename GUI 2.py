from tkinter import *
import tkinter.messagebox as msg
from tkinter import filedialog
from pygame import mixer
from tkinter import ttk
from mutagen.id3 import ID3 # its handle audio meta data
from mutagen.mp3 import MP3
import eyed3
import io
import os
import pydub
from PIL import Image,ImageTk
import time
import threading
root=Tk()

menubar=Menu(root)
root.config(menu=menubar,bg="#fff")
root.title("welcome")
root.iconbitmap(r"C:\Python36\Projects\Music Player\Icons\headphones.ico")
root.geometry("720x500")
stop=PhotoImage(file=r"C:\Python36\Projects\Music Player\Icons\stop-button.png")
play=PhotoImage(file=r"C:\Python36\Projects\Music Player\Icons\play-button.png")
pauseImg=PhotoImage(file=r"c:\Python36\Projects\Music Player\Icons\pause.png")
unpauseImg=PhotoImage(file=r"c:\Python36\Projects\Music Player\Icons\play-button.png")
rewindImg=PhotoImage(file=r"c:\Python36\Projects\Music Player\Icons\refresh.png")
volume=PhotoImage(file=r"c:\Python36\Projects\Music Player\Icons\enable-sound.png")
mute=PhotoImage(file=r"c:\Python36\Projects\Music Player\Icons\mute.png")
nextImg=PhotoImage(file=r"c:\Python36\Projects\Music Player\Icons\next (3).png")
prevImg=PhotoImage(file=r"c:\Python36\Projects\Music Player\Icons\arrow.png")
displayImg=PhotoImage(file=r"Icons\Display_background.png")
def button_hover(e):
    playbutton['bg']="#f5f6fa"
def button_over(e):
    playbutton['bg']="white"
def button_hover_stop(e):
    stopbutton['bg']="#f5f6fa"
def button_over_stop(e):
    stopbutton['bg']="white"

#create a sub menu
def browse_file():
    global filename
    filename=filedialog.askopenfilename()
    playbutton.configure(image=play)
    print("selected:",filename)
def Menu_file():
    submenu=Menu(menubar,tearoff=0)
    menubar.add_cascade(label="file",menu=submenu)
    submenu.add_command(label="new")
    submenu.add_command(label="open",command=browse_file)
    submenu.add_command(label="Save")
    submenu.add_command(label="save as")
    submenu.add_command(label="page setup")
    submenu.add_command(label="print")
    submenu.add_command(label="Exit",command=root.destroy)
def menu_Edit():
    submenu=Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Edit",menu=submenu)
    submenu.add_command(label="Undo")
    submenu.add_command(label="Redo")
    submenu.add_command(label="cut")
    submenu.add_command(label="copy")
    submenu.add_command(label="paste")
    submenu.add_command(label="delete")
    submenu.add_command(label="find")
    submenu.add_command(label="find next")
    submenu.add_command(label="replace")
    submenu.add_command(label="goto")
    submenu.add_command(label="time and date")
Menu_file()
menu_Edit()
submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Format",menu=submenu)
submenu.add_command(label="word wrap")
submenu.add_command(label="font")

submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="View",menu=submenu)
submenu.add_command(label="Status bar")

def about_us():
    msg.showinfo('about title','this is a music player')

main=Menu(menubar,tearoff=0)
menubar.add_cascade(label="help",menu=main)
main.add_command(label="view help",command=about_us)
main.add_command(label="About notepad")

mixer.init()




muted = False


def mute_music():
    global muted
    if (muted):
        mixer.music.set_volume(0.2)
        scale.set(20)
        volumeBtn.configure(image=volume)
        muted=False
    else:
        mixer.music.set_volume(50)
        scale.set(0)
        volumeBtn.configure(image=mute)
        muted=True


def click_btn():
    try:
        global check
        check=playbutton['image']

        if(check=="pyimage2"):
            mixer.music.load(filename)
            music = ID3(filename)
            temp = music.getall("APIC")[0].data
            im = io.BytesIO(temp)
            imageF = Image.open(im)
            global photo
            photo = ImageTk.PhotoImage(imageF)
            lbl_display.configure(image=photo)
            lbl_display.image=photo
            playbutton.configure(image=pauseImg)
            mixer.music.play(start=0)
            a=MP3(filename)
            # print(a)
            total_length =a.info.length
            # print("lengthh:",total_length)
            global mins, sec
            mins, sec = total_length // 60, total_length % 60
            lbl_end.configure(text="{}:{}".format(int(mins),int(sec)))
            t1=threading.Thread(target=start_count,args=(total_length,))
            prog.configure(value=0,to=total_length)
            t1.start()
            # print(mins,sec)
        if(check=="pyimage3"):
            playbutton.configure(image=unpauseImg)
            pause_btn()
        if(check=="pyimage4"):
            playbutton.configure(image=pauseImg)
            unpause_btn()
        statusbar['text']='playing music'+' '+ os.path.basename(filename)
    except:
        msg.showerror('warning','Please select a file')

def start_count(t):
    start_time=0.00
    print(t)
    while(start_time<=t):
        global check
        if(check=="pyimage3"):
            continue
        elif(mixer.music.get_busy()==0):
            lbl_start.configure(text="00:00")
            break
        else:
            mins,sec=divmod(start_time,60)
            mins=round(mins)
            sec=round(sec)
            timeformat="{:02d}:{:02d}".format(mins,sec)
            lbl_start.configure(text=timeformat)
            print("timeformat {}".format(timeformat))
            print("start_time:",start_time)
            prog.configure(value="{}".format(start_time))
            current_time=prog.get()

            print("current time by slider",current_time)
            time.sleep(1)
            start_time+=1

def stop_btn():
    mixer.music.fadeout(700)
    statusbar['text']='stoped music'
    playbutton.configure(image=play)

def vol(val):
    val=float(val)/100
    mixer.music.set_volume(val)
def pause_btn():
    mixer.music.pause()

def unpause_btn():
    mixer.music.unpause()
def rewind_btn():
    mixer.music.play()

statusbar=Label(root,text="welcome to subhransu das music player",anchor=W)
statusbar.pack(side=BOTTOM,fill=BOTH)
lbl_display = Label(root, image=displayImg, height=280, width=450)
lbl_display.pack(side=TOP)
lbl_start=Label(root,text="00:00",bg="white")
lbl_start.place(x=40,y=301)
lbl_end=Label(root,text="00:00",bg="white")
lbl_end.place(x=600,y=301)
blank=Button(root,bg="#fff",borderwidth=0)
blank.pack(side=LEFT,padx=30,fill=X)

previous=Button(root,image=prevImg,command=unpause_btn,bg="#fff",borderwidth=0,cursor="hand2")
previous.pack(side=LEFT,padx=10)
playbutton=Button(root,image=play,command=click_btn,bg="#fff",borderwidth=0,cursor="hand2")
playbutton.pack(side=LEFT,padx=10)
playbutton.bind("<Enter>",button_hover)
playbutton.bind("<Leave>",button_over)

next=Button(root,image=nextImg,command=unpause_btn,bg="#fff",borderwidth=0,cursor="hand2")
next.pack(side=LEFT,padx=10)
stopbutton=Button(root,image=stop,command=stop_btn,bg="#fff",borderwidth=0,cursor="hand2")
stopbutton.pack(side=LEFT,padx=10)
stopbutton.bind("<Enter>",button_hover_stop)
stopbutton.bind("<Leave>",button_over_stop)

rewind=Button(root,image=rewindImg,command=rewind_btn,bg="#fff",borderwidth=0,cursor="hand2")
rewind.pack(side=LEFT,expand=True)

volumeBtn=Button(root,image=volume,bg="#fff",borderwidth=0,cursor="hand2",command=mute_music)
volumeBtn.pack(side=LEFT,expand=True)

prog=ttk.Scale(root, orient=HORIZONTAL, from_=0, to=100 ,length=510,value=00.00)
prog.place(x=80,y=300)
scale=Scale(root,orient=HORIZONTAL,command=vol,cursor="hand2",bg="#fff",border=4,relief="raised")
scale.set(50)
scale.pack(side=LEFT,expand=True)

#mute unmute

root.mainloop()
