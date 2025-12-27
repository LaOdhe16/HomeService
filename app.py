import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, join_room
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import midtransclient

# SETUP DATABASE & APP 
app = Flask(__name__)

# KONFIGURASI DATABASE 
NAMA_FILE_DB = 'yenggeeeee_homeservice.db' 

# Menggunakan path absolute agar Azure bisa menemukannya dengan tepat
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, NAMA_FILE_DB)

# KONFIGURASI KEAMANAN 
app.config['SECRET_KEY'] = 'yengge_project_kuliah_secret_key_12345'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SETUP MIDTRANS 
MIDTRANS_SERVER_KEY = "Mid-server-9NyMBFybZuxA9yqssL8Vz2gN"  
MIDTRANS_CLIENT_KEY = "Mid-client-JOSeyl8ssNZ0G6YG"  

snap = midtransclient.Snap(
    is_production=False, 
    server_key=MIDTRANS_SERVER_KEY,
    client_key=MIDTRANS_CLIENT_KEY
)

db = SQLAlchemy(app)

# SETUP SOCKETIO AZURE
socketio = SocketIO(app, async_mode='eventlet') 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# MODELS (DATABASE TABEL) 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user') 

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(500))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    admin = db.relationship('User', backref='services')
    reviews = db.relationship('Review', backref='service_rel', lazy=True, cascade="all, delete-orphan")

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    status = db.Column(db.String(50), default='UNPAID')
    payment_method = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    service = db.relationship('Service')
    user = db.relationship('User')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    user = db.relationship('User')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ROUTES 

@app.route('/')
def index():
    q = request.args.get('q')
    if q:
        services = Service.query.filter(Service.title.contains(q)).all()
    else:
        services = Service.query.all()
    return render_template('index.html', services=services)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Email atau password salah.', 'error')
    return render_template('auth.html', mode='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar.', 'error')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('auth.html', mode='register')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        my_services = Service.query.filter_by(admin_id=current_user.id).all()
        ids = [s.id for s in my_services]
        bookings = Booking.query.filter(Booking.service_id.in_(ids)).order_by(Booking.date_created.desc()).all()
        income = sum(b.service.price for b in bookings if b.status == 'PAID')
        return render_template('dashboard_admin.html', bookings=bookings, services=my_services, income=income)
    else:
        bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.date_created.desc()).all()
        return render_template('dashboard_user.html', bookings=bookings)

@app.route('/admin/add_service', methods=['POST'])
@login_required
def add_service():
    if current_user.role != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    image = request.form.get('image')

    if title and price:
        new_service = Service(title=title, description=description, price=int(price), image=image, admin_id=current_user.id)
        db.session.add(new_service)
        db.session.commit()
        flash('Jasa berhasil ditambahkan!', 'success')
    else:
        flash('Mohon lengkapi data jasa.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/admin/delete_service/<int:id>')
@login_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    if current_user.role != 'admin' or service.admin_id != current_user.id:
        flash('Anda tidak berhak menghapus jasa ini.', 'error')
        return redirect(url_for('dashboard'))
    try:
        db.session.delete(service)
        db.session.commit()
        flash('Jasa berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Gagal menghapus jasa. Pastikan tidak ada booking aktif.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/service/<int:id>', methods=['GET', 'POST'])
def service_detail(id):
    service = Service.query.get_or_404(id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Login untuk review.', 'error')
            return redirect(url_for('login'))
        if current_user.role != 'user':
            flash('Hanya user biasa yang bisa review.', 'warning')
            return redirect(request.url)
        comment = request.form.get('comment')
        rating = request.form.get('rating')
        if comment and rating:
            new_review = Review(content=comment, rating=int(rating), user_id=current_user.id, service_id=id)
            db.session.add(new_review)
            db.session.commit()
            flash('Ulasan berhasil dikirim!', 'success')
            return redirect(request.url)
    return render_template('detail.html', service=service)

@app.route('/book/<int:service_id>')
@login_required
def book_service(service_id):
    count = Booking.query.count() + 1
    inv_num = f"INV-{int(time.time())}-{count:04d}"
    new_booking = Booking(user_id=current_user.id, service_id=service_id, invoice_number=inv_num, status='UNPAID')
    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for('invoice', booking_id=new_booking.id))

@app.route('/invoice/<int:booking_id>')
@login_required
def invoice(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and booking.service.admin_id != current_user.id:
        return redirect(url_for('index'))
    messages = Message.query.filter_by(booking_id=booking_id).order_by(Message.timestamp.asc()).all()
    return render_template('invoice.html', booking=booking, chat_history=messages, client_key=MIDTRANS_CLIENT_KEY)

@app.route('/get_payment_token/<int:booking_id>')
@login_required
def get_payment_token(booking_id):
    try:
        booking = Booking.query.get_or_404(booking_id)
        param = {
            "transaction_details": {"order_id": booking.invoice_number, "gross_amount": int(booking.service.price)},
            "customer_details": {"first_name": booking.user.name, "email": booking.user.email},
            "item_details": [{"id": str(booking.service.id), "price": int(booking.service.price), "quantity": 1, "name": booking.service.title[:45]}],
            "callbacks": {"finish": url_for('payment_success', booking_id=booking.id, _external=True)}
        }
        transaction = snap.create_transaction(param)
        return jsonify({'token': transaction['token']})
    except Exception as e:
        print(f"Midtrans Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/payment_success/<int:booking_id>')
@login_required
def payment_success(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'PAID'
    booking.payment_method = 'Midtrans Gateway'
    db.session.commit()
    flash('Pembayaran Berhasil Diterima!', 'success')
    return redirect(url_for('invoice', booking_id=booking.id))

@app.route('/force_pay/<int:booking_id>')
def force_pay(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'PAID'
    booking.payment_method = 'Developer Bypass'
    db.session.commit()
    return redirect(url_for('invoice', booking_id=booking_id))

@socketio.on('join')
def on_join(data):
    join_room(data['booking_id'])

@socketio.on('kirim_pesan_private')
def handle_private_message(data):
    msg = Message(booking_id=data['booking_id'], sender_name=current_user.name, role=current_user.role, message=data['msg'])
    db.session.add(msg)
    db.session.commit()
    emit('terima_pesan', {'msg': data['msg'], 'sender': current_user.name}, to=data['booking_id'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
            

    socketio.run(app, debug=True)
