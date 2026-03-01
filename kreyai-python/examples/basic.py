# examples/basic.py
from kreyai import Client

client = Client(api_key="YOUR_API_KEY")

result = client.transcribe(
    "sample.wav",
    language="en",
    diarization=True,
)

print(result["text"])
