
class Enum():
    """ Reverse lookup for Enums """
    @classmethod
    def lookup(cls, val):
        for k, v in vars(cls).items():
            if v == val:
                return k
        raise Exception("MissingValue: '{}' not in {}".format(val, cls.__name__))

class UartProtocol(Enum):
    COMPACT = 0
    POLULU = 1

# Commands to be used over Serial
class UartCommand(Enum):
    SET_TARGET = 0x84 # 3 data bytes
    SET_SPEED = 0x87 # 3 data bytes
    SET_ACCELERATION = 0x89 # 3 data bytes
    GET_POSITION = 0x90 # 0 data
    GET_MOVING_STATE = 0x93 # 0 data
    GET_ERRORS = 0xA1 # 0 data
    GO_HOME = 0xA2 # 0 data
    STOP_SCRIPT = 0xA4 # 0 data
    RESTART_SCRIPT_AT_SUBROUTINE                = 0xA7 # 1 data bytes
    RESTART_SCRIPT_AT_SUBROUTINE_WITH_PARAMETER = 0xA8 # 3 data bytes
    GET_SCRIPT_STATUS = 0xAE # 0 data
    MINI_SSC = 0xFF # (2 data bytes)

# These are the values to put in to bRequest when making a setup packet
# for a control transfer to the Maestro.  See the comments and code in Usc.cs
# for more information about what these requests do and the format of the
# setup packet.
class UscRequest(Enum):
    GET_PARAMETER = 0x81
    SET_PARAMETER = 0x82
    GET_VARIABLES = 0x83
    SET_SERVO_VARIABLE = 0x84 # (also clears the serial timeout timer)
    SET_TARGET = 0x85   # (also clears the serial timeout timer)
    CLEAR_ERRORS = 0x86 # (also clears the serial timeout timer)
    REINITIALIZE = 0x90
    ERASE_SCRIPT = 0xA0
    WRITE_SCRIPT = 0xA1
    SET_SCRIPT_DONE = 0xA2 # value.low.b is 0 for go, 1 for stop, 2 for single-step
    RESTART_SCRIPT_AT_SUBROUTINE = 0xA3
    RESTART_SCRIPT_AT_SUBROUTINE_WITH_PARAMETER = 0xA4
    RESTART_SCRIPT = 0xA5
    START_BOOTLOADER = 0xFF

# These are the bytes used to refer to the different parameters
# in UscRequest.GET_PARAMETER and UscRequest.SET_PARAMETER.  After changing
# any parameter marked as an "Init parameter", you must do UscRequest.REINITIALIZE
# before the new value will be used.
class UscParameter(Enum):
    SERVOS_AVAILABLE                  = (1, 1) # 1 byte - 0-5.  Init parameter.
    SERVO_PERIOD                      = (2, 1) # 1 byte - instruction cycles allocated to each servo/256, (units of 21.3333 us).  Init parameter.
    SERIAL_MODE                       = (3, 1) # 1 byte unsigned value.  Valid values are SERIAL_MODE_*.  Init parameter.
    SERIAL_FIXED_BAUD_RATE            = (4, 2) # 2-byte unsigned value; 0 means autodetect.  Init parameter.
    SERIAL_TIMEOUT                    = (6, 2) # 2-byte unsigned value (units of 10ms)
    SERIAL_ENABLE_CRC                 = (8, 1) # 1 byte boolean value
    SERIAL_NEVER_SUSPEND              = (9, 1) # 1 byte boolean value
    SERIAL_DEVICE_NUMBER              = (10, 1) # 1 byte unsigned value, 0-127
    SERIAL_BAUD_DETECT_TYPE           = (11, 1) # 1 byte - reserved

    IO_MASK_A                         = (12, 1) # 1 byte - reserved, init parameter
    OUTPUT_MASK_A                     = (13, 1) # 1 byte - reserved, init parameter
    IO_MASK_B                         = (14, 1) # 1 byte - reserved, init parameter
    OUTPUT_MASK_B                     = (15, 1) # 1 byte - reserved, init parameter
    IO_MASK_C                         = (16, 1) # 1 byte - pins used for I/O instead of servo, init parameter
    OUTPUT_MASK_C                     = (17, 1) # 1 byte - outputs that are enabled, init parameter
    IO_MASK_D                         = (18, 1) # 1 byte - reserved, init parameter
    OUTPUT_MASK_D                     = (19, 1) # 1 byte - reserved, init parameter
    IO_MASK_E                         = (20, 1) # 1 byte - reserved, init parameter
    OUTPUT_MASK_E                     = (21, 1) # 1 byte - reserved, init parameter

    SCRIPT_CRC                        = (22, 2) # 2 byte CRC of script
    SCRIPT_DONE                       = (24, 1) # 1 byte - if 0, run the bytecode on restart, if 1, stop

    SERIAL_MINI_SSC_OFFSET            = (25, 1) # 1 byte (0-254)


class UscServoParameter(Enum):
    def __init__(self, srvid):
        offset = srvid * 9 + 30
        self.SERVO_HOME                       = (offset + 30, 2) # 2 byte home position (0=off; 1=ignore)
        self.SERVO_MIN                        = (offset + 32, 1) # 1 byte min allowed value (x2^6)
        self.SERVO_MAX                        = (offset + 33, 1) # 1 byte max allowed value (x2^6)
        self.SERVO_NEUTRAL                    = (offset + 34, 2) # 2 byte neutral position
        self.SERVO_RANGE                      = (offset + 36, 1) # 1 byte range
        self.SERVO_SPEED                      = (offset + 37, 1) # 1 byte (5 mantissa,3 exponent) us per 10ms.  Init parameter.
        self.SERVO_ACCELERATION               = (offset + 38, 1) # 1 byte (speed changes that much every 10ms). Init parameter.


class BaudDetectType(Enum):
    AA = 0
    FF = 1

# serialMode: Value of UscParameter.SERIAL_MODE.
class SerialMode(Enum):
    # On the Command Port, user can send commands and receive responses.
    # TTL port/UART are connected to make a USB-to-serial adapter.
    USB_DUAL_PORT = 0

    # On the Command Port, user can send commands to UMC01 and
    # simultaneously transmit bytes on the UART TX line, and user
    # can receive bytes from the UMC01 and the UART RX line.
    # COM2 does not do anything.
    USB_CHAINED = 1

    # On the UART, user can send commands and receive reponses.
    # Command Port and TTL Port don't do anything.
    UART_DETECT_BAUD_RATE = 2
    UART_FIXED_BAUD_RATE = 3


# There are several different errors.  Each error is represented by a
# different bit number from 0 to 15.
class Errors(Enum):
    SERIAL_SIGNAL           = 0
    SERIAL_OVERRUN          = 1
    SERIAL_BUFFER_FULL      = 2
    SERIAL_CRC              = 3
    SERIAL_PROTOCOL         = 4
    SERIAL_TIMEOUT          = 5
    SCRIPT_STACK            = 6
    SCRIPT_CALL_STACK       = 7
    SCRIPT_PROGRAM_COUNTER  = 8


def to_2bytes(val16):
    """ Converts an integer to a byte-array of length 2 """
    val8_lsb = val16 & 0x7F;
    val8_msb = (val16 >> 7) & 0x7F
    return bytes((val8_lsb, val8_msb))