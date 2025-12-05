import requests

# Stream Speech (Beta) (POST /v1/speech/stream)
response = requests.post(
  "https://api.murf.ai/v1/speech/stream",
  headers={
    "api-key": "ap2_9169fc04-7b74-46e2-a112-839e00dc4590"
  },
  json={
    "text": "Hi, How are you doing today?",
    "voiceId": "Matthew",
    "model": "FALCON",
    "multiNativeLocale": "en-US"
  },
)

print(response.json())