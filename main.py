import json
from hikvisionapi import Client
cam = Client("http://192.168.237.120", "admin", "ac22446688", timeout=10)

__VERSION__ = "0.0.1"
print(f"Version: {__VERSION__}")
def get_frame(response):
    response = cam.Streaming.channels[102].picture(method="get", type="opaque_data")
    with open("screen.jpg", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def get_event():
    response = cam.Event.notification.alertStream(method="get", type="stream")
    if response:
        print(json.dumps(response, indent=4))
        return response
    
def is_motion(response):
    event = response[0]["EventNotificationAlert"]["eventState"]
    return event


while True:
    try:
        event = get_event()  
        if is_motion(event) == "active":
                get_frame(event)
    except Exception:
        pass