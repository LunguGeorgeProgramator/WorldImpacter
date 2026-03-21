import json

class Translator:

    locale = None
    lang = {}
    lang_json_path = "translate/%s.json"

    def __init__(self, locale):
        self.locale = locale
        self._load_locale()

    def _load_locale(self):
        with open(self.lang_json_path % self.locale) as f:
            self.lang = json.load(f)

    def get_message(self, message_key):
        return self.lang[message_key] if message_key in self.lang else message_key