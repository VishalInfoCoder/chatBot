import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import os
# Create a SendinBlue API configuration
configuration = sib_api_v3_sdk.Configuration()

# Replace "<your brevo api key here>" with your actual SendinBlue API key
configuration.api_key['api-key'] = os.environ.get('myemailtoken')

# Initialize the SendinBlue API instance
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_verification_email(subject, html, to_address=None, receiver_username=None):
    # SendinBlue mailing parameters
    subject = subject
    sender = {"name": "Infoapto Technologies", "email": "info@infoaptotech.com"}
    html_content = html

    # Define the recipient(s)
    if to_address:
        # You can add multiple email accounts to which you want to send the mail in this list of dicts
        to = [{"email": to_address, "name": receiver_username}]

    # Create a SendSmtpEmail object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return True
    except ApiException as e:
         print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
def send_verification_quota(subject, html, to_address=None, receiver_username=None):
    # SendinBlue mailing parameters
    subject = subject
    sender = {"name": "Infoapto Technologies", "email": "info@infoaptotech.com"}
    html_content = html

    # Define the recipient(s)
    if to_address:
        # You can add multiple email accounts to which you want to send the mail in this list of dicts
        to = [{"email": to_address, "name": receiver_username}]

    # Create a SendSmtpEmail object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return True
    except ApiException as e:
         print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
def send_reset_password_mail(subject, html, to_address=None, receiver_username=None):
    # SendinBlue mailing parameters
    subject = subject
    sender = {"name": "Infoapto Technologies", "email": "info@infoaptotech.com"}
    html_content = html

    # Define the recipient(s)
    if to_address:
        # You can add multiple email accounts to which you want to send the mail in this list of dicts
        to = [{"email": to_address, "name": receiver_username}]

    # Create a SendSmtpEmail object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return True
    except ApiException as e:
         print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)