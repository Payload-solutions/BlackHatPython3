from core.keys import *
from ibm_watson import *
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def init_authenticator():
    try:
        ibm_authenticator = IAMAuthenticator(API_KEY, url=URL)
        assistant = AssistantV2(version="2020-09-24", authenticator=ibm_authenticator)
        assistant.set_service_url(URL)

        # Sessions

        session = assistant.create_session(ASSISTANT_ID).get_result()
        print(json.dumps(session, indent=2))
    except Exception as e:
        print(str(e))
