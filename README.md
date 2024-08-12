# Flask Image Processing Application

This Flask application allows users to authenticate, crop images, extract text from images using OCR, and store the extracted data in a MySQL database.

## Features

- **User Authentication**: Secure login with email and password.
- **Image Cropping**: Crop images based on specified dimensions.
- **Text Extraction**: Extract text from cropped images using Tesseract OCR.
- **Data Storage**: Store extracted contact information and timestamps in a MySQL database.

## Prerequisites

- Python 3.7 or higher
- MySQL Server

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LAKSHMI-DEVI-REDDY-MALLI/ImageTextExtractor
   cd <repository-directory>
2. **Set Up a Virtual Environment (optional but recommended)**:
     python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install Dependencies**:
   pip install -r requirements.txt
4. **Configure the Application**:
   =>Open main.py in a text editor.
   =>Update the SQLALCHEMY_DATABASE_URI configuration with your MySQL database credentials:
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/your_database'
5. **Create Database Tables**:
   Run the application to create the necessary tables in your MySQL database:
   =>python app.py
   After the tables are created, you can stop the server.
6. **Run the Application**:
   python app.py
7. **Access the Application**:
   Open your web browser and go to http://localhost:5000 to use the application.

**Usage**
# Login:

Navigate to the login page at http://localhost:5000/login.
Enter your email and password to access the application.
# Crop Images:

Go to the cropping page at http://localhost:5000/crop.
Provide the input folder path, output folder path, and cropping dimensions (width, height, upper, and left).
Submit the form to crop images in the specified input folder and save them to the output folder.
# Upload Images:

Go to the upload page at http://localhost:5000/upload.
Upload the cropped images.
The application will extract text from the images and store the data in the MySQL database.
# Logout:

Access the logout endpoint at http://localhost:5000/logout to end your session and return to the login page.

**Acknowledgements**
Flask: Micro web framework for Python.
Flask-SQLAlchemy: SQL toolkit and ORM for Python.
Pillow: Python Imaging Library (PIL) fork.
pytesseract: Python wrapper for Google's Tesseract-OCR Engine.
mysqlclient: MySQL database adapter for Python.