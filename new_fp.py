import cv2
import numpy as np
import face_recognition
import sqlite3
import csv
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from datetime import datetime, date
from tkinter.font import Font
import random
from tkinter import Toplevel, Label, Tk, Frame,Entry
from PIL import Image, ImageTk

#Database setup
conn = sqlite3.connect('User_Database.db')  #Connect to the SQLite database
c = conn.cursor()

#Create table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, name TEXT, department TEXT, batch TEXT,
             birthday TEXT, registration_no TEXT, index_no TEXT, encoding BLOB)''')
conn.commit()

def create_main_menu():
    main_menu = Tk()
    main_menu.title("Facial Attendance System")
    main_menu.geometry("800x600")  #Set window size

    #Create the background
    main_menu.configure(bg='#000000')  #Setting background color to black

    stars = []

    def create_star(x, y, size, color):
        star = Label(main_menu, text='*', font=('Arial', size), fg=color, bg='#000000')
        star.place(x=x, y=y)
        stars.append(star)

    def toggle_stars():
        for star in stars:
            star.place_forget()  #Hide all stars

        main_menu.after(500, show_stars)  #Toggle visibility after 500 milliseconds

    def show_stars():
        for star in stars:
            star.place(x=random.randint(0, 800), y=random.randint(0, 600))  #Randomize star positions
            star.config(font=('Arial', random.randint(10, 20)))  #Randomize star size
            star.config(fg=random.choice(['white', 'yellow', 'blue', 'orange','red']))  #Randomize star color

        main_menu.after(500, toggle_stars)  #Toggle visibility after 500 milliseconds

    #Create stars using labels with different colors and sizes
    for _ in range(100):  #Increased number of stars
        x = random.randint(0, 800)  #Adjusted for the enlarged window
        y = random.randint(0, 600)  #Adjusted for the enlarged window
        size = random.randint(10, 20)  #Larger size range
        color = random.choice(['white', 'yellow', 'blue', 'orange'])
        create_star(x, y, size, color)

    label_heading = Label(main_menu, text="Facial Attendance System", font=('Rockwell', 36, 'italic', 'bold'), fg='#FFFFFF', bg='#000000')  # Increased font size
    label_heading.pack(pady=100)  #Increased padding

    button_frame = Frame(main_menu, bg='#000000')
    button_frame.pack(pady=40)  #Increased padding

    button_font = Font(family='Arial', size=18, weight='bold')  #Button font

    #Toggle variable to track button state
    button_state = False

    def on_enter(button):
        nonlocal button_state
        if button_state:
            button.config(bg="#FFA500")  #Orange color
            button_state = False
        else:
            button.config(bg="#4169E1")  #Royal blue color
            button_state = True

    def on_leave(button):
        button.config(bg="#FFA500" if button_state else "#4169E1")  #Adjusted colors

    #Create buttons
    for i, (text, command) in enumerate(zip(["New User Registration", "Mark Attendance"], [open_registration_window, open_attendance_window])):
        button = Button(button_frame, text=text, command=command, font=button_font, bg="#4169E1", fg='white', bd=0, padx=30, pady=15)  #Adjusted button size and colors
        button.grid(row=i, column=0, padx=20, pady=10, sticky="ew")  #Adjusted padding
        button.bind("<Enter>", lambda e, b=button: on_enter(b))
        button.bind("<Leave>", lambda e, b=button: on_leave(b))

    main_menu.after(500, toggle_stars)

    main_menu.mainloop()

def create_user_registration_window():
    registration_window = Toplevel()
    registration_window.title("User Registration")
    registration_window.geometry("600x650")
    #Create a Frame for the image at the top
    image_frame = Frame(registration_window)
    image_frame.pack(side="top", fill="both", expand = True)
    #Load and display the image
    image_path = "C:/Users/ICS/PycharmProjects/pythonProject1/.venv/facer1.png"  #Path to image
    image = Image.open(image_path)
    #Resize the image
    new_size = (600,240)  #Specify the new size
    image = image.resize(new_size, Image.NEAREST)  #Use a basic resizing filter
    photo = ImageTk.PhotoImage(image)


    #Create a Label to hold the image
    image_label = Label(registration_window, image=photo)
    image_label.image = photo
    image_label.pack(side="top", fill="both", expand = True)


    #Create a Frame for the registration form below the image
    form_frame = Frame(registration_window)
    form_frame.pack(side="top", fill="both", expand=True)

    #Add user details to the database.
    def add_user_to_database(name, department, batch, birthday, registration_no, index_no, encoding):
        c.execute(
            "INSERT INTO users (name, department, batch, birthday, registration_no, index_no, encoding) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, department, batch, birthday, registration_no, index_no, encoding))
        conn.commit()

   #Encode the face from the given image path
    def encode_faces(image_path):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Unable to read image file '{image_path}'")
            return None
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img_rgb)
        if len(face_locations) == 0:
            print("Error: No face detected in the image.")
            return None
        face_encodings = face_recognition.face_encodings(img_rgb, face_locations)
        return face_encodings[0]

    #Open a file dialog to select an image and display it
    def browse_image():
        global selected_image_path
        selected_image_path = filedialog.askopenfilename()
        #Display the selected image
        if selected_image_path:
            img = cv2.imread(selected_image_path)
            img_resized = cv2.resize(img, (400, 300))  #Resize image to 400x300
            cv2.imshow("Selected Image", img_resized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    #Register the user by adding their details to the database.
    def register_user(entry_name, entry_department, entry_batch, entry_birthday, entry_registration_no, entry_index_no):
        name = entry_name.get()
        department = entry_department.get()
        batch = entry_batch.get()
        birthday = entry_birthday.get()
        registration_no = entry_registration_no.get()
        index_no = entry_index_no.get()
        #Check if all fields are filled
        if not (name and department and batch and birthday and registration_no and index_no):
            warning_message = "Please fill in all fields."
            messagebox.showwarning("Incomplete Data", warning_message)
            print(warning_message)
            return

        global selected_image_path
        if selected_image_path is None:
            warning_message = "Please select an image."
            messagebox.showwarning("No Image Selected", warning_message)
            print(warning_message)
            return
        encoding = encode_faces(selected_image_path)

        if encoding is None:
            warning_message = "Registration failed. No face detected."
            messagebox.showwarning("Registration Failed", warning_message)
            print(warning_message)
            return

        add_user_to_database(name, department, batch, birthday, registration_no, index_no, encoding.tobytes())
        success_message = "User registered successfully."
        messagebox.showinfo("Registration Successful", success_message)
        print(success_message)
        #Update the CSV file with the new user data
        write_users_to_csv()

    font_label = ('Helvetica', 14, 'bold')
    font_entry = ('Helvetica', 14)
    color_button = '#4682B4'

    labels = ["Name:", "Department:", "Batch:", "Birthday:", "Registration No:", "Index No:"]
    entries = [StringVar() for _ in range(6)]

    title_label = Label(registration_window, text="New User Registration", font=('Helvetica', 29, 'bold'))

    #Create and pack the title label in a Frame to span the entire width
    title_frame = Frame(image_frame, bg="lightblue")
    title_frame.pack(side="top", fill="x", pady=(0,0))
    title_label = Label(title_frame, text="New User Registration", font=('Helvetica', 29, 'bold'), bg="lightblue")
    title_label.pack(fill="x")

    for i, label_text in enumerate(labels):
        frame = Frame(registration_window)
        frame.pack(pady=5, padx=10, fill=X)
        label = Label(frame, text=label_text, font=font_label, width=12, anchor='w')
        label.pack(side=LEFT, padx=(0, 5))
        if i == 1:
            department_options = ['EE', 'CO', 'ME', 'CE']
            entry = Combobox(frame, textvariable=entries[i], values=department_options, font=font_entry, state="readonly")
        elif i == 2:
            batch_options = ['Batch 4', 'Batch 5', 'Batch 6', 'Batch 7', 'Batch 8']
            entry = Combobox(frame, textvariable=entries[i], values=batch_options, font=font_entry, state="readonly")
        else:
            entry = Entry(frame, textvariable=entries[i], font=font_entry)
        entry.pack(side=LEFT, fill=X, expand=True)

    def write_users_to_csv():
        c.execute("SELECT name, index_no, registration_no, department, birthday, batch FROM users")
        users_data = c.fetchall()

        if users_data:
            with open('Registered_Users.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Name", "Index No", "Registration No", "Department", "Birthday", "Batch"])  # Header row
                writer.writerows(users_data)
            print("Registered users data has been written to 'Registered_Users.csv'.")
        else:
            print("No user data found to write.")

    button_browse = Button(registration_window, text="Browse Image", command=browse_image, bg=color_button, fg='white', font=font_label)
    button_browse.pack(pady=10)

    #Submit Button
    button_submit = Button(registration_window, text="Submit", command=lambda: register_user(*entries), bg=color_button, fg='white', font=font_label)
    button_submit.pack(pady=10)

def create_attendance_table():
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    index_no TEXT,
                    date TEXT
                )''')
    conn.commit()

#Create and display the attendance marking window
def create_attendance_marking_window():
    #Mark attendance for the user
    def mark_attendance(name):
        c.execute("SELECT index_no, department FROM users WHERE name = ?", (name,))
        data = c.fetchone()
        if data:
            index_no, department = data
            today = date.today()
            today_str = today.strftime('%Y-%m-%d')
            #Add attendance to the database
            c.execute("SELECT * FROM attendance WHERE index_no = ? AND date = ?", (index_no, today_str))
            if c.fetchone():
                message = f"Attendance for {name} ({index_no}) has already been marked today."
                print(message)

            else:
                now = datetime.now()
                dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
                with open('Attendance.csv', 'a') as f:
                    f.write(f"{index_no},{name},{department},{dt_string}\n")
                print(f"Attendance marked for {name} ({index_no}), {department} at {dt_string}.")
                c.execute("INSERT INTO attendance (index_no, date) VALUES (?, ?)", (index_no, today_str))
                conn.commit()
        else:
            print(f"No user found with the name {name}.")

        def update_status(message):
            status_label.config(text=message)

    def load_known_encodings():
        c.execute("SELECT name, department, batch, encoding FROM users")
        data = c.fetchall()
        names = [row[0] for row in data]
        departments = [row[1] for row in data]
        batches = [row[2] for row in data]
        encodings = [np.frombuffer(row[3]) for row in data]
        return names, departments, batches, encodings

    def main():
        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)

            faces_cur_frame = face_recognition.face_locations(img_s)
            encode_cur_frame = face_recognition.face_encodings(img_s, faces_cur_frame)

            for encode_face, face_loc in zip(encode_cur_frame, faces_cur_frame):
                matches = face_recognition.compare_faces(encode_list_known, encode_face)
                face_dis = face_recognition.face_distance(encode_list_known, encode_face)
                match_index = np.argmin(face_dis)

                if matches[match_index]:
                    name = names[match_index]
                    department = departments[match_index]
                    batch = batches[match_index]
                    print(name, department, batch)
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = 4 * y1, 4 * x2, 4 * y2, 4 * x1
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 + 60), (x2, y2), (0, 255, 0), 2, cv2.FILLED)
                    cv2.putText(img, f"Name: {name}", (x1 + 6, y2 + 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
                    cv2.putText(img, f"Department: {department}", (x1 + 6, y2 + 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
                    cv2.putText(img, f"Batch: {batch}", (x1 + 6, y2 + 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
                    mark_attendance(name)

            cv2.imshow('Webcam', img)
            cv2.waitKey(2)

    create_attendance_table()
    names, departments, batches, encode_list_known = load_known_encodings()
    main()

def open_registration_window():
    create_user_registration_window()

def open_attendance_window():
    create_attendance_marking_window()

create_main_menu()
