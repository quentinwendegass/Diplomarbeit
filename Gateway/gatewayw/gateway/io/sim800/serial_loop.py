import threading
from queue import Queue
from threading import Thread

from gateway.utils import clear_str, logger
from gateway.io.sim800.at_parser import CallerIdentificationParser


class SerialError(Exception):
    pass


class EchoError(SerialError):
    pass


class SerialLoop(Thread):
    """
    SerialLoop is a thread for communication with the sim800 module over the serial interface.
    """

    def __init__(self, emitter, serial, debug):
        """
        Construct a new 'SerialLoop' object.

        :param emitter: Sim800 object
        :param serial: serial object
        :param debug: indicates debug mode
        :type emitter: object
        :type serial: object
        :type debug: bool
        :return: returns nothing
        """

        super(SerialLoop, self).__init__()

        if not hasattr(emitter, 'emit'):
            raise ValueError

        # If debug is enabled the serial connection is emulated with the commandline
        self.debug = debug

        if not debug:
            # Initialize a new serial connection
            self.serial = serial

        self.emitter = emitter
        self.echo = True
        self.caller_identification = False

        # The Events that should be written and emitted, when a message returns from the serial interface
        self.command_queue = Queue(64)

        # Set running to stop the loop
        self.running = threading.Event()

        self.daemon = True

    @staticmethod
    def _get_event_from_queue(command_queue):

        # Get the next event from the queue
        event = command_queue.get()
        command = event.command

        # Remove \r\n
        command.command = clear_str(command.command)

        return event, command

    def _verify_echo(self, command):
        """
        Reads from the serial interface and checks if the data is the same as the passed command.

        :param command: command object of the event
        :return: nothing
        :raise EchoError: raises if the echo is not the same as the command
        """

        # Verify the command if echo mode is on
        if self.echo:
            # Get the data from the serial interface, remove \r\n and convert it to a string
            response = self._read()
            response = clear_str(response.decode('utf-8'))

            # The sim800 module sends usually the same command back first
            if response != command.command:
                # Print an error and continue with the next command if not the same is send back
                logger.error('Sim800', 'SerialError(WrongEcho: {})'.format(response))
                raise EchoError(response, command.command)

    def _read_response(self, event):
        """
        Reads from the serial interface and fills the event object with the response.

        :param event: event object
        :return: nothing
        :raise SerialError: raises if the serial data can not be decoded
        """

        command = event.command

        # Listen on the serial interface until an error or success
        while True:
            res = self._read()
            # Get the data from the serial interface, remove \r\n and convert it to a string
            try:
                response = clear_str(res.decode('utf-8'))
            except UnicodeDecodeError:
                logger.error('Sim800', 'SerialError')
                event.error = True
                raise SerialError('Received data could not be decoded!')

            # If the prompt char is send back, serial800 expects some kind of data
            if '>' in response and command.data:
                self._write(command.data)
                continue

            if 'OK' in response:
                event.error = False
                break
            elif 'ERROR' in response:
                event.error_message = response
                event.error = True
                break
            elif len(response) > 0:
                # Save the transmitted data in the content property of
                # the event line by line until OK or ERROR is send
                if not self._emit_serial_event(response):
                    event.content.append(response)

    def _emit_serial_event(self, response):
        """
        Checks the response string for an event.

        :param response: event from serial interface e.g. RING
        :type response str
        :return: boolean that indicates if the passed data was processed
        """

        logger.debug('Sim800', 'Got other data: {}'.format(response))
        if response == 'RING':
            logger.debug('Sim800', 'Processing ring event...')
            number = None

            if self.caller_identification:
                data = self._read()
                caller_identification = CallerIdentificationParser.parse([data.decode('utf-8')])
                number = caller_identification.number

            # Emit the ring event
            self.emitter.emit('ring', number)
            logger.info('Sim800', 'Ring event!')
            return True
        return False

    def run(self):
        """
        Is there for writing commands to the serial interface and reading the response

        :return: returns nothing
        """

        logger.info('Sim800', 'Started Service!')

        while not self.running.is_set():
            # Write the event to the serial interface and emit the returning value
            if not self.command_queue.empty():
                event, command = self._get_event_from_queue(self.command_queue)

                # Write the command to the serial interface
                self._write(command.command)

                try:
                    self._verify_echo(command)           # Verify the echo of the command if activated
                    self._read_response(event)  # Fill the event with the response from the serial interface
                except EchoError or SerialError:
                    continue

                if not event.error:
                    # Parse the event content
                    event.data = command.parser.parse(event.content)

                # Set the event for tasks that are waiting for it
                event.set()

            # If no events are in the queue, just listen on the serial port
            else:
                # Get the data from the serial interface, remove \r\n and convert it to a string
                res = self._read()
                try:
                    response = clear_str(res.decode('utf-8'))
                    if not response:
                        continue

                    self._emit_serial_event(response)

                except UnicodeDecodeError:
                    logger.error('Sim800', 'SerialError')

    def _read(self):
        """
        Reads from the serial interface

        :return: returns the value from the serial interface
        :rtype: bytearray
        """

        # When debug mode is enabled get the data from the command line
        if self.debug:
            return str.encode(input())
        else:
            # Read the data from the serial interface
            data = self.serial.readline()
            if data:
                logger.debug('Sim800', 'Received data from serial interface: ' + str(data))
            return data

    def _write(self, data):
        """
        Writes data to the serial interface

        :param data: data that should be written
        :type data: bytearray, str
        :return: returns nothing
        """

        # When the data is not a string or bytes raise an value error
        if type(data) != bytes and type(data) != str:
            error = ValueError('Data must be type string or bytes')
            logger.info('Sim800', error.args[0])
            raise error

        # If the data is a string encode it to bytes
        elif type(data) == str:
            data = str.encode(data)

        logger.debug('Sim800', 'Wrote data to serial interface: ' + str(data))

        # Write the data to the serial interface
        if not self.debug:
            self.serial.write(data)
