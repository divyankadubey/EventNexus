#!/usr/bin/env python3
"""
Demo script to show email content without actually sending
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_email_service import EnhancedEmailService
from datetime import datetime

def show_email_demo():
    """Show what the email would look like"""
    
    # Create test guest and event
    class MockGuest:
        def __init__(self):
            self.name = "Samarth Choudhary"
            self.email = "samarthchoudhary26sept@gmail.com"
            self.phone = "7900260905"
            self.guest_count = 1
            self.dietary_requirements = "Vegetarian options please"
    
    class MockEvent:
        def __init__(self):
            self.name = "Event Nexus Launch Party"
            self.description = "Join us for the grand launch of Event Nexus - the ultimate event management platform!"
            self.event_date = datetime.now().date()
            self.event_time = datetime.now().time()
            self.location = "Virtual Event Platform"
    
    # Create email service instance
    email_service = EnhancedEmailService()
    
    # Create mock objects
    guest = MockGuest()
    event = MockEvent()
    
    # Generate email content
    html_content = email_service._generate_invitation_template(guest, event)
    text_content = email_service._generate_invitation_text(guest, event)
    
    print("🎨 EMAIL PREVIEW - What will be sent:")
    print("=" * 60)
    print(f"📧 To: {guest.email}")
    print(f"📧 From: eventnexus@gmail.com")
    print(f"📧 Subject: 🎉 Event Nexus Invitation: {event.name}")
    print("=" * 60)
    print("\n📄 HTML Email Content:")
    print("-" * 40)
    print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
    print("\n" + "=" * 60)
    print("\n📝 Plain Text Email Content:")
    print("-" * 40)
    print(text_content)
    print("\n" + "=" * 60)
    print("\n✅ This is exactly what users will receive!")
    print("🚀 Once you set up the Gmail App Password, these emails will be sent instantly!")

if __name__ == '__main__':
    show_email_demo()
