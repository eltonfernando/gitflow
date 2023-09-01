# -*- coding: utf-8 -*-
from hikvisionapi import Client


class Device:
    def __init__(self, ip: str, user: str, password: str) -> None:
        self.cam = Client(f"http://{ip}", user, password, timeout=10)

    def start(self) -> None:
        while True:
            print("loop")
            event = self.get_event()
            if self.is_motion(event):
                self.get_frame()

    def get_event(self) -> dict:
        try:
            response = self.cam.Event.notification.alertStream(
                method="get", type="stream"
            )
            if response:
                return response[0]

        except Exception as error:
            print(error)

    def is_motion(self, data_event: dict) -> None:
        data = data_event.get("EventNotificationAlert")
        event_status = data.get("eventState")
        if event_status == "inactive":
            return False
        else:
            return True

    def get_frame(self) -> None:
        response = self.cam.Streaming.channels[102].picture(
            method="get", type="opaque_data"
        )
        with open("screen.jpg", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
