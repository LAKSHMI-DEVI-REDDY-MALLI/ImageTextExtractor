from flask import Flask, render_template, request, redirect, url_for, session
from collections import Counter
from PIL import Image
import pytesseract
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://twitter_db_user:swEqodl2aP_PrUrU0AkA@mysql.razs.me/angular_twitter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ExtractedData(db.Model):
    contact_name = db.Column(db.String(255), primary_key=True)
    count = db.Column(db.Integer, default=1)
    last_seen = db.Column(db.DateTime)
    image_count = db.Column(db.Integer, default=1)

# Dummy user data for demonstration
users = {
    'user@example.com': 'password123'
}

@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('crop'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['email'] = email
            return redirect(url_for('crop'))
        else:
            return 'Invalid email or password'
    return render_template('login.html')

@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        input_folder = request.form['input_folder']
        output_folder = request.form['output_folder']
        crop_width = int(request.form['crop_width'])
        crop_height = int(request.form['crop_height'])
        crop_upper = int(request.form['crop_upper'])
        crop_left = int(request.form['crop_left'])
        
        crop_images_in_folder(input_folder, output_folder, crop_width, crop_height, crop_upper, crop_left)
        
        return redirect(url_for('upload'))
    
    return render_template('crop.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'files[]' not in request.files:
            return 'No file part'
        
        files = request.files.getlist('files[]')

        for file in files:
            if file.filename == '':
                return 'No selected file'

            if file:
                image = Image.open(file)
                extracted_text = pytesseract.image_to_string(image)
                contact_names, last_seen_times = extract_contact_info(extracted_text)
                contact_name_counts = Counter(contact_names)
                
                for contact_name, last_seen in zip(contact_name_counts.keys(), last_seen_times):
                    try:
                        format_string = '%I:%M %p'
                        last_seen_datetime = datetime.strptime(last_seen, format_string)
                    except ValueError:
                        format_string = '%I:%M%p'
                        last_seen_datetime = datetime.strptime(last_seen, format_string)

                    existing_data = ExtractedData.query.filter_by(contact_name=contact_name).first()

                    if existing_data:
                        existing_data.count += 1
                    else:
                        new_data = ExtractedData(
                            contact_name=contact_name,
                            last_seen=last_seen_datetime,
                            image_count=1,
                            count=1
                        )
                        db.session.add(new_data)

        db.session.commit()

        return 'Upload successful!'

    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

def extract_contact_info(extracted_text):
    contact_names = []
    last_seen_times = []

    lines = extracted_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Ignore irrelevant lines
        if "¢" in line or "yesterday" in line.lower() or any(word.lower() in line.lower() for word in ["IG@OGeSGRODO", "SOOOS", "today", "aGe", "-POSOC", "2e6", "@00@", "BGOZEGOOSCSBOOO", "5 e", "BSar2a eg", "@9g DdDOevec", "i> Bo", "SOS Aer Sh BOOM", "0G: =~ HG"]):
            continue

        # Match time
        match_time = re.match(r'^\d{1,2}:\d{2}\s*(?:AM|PM)?$', line)
        if match_time:
            last_seen_times.append(line)
            continue

        # Match name
        match_name = re.match(r'^[\w\s.@+-]+$', line)
        if match_name:
            contact_names.append(line)

    return contact_names, last_seen_times


def crop_images_in_folder(input_folder, output_folder, crop_width, crop_height, crop_upper, crop_left):
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)

            with Image.open(input_image_path) as img:
                crop_right = crop_left + crop_width
                crop_lower = crop_upper + crop_height
                cropped_img = img.crop((crop_left, crop_upper, crop_right, crop_lower))
                cropped_img.save(output_image_path)

            print(f"Cropping completed for {filename}!")

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
