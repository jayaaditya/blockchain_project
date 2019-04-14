import blockchain.settings as settings

import threading

from django.core import mail

def send_mail_async(subject, body, email):
    t = threading.Thread(target=mail.send_mail, 
            args=(subject,body,settings.EMAIL_HOST_USER,[email],),
            kwargs = {'fail_silently': False}
            )
    t.start()
