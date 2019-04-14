from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'signup/$', views.signup, name='signup'),
        url(r'createaccount/$', views.createAccount, name = "Create Account"),
        url(r'sendmail/$', views.sendMail, name = "Send Mail"),
        url(r'index/$', views.index, name = "Main Page"),
        url(r'login/$', views.signin),
        url(r'addaddress/$', views.addAddress),
        url(r'logout/$', views.signout),
        ]
