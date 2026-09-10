"""
Unit tests for EventNexus models
Tests for User, Event, Guest, and Booking models
"""

import pytest
from datetime import datetime, timedelta
from app import app, db
from models import User, Event, Guest, Booking


@pytest.fixture
def client():
    """Create a test client with a fresh database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def app_context():
    """Provide application context for database operations"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


class TestUserModel:
    """Tests for User model and authentication"""
    
    def test_password_hashing(self, app_context):
        """Test that passwords are hashed correctly"""
        user = User(username='testuser', email='test@gmail.com')
        user.set_password('mypassword123')
        
        # Password should not be stored as plain text
        assert user.password_hash != 'mypassword123'
        assert user.password_hash is not None
    
    def test_check_correct_password(self, app_context):
        """Test that correct password passes verification"""
        user = User(username='testuser', email='test@gmail.com')
        user.set_password('mypassword123')
        
        assert user.check_password('mypassword123') == True
    
    def test_check_wrong_password(self, app_context):
        """Test that wrong password fails verification"""
        user = User(username='testuser', email='test@gmail.com')
        user.set_password('mypassword123')
        
        assert user.check_password('wrongpassword') == False
    
    def test_check_empty_password(self, app_context):
        """Test that empty password fails verification"""
        user = User(username='testuser', email='test@gmail.com')
        user.set_password('mypassword123')
        
        assert user.check_password('') == False
    
    def test_password_case_sensitive(self, app_context):
        """Test that passwords are case sensitive"""
        user = User(username='testuser', email='test@gmail.com')
        user.set_password('MyPassword123')
        
        assert user.check_password('mypassword123') == False
        assert user.check_password('MyPassword123') == True
    
    def test_user_to_dict(self, app_context):
        """Test user to_dict() method"""
        user = User(
            username='testuser',
            email='test@gmail.com',
            full_name='Test User',
            role='Admin'
        )
        
        user_dict = user.to_dict()
        
        assert user_dict['username'] == 'testuser'
        assert user_dict['email'] == 'test@gmail.com'
        assert user_dict['full_name'] == 'Test User'
        assert user_dict['role'] == 'Admin'
        assert 'created_at' in user_dict
    
    def test_user_role_default(self, app_context):
        """Test that default role is User"""
        user = User(username='testuser', email='test@gmail.com')
        
        assert user.role == 'User'
    
    def test_user_active_default(self, app_context):
        """Test that users are active by default"""
        user = User(username='testuser', email='test@gmail.com')
        
        assert user.is_active == True


class TestEventModel:
    """Tests for Event model"""
    
    def test_event_creation(self, app_context):
        """Test creating an event"""
        event = Event(
            name='Test Event',
            description='Test Description',
            event_date=datetime.now().date() + timedelta(days=1),
            location='Test Location',
            budget=5000.00
        )
        
        db.session.add(event)
        db.session.commit()
        
        assert event.id is not None
        assert event.name == 'Test Event'
        assert event.status == 'Planning'  # Default status
    
    def test_event_status_enum(self, app_context):
        """Test event status values"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        
        assert event.status == 'Planning'
        
        event.status = 'Confirmed'
        assert event.status == 'Confirmed'
    
    def test_event_to_dict(self, app_context):
        """Test event to_dict() method"""
        event = Event(
            name='Test Event',
            description='Description',
            event_date=datetime.now().date() + timedelta(days=1),
            location='Location'
        )
        
        db.session.add(event)
        db.session.commit()
        
        event_dict = event.to_dict()
        
        assert event_dict['name'] == 'Test Event'
        assert event_dict['description'] == 'Description'
        assert event_dict['location'] == 'Location'
        assert 'event_date' in event_dict
        assert 'created_at' in event_dict
    
    def test_event_with_capacity(self, app_context):
        """Test event with venue capacity"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1),
            venue_capacity=100
        )
        
        db.session.add(event)
        db.session.commit()
        
        assert event.venue_capacity == 100


class TestGuestModel:
    """Tests for Guest model"""
    
    def test_guest_creation(self, app_context):
        """Test creating a guest"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        guest = Guest(
            event_id=event.id,
            name='John Doe',
            email='john@gmail.com',
            phone='9876543210'
        )
        
        db.session.add(guest)
        db.session.commit()
        
        assert guest.id is not None
        assert guest.rsvp_status == 'Pending'  # Default
        assert guest.guest_count == 1  # Default
    
    def test_guest_rsvp_status(self, app_context):
        """Test guest RSVP status"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        guest = Guest(
            event_id=event.id,
            name='John Doe',
            email='john@gmail.com'
        )
        
        assert guest.rsvp_status == 'Pending'
        
        guest.rsvp_status = 'Accepted'
        db.session.commit()
        
        assert guest.rsvp_status == 'Accepted'
    
    def test_guest_check_in(self, app_context):
        """Test guest check-in tracking"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        guest = Guest(
            event_id=event.id,
            name='John Doe',
            email='john@gmail.com'
        )
        
        assert guest.checked_in == False
        
        guest.checked_in = True
        guest.check_in_time = datetime.now()
        db.session.commit()
        
        assert guest.checked_in == True
        assert guest.check_in_time is not None
    
    def test_guest_to_dict(self, app_context):
        """Test guest to_dict() method"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        guest = Guest(
            event_id=event.id,
            name='John Doe',
            email='john@gmail.com',
            phone='9876543210'
        )
        
        db.session.add(guest)
        db.session.commit()
        
        guest_dict = guest.to_dict()
        
        assert guest_dict['name'] == 'John Doe'
        assert guest_dict['email'] == 'john@gmail.com'
        assert guest_dict['phone'] == '9876543210'
        assert guest_dict['event_name'] == 'Test Event'


class TestBookingModel:
    """Tests for Booking model"""
    
    def test_booking_creation(self, app_context):
        """Test creating a booking"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        booking = Booking(
            event_id=event.id,
            booking_type='Venue',
            vendor_name='Test Venue',
            cost=50000.00
        )
        
        db.session.add(booking)
        db.session.commit()
        
        assert booking.id is not None
        assert booking.status == 'Pending'  # Default
    
    def test_booking_status(self, app_context):
        """Test booking status values"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        booking = Booking(
            event_id=event.id,
            booking_type='Catering',
            vendor_name='Test Caterer'
        )
        
        assert booking.status == 'Pending'
        
        booking.status = 'Confirmed'
        assert booking.status == 'Confirmed'
    
    def test_booking_type_enum(self, app_context):
        """Test booking type values"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        types = ['Venue', 'Catering', 'Photography', 'Music', 'Decoration', 'Other']
        
        for booking_type in types:
            booking = Booking(
                event_id=event.id,
                booking_type=booking_type,
                vendor_name=f'Test {booking_type}'
            )
            assert booking.booking_type == booking_type
    
    def test_booking_to_dict(self, app_context):
        """Test booking to_dict() method"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        booking = Booking(
            event_id=event.id,
            booking_type='Venue',
            vendor_name='Test Venue',
            cost=50000.00
        )
        
        db.session.add(booking)
        db.session.commit()
        
        booking_dict = booking.to_dict()
        
        assert booking_dict['booking_type'] == 'Venue'
        assert booking_dict['vendor_name'] == 'Test Venue'
        assert booking_dict['cost'] == 50000.00
        assert booking_dict['event_name'] == 'Test Event'


class TestDatabaseRelationships:
    """Tests for relationships between models"""
    
    def test_event_guest_relationship(self, app_context):
        """Test that guests are linked to events"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        guest1 = Guest(event_id=event.id, name='Guest 1', email='guest1@gmail.com')
        guest2 = Guest(event_id=event.id, name='Guest 2', email='guest2@gmail.com')
        
        db.session.add(guest1)
        db.session.add(guest2)
        db.session.commit()
        
        assert len(event.guests) == 2
        assert guest1.event.name == 'Test Event'
    
    def test_event_booking_relationship(self, app_context):
        """Test that bookings are linked to events"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        booking1 = Booking(event_id=event.id, booking_type='Venue', vendor_name='Venue 1')
        booking2 = Booking(event_id=event.id, booking_type='Catering', vendor_name='Caterer 1')
        
        db.session.add(booking1)
        db.session.add(booking2)
        db.session.commit()
        
        assert len(event.bookings) == 2
        assert booking1.event.name == 'Test Event'
    
    def test_cascade_delete_guests(self, app_context):
        """Test that deleting an event deletes its guests"""
        event = Event(
            name='Test Event',
            event_date=datetime.now().date() + timedelta(days=1)
        )
        db.session.add(event)
        db.session.commit()
        
        guest = Guest(event_id=event.id, name='Guest', email='guest@gmail.com')
        db.session.add(guest)
        db.session.commit()
        
        event_id = event.id
        guest_id = guest.id
        
        # Delete event
        db.session.delete(event)
        db.session.commit()
        
        # Guest should also be deleted
        deleted_guest = Guest.query.get(guest_id)
        assert deleted_guest is None
