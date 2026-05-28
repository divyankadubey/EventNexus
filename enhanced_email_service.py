"""
Enhanced Email Service for Event Management System
Handles event invitations, confirmations, and notifications
"""

import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from datetime import datetime
import re

# Load environment variables
load_dotenv()


class EnhancedEmailService:
    """Enhanced email service for event communications"""
    
    def __init__(self, app=None):
        """Initialize email service with Flask app"""
        self.app = app
        self.mail = None
        self.enabled = False
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email service with Flask app"""
        self.app = app
        
        # Configure email settings
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
        app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
        
        # Check if email is enabled
        self.enabled = (
            os.getenv('MAIL_ENABLED', 'True').lower() == 'true' and
            app.config.get('MAIL_USERNAME') and
            app.config.get('MAIL_PASSWORD')
        )
        
        # Development mode - log emails instead of sending
        self.dev_mode = os.getenv('EMAIL_DEV_MODE', 'False').lower() == 'true'
        
        if self.enabled:
            try:
                self.mail = Mail(app)
                print("✅ Enhanced email service initialized successfully")
            except Exception as e:
                print(f"⚠️ Email initialization failed: {e}")
                self.enabled = False
        else:
            print("⚠️ Email service disabled or not configured")
    
    def validate_email(self, email):
        """Validate email format"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def send_event_invitation(self, guest, event):
        """Send event invitation email to guest"""
        if not self.enabled or not self.mail:
            print("⚠️ Email service not enabled or not configured")
            return False
        
        if not self.validate_email(guest.email):
            print(f"⚠️ Invalid email address: {guest.email}")
            return False
        
        try:
            # Create email message
            subject = f"🎉 Event Nexus Invitation: {event.name}"
            
            # HTML email template
            html_body = self._generate_invitation_template(guest, event)
            
            # Plain text version
            text_body = self._generate_invitation_text(guest, event)
            
            msg = Message(
                subject=subject,
                recipients=[guest.email],
                html=html_body,
                body=text_body,
                sender=self.app.config.get('MAIL_DEFAULT_SENDER')
            )
            
            # Send email
            if self.dev_mode:
                # Development mode - log email content instead of sending
                print(f"📧 [DEV MODE] Event invitation would be sent to {guest.email}")
                print(f"📧 [DEV MODE] Subject: {subject}")
                return True
            else:
                # Production mode - send actual email
                self.mail.send(msg)
                print(f"✅ Event invitation sent to {guest.email}")
                return True
            
        except Exception as e:
            print(f"❌ Failed to send invitation to {guest.email}: {e}")
            return False
    
    def _generate_invitation_template(self, guest, event):
        """Generate HTML email template for event invitation"""
        event_date = event.event_date.strftime('%A, %B %d, %Y') if event.event_date else 'TBD'
        event_time = event.event_time.strftime('%I:%M %p') if event.event_time else 'TBD'
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Event Invitation - {event.name}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    margin: -30px -30px 30px -30px;
                    border-radius: 10px 10px 0 0;
                }}
                .event-details {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .detail-row {{
                    display: flex;
                    margin: 10px 0;
                }}
                .detail-label {{
                    font-weight: bold;
                    min-width: 120px;
                    color: #666;
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    margin: 20px 0;
                    text-align: center;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    color: #666;
                    font-size: 14px;
                }}
                .emoji {{
                    font-size: 1.2em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1><span class="emoji">🎉</span> Event Nexus Invitation</h1>
                    <p>You're officially invited to an amazing event experience</p>
                </div>
                
                <h2>Dear {guest.name},</h2>
                
                <p>Congratulations! You have been successfully registered for <strong>{event.name}</strong>. We're thrilled to have you join us for what promises to be an unforgettable experience.</p>
                
                <div class="event-details">
                    <h3><span class="emoji">📅</span> Event Details</h3>
                    <div class="detail-row">
                        <span class="detail-label">Event:</span>
                        <span>{event.name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Date:</span>
                        <span>{event_date}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Time:</span>
                        <span>{event_time}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Location:</span>
                        <span>{event.location or 'To be announced'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Guests:</span>
                        <span>{guest.guest_count} person(s)</span>
                    </div>
                </div>
                
                {f'<p><strong>About the event:</strong> {event.description}</p>' if event.description else ''}
                
                <p><strong>What to expect:</strong></p>
                <ul>
                    <li>Networking opportunities with amazing people</li>
                    <li>Exciting activities and entertainment</li>
                    <li>Memorable experiences and great food</li>
                    <li>A chance to make new connections</li>
                </ul>
                
                <div style="text-align: center;">
                    <div class="cta-button">
                        <span class="emoji">📍</span> Mark Your Calendar!
                    </div>
                </div>
                
                <p><strong>Important Information:</strong></p>
                <ul>
                    <li>Please arrive 15 minutes early for check-in</li>
                    <li>Bring a valid ID for verification</li>
                    <li>Dress code: Smart casual</li>
                    <li>Free parking available on-site</li>
                </ul>
                
                {f'<p><strong>Dietary Requirements:</strong> We have noted your dietary preferences: {guest.dietary_requirements or "None specified"}</p>' if guest.dietary_requirements else ''}
                
                <p>We look forward to welcoming you to <strong>{event.name}</strong>! If you have any questions or need to make changes to your registration, please don't hesitate to contact us.</p>
                
                <p>Best regards,<br>
                The Event Management Team<br>
                <span class="emoji">🎊</span></p>
                
                <div class="footer">
                    <p>This email was sent to {guest.email} because you registered for {event.name}.<br>
                    If you didn't register for this event, please contact us immediately.</p>
                    <p>© 2024 Event Nexus. All rights reserved.<br>
                    <strong>From:</strong> eventnexus@gmail.com | <strong>Powered by:</strong> Event Nexus Platform</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _generate_invitation_text(self, guest, event):
        """Generate plain text version of event invitation"""
        event_date = event.event_date.strftime('%A, %B %d, %Y') if event.event_date else 'TBD'
        event_time = event.event_time.strftime('%I:%M %p') if event.event_time else 'TBD'
        
        return f"""
🎉 You're Invited! {event.name}

Dear {guest.name},

Congratulations! You have been successfully registered for {event.name}. We're thrilled to have you join us for what promises to be an unforgettable experience.

📅 Event Details:
Event: {event.name}
Date: {event_date}
Time: {event_time}
Location: {event.location or 'To be announced'}
Guests: {guest.guest_count} person(s)

{f'About the event: {event.description}' if event.description else ''}

What to expect:
• Networking opportunities with amazing people
• Exciting activities and entertainment
• Memorable experiences and great food
• A chance to make new connections

Important Information:
• Please arrive 15 minutes early for check-in
• Bring a valid ID for verification
• Dress code: Smart casual
• Free parking available on-site

{f'Dietary Requirements: We have noted your dietary preferences: {guest.dietary_requirements}' if guest.dietary_requirements else ''}

We look forward to welcoming you to {event.name}! If you have any questions or need to make changes to your registration, please don't hesitate to contact us.

Best regards,
The Event Management Team
🎊

---
This email was sent to {guest.email} because you registered for {event.name}.
If you didn't register for this event, please contact us immediately.
© 2024 Event Nexus. All rights reserved.
From: eventnexus@gmail.com | Powered by: Event Nexus Platform
        """


# Global email service instance
enhanced_email_service = EnhancedEmailService()
