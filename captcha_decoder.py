import base64
import os
import time

import requests

client_key = os.getenv("API_KEY")
api_base_url = "https://api.anti-captcha.com"


def decode_image(image_path):
    with open(image_path, "rb") as img_file:
        image_base64 = base64.b64encode(img_file.read())
        result = requests.post(f"{api_base_url}/createTask", json={
            "clientKey": client_key,
            "task": {
                "type": "ImageToTextTask",
                "body": image_base64
            }
        })
    task_id = result.json().get("taskId")
    decoded_image = None

    while True:
        result = requests.post(f"{api_base_url}/getTaskResult", json={
            "clientKey": client_key,
            "taskId": task_id
        })
        result_status = result.json().get("status")
        if result_status == "processing":
            time.sleep(1)
        elif result_status == "ready":
            decoded_image = result.json().get("solution").get("text")
            break

    return decoded_image
