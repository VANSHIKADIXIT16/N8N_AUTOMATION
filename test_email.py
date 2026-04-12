import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from backend.utils import send_email_gmail

if __name__ == "__main__":
    # Test with a known email address (user should provide one, or use a dummy for now to see if it reaches the API)
    test_email = "test@example.com" # Replace with a real email for actual testing
    subject = "Test Application Update"
    content = "Status: Shortlisted (Test)"
    
    print(f"Attempting to send test email to {test_email}...")
    success = send_email_gmail(test_email, subject, content)
    
    if success:
        print("✅ Test email sent successfully!")
    else:
        print("❌ Failed to send test email. Check if token.json exists and is valid.")
