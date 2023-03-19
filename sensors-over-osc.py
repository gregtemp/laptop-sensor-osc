import asyncio
import time
from pythonosc import osc_message_builder
from pythonosc import udp_client

import winrt.windows.devices.sensors as sensors
import winrt.windows.devices.geolocation as geolocation
from winrt.windows.foundation import TimeSpan

# Configuration
localhost = "127.0.0.1"
port = 9999

# Initialize OSC client
client = udp_client.SimpleUDPClient(localhost, port)

def send_osc_message(address, data):
    client.send_message(address, data)

async def get_location():
    geolocator = geolocation.Geolocator()
    location = await geolocator.get_geoposition_async()
    return location

async def main():
    # Get accelerometer, inclinometer, and compass references
    accelerometer = sensors.Accelerometer.get_default()
    inclinometer = sensors.Inclinometer.get_default()
    compass = sensors.Compass.get_default()

    if accelerometer is not None:
        # Set accelerometer report interval
        report_interval = min(accelerometer.minimum_report_interval, 10)
        accelerometer.report_interval = report_interval

    if inclinometer is not None:
        # Set inclinometer report interval
        report_interval = min(inclinometer.minimum_report_interval, 10)
        inclinometer.report_interval = report_interval

    if compass is not None:
        # Set compass report interval
        report_interval = min(compass.minimum_report_interval, 10)
        compass.report_interval = report_interval

    while True:
        # Send accelerometer data (if available)
        if accelerometer is not None:
            reading = accelerometer.get_current_reading()
            if reading is not None:
                data = [reading.acceleration_x, reading.acceleration_y, reading.acceleration_z]
                send_osc_message("/accelerometer", data)

        # Send inclinometer data (if available)
        if inclinometer is not None:
            reading = inclinometer.get_current_reading()
            if reading is not None:
                data = [reading.pitch_degrees, reading.roll_degrees, reading.yaw_degrees]
                send_osc_message("/inclinometer", data)

        # Send compass data (if available)
        if compass is not None:
            reading = compass.get_current_reading()
            if reading is not None:
                data = [reading.heading_magnetic_north, reading.heading_true_north]
                send_osc_message("/compass", data)

        # Send geolocation data (if available)
        location = await get_location()
        if location is not None:
            data = [location.coordinate.latitude, location.coordinate.longitude, location.coordinate.altitude]
            send_osc_message("/geolocation", data)

        # Wait for a short period before reading the sensors again
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(main())
