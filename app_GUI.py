import cv2
import tkinter as tk
from tkinter import END
from PIL import Image, ImageTk
import sqlite3

class MyGUI:

    def __init__(self):

        # Creation of Root window
        self.root = tk.Tk()
        self.root.geometry("1050x800") #HeightxWidth
        self.root.configure(bg="black") #background color
        self.root.title("Facial Recognition") #title of the window

        # Create a menubar at the top border of root window
        self.menubar = tk.Menu(self.root)
        self.file_menubar = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.file_menubar, label="Settings", activebackground = '#0000CD')
        self.file_menubar.add_command(label="Shut Down", command=exit)
        self.root.config(menu=self.menubar)

        # Creation of label for the first frame which will contain the camera display
        # (The creation of this frame is inside camera_display function)
        self.frame1_label = tk.Label(self.root, bg="#0000CD")
        self.frame1_label.pack_propagate(False) #this tells the frame that it must not resize it's parent window regarding it's own size 

        # Creation of the second frame for buttons 
        self.frame2 = tk.Frame(self.root, bg="blue")
        self.frame2.pack_propagate(False) # not allowing it to resize the window 

        # Create a button to switch facial recognition status on/off (tbh this has no significant use here but still i am using it here)
        self.deactivate_recognition_bttn = tk.Button(self.frame2, text="Facial Recognition", command=self.toggle_recognition)
        self.deactivate_recognition_bttn.config(bg="white")
        self.deactivate_recognition_bttn.grid(row=0, column=0, padx=30, pady=10)

        #Create a button to show record inside the Database(this is what i am still confised)
        self.query_btn = tk.Button(self.frame2, text="Show Database Records", command=self.retrieve_records)
        self.query_btn.config(bg="white")
        self.query_btn.grid(row=0, column=1, padx=30, pady=10)

        # Creation of the textbox for the console output
        # Font size will affect the size of the textbox in perspective to the root window
        self.textbox = tk.Text(self.root, width=40, height=32.4, font=('Arial', 11))

        #Creation of third frame for database input
        self.frame3 = tk.Frame(self.root, bg="blue")
        self.frame3.pack_propagate(False)
        #Cretion of Textbox Labels for Database input inside Frame #3
        self.name_db_input = tk.Label(self.frame3, text="Name:", width=10)
        self.name_db_input.config(bg="white")
        self.name_db_input.grid(row=0, column=0, padx=25, pady=10)
        self.lastname_db_input = tk.Label(self.frame3, text="Last Name:", width=10)
        self.lastname_db_input.config(bg="white")
        self.lastname_db_input.grid(row=1, column=0, padx=25, pady=10)
        self.age_db_input = tk.Label(self.frame3, text="Age:", width=10)
        self.age_db_input.config(bg="white")
        self.age_db_input.grid(row=2, column=0, padx=25, pady=10)
        #Creation of Textboxs for Database input
        self.name_txtbox = tk.Entry(self.frame3)
        self.name_txtbox.grid(row=0, column=1, padx=25, pady=10)
        self.lastname_txtbox = tk.Entry(self.frame3)
        self.lastname_txtbox.grid(row=1, column=1, padx=25, pady=10)
        self.age_txtbox = tk.Entry(self.frame3)
        self.age_txtbox.grid(row=2, column=1, padx=25, pady=10)
        #Create button for submission of Database input
        self.submit_btn = tk.Button(self.frame3, text="Add Record to Database", command=self.database_submit)
        self.submit_btn.grid(row=3, column=1, padx=25, pady=10)

        # Set up camera video capture
        self.video_capture = cv2.VideoCapture(0) #Use 0 for default camera   

        # Load Haar cascades for face and smile detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

        # Root window grid positioning
        self.frame1_label.grid(row=0, column=0, padx=10, pady=10)
        self.frame2.grid(row=1, column=0, padx=10, pady=10)
        self.frame3.grid(row=1, column=1, padx=10, pady=10)
        self.textbox.grid(row=0, column=1)

        #Call main functions
        self.recognition_enabled = False
        self.face_detected = False  # Flag to track if a face has been detected
        self.camera_display()
        self.root.mainloop()
   

        #function to capture and detect face

    def camera_display(self):
        ret, frame1 = self.video_capture.read()

        if ret and self.recognition_enabled:
            faces = self.detect_faces(frame1)

            if len(faces) > 0 and not self.face_detected:
                self.face_detected = True  # Set the flag to True
                self.textbox.insert(END, "Face detected!, You look GREAT today.\n")
                self.textbox.see(END)

            elif len(faces) == 0:
                self.face_detected = False  # Reset the flag

            for (x, y, w, h) in faces:
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #diaplaying the name of the persoin fromn the databse ti the main screen 
                
                name="harry" #get the name from the database
                cv2.putText(frame1,name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)

                face_roi = frame1[y:y+h, x:x+w]
                smiles = self.detect_smiles(face_roi)
                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(face_roi, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)

        self.camera_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        self.resized_camera_frame = cv2.resize(self.camera_frame, (690, 545))

        self.img = Image.fromarray(self.resized_camera_frame)
        self.img_tk = ImageTk.PhotoImage(image=self.img)

        self.frame1_label.configure(image=self.img_tk)
        self.frame1_label.image = self.img_tk

        self.root.after(10, self.camera_display)

    #Create submit function for database input records
    def database_submit(self):
        #Create database or connecto to one
        conn = sqlite3.connect('myDB.db')
        #Create cursor
        c = conn.cursor()
        #Insert records into Database table
        c.execute("INSERT INTO NewUsers VALUES (:name_txtbox, :lastname_txtbox, :age_txtbox)",
                {
                    'name_txtbox': self.name_txtbox.get(),
                    'lastname_txtbox': self.lastname_txtbox.get(),
                    'age_txtbox': self.age_txtbox.get()
                })
        #Commit changes
        conn.commit()
        #Close connection
        conn.close()
        #Clear text boxes
        self.name_txtbox.delete(0, END)
        self.lastname_txtbox.delete(0, END)
        self.age_txtbox.delete(0, END)

    #Create function for retriving database records
    def retrieve_records(self):
        #Create database or connecto to one
        conn = sqlite3.connect('myDB.db')
        #Create cursor
        c = conn.cursor()
        #Query database
        c.execute("SELECT *, oid FROM NewUsers")
        records = c.fetchall()
        for x in records:
            self.textbox.insert(tk.END, str(x[0])+ " " + str(x[1])+ " " + str(x[2]) + "\n")

        #Commit changes
        conn.commit()
        #Close connection
        conn.close()

    # Facial recognition
    def detect_faces(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    # Smile recognition
    def detect_smiles(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        smiles = self.smile_cascade.detectMultiScale(gray, scaleFactor=1.7, minNeighbors=20)
        return smiles

    def toggle_recognition(self):
        if self.recognition_enabled:
            self.recognition_enabled = False
            self.deactivate_recognition_bttn.config(bg="white")
        else:
            self.recognition_enabled = True
            self.deactivate_recognition_bttn.config(bg="green")

    #Destroy Root window when done
    cv2.destroyAllWindows()

MyGUI()
