# Facial Recognition Attendance System

This project automates the student attendance process using facial recognition technology. It leverages Python libraries and a SQLite database to detect and log student attendance in real time via a webcam.

## Table of Contents
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [File Structure](#file-structure)
7. [How It Works](#how-it-works)
8. [License](#license)

## Features
- Real-time face detection and recognition.
- Attendance logging with timestamps in a SQLite database.
- User interface for registering student details and facial data.
- Export attendance records in CSV format for easy analysis.
- Modular and user-friendly design.

## Technologies Used
- Programming Language: Python
- Libraries and Frameworks:
  - `OpenCV` for image processing and real-time video streaming.
  - `face_recognition` for facial detection and recognition.
  - `SQLite3` for database management.
  - `Tkinter` for the graphical user interface.
  - `CSV` for attendance records.
  - `Pillow` for image handling.
  - `NumPy` for numerical operations.

## Prerequisites
Ensure you have the following installed on your system:
1. Python 3.8 or later: [Download Python](https://www.python.org/downloads/)
2. Required Python libraries (install during setup):
   - OpenCV
   - NumPy
   - face_recognition
   - Pillow
   - SQLite3 (pre-installed with Python)
   - Tkinter (pre-installed with Python)
