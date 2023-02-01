from machine import Pin, PWM
import time


def blick(led: PWM):
    for i in range(0, 1024):
        led.duty(i)
        time.sleep_ms(1)
    for i in range(1023, -1, -1):
        led.duty(i)
        time.sleep_ms(1)


def main():
    p4 = PWM(Pin(12, Pin.OUT), freq=1000)
    p5 = PWM(Pin(13, Pin.OUT), freq=1000)
    while True:
        blick(p4)
        time.sleep_ms(500)
        blick(p5)
        time.sleep_ms(500)


if __name__ == '__main__':
    main()
