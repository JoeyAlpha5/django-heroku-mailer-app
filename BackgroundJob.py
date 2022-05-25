# env set up
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailer.settings')
import django
django.setup()

# aggregates
from django.db.models.aggregates import Sum

# email sending and date
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime

# models
from app.models import payment
from django.contrib.auth.models import User

# serializer
from django.core.serializers import serialize



def generateStatements():
    users =  User.objects.all()
    for user in users:
        payments = serialize("python",payment.objects.filter(user=user))
        total_payments = payment.objects.filter(user=user).aggregate(Sum('amount'))
        total_amount_paid = total_payments['amount__sum']
        statement_number = len(payments)
        statement_date = datetime.now().strftime("%d/%m/%Y")
        customer_name = user.first_name + " " + user.last_name
        customer_email = user.email


        # send the email
        html_message = render_to_string('email_template.html', {"customer_name":customer_name, "total_payments":total_amount_paid})
        message = EmailMessage("Monthly Statement",html_message, '', [customer_email])
        message.content_subtype = "html"
        message.send()



generateStatements()