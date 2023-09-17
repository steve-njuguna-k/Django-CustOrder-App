# Import necessary packages
import os
import africastalking as at
from dotenv import load_dotenv
import phonenumbers

# Load environment variables from .env file
load_dotenv()

# Initialize Africas Talking SDK with credentials from environment variables
username = os.environ.get("AT_USERNAME")   # Use 'sandbox' for development in the test environment
api_key = os.environ.get("AT_API_KEY")      # Use your sandbox app API key for development in the test environment
sender = os.environ.get("AT_SMS_SHORTCODE")  # Use your sandbox shortcode for development in the test environment

# Initialize the Africas Talking client with the required credentials
at.initialize(username, api_key)

# Initialize a service, in this case, SMS
sms = at.SMS

# Create a function to send an SMS with order details to a customer
def send_sms(customer_name, item, quantity, total, phone_number):
    # Parse and validate the phone number using the phonenumbers library
    parsed_phone_number = phonenumbers.parse(phone_number, 'KE')
    validated_phone_number = phonenumbers.format_number(parsed_phone_number, phonenumbers.PhoneNumberFormat.E164)

    # Check if the phone number is valid
    if validated_phone_number:
        # Compose the SMS message with order details
        message = f"Hello {customer_name}, this is to inform you that your order of {quantity} {item}(s), for a total of Ksh. {total} is ready for pickup. Thank you for your service."
        
        # Send the customized message to the validated phone number
        try:
            sms.send(message, [validated_phone_number], sender)
        except Exception as e:
            # Handle any exceptions that occur during SMS sending
            raise Exception(f'An Error Occurred: {e}')
    else:
        # Raise an exception for an invalid phone number
        raise Exception("Invalid Phone Number")
