"""
SQLite Database setup script for Event Management System
This script creates the database and tables using SQLite (no MySQL needed)
"""

from app import app, db
from models import Event, Guest, Booking
from datetime import datetime, date, time

def setup_sqlite_database():
    """Create SQLite database and tables with sample data"""
    try:
        print("="*50)
        print("Setting up SQLite Database...")
        print("="*50)
        
        with app.app_context():
            # Create all tables
            print("\nCreating database tables...")
            db.create_all()
            print("✓ Tables created successfully!")
            
            # Check if data already exists
            if Event.query.first():
                print("\n⚠ Database already contains data. Skipping sample data insertion.")
                print("✓ Database is ready to use!")
                return True
            
            # Insert sample events
            print("\nInserting sample data...")
            
            event1 = Event(
                name='Annual Tech Conference 2025',
                description='A comprehensive technology conference featuring industry leaders',
                event_date=date(2025, 11, 15),
                event_time=time(9, 0),
                location='Convention Center, Delhi',
                budget=500000.00,
                status='Planning'
            )
            
            event2 = Event(
                name='Corporate Gala Dinner',
                description='Year-end celebration and awards ceremony',
                event_date=date(2025, 12, 20),
                event_time=time(19, 0),
                location='Grand Hotel, Mumbai',
                budget=300000.00,
                status='Planning'
            )
            
            db.session.add(event1)
            db.session.add(event2)
            db.session.commit()
            print("✓ Events added")
            
            # Insert sample guests
            guest1 = Guest(
                event_id=event1.id,
                name='Rahul Sharma',
                email='rahul.sharma@example.com',
                phone='+91-9876543210',
                rsvp_status='Accepted',
                guest_count=1
            )
            
            guest2 = Guest(
                event_id=event1.id,
                name='Priya Patel',
                email='priya.patel@example.com',
                phone='+91-9876543211',
                rsvp_status='Pending',
                guest_count=2
            )
            
            guest3 = Guest(
                event_id=event2.id,
                name='Amit Kumar',
                email='amit.kumar@example.com',
                phone='+91-9876543212',
                rsvp_status='Accepted',
                guest_count=1
            )
            
            db.session.add_all([guest1, guest2, guest3])
            db.session.commit()
            print("✓ Guests added")
            
            # Insert sample bookings
            booking1 = Booking(
                event_id=event1.id,
                booking_type='Venue',
                vendor_name='Convention Center Delhi',
                description='Main hall booking for 500 attendees',
                cost=150000.00,
                booking_date=date(2025, 11, 15),
                status='Confirmed',
                contact_info='venue@convention.com'
            )
            
            booking2 = Booking(
                event_id=event1.id,
                booking_type='Catering',
                vendor_name='Royal Caterers',
                description='Full day catering with lunch and snacks',
                cost=200000.00,
                booking_date=date(2025, 11, 15),
                status='Pending',
                contact_info='contact@royalcaterers.com'
            )
            
            booking3 = Booking(
                event_id=event2.id,
                booking_type='Venue',
                vendor_name='Grand Hotel Mumbai',
                description='Banquet hall for 150 guests',
                cost=100000.00,
                booking_date=date(2025, 12, 20),
                status='Confirmed',
                contact_info='bookings@grandhotel.com'
            )
            
            db.session.add_all([booking1, booking2, booking3])
            db.session.commit()
            print("✓ Bookings added")
            
            print("\n" + "="*50)
            print("DATABASE SETUP COMPLETE!")
            print("="*50)
            print("\nDatabase file created: event_management.db")
            print("Sample data includes:")
            print("  - 2 Events")
            print("  - 3 Guests")
            print("  - 3 Bookings")
            print("\nYou can now run the application with:")
            print("  python app.py")
            print("\nThen visit: http://localhost:5000")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = setup_sqlite_database()
    sys.exit(0 if success else 1)
