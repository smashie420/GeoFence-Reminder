import serial
import time
import pynmea2
import threading


class GPS:
    def __init__(self, serialPath='/dev/serial0', baudrate=9600, timeout=5):
        self._latitude = -1  # Default to -1 (no data)
        self._longitude = -1  # Default to -1 (no data)
        self._speed = -1  # Default to -1 (no data)
        self._last_received_time = time.time()  # Track the last time data was received

        self._ser = serial.Serial(serialPath, baudrate, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False)
        self._ser.flushInput()
        self._ser.flushOutput()

        # Background thread for reading GPS data
        backgroundThread = threading.Thread(name='background', target=self.getData, daemon=True)
        backgroundThread.start()
        time.sleep(0.5)

        # Start monitoring thread to detect data loss
        monitorThread = threading.Thread(name='monitor', target=self.monitorData, daemon=True)
        monitorThread.start()

    def getData(self):
        while True:
            try:
                data_raw = self._ser.readline().decode('utf-8').strip()
                if data_raw.startswith('$GPRMC'):
                    msg = pynmea2.parse(data_raw)

                    if msg.status != "A":  # Check if GPS response is valid
                        continue

                    # Update last received time
                    self._last_received_time = time.time()

                    # Update GPS data
                    self._latitude = msg.latitude
                    self._longitude = msg.longitude
                    self._speed = msg.spd_over_grnd * 1.151  # Convert knots to MPH
                    '''
                    print(f"Time (UTC): {msg.timestamp}")
                    print(f"Date: {msg.datestamp}")
                    print(f"Latitude: {msg.latitude} {msg.lat_dir}")
                    print(f"Longitude: {msg.longitude} {msg.lon_dir}")
                    print(f"Speed: {msg.spd_over_grnd} knots")
                    print(f"Status: {'Valid' if msg.status == 'A' else 'Invalid'}")
                    print("-" * 50)'
                    '''
                time.sleep(0.1)
            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")
            except UnicodeDecodeError:
                continue

    def monitorData(self, timeout=5):
        """Checks if new data is arriving. If no data for `timeout` seconds, set lat/lon to -1."""
        while True:
            if time.time() - self._last_received_time > timeout:
                self._latitude = -1
                self._longitude = -1
                self._speed = -1
                print("No GPS data received for a while. Setting values to -1.")
            time.sleep(1)

    def getLatitude(self):
        return self._latitude

    def getLongitude(self):
        return self._longitude

    def getSpeed(self):
        return self._speed