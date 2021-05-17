from my_project.core.dates import normalized
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone


def send_mail(subject,to,context):
    # dados context:
    # title, dados (itera os dados do chamado e etc)

    html_message = render_to_string('mail_template.html', context)
    plain_message = strip_tags(html_message)
    #from_email = 'From <from@example.com>'

    mail.send_mail(subject=subject, from_email=settings.FROM_EMAIL,message=plain_message, recipient_list=to, html_message=html_message)
    
def send_mail_notas_presas(subject,to,horario,quantidade):
    # dados context:
    # title, dados (itera os dados do chamado e etc)
    context = {
        'horario':horario,
        'quantidade': quantidade
    }

    html_message = render_to_string('notas_presas_template.html', context)
    plain_message = strip_tags(html_message)
    #from_email = 'From <from@example.com>'

    mail.send_mail(subject=subject, from_email=settings.FROM_EMAIL,message=plain_message, recipient_list=to, html_message=html_message)