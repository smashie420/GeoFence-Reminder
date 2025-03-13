import time
import RPi.GPIO as GPIO
import math
import atexit


class LED:
    """
    A class to control an RGB LED using Pulse Width Modulation (PWM).

    Attributes
    ----------

    _common_anode : bool
        Defines if the LED is common anode (default: True).

    _pin : list
        List of GPIO pin numbers for Red, Green, and Blue LEDs.

    _brightness : int
        Brightness level (default: 10%).

    _rgbColor : list
        Stores the current RGB color after brightness adjustment.

    _state : int
        Stores LED state (0 for off, 1 for on).

    red, green, blue : GPIO.PWM
        PWM objects controlling Red, Green, and Blue pins.
    """
    def __init__(self, pins, common_anode=True):
        self._common_anode = common_anode
        self._pin = pins or None

        self._brightness = 10
        self._rgbColor = None
        self._state = 0

        self.red = None
        self.green = None
        self.blue = None

        self.initilizePins()



    def initilizePins(self):
        """
        Sets up the Raspberry Pi GPIO pins for the RGB LED and initializes PWM.

        If pins are not provided, an error message is displayed.
        """

        if(not self._pin):
            print("Initilize pins using an array!\nExample: foo = LED([1,2,3])")
            return

        RED_PIN, GREEN_PIN, BLUE_PIN = self._pin
        print(f"led.py:         Initializing pins: Red: {RED_PIN}, Green: {GREEN_PIN}, Blue: {BLUE_PIN}")
        

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RED_PIN, GPIO.OUT)
        GPIO.setup(GREEN_PIN, GPIO.OUT)
        GPIO.setup(BLUE_PIN, GPIO.OUT)

        #Set up PWM
        self.red = GPIO.PWM(RED_PIN, 1000)  # 1 kHz frequency
        self.green = GPIO.PWM(GREEN_PIN, 1000)
        self.blue = GPIO.PWM(BLUE_PIN, 1000)

        # 100% duty cycle = OFF for common anode
        self.red.start(100)
        self.green.start(100)
        self.blue.start(100)

        print("led.py:         PWM setup complete")

    def setColor(self, rgb):
        """
        Sets the LED color using RGB values.

        Converts 8-bit RGB values (0-255) to PWM duty cycle (0-100%),
        applies brightness adjustment, and turns the LED on.

        Parameters
        ----------
        rgb : list
            A list of three integers representing the Red, Green, and Blue values (0-255).
        """
        if(  
            (rgb[0] < 0 or rgb[0] > 255) or 
            (rgb[1] < 0 or rgb[1] > 255) or
            (rgb[2] < 0 or rgb[2] > 255)
        ):
            raise IndexError("\n\nRGB BALUES OUTSIDE RANGE! (0-255)")

        #convert RGB values into fractions of percentages out of 100 (0-100, 0-100, 0-100)
        convertedRGB = [math.floor(((rgb[0]/255)*100)), math.floor((rgb[1]/255)*100), math.floor((rgb[2]/255)*100)]
        # brightness factor
        convertedPlusBrightnessRGB = [convertedRGB[0]* (self._brightness * (10**-2)), convertedRGB[1]* (self._brightness * (10**-2)), convertedRGB[2]* (self._brightness * (10**-2))]
        self._rgbColor = convertedPlusBrightnessRGB
        self.turnOn()

        self._state = 1

    def getState(self):
        """
        Returns the current LED state.

        Returns
        -------
        int
            1 if the LED is on, 0 if it is off.
        """
        return self._state

    def turnOn(self):
        """
        Turns on the LED with the currently set color.

        If no color is set, prompts the user to set a color first.
        Adjusts duty cycles based on whether the LED is common anode or common cathode.
        """

        if(not self._rgbColor):
            raise ValueError("\n\nColor isn't set!\nUse foo.setColor([255,255,255])")

        if self._common_anode:
            r, g, b = 100 - self._rgbColor[0], 100 - self._rgbColor[1], 100 - self._rgbColor[2]  # Invert duty cycle
        else:
            r, g, b = self._rgbColor  # Use the direct values for common cathode

        self.red.ChangeDutyCycle(r)
        self.green.ChangeDutyCycle(g)
        self.blue.ChangeDutyCycle(b)

        self._state = 1

    def turnOff(self):
        """
        Turns off the LED by setting duty cycles to 100% for common anode LEDs
        and 0% for common cathode LEDs.
        """
        if self._common_anode:
            # 100% duty cycle means OFF for common anode
            self.red.ChangeDutyCycle(100)
            self.green.ChangeDutyCycle(100)
            self.blue.ChangeDutyCycle(100)
        else:
            # 0% duty cycle means OFF for common cathode
            self.red.ChangeDutyCycle(0)
            self.green.ChangeDutyCycle(0)
            self.blue.ChangeDutyCycle(0)

        self._state = 0

    
    def setBrightness(self, brightness):
        """
        Sets the brightness level of the LED.

        Parameters
        ----------
        brightness : int
            A value between 0 and 100 representing the brightness percentage.
        """
        if(brightness < 0 or brightness > 100):
            raise IndexError("\n\nBrightness is outside of the range! (0-100)")

        self._brightness = brightness
    


