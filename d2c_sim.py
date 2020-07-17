# Simple script to send device-to-cloud messages in JSON format.
# The provided values are generated in 1 second intervals and batched into one message.
# Note that the total message size for Azure IoT Hub messages is limited to 4KB.
#
# Usage: d2c_sim.py [value1] [value2] [value2] ...
import asyncio
import json
import datetime
import random
import os
import sys
from azure.iot.device.aio import IoTHubDeviceClient


def serialize_datetime(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()


async def main():
    connection_string = os.getenv("DEVICE_CONNECTION_STRING")
    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    await device_client.connect()

    try:
        values = list(map(float, sys.argv[1:])) or [42]
        payload = []
        for value in values:
            print("Collecting value:", value)
            payload.append({ "DeviceId": "microsoft-sphere-device", 
                "ValueId": "Temperature",
                "Value": value,
                "TimeStamp": datetime.datetime.now(datetime.timezone.utc) })
            await asyncio.sleep(1)
        
        message = json.dumps(payload, default=serialize_datetime)
        print("Sending message:", message)
        await device_client.send_message(message)
    finally:
        await device_client.disconnect()

asyncio.run(main())
