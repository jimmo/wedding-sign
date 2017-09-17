import machine, time

class HCSR04:
  def __init__(self, trigger_pin, echo_pin):
    self.trigger_pin = trigger_pin
    self.echo_pin = echo_pin

  def _echo(self):
    self.trigger_pin.init(mode=machine.Pin.OUT, pull=None, value=0)
    time.sleep_us(5)
    self.trigger_pin.value(1)
    time.sleep_us(10)
    self.trigger_pin.value(0)
    self.echo_pin.init(mode=machine.Pin.IN, pull=None)
    return machine.time_pulse_us(self.echo_pin, 1, 500*2*30)

  def distance_mm(self):
    # To calculate the distance we get the pulse_time and divide it by 2
    # (the pulse walk the distance twice) and by 29.1 becasue
    # the sound speed on air (343.2 m/s), that It's equivalent to
    # 0.34320 mm/us that is 1mm each 2.91us
    # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
    t = self._echo()
    if t < 0:
      return 4000
    return t * 100 // 582
