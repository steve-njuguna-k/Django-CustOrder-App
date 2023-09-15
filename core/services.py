# import package
import os
import africastalking as at
from dotenv import load_dotenv
import phonenumbers

# the load_dotenv function gets the environment variables defined in .env file
load_dotenv()

# Initialize SDK
username = os.environ.get("AT_USERNAME")   # use 'sandbox' for development in the test environment
api_key = os.environ.get("AT_API_KEY")  # use your sandbox app API key for development in the test environment
sender = os.environ.get("AT_SMS_SHORTCODE") # use your sandbox shortcode for development in the test environment

# Initialize the Africas Talking client with the required credentials
at.initialize(username, api_key)

# Initialize a service e.g. SMS
sms = at.SMS

# create a function to send a customer a sms with order details
def send_sms(customer_name, item, quantity, total, phone_number):
    parsed_phone_number = phonenumbers.parse(phone_number, 'KE')
    validated_phone_number = phonenumbers.format_number(parsed_phone_number, phonenumbers.PhoneNumberFormat.E164)

    if validated_phone_number:
        message = f"Hello {customer_name}, this is to inform you that your order of {quantity} {item} (s), for a total of Ksh. {total} is ready for pickup. Thank you for your service."
        
        # For each entry send a customized message
        try:
            sms.send(message, [validated_phone_number], sender)
        except Exception as e:
            raise Exception(f'An Error Occured: {e}')
    else:
        raise Exception("Invalid Phone Number")