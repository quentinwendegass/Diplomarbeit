from gateway.io.sim800.serial_loop import SerialLoop, EchoError, SerialError
from gateway.io.sim800 import ATEvent, ATCommand, at_parser
import queue
import pytest
from unittest.mock import Mock


@pytest.fixture
def sms_command():
    return ATCommand('AT+CMGL="ALL"', name='ListAllSMS', parser=at_parser.SMSListParser)


@pytest.fixture
def command_queue():
    q = queue.Queue(64)
    dial_command = ATCommand('ATD{};\r\n'.format('+436661111'), name='DialNumber')
    list_sms_command = ATCommand('AT+CMGL="ALL"\r\n', name='ListAllSMS', parser=at_parser.SMSListParser)
    q.put(ATEvent('DialNumber', dial_command))
    q.put(ATEvent('ListAllSMS', list_sms_command))

    assert '\r\n' in dial_command.command

    return q


@pytest.fixture
def event():
    command = ATCommand('AT+CMGL="ALL"\r\n', name='ListAllSMS', parser=at_parser.SMSListParser)
    event = ATEvent('ListAllSMS', command)
    return event


@pytest.fixture
def emitter_mock():
    mock = Mock()
    attrs = {'emit.return_value': None}
    mock.configure_mock(**attrs)
    return mock


@pytest.fixture
def serial_mock():
    mock = Mock()
    attrs = {'write.return_value': '', 'readline.side_effect': ['']}
    mock.configure_mock(**attrs)
    return mock


def test_get_event_from_queue(command_queue, emitter_mock, serial_mock):
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    event, command = serialloop._get_event_from_queue(command_queue)

    assert event.name == 'DialNumber'
    assert command.name == 'DialNumber'
    assert '\r\n' not in command.command

    assert command_queue.qsize() == 1

    event, command = serialloop._get_event_from_queue(command_queue)

    assert event.name == 'ListAllSMS'
    assert command.name == 'ListAllSMS'
    assert command_queue.qsize() == 0
    assert command_queue.empty()


def test_verify_echo_success(sms_command, emitter_mock, serial_mock):
    ret = sms_command.command.encode('utf-8')
    serial_mock.readline.side_effect = [ret]
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    serialloop._verify_echo(sms_command)
    serial_mock.readline.assert_called_once()


def test_verify_echo_failure(serial_mock, emitter_mock, sms_command):
    serialloop = SerialLoop(emitter_mock, serial_mock, False)
    serial_mock.readline.side_effect = [b'wrong echo']

    with pytest.raises(EchoError):
        serialloop._verify_echo(sms_command)

    serial_mock.readline.assert_called_once()


def test_verify_echo_off(emitter_mock, serial_mock, sms_command):
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    serialloop.echo = False
    serialloop._verify_echo(sms_command)
    serial_mock.readline.assert_not_called()


def test_read_response_ok(event, emitter_mock, serial_mock):
    serial_mock.readline.side_effect = [b'Line1', b'Line2', b'Line3', b'OK: Some Message']
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    assert type(event.content) == list
    assert len(event.content) == 0

    serialloop._read_response(event)

    assert len(event.content) == 3
    assert not event.error
    assert event.error_message is ''
    assert event.data is None
    assert event.content[0] == 'Line1'


def test_read_response_error(event, emitter_mock, serial_mock):
    serial_mock.readline.side_effect = [b'Line1', b'Line3', b'ERROR<Error Code>']
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    serialloop._read_response(event)

    assert len(event.content) == 2
    assert event.error
    assert event.error_message == 'ERROR<Error Code>'
    assert event.content[0] == 'Line1'


def test_read_response_interruption(event, emitter_mock, serial_mock):
    serial_mock.readline.side_effect = [b'Line1', b'Line2', b'RING', b'Line3', b'OK: Some Message']
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    assert type(event.content) == list
    assert len(event.content) == 0

    serialloop._read_response(event)

    assert len(event.content) == 3
    assert not event.error
    assert event.error_message is ''
    assert event.data is None

    assert event.content[0] == 'Line1'
    emitter_mock.emit.assert_called_once_with('ring', None)


def test_read_response_serial_error(event, emitter_mock, serial_mock):
    serial_mock.readline.side_effect = [b'Line1', b'\xde\xad\xbe\xef', b'OK']
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    with pytest.raises(SerialError):
        serialloop._read_response(event)

    assert len(event.content) == 1
    assert event.error


def test_emit_serial_event(serial_mock, emitter_mock):
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    emitted = serialloop._emit_serial_event('RING')
    assert emitted
    emitter_mock.emit.assert_called_once_with('ring', None)

    emitter_mock.emit.reset_mock()

    emitted = serialloop._emit_serial_event('NOTREGOGNIZEDDATA')
    assert not emitted
    emitter_mock.emit.assert_not_called()


def test_emit_serial_event_caller_identification(serial_mock, emitter_mock):
    serial_mock.readline.side_effect = [b'+CLIP: "+4366611199",129']
    serialloop = SerialLoop(emitter_mock, serial_mock, False)
    serialloop.caller_identification = True

    emitted = serialloop._emit_serial_event('RING')

    assert emitted
    emitter_mock.emit.assert_called_once_with('ring', '+4366611199')


def test_read(serial_mock, emitter_mock):
    data = b'Test'
    serialloop = SerialLoop(emitter_mock, serial_mock, False)
    serial_mock.readline.side_effect = [data]

    ret_data = serialloop._read()

    serial_mock.readline.assert_called_once()
    assert type(ret_data) == bytes
    assert data == ret_data


def test_write(serial_mock, emitter_mock):
    serialloop = SerialLoop(emitter_mock, serial_mock, False)
    serialloop._write('Test')

    serial_mock.write.assert_called_once_with(b'Test')


def test_write_value_error(serial_mock, emitter_mock):
    serialloop = SerialLoop(emitter_mock, serial_mock, False)

    with pytest.raises(ValueError):
        serialloop._write(object())

    serial_mock.write.assert_not_called()
