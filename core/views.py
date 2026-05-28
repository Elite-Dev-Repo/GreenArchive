from django.shortcuts import render
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import os
from dotenv import load_dotenv

load_dotenv()



# Create your views here.



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # client_class is only needed if you are using specific OAuth2 flows
    client_class = OAuth2Client
    # This must match your frontend development URL exactly
    callback_url = os.getenv('FRONTEND_URL')
    

