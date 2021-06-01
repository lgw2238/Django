from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string


# sendEmail views.py


# Create your views here.
# def send(receiverEmail):
#    return HttpResponse('sendEmail views - sendFunction()')

def send(receiverEmail, verifyCode):
     try:
         content = {'verifyCode': verifyCode}
         msg_html = render_to_string('sendEmail/email_format.html', content)
         msg = EmailMessage(subject='인증코드발송메일', body=msg_html, from_email='lgw2236@gmail.com',
                            bcc=[receiverEmail])
         msg.content_subtype='html'
         msg.send()
         return True
     except:
         return False