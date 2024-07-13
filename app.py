from flask import Flask, request
from celery import Celery
import smtplib
from datetime import datetime
import logging

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Set up logging
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

@celery.task
def send_email(recipient):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with actual SMTP server details
        server.starttls()
        server.login("banklejohn@gmail.com", "rfjdemnclfefhvsf")  # Replace with actual credentials
        message = "Subject: Test Email\n\nThis is a test email."
        server.sendmail("bankolejohn@gmail.com", recipient, message)
        server.quit()
        return f"Email sent to {recipient}"
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        result = send_email.delay(sendmail)
        return f"Email has been queued to {sendmail}, task id: {result.id}"

    if talktome:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Current time logged: {current_time}")
        return f"Current time {current_time} has been logged"

    return "Welcome to the messaging system!"

if __name__ == '__main__':
    app.run(debug=True)
