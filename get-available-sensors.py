import winrt.windows.devices.sensors as sensors
import winrt.windows.devices.geolocation as geolocation

# Get accelerometer reference
accelerometer = sensors.Accelerometer.get_default()

# Get inclinometer reference
inclinometer = sensors.Inclinometer.get_default()

# Get compass reference
compass = sensors.Compass.get_default()

if accelerometer is not None:
    print("Accelerometer available")
    print(accelerometer.minimum_report_interval)
else:
    print("Accelerometer not available")

if inclinometer is not None:
    print("Inclinometer available")
    print(inclinometer.minimum_report_interval)
else:
    print("Inclinometer not available")

if compass is not None:
    print("Compass available")
    print(compass.minimum_report_interval)
    
else:
    print("Compass not available")

if geolocator is not None:
    print("Geolocator available")
else:
    print("Geolocator not available")
