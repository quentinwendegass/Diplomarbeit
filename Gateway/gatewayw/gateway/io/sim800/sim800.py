import asyncio

from pyee import EventEmitter

from serial import Serial

from gateway.io.sim800.serial_loop import SerialLoop
from gateway.io.sim800.at_command import ATCommand
from gateway.io.sim800.at_event import ATEvent
from gateway.io.sim800.at_parser import *
from gateway.io.sim800.at_response import *
from gateway.utils import clear_str


class Sim800Error(Exception):
    pass


def _raise_event_error(event):
    if event.error:
        raise Sim800Error(event.name, event.error_message)
    return event


class Sim800(EventEmitter):
    """
    Sim800 processes AT-Commands over the serial interface
    """

    def __init__(self, serial_port='/dev/serial0', debug=False, loop=asyncio.get_event_loop()):
        """
        Construct a new 'SerialLoop' object.

        :param serial_port: port of the serial interface
        :param debug: indicates debug mode
        :type serial_port: str
        :type debug: bool
        :return: returns nothing
        """

        super().__init__(scheduler=asyncio.run_coroutine_threadsafe, loop=loop)

        # Create serial loop
        serial = Serial(serial_port, baudrate=9600, timeout=1)
        self.serial_loop = SerialLoop(self, serial, debug)
        if debug:
            self.serial_loop.echo = False
        # Set the event loop
        self._event_loop = loop

        # Start the thread
        self.serial_loop.start()

        self.debug = debug

    def close(self):
        """
        Closes the SerialLoop thread

        :return: returns nothing
        :rtype: str
        """

        self.serial_loop.running.set()

    async def write(self, command):
        """
        Writes the command to the serial interface.

        :param command: command that should be written to the serial interface
        :return: returns the response event if no callback is set on the command
        """

        event = ATEvent(command.name, command)
        self.serial_loop.command_queue.put(event)

        await event.wait()
        return event

    async def answer_call(self):
        """
        Answer an incoming call.

        :return: event
        """

        return await self.write(ATCommand('ATA\r\n', name='AnswerCall'))

    async def hang_up_call(self):
        """
        Disconnect the current call.

        :return: event
        """

        return await self.write(ATCommand('ATH\r\n', name='HangUpCall'))

    async def dial_number(self, number):
        """
        Call a participant.

        :param number: phone number of the participant
        :type number: str
        :return: event
        """

        # Remove all \n and \r from the number
        number = clear_str(number)
        return await self.write(ATCommand('ATD{};\r\n'.format(number), name='DialNumber'))

    async def send_sms(self, number, text):
        """
        Send a sms to a participant.

        :param number: phone number of the participant
        :param text: message of the sms
        :type number: str
        :type text: str
        :return: event
        """

        # Remove all \n\r from the strings and add <ctrl-Z/ESC> after the message of the sms
        number = clear_str(number)
        text = clear_str(text)
        text += '\x1A'

        return await self.write(ATCommand('AT+CMGS="{}"\r'.format(number), name='SendSMS', data=text))

    async def request_unread_sms(self):
        """
        Read all unread sms.

        Event Data: [SMS]

        :return: event
        """
        return await self.write(ATCommand('AT+CMGL="REC UNREAD"\r\n', name='ListUnreadSMS', parser=SMSListParser))

    async def request_all_sms(self):
        """
        Read all sms.

        Event Data: [SMS]

        :return: event
        """

        return await self.write(ATCommand('AT+CMGL="ALL"\r\n', name='ListAllSMS', parser=SMSListParser))

    async def set_sms_mode(self, mode=None):
        """
        Set the sms mode.

        Mode can be either 0 or 1
        0: PDU mode
        1: Text mode

        :param mode: sms mode
        :type mode: int
        :return: event
        """

        return await self.write(ATCommand('AT+CMGF={}\r\n'.format(mode), name='SMSMode'))

    async def power_off(self, mode):
        """
        Shutdown the sim-module.

        Mode can be either 0 or 1
        0: Power off urgently
        1: Normal power off

        :param mode: mode for power off
        :return: event
        """

        return await self.write(ATCommand('AT+CPOWD={}\r\n'.format(mode), name='PowerOff'))

    async def request_signal_quality(self):
        """
        Read the signal quality.

        Event Data: SignalQuality

        :return: event
        """

        return await self.write(ATCommand('AT+CSQ\r\n', name='SignalQuality', parser=SignalQualityParser))

    async def reset_default_configuration(self):
        """
        Reset sim-module to default configuration.

        :return: event
        """

        return await self.write(ATCommand('ATZ\r\n', name='ResetDefaultConfiguration'))

    async def enter_pin(self, pin):
        """
        Enter the sim card pin.

        :param pin: pin, puk or puk2
        :return: event
        """

        return await self.write(ATCommand('AT+CPIN={}\r\n'.format(pin), name='EnterPIN'))

    async def request_pin_status(self):
        """
        Read the pin status of the sim card.

        Event Data: PinStatus

        :return: event
        """

        return await self.write(ATCommand('AT+CPIN?\r\n', name='PINStatus', parser=PinStatusParser))

    async def request_imei(self):
        """
        Read the imei.

        Event Data: IMEI

        :return: event
        """

        return await self.write(ATCommand('AT+GSN\r\n', name='IMEI', parser=IMEIParser))

    async def request_network_status(self):
        """
        Reads the current network status.

        Event Data: NetworkStatus

        :return: event
        """

        return await self.write(ATCommand('AT+CREG?\r\n', name='NetworkStatus', parser=NetworkStatusParser))

    async def set_echo_mode(self, mode):
        """
        Set the echo mode.

        0: Echo mode off
        1: Echo mode on

        :param mode: echo mode
        :type mode: int
        :return: event
        """

        event = await self.write(ATCommand('ATE{}\r\n'.format(mode), name='EchoMode'))

        if not event.error:
            self.serial_loop.echo = bool(mode)

        return event

    async def set_caller_identification_mode(self, mode):
        """
        Set the caller identification mode.

        0: No caller identification
        1: Get caller identification on ring

        :param mode: caller identification mode
        :type mode: int
        :return: event
        """

        event = await self.write(ATCommand('AT+CLIP={}\r\n'.format(mode), name='CallerIdentificationMode'))

        if not event.error:
            self.serial_loop.caller_identification = bool(mode)

        return event

    async def set_error_mode(self, mode):
        """
        Set the error mode.

        0: Disable CME error
        1: Enable CME error with error codes
        2: Enable CME error with verbose message

        :param mode: error mode
        :type mode: int
        :return: event
        """

        return await self.write(ATCommand('AT+CMEE={}\r\n'.format(mode), name='ErrorMode'))

    async def request_subscriber_number(self):
        """
        Read the subscriber number and additional parameters.

        :return: event
        """

        return await self.write(ATCommand('AT+CNUM\r\n', name='SubscriberNumber', parser=SubscriberNumberParser))

    async def request_imsi(self):
        """
        Read the operator imsi.

        :return: event
        """

        return await self.write(ATCommand('AT+CIMI\r\n', name='IMSI', parser=IMEIParser))

    async def transmit_dtmf_tone(self, tone):
        """
        Transmits one ore more dtmf tones.
        Supported characters: 0-9, #,*, A-D

        :param tone: tones
        :type tone: str
        :return: event
        """
        return await self.write(ATCommand('AT+VTS="{}"\r\n'.format(tone), name='DTMFTone'))

    # TODO: Fill in the right parameter for n in hold_call and resume_call

    async def hold_call(self):
        return await self.write(ATCommand('AT+CHLD=n\r\n', name='CallHold'))

    async def resume_call(self):
        return await self.write(ATCommand('AT+CHLD=n\r\n', name='CallResume'))

    async def setup(self, pin=None):
        """
        Setup the module to return error codes and set sms commands to text mode.

        :return: nothing
        """

        try:

            if pin:
                event = _raise_event_error(await self.request_pin_status())
                if event.data != PINStatus.Ready:
                    _raise_event_error(await self.enter_pin(pin))

            _raise_event_error(await self.set_sms_mode(1))
            _raise_event_error(await self.set_error_mode(1))
            _raise_event_error(await self.set_caller_identification_mode(1))
        except Sim800Error:
            raise
