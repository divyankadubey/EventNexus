"""
Twilio SMS Service for Event Management System
Replaces MSG91 with Twilio for OTP and SMS notifications
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import random
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()


class TwilioService:
    """Twilio SMS service for sending OTP and notifications"""
    
    def __init__(self):
        """Initialize Twilio client with credentials from environment"""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        # Support multiple from numbers (comma-separated)
        phone_numbers_env = os.getenv('TWILIO_PHONE_NUMBERS', '')
        self.from_numbers = []
        if phone_numbers_env:
            self.from_numbers = [num.strip() for num in phone_numbers_env.split(',') if num.strip()]
        # Fallback to single number if list not provided
        if not self.from_numbers and self.phone_number:
            self.from_numbers = [self.phone_number]
        # Round-robin index
        self._from_index = 0
        self.enabled = os.getenv('TWILIO_ENABLED', 'True').lower() == 'true'
        
        # Initialize Twilio client if enabled
        if self.enabled and self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                print("✅ Twilio service initialized successfully")
            except Exception as e:
                print(f"⚠️ Twilio initialization failed: {e}")
                self.client = None
        else:
            self.client = None
            print("⚠️ Twilio service disabled or not configured")
    
    def _get_next_from_number(self):
        """Select next Twilio 'from' number in round-robin order."""
        if not self.from_numbers:
            return None
        number = self.from_numbers[self._from_index % len(self.from_numbers)]
        # advance pointer for next call
        self._from_index = (self._from_index + 1) % max(1, len(self.from_numbers))
        return number
    
    def generate_otp(self, length=6):
        """
        Generate a random OTP
        
        Args:
            length (int): Length of OTP (default: 6)
            
        Returns:
            str: Generated OTP
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    def send_otp(self, phone, otp, event_name=None):
        """
        Send OTP via SMS to the given phone number
        
        Args:
            phone (str): 10-digit phone number (without country code)
            otp (str): OTP to send
            event_name (str, optional): Event name for context
            
        Returns:
            tuple: (success: bool, message: str, message_sid: str)
        """
        if not self.enabled or not self.client:
            return False, "Twilio service is not enabled or configured", None
        
        # Format phone number for India (+91)
        formatted_phone = self._format_phone_number(phone)
        
        # Create message body
        if event_name:
            message_body = f"Your OTP for {event_name} is: {otp}. Valid for 10 minutes. - Nexus Event Management"
        else:
            message_body = f"Your verification OTP is: {otp}. Valid for 10 minutes. - Nexus Event Management"
        
        try:
            # Try sending from available numbers (round-robin with fallback)
            last_error = None
            attempts = len(self.from_numbers) if self.from_numbers else 1
            for _ in range(attempts):
                from_number = self._get_next_from_number()
                try:
                    message = self.client.messages.create(
                        body=message_body,
                        from_=from_number,
                        to=formatted_phone
                    )
                    print(f"✅ OTP sent successfully from {from_number}! SID: {message.sid}")
                    return True, f"OTP sent to {phone}", message.sid
                except TwilioRestException as e:
                    last_error = f"Twilio error from {from_number}: {e.msg}"
                    print(f"❌ {last_error}")
                    # try next number
                    continue
            
            # If we got here, all attempts failed
            return False, (last_error or "Failed to send OTP"), None
            
        except TwilioRestException as e:
            error_msg = f"Twilio error: {e.msg}"
            print(f"❌ {error_msg}")
            return False, error_msg, None
            
        except Exception as e:
            error_msg = f"Failed to send OTP: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg, None
    
    def send_sms(self, phone, message):
        """
        Send a custom SMS message
        
        Args:
            phone (str): 10-digit phone number
            message (str): Message to send
            
        Returns:
            tuple: (success: bool, response_message: str, message_sid: str)
        """
        if not self.enabled or not self.client:
            return False, "Twilio service is not enabled or configured", None
        
        formatted_phone = self._format_phone_number(phone)
        
        try:
            # Try sending from available numbers (round-robin with fallback)
            last_error = None
            attempts = len(self.from_numbers) if self.from_numbers else 1
            for _ in range(attempts):
                from_number = self._get_next_from_number()
                try:
                    sms = self.client.messages.create(
                        body=message,
                        from_=from_number,
                        to=formatted_phone
                    )
                    print(f"✅ SMS sent successfully from {from_number}! SID: {sms.sid}")
                    return True, f"Message sent to {phone}", sms.sid
                except TwilioRestException as e:
                    last_error = f"Twilio error from {from_number}: {e.msg}"
                    print(f"❌ {last_error}")
                    continue
            
            return False, (last_error or "Failed to send SMS"), None
            
        except TwilioRestException as e:
            error_msg = f"Twilio error: {e.msg}"
            print(f"❌ {error_msg}")
            return False, error_msg, None
            
        except Exception as e:
            error_msg = f"Failed to send SMS: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg, None
    
    def send_event_reminder(self, phone, guest_name, event_name, event_date, event_time):
        """
        Send event reminder SMS to guest
        
        Args:
            phone (str): Guest phone number
            guest_name (str): Name of the guest
            event_name (str): Name of the event
            event_date (str): Event date
            event_time (str): Event time
            
        Returns:
            tuple: (success: bool, message: str, message_sid: str)
        """
        message = f"""
Hi {guest_name}!

Reminder: You're invited to {event_name}

📅 Date: {event_date}
⏰ Time: {event_time}

We look forward to seeing you!
- Nexus Event Management
        """.strip()
        
        return self.send_sms(phone, message)
    
    def send_rsvp_confirmation(self, phone, guest_name, event_name, rsvp_status):
        """
        Send RSVP confirmation SMS
        
        Args:
            phone (str): Guest phone number
            guest_name (str): Name of the guest
            event_name (str): Name of the event
            rsvp_status (str): RSVP status (Accepted/Declined)
            
        Returns:
            tuple: (success: bool, message: str, message_sid: str)
        """
        if rsvp_status == 'Accepted':
            message = f"Hi {guest_name}! Thank you for confirming your attendance to {event_name}. We're excited to see you! - Nexus Event"
        else:
            message = f"Hi {guest_name}, we've received your RSVP for {event_name}. Thank you for letting us know. - Nexus Event"
        
        return self.send_sms(phone, message)
    
    def verify_otp(self, stored_otp, user_otp, created_at, expiry_minutes=10):
        """
        Verify OTP with expiry check
        
        Args:
            stored_otp (str): OTP stored in database
            user_otp (str): OTP entered by user
            created_at (datetime): When OTP was created
            expiry_minutes (int): OTP validity in minutes
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Check if OTP matches
        if str(stored_otp) != str(user_otp):
            return False, "Invalid OTP. Please check and try again."
        
        # Convert string to datetime if needed
        if isinstance(created_at, str):
            try:
                created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return False, "Invalid OTP timestamp"
        
        # Check if OTP is expired
        expiry_time = created_at + timedelta(minutes=expiry_minutes)
        if datetime.utcnow() > expiry_time:
            return False, "OTP has expired. Please request a new one."
        
        return True, "OTP verified successfully!"
    
    def _format_phone_number(self, phone):
        """
        Format phone number to international format
        
        Args:
            phone (str): 10-digit phone number
            
        Returns:
            str: Formatted phone number with country code (+91 for India)
        """
        # Remove any non-digit characters
        phone = ''.join(filter(str.isdigit, phone))
        
        # Add country code if not present
        if not phone.startswith('+'):
            if len(phone) == 10:
                phone = f'+91{phone}'  # India country code
            elif len(phone) == 11 and phone.startswith('91'):
                phone = f'+{phone}'
            elif len(phone) == 12 and phone.startswith('91'):
                phone = f'+{phone}'
        
        return phone
    
    def get_account_info(self):
        """
        Get Twilio account information
        
        Returns:
            dict: Account information or error message
        """
        if not self.client:
            return {'error': 'Twilio not configured'}
        
        try:
            account = self.client.api.accounts(self.account_sid).fetch()
            return {
                'friendly_name': account.friendly_name,
                'status': account.status,
                'type': account.type
            }
        except Exception as e:
            return {'error': str(e)}


# Initialize global service instance
twilio_service = TwilioService()


# Example usage and testing
if __name__ == '__main__':
    print("🔧 Twilio Service Testing")
    print("=" * 50)
    
    # Test OTP generation
    otp = twilio_service.generate_otp()
    print(f"Generated OTP: {otp}")
    
    # Get account info
    info = twilio_service.get_account_info()
    print(f"\nAccount Info: {info}")
    
    # Test phone formatting
    test_phones = ['9876543210', '919876543210', '+919876543210']
    for phone in test_phones:
        formatted = twilio_service._format_phone_number(phone)
        print(f"Formatted {phone} -> {formatted}")
    
    print("\n✅ Service ready to use!")
    print("📝 Remember to set your credentials in .env file")
