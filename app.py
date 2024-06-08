import os
import json
import numpy as np
import pickle
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import face_recognition

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://martin:password@localhost/reconocimiento_facial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    face_encoding = db.Column(db.LargeBinary, nullable=True)

@app.route('/')
def index():
    return redirect(url_for('sign_in'))

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Sesión iniciada exitosamente!')
            return redirect(url_for('home'))
        flash('Correo electrónico o contraseña incorrectos')
    return render_template('sign_in.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            image = face_recognition.load_image_file(file_path)
            face_encodings = face_recognition.face_encodings(image)

            if not face_encodings:
                flash('No se encontró un rostro en la imagen subida.')
                return redirect(url_for('sign_up'))

            face_encoding = pickle.dumps(face_encodings[0])
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, password=hashed_password, image=filename, face_encoding=face_encoding)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Cuenta creada exitosamente!')
                return redirect(url_for('sign_in'))
            except IntegrityError:
                db.session.rollback()
                flash('El correo electrónico ya existe')
        else:
            flash('Tipo de archivo no válido. Por favor sube un archivo de imagen.')
    return render_template('sign_up.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    return render_template('home.html')

@app.route('/sign_in_face', methods=['POST'])
def sign_in_face():
    data = request.json
    email = data['email']
    face_descriptor = np.array(data['faceDescriptor'], dtype=float)

    user = User.query.filter_by(email=email).first()
    if user:
        user_face_encoding = pickle.loads(user.face_encoding)
        matches = face_recognition.compare_faces([user_face_encoding], face_descriptor)
        if matches[0]:
            session['user_id'] = user.id
            return jsonify(success=True)
    return jsonify(success=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    with app.app_context():
        db.create_all()
    app.run(debug=True)
