import os

from amplitude import Amplitude, BaseEvent

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


class AmplitudeClient:
    key = os.getenv('AMPLITUDE_API_KEY')
    amplitude = Amplitude(key)

    def registered(self, tgId):
        event = BaseEvent(
            event_type="registered",
            user_id=str(tgId),
            event_properties={
                "source": "telegram"
            }
        )

        self._send(event)

    def character_selected(self, character_id):
        event = BaseEvent(
            event_type="character chose",
            user_id=str(character_id),
            event_properties={
                "source": "telegram"
            }
        )
        self._send(event)
    def event_get_response(self):
        pass
    def started_chat(self):
        pass

    def send_response_for_user(self):
        pass

    def _send(self, event):
        self.amplitude.track(event)
