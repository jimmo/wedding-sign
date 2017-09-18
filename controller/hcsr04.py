import machine, utime

class HCSR04:
  __slots__ = ['_trigger_pin', '_echo_pin', 'mm']

  def __init__(self, trigger_pin, echo_pin):
    self._trigger_pin = trigger_pin
    self._echo_pin = echo_pin
    self.mm = 4000

  @micropython.native
  def update(self):
    self._trigger_pin.init(mode=machine.Pin.OUT, pull=machine.Pin.PULL_NONE, value=0)
    utime.sleep_us(5)
    self._trigger_pin.value(1)
    utime.sleep_us(10)
    self._trigger_pin.value(0)
    self._echo_pin.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_NONE)
    t = machine.time_pulse_us(self._echo_pin, 1, 500*2*30)
    if t < 0:
      self.mm = 4000
    else:
      self.mm = t * 3432 // 20000
