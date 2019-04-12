import gateway.io.sim800.at_parser as atparser
import gateway.io.sim800.at_response as atresponse
from gateway.core.config import set_config
import os


def test_sms_list_parser():
    content = ['+CMGL: 1,"REC UNREAD","+85291234567",,"07/02/18,00:05:10+32"',
               'Reading text messages is easy.',
               '+CMGL: 2,"REC UNREAD","+85291234567",,"07/02/18,00:07:22+32"',
               'A simple demo of SMS text messaging.']

    data = atparser.SMSListParser.parse(content)

    assert type(data) == list
    assert len(data) == 2
    assert isinstance(data[0], atresponse.SMS)
    assert data[0].message == content[1]
    assert data[0].status == atresponse.SMS.Status.Unread
    assert data[0].time.minute == 5
    assert data[0].address_name is None
    assert data[1].address == '+85291234567'
    assert data[1].message == 'A simple demo of SMS text messaging.'

    content = ['+CMGL: 1,"REC UNREAD","+85291234567",,',
               'Reading text messages is easy.']

    data = atparser.SMSListParser.parse(content)

    assert len(data) == 1
    assert data[0].time is None
    assert data[0].address_name is None
    assert data[0].index == 1


def test_network_status_parser():
    content = ['+CREG: 2,1,"008E","CE87"']

    data = atparser.NetworkStatusParser.parse(content)

    assert isinstance(data, atresponse.NetworkStatus)
    assert data.stat == atresponse.NetworkStatus.Status.RegisteredHome
    assert data.n == 2
    assert data.lac == '008E'
    assert data.ci == 'CE87'

    content = ['+CREG: 2,0']

    data = atparser.NetworkStatusParser.parse(content)

    assert data.stat == atresponse.NetworkStatus.Status.NotRegistered
    assert data.n == 2
    assert data.ci is None
    assert data.lac is None


def test_signal_quality_parser():
    content = ['+CSQ:18,99']

    data = atparser.SignalQualityParser.parse(content)

    assert isinstance(data, atresponse.SignalQuality)
    assert data.ber == 99
    assert data.rssi == 18


def test_pin_status_parser():
    content = ['+CPIN:READY']

    data = atparser.PinStatusParser.parse(content)

    assert isinstance(data, atresponse.PINStatus)
    assert data == atresponse.PINStatus.Ready


def test_imei_parser():
    content = ['Testimei']

    data = atparser.IMEIParser.parse(content)

    assert isinstance(data, atresponse.IMEI)
    assert data.imei == 'Testimei'


def test_subscriber_number_parser():
    content = ['+CNUM: ,"+48723976327",145']

    data = atparser.SubscriberNumberParser.parse(content)

    assert isinstance(data, atresponse.SubscriberNumber)
    assert data.number == '+48723976327'
    assert data.type == 145


def test_imsi_parser():
    config_path = os.environ['GATEWAY_CONFIG_PATH']
    set_config(config_path)

    content = ['214074200044176']

    data = atparser.IMSIParser.parse(content)

    assert isinstance(data, atresponse.IMSI)
    assert data.country == 'Spain'
    assert data.network == 'Movistar'


def test_caller_identification_parser():
    content = ['+CLIP: "+4366611199",129']
    data = atparser.CallerIdentificationParser.parse(content)

    assert isinstance(data, atresponse.CallerIdentification)
    assert data.number == '+4366611199'
    assert data.type == 129
    assert data.subaddr is None

    content = ['+CLIP: "+4366611199",129,iwas,3,asf,1']
    data = atparser.CallerIdentificationParser.parse(content)

    assert isinstance(data, atresponse.CallerIdentification)
    assert data.number == '+4366611199'
    assert data.type == 129
    assert data.subaddr == 'iwas'
