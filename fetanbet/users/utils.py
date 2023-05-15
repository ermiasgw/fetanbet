from django.core import signing
from django.core.mail import send_mail
import datetime

# send email confirmation with the url for the token
def sendemailconfirmation(user):
    token = generatetoken(user)
    confirmation_url = 'http://localhost:8000/api/confirm-email/?token=' + token
    subject = 'email confirmation for fetanbet'
    message = f'please follow this link {confirmation_url} to confirm your email'
    send_mail(subject, message, "from@example.com", [user.email], fail_silently=False,)

# generate token by dumping user id and timestamp to find user id later
def generatetoken(user):
    key = 'confirm_email'
    timestamp = str(datetime.datetime.now())
    data = {'user':user.id, 'timestamp':timestamp}
    return signing.dumps(data, key=key)

def load_token(token):
    key = 'confirm_email'
    data = signing.loads(token, key=key)
    return data.values()