import asyncio
import time
from pythonosc import osc_message_builder
from pythonosc import udp_client

import winrt.windows.devices.sensors as sensors
from winrt.windows.foundation import TimeSpan

# Configuration
localhost = "127.0.0.1"
port = 9999

# Initialize OSC client
client = udp_client.SimpleUDPClient(localhost, port)

def send_osc_message(address, data):
    client.send_message(address, data)

async def main():
    # Get accelerometer, inclinometer, and compass references
    accelerometer = sensors.Accelerometer.get_default()

    if accelerometer is not None:
        # Set accelerometer report interval
        report_interval = accelerometer.minimum_report_interval
        accelerometer.report_interval = report_interval

    while True:
        # Send accelerometer data (if available)
        if accelerometer is not None:
            reading = accelerometer.get_current_reading()
            if reading is not None:
                data = [reading.acceleration_x, reading.acceleration_y, reading.acceleration_z]
                send_osc_message("/accelerometer", data)

        # Wait for a short period before reading the sensors again
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(main())
