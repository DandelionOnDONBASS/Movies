from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.timezone import now



class User(AbstractUser):
    is_verifield_email = models.BooleanField(default=False)






class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    
    def __str__(self):
        return f'EmailVerification object for {self.user.email}'
    
    def send_verification_email(self):
        link = reverse('users:email_verifications', kwargs={'email': self.user.email, 'code':self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение уетной записи для {self.user.username}'
        message = 'Для подтверждения ученой записи для {} перейдите по ссылке {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email= "from@example.com",
            recipient_list= [self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False