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
sender = os.environ.get("AT_SMS_SHORTCODE")

# Initialize the Africas Talking client with the required credentials
at.initialize(username, api_key)

# Initialize a service e.g. SMS
sms = at.SMS

# create a function to send a customer a sms with order details
def send_sms(customer_name, item, quantity, total, phone_number):
    print(customer_name, item, quantity, total, phone_number)
    phn = phonenumbers.parse(phone_number)
    validated_phone_number = phonenumbers.format_number(phn, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    print(validated_phone_number)

    if validated_phone_number:
        message = f"Hello {customer_name}, this is to inform you that your order of {quantity} {item} (s), for a total of Ksh. {total} is ready for pickup. Thank you for your service."
        
        # For each entry send a customized message
        try:
            print("Sent")
            response = sms.send(message, [validated_phone_number], sender)
            print(response)
        except Exception as e:
            print(f'We seem to have encountered a problem: {e}')
    else:
        print("Not a valid Phone Number")