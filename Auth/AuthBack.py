import requests
import Settings.Settingsback

class CreateSession:

    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.config = Settings.Settingsback.load_config

    def login(self, url, login, password):
        self.session.auth = (login, password)

        response = self.session.get(
            url,
            verify=False
        )

        response.raise_for_status()

        return response

    def logout(self):
        self.session.close()

    def post(self, url, **kwargs):
        response = self.session.post(
            url,
            **kwargs
        )

        response.raise_for_status()

        return response

