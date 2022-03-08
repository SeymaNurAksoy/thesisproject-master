from base64 import urlsafe_b64encode
from email.message import EmailMessage
from readline import get_current_history_length
from tokenize import generate_tokens
from django.conf import settings
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser,User
from .models import Profile
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
#@receiver(post_save,sender=Profile)
def createProfile(sender,instance,created,**kwargs):
    print("Profile signal triggered ")
    user = instance
    profile = Profile.objects.create(
        user = user,
        username = user.username,
        email = user.email,
        name = user.first_name

    )



def deleteUser(sender,instance,**kwargs):
    user = instance.user
    user.delete()


def send_activation_email(request,instance):
    user = instance.user

    current_site = get_current_history_length(request)
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_b64encode(force_bytes(user.pk)),
        'token': generate_tokens.make_token(user)
    }
    email_subject = 'Hesabınızı Aktifleştirin'
    email_body = render_to_string('account/activate.html', context)
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER,
                         to=[user.email])
    email.send()

post_save.connect(deleteUser,sender= Profile)
post_save.connect(createProfile,sender=User)