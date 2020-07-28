# Import smtplib for the actual sending function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Import the email modules we'll need
from email.message import EmailMessage

from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view



# from qualeval.be.util import initialize_logging

# logging, config=initialize_logging()

def emailNotify(sender, to, cc, Subject, content):
    # logger=logging.getLogger('email Notify')
    try:
        msg = MIMEMultipart()
        msg['Subject'] = Subject
        msg['From'] = sender
        msg['To'] = ','.join(to)
        msg['Cc'] = ','.join(cc)
        content = MIMEText(content, 'html') # convert the body to a MIME compatible string
        msg.attach(content)

        # Send the message via our own SMTP server.
        From=sender
        password='04vamsi@1998'
        s = smtplib.SMTP_SSL('smtp.gmail.com',465)
        s.login(From,password)
        s.sendmail(msg['From'], to+cc, msg.as_string())
        s.quit()
        # logger.info("Sent email to %s",to+cc)
        return True
    except Exception as e:
        print('email not sent')
        print(str(e))
        # logger.error(str(e),exc_info=True)
        return False