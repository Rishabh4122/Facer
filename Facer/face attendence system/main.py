import face_recognition
import cv2
import numpy as np
import csv
from datetime import *
import tkinter as Tk
from tkinter import *
from tkinter import ttk
import os
from alt import capture_image
import customtkinter
from PIL import Image, ImageTk

        

# Define the list of known faces and their encodings
Rishabh_image = face_recognition.load_image_file("photos/Rishabh.jpg")
Rishabh_encoding = face_recognition.face_encodings(Rishabh_image)[0]
                                        
henry_image = face_recognition.load_image_file("photos/henry.jpg")
henry_encoding = face_recognition.face_encodings(henry_image)[0]

robert_image = face_recognition.load_image_file("photos/ben.jpg")
robert_encoding = face_recognition.face_encodings(robert_image)[0]

ben_image = face_recognition.load_image_file("photos/robert.jpg")
ben_encoding = face_recognition.face_encodings(robert_image)[0]

known_face_encoding = [ Rishabh_encoding, henry_encoding, ben_encoding, robert_encoding,]

known_faces_names = ["Rishabh ", "henry", "ben", "robert"]

students = known_faces_names.copy()

#Function that will be called when the 'Start' button is clicked
def start_recognition():
    video_capture = cv2.VideoCapture(0)
    
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d") #statement for fetching current date for the csv file 
    f = open (current_date+'.csv','w+',newline='')
    Inwriter = csv.writer(f)
    
    while True: 
        _,frame = video_capture.read()
        small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        rgb_small_frame=small_frame[:,:,::-1]
        
        # Perform face recognition on the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name=""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:   #this code snippet checks if the best match index exists or not
                name = known_faces_names[best_match_index]  #if the element exists then means a match has been found
            face_names.append(name)
            if name in known_faces_names:
                if name in students:                    #conditional statement for printing the results of facial recognition.
                    print("Marked present : ",name)
                    students.remove(name)
                    print("Students yet to appear : ", students)
                    current_time = now.strftime("%H-%M-%S")
                    Inwriter.writerow([name,current_time])     
        cv2.imshow("Attendance system",frame) 
        #exit when ESC is pressed.
        #exits the loop and stop the video capture.
        if cv2.waitKey(1) & 0xFF == 27:
           break    
    video_capture.release()
    cv2.destroyAllWindows()
    f.close()

# GUI starts here
root = Tk()
root.title('FACER')     #sets title to FACER
root.iconbitmap(r'gui/title facer.ico')   #sets GUI applicaion icon to this path image

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size based on screen size
window_width = int(screen_width * 0.5)
window_height = int(screen_height * 0.5)

root.geometry(f"{window_width}x{window_height}")
root.configure(background='#292826')


#Create a canvas for the background image
canvas=Canvas(root, width=window_width, height=window_height)
canvas.pack(fill=BOTH, expand=YES)

#Load the background image
background_image=PhotoImage(file="gui/bg.png")
canvas.create_image(0,0, anchor=NW, image=background_image)
#define our images

# Addlabel for the title
l1 = Label(root , text='Welcome to the Facial Recognition System' , fg='#ffffff',bg='#292826',font=("Times New Roman", 16), justify=CENTER)
l1.place(relx=0.5, rely=0.1, anchor=CENTER)


# Add a button to start the recognition
b1 = ttk.Button(root, text='Start', command=start_recognition)
b1.place(relx=0.5, rely=0.3, anchor=CENTER) # Use place() to center the button on the canvas

b2= ttk.Button(root, text="New Face Profile", command=lambda:capture_image(0,"images"))
b2.place(relx=0.5, rely=0.5, anchor=CENTER) # Use place() to center the button on the canvas

l2 = Label(root , text='Help' , fg='#ffffff',bg='#292826',font=("Times New Roman", 14), justify=CENTER)
l2.place(relx=0.5, rely=0.8, anchor=CENTER)

l3 = Label(root , text='Press "Start" button to mark your attendance.\nPress "New Face Profile" button to add your new face profile to the existing data. ' , fg='#ffffff',bg='#292826',font=("Times New Roman ", 13), justify=CENTER)
l3.place(relx=0.5, rely=0.9, anchor=CENTER)
root.mainloop()
