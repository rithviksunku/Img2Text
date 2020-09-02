import io
import json
import cv2
import requests
import tkinter as tk
from tkinter import filedialog, Text, Frame
import cv2, time
import os
import pyperclip

root = tk.Tk()

def GetPhoto():
    videoCaptureObject = cv2.VideoCapture(0)
    while(True):
        ret,frame = videoCaptureObject.read()
        cv2.imshow('Capturing Video',frame)
        if(cv2.waitKey(1) & 0xFF == ord('c')):
            cv2.imwrite("NewPicture.jpg", frame)
            videoCaptureObject.release()
            cv2.destroyAllWindows()

def Converts():
    img = cv2.imread('NewPicture.jpg')

    url_api = 'https://api.ocr.space/parse/image'
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    results = requests.post(url_api, files={'NewPicture.jpg': file_bytes}, data={"apikey": "323ebb9ff588957"})

    results = results.content.decode()
    results = json.loads(results)

    text_detected = results.get("ParsedResults")[0].get("ParsedText")
    output = tk.Label(frame, text=text_detected)
    output.pack()
    pyperclip.copy(text_detected)


def GetText():
    filename = filedialog.askopenfilename(title='Select File', filetypes=[("Image Files", "*.jpg")])
    img = cv2.imread(str(filename))

    url_api = 'https://api.ocr.space/parse/image'
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    results = requests.post(url_api, files={str(filename): file_bytes}, data={"apikey": "323ebb9ff588957"})

    results = results.content.decode()
    results = json.loads(results)

    text_detected = results.get("ParsedResults")[0].get("ParsedText")
    output = tk.Label(frame, text=text_detected)
    output.pack()
    pyperclip.copy(text_detected)


canvas = tk.Canvas(root, height=600, width=500, bg="#000000")
canvas.pack()

frame: Frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

background_image = tk.PhotoImage(file='logo.png')
background_label = tk.Label(image=background_image)
background_label.place(relwidth=1, relheight=.1, relx=0, rely=0)

output_section = tk.Label(frame, text = 'Your Outputted Text Will Appear Here: ', font=('Modern', 20), fg='#003262')
output_section.place(relwidth=1, relheight=.1, relx=0, rely=0)

openFile = tk.Button(root, text='   Open File   ', font=('Modern', 18), padx=8, pady=10, fg='#003262', bg='black', command=GetText)
openFile.pack(fill='both')

takePhoto = tk.Button(root, text='  Take Photo  ', font=('Modern', 18), padx=8, pady=10, fg='#003262', bg='black', command=GetPhoto)
takePhoto.pack(fill='both')

convertPhoto = tk.Button(root, text='Convert Photo', font=('Modern', 18), padx=8, pady=10, fg='#003262', bg='black', command=Converts)
convertPhoto.pack(fill='both')
root.mainloop()

