from serial import Serial
from queue import Queue
from threading import Thread
from sim800.utils import clear_str
from sim800.event import Event


class SerialLoop(Thread):
    """
    SerialLoop is a thread there for communicate with the sim800 module over the serial interface
    """

    def __init__(self, sim, serial_port, debug):
        """
        Construct a new 'SerialLoop' object.

        :param sim: Sim800 object
        :param serial_port: port of the serial interface
        :param debug: indicates debug mode
        :return: returns nothing
        """

        super(SerialLoop, self).__init__()

        # If debug is enabled the serial connection is emulated with the commandline
        self.debug = debug

        if not debug:
            # Initialize a new serial connection
            self.serial = Serial(serial_port, baudrate=9600, timeout=1)

        # Set the sim800 object to emit events
        self.sim = sim

        # The Events that should be written and emitted, when a message returns from the serial interface
        self.event_queue = Queue(64)

        # Set running to False to stop the loop
        self.running = True

    def run(self):
        """
        Is there for writing commands to the serial interface and reading the response
        :return: returns nothing
        """

        while self.running:

            # Write the event to the serial interface and emit the returning value
            if not self.event_queue.empty():

                # Get the next event from the queue
                event = self.event_queue.get()

                # Write the command to the serial interface
                self._write(event['command'])

                # Remove \r\n
                data = clear_str(event['command'])

                # Get the data from the serial interface, remove \r\n and convert it to a string
                response = clear_str(self._read().decode('utf-8'))

                # If the prompt char is send back, serial800 expects some kind of data
                if response == '>':
                    self._write(event['data'] + '\r')

                # The sim800 module sends usually the same command back first
                elif response != data:
                    # Print an error and continue with the next command if not the same is send back
                    print("Error: Wrong event returned on serial port! Got: {}, Command: {}".format(response, data))
                    continue

                # Create new event object
                e = Event(event['name'])

                # Listen on the serial interface until an error or success
                while True:
                    # Get the data from the serial interface, remove \r\n and convert it to a string
                    response = clear_str(self._read().decode('utf-8'))

                    if 'OK' in response:
                        e.error = False
                        break
                    elif 'ERROR' in response:
                        e.error_message = response
                        e.error = True
                        break
                    elif len(response) > 0:
                        # Save the transmitted data in the content property of the event
                        e.content.append(response)

                # Emit an event to the last called command function
                self.sim.emit(event['name'], e)

            # If no events are in the queue, just listen on the serial port
            else:
                # Get the data from the serial interface, remove \r\n and convert it to a string
                response = clear_str(self._read().decode('utf-8'))

                if response == 'RING':
                    # Emit the ring event
                    self.sim.emit('ring')

    def _read(self):
        """
        Reads from the serial interface
        :return: returns the value from the serial interface
        """

        # When debug mode is enabled get the data from the command line
        if self.debug:
            return str.encode(input())
        else:
            # Read the data from the serial interface
            return self.serial.readline()

    def _write(self, data):
        """
        Writes data to the serial interface

        :param data: data that should be written
        :return: returns nothing
        """

        # When the data is not a string or bytes raise an value error
        if type(data) != bytes and type(data) != str:
            raise ValueError('Data must be type string or bytes')

        # If the data is a string encode it to bytes
        elif type(data) == str:
            data = str.encode(data)

        # If debug is enabled print the data to the console
        if self.debug:
            print(data)
            return

        # Else write the data to the serial interface
        self.serial.write(data)