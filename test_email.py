#!/usr/bin/env python3
"""
Test script to verify email configuration and send test emails
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Guest, Event
from enhanced_email_service import enhanced_email_service
from datetime import datetime

def test_email_configuration():
    """Test email service configuration"""
    with app.app_context():
        print("🔧 Testing Email Configuration...")
        
        # Check if email service is enabled
        if enhanced_email_service.enabled:
            print("✅ Email service is enabled")
            print(f"📧 SMTP Server: {app.config.get('MAIL_SERVER')}")
            print(f"🔐 SMTP Username: {app.config.get('MAIL_USERNAME')}")
            print(f"📤 Default Sender: {app.config.get('MAIL_DEFAULT_SENDER')}")
        else:
            print("❌ Email service is not enabled or not configured")
            print("Please check your .env file configuration")
            return False
        
        return True

def send_test_email_to_samarth():
    """Send test email to samarthchoudhary26sept@gmail.com"""
    with app.app_context():
        print("📧 Sending test email to samarthchoudhary26sept@gmail.com...")
        
        # Create test event
        test_event = Event(
            name="Event Nexus Test Event",
            description="This is a test event to verify our email system is working perfectly. You're receiving this email because our Event Management System is now fully functional with real-time email notifications!",
            event_date=datetime.now().date(),
            event_time=datetime.now().time(),
            location="Virtual Event Platform",
            venue_capacity=100
        )
        
        # Create test guest (you)
        test_guest = Guest(
            name="Samarth Choudhary",
            email="samarthchoudhary26sept@gmail.com",
            phone="7900260905",
            guest_count=1,
            dietary_requirements="None - Test email"
        )
        
        # Send the email
        try:
            email_sent = enhanced_email_service.send_event_invitation(test_guest, test_event)
            if email_sent:
                print("✅ Test email sent successfully!")
                print("📨 Check your inbox: samarthchoudhary26sept@gmail.com")
                print("📱 Also check spam folder if not in inbox")
                return True
            else:
                print("❌ Email sending failed")
                return False
        except Exception as e:
            print(f"❌ Email error: {e}")
            return False

def send_real_time_test():
    """Test real-time email sending like user registration"""
    with app.app_context():
        print("🚀 Testing real-time email sending...")
        
        # Get a real event from database or create one
        event = Event.query.first()
        if not event:
            # Create a sample event
            event = Event(
                name="Event Nexus Launch Party",
                description="Join us for the grand launch of Event Nexus - the ultimate event management platform! Experience real-time registrations, beautiful email invitations, and seamless event coordination.",
                event_date=datetime.now().date(),
                event_time=datetime.now().time(),
                location="Event Nexus Headquarters",
                venue_capacity=50
            )
            db.session.add(event)
            db.session.commit()
            print("✅ Created sample event for testing")
        
        # Create test guest registration
        test_guest = Guest(
            event_id=event.id,
            name="Samarth Choudhary",
            email="samarthchoudhary26sept@gmail.com",
            phone="7900260905",
            rsvp_status="Accepted",
            guest_count=1,
            dietary_requirements="Vegetarian options please"
        )
        
        try:
            # Send real-time invitation
            email_sent = enhanced_email_service.send_event_invitation(test_guest, event)
            
            if email_sent:
                print("✅ Real-time email sent successfully!")
                print(f"📧 Event: {event.name}")
                print(f"📅 Date: {event.event_date}")
                print(f"🕐 Time: {event.event_time}")
                print(f"📍 Location: {event.location}")
                print("📨 Check samarthchoudhary26sept@gmail.com for the invitation!")
                return True
            else:
                print("❌ Real-time email failed")
                return False
                
        except Exception as e:
            print(f"❌ Real-time email error: {e}")
            return False

if __name__ == '__main__':
    print("🎯 Event Nexus Email Testing System")
    print("=" * 50)
    
    # Test 1: Configuration
    if not test_email_configuration():
        print("\n❌ Please fix email configuration first")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Test 2: Basic test email
    if send_test_email_to_samarth():
        print("\n✅ Basic email test passed!")
    
    print("\n" + "=" * 50)
    
    # Test 3: Real-time simulation
    if send_real_time_test():
        print("\n✅ Real-time email test passed!")
    
    print("\n🎉 All tests completed!")
    print("📧 Check samarthchoudhary26sept@gmail.com for test emails")
    print("📱 Don't forget to check spam folder!")
