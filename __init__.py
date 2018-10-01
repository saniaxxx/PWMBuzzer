from modules import cbpi
from modules import buzzer
from thread import start_new_thread
import time

try:
    import RPi.GPIO as GPIO
except Exception as e:
    pass

class PWMBuzzer(buzzer.Buzzer):
    frequency = 5000
    p = None

    def __init__(self, gpio, beep_level):
        super(PWMBuzzer, self).__init__(gpio, beep_level)
        self.p = GPIO.PWM(int(self.gpio), float(self.frequency))        
        
    def beep(self):
        if self.state is False:
            cbpi.app.logger.error("BUZZER not working")
            return

        def play(sound):
            self.p.start(0)
            def output(level):
                if level == GPIO.LOW:
                    self.p.ChangeDutyCycle(0)
                else :
                    self.p.ChangeDutyCycle(50)
            try:
                for i in sound:
                    if (isinstance(i, str)):
                        if i == "H" and self.beep_level == "HIGH":
                            output(GPIO.HIGH)
                        elif i == "H" and self.beep_level != "HIGH":
                            output(GPIO.LOW)
                        elif i == "L" and self.beep_level == "HIGH":
                            output(GPIO.LOW)
                        else:
                            output(GPIO.HIGH)
                    else:
                        time.sleep(i)
            except Exception as e:
                pass
            self.p.stop()

        start_new_thread(play, (self.sound,))

@cbpi.initalizer(order=2)
def init(cbpi):
    gpio = cbpi.get_config_parameter("buzzer", 25)
    beep_level = cbpi.get_config_parameter("buzzer_beep_level", "HIGH")

    cbpi.buzzer = PWMBuzzer(gpio, beep_level)
    cbpi.beep()
    cbpi.app.logger.info("PWMBUZZER INIT OK")
