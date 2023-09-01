# -*- coding: utf-8 -*-
from hikvisionapi import Client


class Device:
    def __init__(self, ip: str, user: str, password: str) -> None:
        self.cam = Client(f"http://{ip}", user, password, timeout=10)

    def start(self) -> None:
        """
        Starts the execution of the program.

        This function enters an infinite loop and repeatedly performs the following steps:
        1. Prints the string "loop".
        2. Retrieves an event using the `get_event()` method.
        3. Checks if the retrieved event is a motion event using the `is_motion()` method.
        4. If the event is a motion event, calls the `get_frame()` method.

        This function does not take any parameters and does not return any value.
        """
        while True:
            print("loop")
            event = self.get_event()
            if self.is_motion(event):
                self.get_frame()

    def get_event(self) -> dict:
        """
        Retrieves an event from the alert stream.

        Returns:
            dict: The retrieved event from the alert stream.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            response = self.cam.Event.notification.alertStream(
                method="get", type="stream"
            )
            if response:
                return response[0]

        except Exception as error:
            print(error)

    def is_motion(self, data_event: dict) -> None:
        """
        Checks if the given data event represents a motion event.

        Parameters:
            - data_event (dict): The data event to be checked.

        Returns:
            - bool: True if the event represents motion, False otherwise.
        """
        data = data_event.get("EventNotificationAlert")
        event_status = data.get("eventState")
        if event_status == "inactive":
            return False
        else:
            return True

    def get_frame(self) -> None:
        """
        Get the current frame from the camera and save it as an image file.

        This function retrieves the current frame from the camera's streaming channel and saves it as a JPEG image file named "screen.jpg". The frame is obtained by making a GET request to the camera's streaming channel, specifying the picture method with the type parameter set to "opaque_data". The response is then iterated over in chunks of size 1024 and each chunk is written to the file "screen.jpg" using a binary write mode.

        Parameters:
        - None

        Returns:
        - None
        """
        response = self.cam.Streaming.channels[102].picture(
            method="get", type="opaque_data"
        )
        with open("screen.jpg", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
