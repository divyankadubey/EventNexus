from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
from models import db, Event, Guest, Booking, User
from config import Config
from datetime import datetime
from sqlalchemy import func
from functools import wraps
import re
import random
import os
import json
from twilio_service import twilio_service
from qr_service import qr_service
from email_service import email_otp_service
from enhanced_email_service import enhanced_email_service

app = Flask(__name__)
app.config.from_object(Config) 

# Update configuration for development
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    WTF_CSRF_ENABLED=False  # Disable CSRF for development
)

# Test route to verify server is running
@app.route('/test')
def test():
    return 'Server is running!', 200

# Initialize database
db.init_app(app)

# Initialize enhanced email service
enhanced_email_service.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    
    # Update existing guests to have guest_count = 1 if not set
    from models import Guest
    guests_to_update = Guest.query.filter(Guest.guest_count.is_(None)).all()
    for guest in guests_to_update:
        guest.guest_count = 1
    if guests_to_update:
        db.session.commit()
        print(f"Updated {len(guests_to_update)} guests with default guest_count")


# Validation helper functions
def validate_gmail(email):
    """Validate that email is a Gmail address"""
    if not email:
        return True  # Allow empty email
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate that phone is exactly 10 digits"""
    if not phone:
        return True  # Allow empty phone
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone) is not None


def validate_future_date(date_str):
    """Validate that the date is today or in the future"""
    try:
        input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        if input_date < today:
            return False, "Event date cannot be in the past. Please select today's date or a future date."
        return True, ""
    except ValueError as e:
        return False, "Invalid date format. Please use YYYY-MM-DD."

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


# Role-based decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Check if it's an AJAX/JSON request
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'Please login to access this feature'
                }), 401
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'Admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'User':
            flash('Access denied. User privileges required.', 'error')
            return redirect(url_for('admin_dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ============= AUTHENTICATION ROUTES =============

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.role == 'Admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            session['role'] = user.role
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect based on role
            if user.role == 'Admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username/email or password', 'error')
    
    return render_template('auth/login.html')
              

@app.route('/register', methods=['GET', 'POST']) 
def register():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            full_name = request.form.get('full_name')
            
            # Validate passwords match
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('auth/register.html')
            
            # Validate Gmail only
            if not email.lower().endswith('@gmail.com'):
                flash('Invalid email! Only @gmail.com addresses are allowed.', 'error')
                return render_template('auth/register.html')
            
            # Validate phone number
            if phone and not validate_phone(phone):
                flash('Invalid phone number. Must be 10 digits.', 'error')
                return render_template('auth/register.html')
            
            # Check if username exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return render_template('auth/register.html')
            
            # Check if email exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return render_template('auth/register.html')
            
            # Check if phone exists
            if phone and User.query.filter_by(phone=phone).first():
                flash('Phone number already registered', 'error')
                return render_template('auth/register.html')
            
            # Create new user
            user = User(
                username=username,
                email=email,
                phone=phone,
                full_name=full_name
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('auth/register.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))


# ============= MOBILE OTP AUTHENTICATION =============

@app.route('/mobile-register', methods=['GET', 'POST'])
def mobile_register():
    """Register new user with mobile number (OTP verification disabled)"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            
            # Validate phone number
            if not validate_phone(phone):
                return jsonify({'success': False, 'message': 'Invalid phone number. Must be 10 digits.'}), 400
            
            # Check if phone exists
            if User.query.filter_by(phone=phone).first():
                return jsonify({'success': False, 'message': 'Phone number already registered'}), 400
            
            # Check if email exists (if provided)
            if email and User.query.filter_by(email=email).first():
                return jsonify({'success': False, 'message': 'Email already registered'}), 400
            
            # Create username from phone
            username = f"user_{phone}"
            
            # Create new user directly (skip OTP verification)
            user = User(
                username=username,
                phone=phone,
                email=email or f"{phone}@temp.com",
                full_name=full_name
            )
            # Set phone number as default password (user can change later)
            user.set_password(phone)  
            
            db.session.add(user)
            db.session.commit()
            
            # Auto-login user
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            
            return jsonify({
                'success': True,
                'message': 'Registration successful! You are now logged in.',
                'redirect': url_for('dashboard')
            })
                
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    return render_template('auth/mobile_register.html')


@app.route('/mobile-register/verify-otp', methods=['POST'])
def verify_registration_otp():
    """Verify OTP and complete registration"""
    try:
        user_otp = request.form.get('otp') or request.json.get('otp')
        
        if 'pending_registration' not in session:
            return jsonify({'success': False, 'message': 'No pending registration found'}), 400
        
        pending = session['pending_registration']
        stored_otp = pending.get('otp')
        
        # Verify OTP
        if str(stored_otp) == str(user_otp):
            # Create username from phone
            username = f"user_{pending['phone']}"
            
            # Create new user
            user = User(
                username=username,
                phone=pending['phone'],
                email=pending.get('email', f"{pending['phone']}@temp.com"),
                full_name=pending['full_name']
            )
            # Set a default password (user can change later)
            user.set_password(pending['phone'])  
            
            db.session.add(user)
            db.session.commit()
            
            # Clear pending registration
            session.pop('pending_registration', None)
            
            # Auto-login user
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            
            return jsonify({
                'success': True,
                'message': 'Registration successful!',
                'redirect': url_for('dashboard')
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid OTP'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/mobile-login', methods=['GET', 'POST'])
def mobile_login():
    """Login with mobile number and OTP"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            phone = request.form.get('phone')
            
            # Validate phone
            if not validate_phone(phone):
                return jsonify({'success': False, 'message': 'Invalid phone number'}), 400
            
            # Check if user exists
            user = User.query.filter_by(phone=phone).first()
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Phone number not registered. Please sign up first.'
                }), 404
            
            # Generate OTP
            otp = twilio_service.generate_otp()
            
            # Send OTP
            success, message, message_sid = twilio_service.send_otp(
                phone,
                otp,
                "Login Verification"
            )
            
            if success:
                # Store OTP in session
                session['login_otp'] = {
                    'phone': phone,
                    'otp': otp,
                    'user_id': user.id,
                    'timestamp': datetime.utcnow().isoformat()
                }
                return jsonify({
                    'success': True,
                    'message': 'OTP sent to your mobile number!',
                    'phone': phone
                })
            else:
                return jsonify({'success': False, 'message': message}), 500
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    return render_template('auth/mobile_login.html')


@app.route('/mobile-login/verify-otp', methods=['POST'])
def verify_login_otp():
    """Verify OTP and login user"""
    try:
        user_otp = request.form.get('otp') or request.json.get('otp')
        
        if 'login_otp' not in session:
            return jsonify({'success': False, 'message': 'No pending login found'}), 400
        
        login_data = session['login_otp']
        stored_otp = login_data.get('otp')
        
        # Verify OTP
        if str(stored_otp) == str(user_otp):
            user = User.query.get(login_data['user_id'])
            
            if user:
                # Login user
                session.pop('login_otp', None)
                session['user_id'] = user.id
                session['username'] = user.username
                session['full_name'] = user.full_name
                
                return jsonify({
                    'success': True,
                    'message': f'Welcome back, {user.full_name}!',
                    'redirect': url_for('dashboard')
                })
            else:
                return jsonify({'success': False, 'message': 'User not found'}), 404
        else:
            return jsonify({'success': False, 'message': 'Invalid OTP'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


# Public landing page
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Admin Dashboard Route
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard showing comprehensive overview"""
    total_events = Event.query.count()
    upcoming_events = Event.query.filter(Event.event_date >= datetime.now().date()).count()
    total_guests = Guest.query.count()
    total_users = User.query.count()
    
    # RSVP statistics
    rsvp_stats = {
        'pending': Guest.query.filter_by(rsvp_status='Pending').count(),
        'accepted': Guest.query.filter_by(rsvp_status='Accepted').count(),
        'declined': Guest.query.filter_by(rsvp_status='Declined').count()
    }
    
    # Recent events
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_events=total_events,
                         upcoming_events=upcoming_events,
                         total_guests=total_guests,
                         total_users=total_users,
                         rsvp_stats=rsvp_stats,
                         recent_events=recent_events)

# Legacy Dashboard Route (redirects based on role)
@app.route('/dashboard')
@login_required
def dashboard():
    """Redirect to appropriate dashboard based on user role"""
    user = User.query.get(session['user_id'])
    if user and user.role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

# User Dashboard Route  
@app.route('/user/dashboard')
@user_required
def user_dashboard():
    """User dashboard for event discovery and bookings"""
    # Show upcoming events for users to discover
    upcoming_events = Event.query.filter(
        Event.event_date >= datetime.now().date(),
        Event.status == 'Confirmed'
    ).order_by(Event.event_date.asc()).limit(10).all()
    
    # User's bookings (if any)
    user_id = session.get('user_id')
    user_bookings = []
    if user_id:
        # Get events where user has registered as guest
        user_guest_entries = Guest.query.filter_by(email=session.get('username', '')).all()
        user_events = [guest.event for guest in user_guest_entries]
        user_bookings = user_events
    
    return render_template('user/dashboard.html',
                         upcoming_events=upcoming_events,
                         user_bookings=user_bookings)


# ============= EVENT ROUTES =============

@app.route('/events')
@login_required
def events_list():
    """List all events"""
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('events/list.html', events=events)


def validate_future_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if date < datetime.now().date():
            return False, 'Error: Date must be in the future'
        return True, ''
    except ValueError:
        return False, 'Error: Invalid date format (YYYY-MM-DD)'


@app.route('/events/create', methods=['GET', 'POST'])
@admin_required
def event_create():
    """Create a new event"""
    if request.method == 'POST':
        # Validate date
        is_valid_date, date_error = validate_future_date(request.form['event_date'])
        if not is_valid_date:
            flash(date_error, 'error')
            return render_template('events/create.html', form_data=request.form)
            
        try:
            event = Event(
                name=request.form['name'],
                description=request.form.get('description'),
                event_date=datetime.strptime(request.form['event_date'], '%Y-%m-%d').date(),
                event_time=datetime.strptime(request.form['event_time'], '%H:%M').time() if request.form.get('event_time') else None,
                location=request.form.get('location'),
                latitude=float(request.form.get('latitude')) if request.form.get('latitude') else None,
                longitude=float(request.form.get('longitude')) if request.form.get('longitude') else None,
                venue_capacity=int(request.form.get('venue_capacity')) if request.form.get('venue_capacity') else None,
                budget=float(request.form.get('budget', 0)),
                status=request.form.get('status', 'Planning')
            )
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('events_list'))
        except Exception as e:
            flash(f'Error creating event: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('events/create.html')


@app.route('/events/<int:id>')
def event_detail(id):
    """View event details"""
    event = Event.query.get_or_404(id)
    guests = Guest.query.filter_by(event_id=id).all()
    bookings = Booking.query.filter_by(event_id=id).all()
    
    # Calculate total booking cost
    total_booking_cost = sum([float(b.cost) for b in bookings])
    
    return render_template('events/detail.html', 
                         event=event, 
                         guests=guests, 
                         bookings=bookings,
                         total_booking_cost=total_booking_cost)


@app.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def event_edit(id):
    """Edit an event"""
    event = Event.query.get_or_404(id)
    
    if request.method == 'POST':
        # Validate date
        is_valid_date, date_error = validate_future_date(request.form['event_date'])
        if not is_valid_date:
            flash(date_error, 'error')
            return render_template('events/edit.html', event=event, form_data=request.form)
            
        try:
            event.name = request.form['name']
            event.description = request.form.get('description')
            event.event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()
            event.event_time = datetime.strptime(request.form['event_time'], '%H:%M').time() if request.form.get('event_time') else None
            event.location = request.form.get('location')
            event.latitude = float(request.form.get('latitude')) if request.form.get('latitude') else None
            event.longitude = float(request.form.get('longitude')) if request.form.get('longitude') else None
            event.venue_capacity = int(request.form.get('venue_capacity')) if request.form.get('venue_capacity') else None
            event.budget = float(request.form.get('budget', 0))
            event.status = request.form.get('status', 'Planning')
            
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('event_detail', id=id))
        except Exception as e:
            flash(f'Error updating event: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('events/edit.html', event=event)


@app.route('/events/<int:id>/delete', methods=['POST'])
@admin_required
def event_delete(id):
    """Delete an event"""
    try:
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting event: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('events_list'))


# ============= GUEST API ROUTES =============

@app.route('/api/guests', methods=['POST'])
def api_create_guest():
    """API endpoint for creating guests from user dashboard"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('phone'):
            return jsonify({
                'success': False,
                'message': 'Name, email, and phone are required'
            }), 400
        
        # Get event
        event_id = data.get('event_id')
        if not event_id:
            return jsonify({
                'success': False,
                'message': 'Event ID is required'
            }), 400
        
        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404
        
        # Validate email format (remove Gmail restriction for API)
        email = data['email']
        if not enhanced_email_service.validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email address format'
            }), 400
        
        # Validate phone
        phone = data['phone']
        if not validate_phone(phone):
            return jsonify({
                'success': False,
                'message': 'Phone number must be exactly 10 digits'
            }), 400
        
        # Check venue capacity
        guest_count = int(data.get('guest_count', 1))
        if event.venue_capacity:
            current_guests = db.session.query(func.sum(Guest.guest_count)).filter_by(event_id=event_id).scalar() or 0
            if current_guests + guest_count > event.venue_capacity:
                return jsonify({
                    'success': False,
                    'message': f'Adding {guest_count} guests would exceed venue capacity of {event.venue_capacity}. Current guests: {current_guests}'
                }), 400
        
        # Create guest
        guest = Guest(
            event_id=event_id,
            name=data['name'],
            email=email,
            phone=phone,
            rsvp_status='Accepted',  # Auto-accept for user registrations
            guest_count=guest_count,
            dietary_requirements=data.get('dietary_requirements', '')
        )
        db.session.add(guest)
        db.session.commit()
        
        # Send event invitation email
        email_sent = False
        try:
            email_sent = enhanced_email_service.send_event_invitation(guest, event)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        # Generate QR code
        try:
            qr_service.generate_qr_code(guest)
        except Exception as e:
            print(f"QR code generation failed: {e}")
        
        return jsonify({
            'success': True,
            'message': f'Registration successful! {"Invitation email sent to " + email if email_sent else "Email notification failed"}',
            'guest_id': guest.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@app.route('/api/events/<int:event_id>')
def api_get_event(event_id):
    """API endpoint to get event details"""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({
                'success': False,
                'message': 'Event not found'
            }), 404
        
        return jsonify({
            'success': True,
            'event': event.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading event: {str(e)}'
        }), 500

# ============= GUEST ROUTES =============

@app.route('/guests')
@user_required
def guests_list():
    """List all guests"""
    guests = Guest.query.order_by(Guest.created_at.desc()).all()
    return render_template('guests/list.html', guests=guests)


@app.route('/guests/<int:id>/qr')
@login_required
def view_guest_qr(id):
    """View guest QR code"""
    guest = Guest.query.get_or_404(id)
    return render_template('guests/qr_display.html', guest=guest)


@app.route('/guests/create', methods=['GET', 'POST'])
@user_required
def guest_create():
    """Create a new guest"""
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            phone = request.form.get('phone')
            event_id = int(request.form['event_id'])
            guest_count = int(request.form.get('guest_count', 1))
            
            # Validate Gmail
            if email and not validate_gmail(email):
                flash('Error: Only Gmail addresses are accepted (e.g., user@gmail.com)', 'error')
                events = Event.query.all()
                return render_template('guests/create.html', events=events)
            
            # Validate Phone
            if phone and not validate_phone(phone):
                flash('Error: Phone number must be exactly 10 digits', 'error')
                events = Event.query.all()
                return render_template('guests/create.html', events=events)
            
            # Check venue capacity
            event = Event.query.get(event_id)
            if event and event.venue_capacity:
                current_guests = db.session.query(func.sum(Guest.guest_count)).filter_by(event_id=event_id).scalar() or 0
                if current_guests + guest_count > event.venue_capacity:
                    flash(f'Error: Adding {guest_count} guests would exceed venue capacity of {event.venue_capacity}. Current guests: {current_guests}', 'error')
                    events = Event.query.all()
                    return render_template('guests/create.html', events=events)
            
            guest = Guest(
                event_id=event_id,
                name=request.form['name'],
                email=email,
                phone=phone,
                rsvp_status=request.form.get('rsvp_status', 'Pending'),
                guest_count=guest_count,
                dietary_requirements=request.form.get('dietary_requirements')
            )
            db.session.add(guest)
            db.session.commit()
            
            # Send event invitation email
            if email and event:
                try:
                    email_sent = enhanced_email_service.send_event_invitation(guest, event)
                    if email_sent:
                        flash(f'Guest added successfully! Invitation email sent to {email}', 'success')
                    else:
                        flash('Guest added successfully! (Email notification failed)', 'warning')
                except Exception as e:
                    flash(f'Guest added successfully! (Email error: {str(e)})', 'warning')
            else:
                flash('Guest added successfully!', 'success')
            
            return redirect(url_for('guests_list'))
        except Exception as e:
            flash(f'Error adding guest: {str(e)}', 'error')
            db.session.rollback()
    
    events = Event.query.all()
    return render_template('guests/create.html', events=events)


@app.route('/guests/<int:id>/edit', methods=['GET', 'POST'])
@user_required
def guest_edit(id):
    """Edit a guest"""
    guest = Guest.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            phone = request.form.get('phone')
            
            # Validate Gmail
            if email and not validate_gmail(email):
                flash('Error: Only Gmail addresses are accepted (e.g., user@gmail.com)', 'error')
                events = Event.query.all()
                return render_template('guests/edit.html', guest=guest, events=events)
            
            # Validate Phone
            if phone and not validate_phone(phone):
                flash('Error: Phone number must be exactly 10 digits', 'error')
                events = Event.query.all()
                return render_template('guests/edit.html', guest=guest, events=events)
            
            guest.event_id = int(request.form['event_id'])
            guest.name = request.form['name']
            guest.email = email
            guest.phone = phone
            guest.rsvp_status = request.form.get('rsvp_status', 'Pending')
            guest.guest_count = int(request.form.get('guest_count', 1))
            guest.dietary_requirements = request.form.get('dietary_requirements')
            
            db.session.commit()
            flash('Guest updated successfully!', 'success')
            return redirect(url_for('guests_list'))
        except Exception as e:
            flash(f'Error updating guest: {str(e)}', 'error')
            db.session.rollback()
    
    events = Event.query.all()
    return render_template('guests/edit.html', guest=guest, events=events)


@app.route('/guests/<int:id>/delete', methods=['POST'])
@user_required
def guest_delete(id):
    """Delete a guest"""
    try:
        guest = Guest.query.get_or_404(id)
        db.session.delete(guest)
        db.session.commit()
        flash('Guest deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting guest: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('guests_list'))


# ============= BOOKING ROUTES =============

@app.route('/bookings')
@user_required
def bookings_list():
    """List all bookings"""
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('bookings/list.html', bookings=bookings)


@app.route('/bookings/create', methods=['GET', 'POST'])
@user_required
def booking_create():
    """Create a new booking"""
    if request.method == 'POST':
        try:
            # Automatically set status to Confirmed instead of Pending
            booking = Booking(
                event_id=int(request.form['event_id']),
                booking_type=request.form['booking_type'],
                vendor_name=request.form['vendor_name'],
                description=request.form.get('description'),
                cost=float(request.form.get('cost', 0)),
                booking_date=datetime.strptime(request.form['booking_date'], '%Y-%m-%d').date() if request.form.get('booking_date') else None,
                status='Confirmed',  # Auto-confirm bookings
                contact_info=request.form.get('contact_info'),
                notes=request.form.get('notes')
            )
            db.session.add(booking)
            db.session.commit()
            flash('Booking created and automatically confirmed!', 'success')
            return redirect(url_for('bookings_list'))
        except Exception as e:
            flash(f'Error creating booking: {str(e)}', 'error')
            db.session.rollback()
    
    events = Event.query.all()
    return render_template('bookings/create.html', events=events)


@app.route('/bookings/<int:id>/edit', methods=['GET', 'POST'])
@user_required
def booking_edit(id):
    """Edit a booking"""
    booking = Booking.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            booking.event_id = int(request.form['event_id'])
            booking.booking_type = request.form['booking_type']
            booking.vendor_name = request.form['vendor_name']
            booking.description = request.form.get('description')
            booking.cost = float(request.form.get('cost', 0))
            booking.booking_date = datetime.strptime(request.form['booking_date'], '%Y-%m-%d').date() if request.form.get('booking_date') else None
            booking.status = request.form.get('status', 'Pending')
            booking.contact_info = request.form.get('contact_info')
            booking.notes = request.form.get('notes')
            
            db.session.commit()
            flash('Booking updated successfully!', 'success')
            return redirect(url_for('bookings_list'))
        except Exception as e:
            flash(f'Error updating booking: {str(e)}', 'error')
            db.session.rollback()
    
    events = Event.query.all()
    return render_template('bookings/edit.html', booking=booking, events=events)


@app.route('/bookings/<int:id>/delete', methods=['POST'])
@user_required
def booking_delete(id):
    """Delete a booking"""
    try:
        booking = Booking.query.get_or_404(id)
        db.session.delete(booking)
        db.session.commit()
        flash('Booking deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting booking: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('bookings_list'))


# ============= OTP ROUTES (TWILIO) =============

@app.route('/guests/<int:id>/send-otp', methods=['POST'])
def send_guest_otp(id):
    """Send OTP to guest via SMS for verification"""
    try:
        guest = Guest.query.get_or_404(id)
        
        if not guest.phone:
            return jsonify({
                'success': False, 
                'message': 'Guest does not have a phone number'
            }), 400
        
        # Validate phone number
        if not validate_phone(guest.phone):
            return jsonify({
                'success': False,
                'message': 'Invalid phone number format. Must be 10 digits.'
            }), 400
        
        # Generate OTP
        otp = twilio_service.generate_otp()
        
        # Get event name for context
        event_name = guest.event.name if guest.event else None
        
        # Send OTP via Twilio
        success, message, message_sid = twilio_service.send_otp(
            guest.phone, 
            otp, 
            event_name
        )
        
        if success:
            # Save OTP to database
            guest.otp = otp
            guest.otp_verified = False
            db.session.commit()
            
            flash(f'OTP sent successfully to {guest.phone}!', 'success')
            return jsonify({
                'success': True,
                'message': message,
                'message_sid': message_sid
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sending OTP: {str(e)}'
        }), 500


@app.route('/guests/<int:id>/verify-otp', methods=['POST'])
def verify_guest_otp(id):
    """Verify guest OTP"""
    try:
        guest = Guest.query.get_or_404(id)
        user_otp = request.form.get('otp') or request.json.get('otp')
        
        if not user_otp:
            return jsonify({
                'success': False,
                'message': 'Please enter OTP'
            }), 400
        
        if not guest.otp:
            return jsonify({
                'success': False,
                'message': 'No OTP was sent. Please request a new OTP.'
            }), 400
        
        # Verify OTP (simple comparison for now)
        if str(guest.otp) == str(user_otp):
            guest.otp_verified = True
            guest.rsvp_status = 'Accepted'
            db.session.commit()
            
            flash('Phone number verified successfully!', 'success')
            return jsonify({
                'success': True,
                'message': 'OTP verified successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid OTP. Please try again.'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error verifying OTP: {str(e)}'
        }), 500


@app.route('/guests/<int:id>/send-reminder', methods=['POST'])
def send_event_reminder(id):
    """Send event reminder SMS to guest"""
    try:
        guest = Guest.query.get_or_404(id)
        event = guest.event
        
        if not guest.phone:
            return jsonify({
                'success': False,
                'message': 'Guest does not have a phone number'
            }), 400
        
        # Send reminder
        success, message, message_sid = twilio_service.send_event_reminder(
            guest.phone,
            guest.name,
            event.name,
            event.event_date.strftime('%d %b %Y') if event.event_date else 'TBD',
            event.event_time.strftime('%I:%M %p') if event.event_time else 'TBD'
        )
        
        if success:
            flash(f'Reminder sent to {guest.name}!', 'success')
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sending reminder: {str(e)}'
        }), 500


# ============= FEATURE 1: QR CODE CHECK-IN SYSTEM =============

@app.route('/guests/<int:id>/generate-qr', methods=['GET'])
@user_required
def generate_guest_qr(id):
    """Generate QR code for guest"""
    try:
        guest = Guest.query.get_or_404(id)
        
        # Generate QR code
        qr_image, token = qr_service.generate_qr_code(
            guest_id=guest.id,
            event_id=guest.event_id,
            guest_name=guest.name
        )
        
        if qr_image and token:
            # Save token to database
            guest.qr_token = token
            db.session.commit()
            
            return jsonify({
                'success': True,
                'qr_image': qr_image,
                'message': 'QR code generated successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate QR code'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/check-in', methods=['GET', 'POST'])
@user_required
def check_in_page():
    """QR code scanner page for check-in"""
    if request.method == 'POST':
        try:
            qr_data = request.json.get('qr_data')
            
            # Verify QR code
            decoded_data = qr_service.verify_qr_code(qr_data)
            
            if not decoded_data:
                return jsonify({
                    'success': False,
                    'message': 'Invalid QR code'
                }), 400
            
            # Find guest
            guest = Guest.query.get(decoded_data['guest_id'])
            
            if not guest:
                return jsonify({
                    'success': False,
                    'message': 'Guest not found'
                }), 404
            
            # Verify token matches
            if guest.qr_token != decoded_data['token']:
                return jsonify({
                    'success': False,
                    'message': 'Invalid or expired QR code'
                }), 400
            
            # Check if already checked in
            if guest.checked_in:
                return jsonify({
                    'success': False,
                    'message': f'{guest.name} is already checked in at {guest.check_in_time.strftime("%I:%M %p")}',
                    'already_checked_in': True
                }), 400
            
            # Mark as checked in
            guest.checked_in = True
            guest.check_in_time = datetime.now()  # Local time (India timezone)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'✅ Welcome {guest.name}! Check-in successful!',
                'guest_name': guest.name,
                'event_name': guest.event.name,
                'check_in_time': guest.check_in_time.strftime('%I:%M %p')
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
    
    # GET request - show scanner page
    return render_template('check_in/scanner.html')


@app.route('/guests/<int:id>/check-in-status', methods=['GET'])
@user_required
def guest_check_in_status(id):
    """Get guest check-in status"""
    try:
        guest = Guest.query.get_or_404(id)
        
        return jsonify({
            'success': True,
            'checked_in': guest.checked_in,
            'check_in_time': guest.check_in_time.strftime('%Y-%m-%d %H:%M:%S') if guest.check_in_time else None,
            'has_qr': bool(guest.qr_token)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ============= FEATURE 3: ANALYTICS DASHBOARD =============

@app.route('/analytics')
@login_required
def analytics_dashboard():
    """Analytics dashboard with charts and statistics"""
    try:
        # Get all data
        events = Event.query.all()
        guests = Guest.query.all()
        bookings = Booking.query.all()
        
        # Calculate statistics
        stats = {
            'total_events': len(events),
            'total_guests': len(guests),
            'total_bookings': len(bookings),
            'checked_in_count': len([g for g in guests if g.checked_in]),
            'rsvp_accepted': len([g for g in guests if g.rsvp_status == 'Accepted']),
            'rsvp_declined': len([g for g in guests if g.rsvp_status == 'Declined']),
            'rsvp_pending': len([g for g in guests if g.rsvp_status == 'Pending']),
            'total_budget': sum([float(e.budget) for e in events if e.budget]),
            'total_actual_cost': 0  # Actual cost tracking not implemented yet
        }
        
        # Event statistics
        event_stats = []
        for event in events:
            event_guests = [g for g in guests if g.event_id == event.id]
            event_stats.append({
                'name': event.name,
                'guest_count': len(event_guests),
                'checked_in': len([g for g in event_guests if g.checked_in]),
                'accepted': len([g for g in event_guests if g.rsvp_status == 'Accepted']),
                'budget': float(event.budget) if event.budget else 0,
                'actual_cost': 0  # Actual cost tracking not implemented
            })
        
        # Monthly event distribution
        from collections import defaultdict
        monthly_events = defaultdict(int)
        for event in events:
            if event.event_date:
                month_key = event.event_date.strftime('%Y-%m')
                monthly_events[month_key] += 1
        
        return render_template('analytics/dashboard.html', 
                             stats=stats, 
                             event_stats=event_stats,
                             monthly_events=dict(monthly_events))
        
    except Exception as e:
        flash(f'Error loading analytics: {str(e)}', 'error')
        return redirect(url_for('dashboard'))


@app.route('/analytics/api/data')
@login_required
def analytics_api():
    """API endpoint for analytics data (for AJAX updates)"""
    try:
        events = Event.query.all()
        guests = Guest.query.all()
        
        # RSVP Distribution
        rsvp_data = {
            'accepted': len([g for g in guests if g.rsvp_status == 'Accepted']),
            'declined': len([g for g in guests if g.rsvp_status == 'Declined']),
            'pending': len([g for g in guests if g.rsvp_status == 'Pending'])
        }
        
        # Check-in Rate
        checkin_data = {
            'checked_in': len([g for g in guests if g.checked_in]),
            'not_checked_in': len([g for g in guests if not g.checked_in])
        }
        
        # Guests per Event
        event_guest_data = []
        for event in events[:10]:  # Top 10 events
            guest_count = Guest.query.filter_by(event_id=event.id).count()
            event_guest_data.append({
                'event': event.name,
                'guests': guest_count
            })
        
        # Budget Analysis
        budget_data = []
        for event in events:
            if event.budget:
                budget_data.append({
                    'event': event.name,
                    'budget': float(event.budget or 0),
                    'actual': 0  # Actual cost tracking not implemented
                })
        
        return jsonify({
            'success': True,
            'rsvp': rsvp_data,
            'checkin': checkin_data,
            'event_guests': event_guest_data,
            'budget': budget_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
