from elevenlabs import save
from elevenlabs.client import ElevenLabs
from decouple import config

KEY = config('ELEVENLABS_TOKEN')
client = ElevenLabs(api_key=KEY)

response = client.voices.get_all()
audio = client.generate(text="тест 1, тест 2, тест 3", voice=response.voices[6])
print(response.voices)

save(audio, "output_audio.mp3")