import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from django.conf import settings


def send_mail(subject, plain_content, html_content, to_list, from_list):
    """
    Sends emails to users using SMTP2GO
    """
    try:
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = formataddr((str(Header('Proxmate', 'utf-8')), from_list))
        msg['To'] = to_list

        html_message = MIMEText(html_content, 'html')
        msg.attach(html_message)

        mailServer = smtplib.SMTP('mail.smtp2go.com', 2525)  # 8025, 587 and 25 can also be used.
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(settings.SMTP2GO_USERNAME, settings.SMTP2GO_PASSWORD)
        mailServer.sendmail(from_list, to_list, msg.as_string())
        mailServer.close()
    except:
        pass