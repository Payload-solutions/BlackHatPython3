from core.keys import *
import json
from ibm_watson import *
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



ibm_authenticator = IAMAuthenticator(API_KEY, url = URL)
discovery = Dicovery

