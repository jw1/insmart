from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from insmart import settings

def send_alert_emails(alert):
    users = User.objects.filter(email__isnull=False)

    for user in users:
        if user.userprofile.active and len(user.email) >= 3:
            print("sending emails to " + user.email)

            text = "" + \
                    "An alert has been generated on the InSmart system.\n" + \
                    "Please login to the InSmart system at your earliest convenience to view more details.\n" + \
                    "\n" + \
                    "Sincerely,\n" + \
                    "\n" + \
                    "The InSmart Team"

            try:
                send_mail(
                    'InSmart Inventory Alert',
                    text,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
            except Exception as e:
                print( '%s (%s)' % (e.message, type(e)))
