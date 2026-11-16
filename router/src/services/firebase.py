import os

import firebase_admin
from firebase_admin import credentials, firestore
from google.auth.credentials import AnonymousCredentials


class EmulatorCredentials(credentials.Base):
    def get_credential(self):
        return AnonymousCredentials()


os.environ["FIRESTORE_EMULATOR_HOST"]

firebase_app = firebase_admin.initialize_app(
    credential=EmulatorCredentials(),
    options={"projectId": os.environ["GOOGLE_CLOUD_PROJECT"]},
)
firestore_client = firestore.client(app=firebase_app)
