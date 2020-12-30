
import serial
from collections import namedtuple

from protocol import UartCommand, UartProtocol, to_2bytes


class ServoController():
    def __init__(self, path, protocol=UartProtocol.COMPACT, dev_id=12):
        self.device = serial.Serial(path)
        self.protocol = protocol
        self.dev_id = dev_id

        self.min = 4000
        self.max = 8000

    def write(self, cmd, args=bytes()):
        if self.protocol == UartProtocol.COMPACT:
            cmd = bytes([cmd]) + args
        elif self.protocol == UartProtocol.POLULU:
            cmd = bytes([0xAA, self.dev_id, cmd & 0x7F]) + args

        self.device.write(cmd)

    def set_pwm(self, ch, time, period):
        self.write(0x8A, bytes([ch]) + 
            to_2bytes(time) + 
            to_2bytes(period)
        )

    def set_target(self, ch, target):
        self.write(UartCommand.SET_TARGET, bytes([ch]) + to_2bytes(target))

    def set_target_norm(self, ch, target):
        delta = (self.max - self.min) / 2
        val = self.min + delta * (1.0 + target)
        self.set_target(ch, int(val))

    def set_speed(self, ch, speed):
        self.write(UartCommand.SET_SPEED, bytes([ch]) + to_2bytes(speed))

    def set_acceleration(self, ch, acceleration):
        self.write(UartCommand.SET_ACCELERATION, bytes([ch]) + to_2bytes(acceleration))

    def get_position(self, ch):
        self.write(UartCommand.GET_POSITION, bytes([ch]))
        result = self.device.read(2)
        return int.from_bytes(result, 'little')

    def get_moving_state(self):
        self.write(UartCommand.GET_MOVING_STATE)
        result = self.device.read(1)
        return result[0]

    def get_errors(self):
        self.write(UartCommand.GET_ERRORS)
        result = self.device.read(2)
        return [r for r in result]

    def go_home(self):
        self.write(0xA2)
