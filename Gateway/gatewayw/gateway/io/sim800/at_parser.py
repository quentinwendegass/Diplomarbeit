import json
from datetime import datetime

import gateway.utils as utils
from gateway.io.sim800.at_response import *
from gateway.core.config import get_apn_config_path


class ParseError(Exception):  # TODO: Raise error on failure
    pass


class ATParser:
    """
    Parser with an basic implementation that does nothing.

    All custom parser should extend this class.
    """

    @staticmethod
    def parse(content):
        """
        Parses the received data.

        :param content: array of received lines
        :return: the parsed data
        """
        return None


class SMSListParser(ATParser):
    """
    Parser that returns al list of SMS objects.
    """

    @staticmethod
    def parse(content):
        sms = []

        # Every second line represents the information of the sms. The other line is the message of the sms.
        for i, line in enumerate(content[::2]):
            # Remove the command name from the string and split the data
            data = utils.split_str(line[line.index(':') + 1:])
            data[0] = data[0].strip()

            # Add a new sms object to the list
            s = SMS(int(data[0]), data[1][1:-1], data[2][1:-1], content[i * 2 + 1])
            if data[3]:
                s.address_name = data[3][1:-1]
            if len(data) > 4 and data[4]:
                time_str = data[4][1:-1]

                # Get the index where the timezone starts
                try:
                    zone_index = time_str.index('-')
                except ValueError:
                    try:
                        zone_index = time_str.index('+')
                    except ValueError:
                        zone_index = len(time_str) - 1

                # Convert the timestamp to a datetime object without the timezone
                s.time = datetime.strptime(time_str[0:zone_index], '%y/%m/%d,%H:%M:%S')

            sms.append(s)
        return sms


class NetworkStatusParser(ATParser):
    """
    Parser that returns a NetworkStatus object.
    """

    @staticmethod
    def parse(content):
        data = utils.split_str(content[0][content[0].index(':') + 1:])

        status = NetworkStatus(int(data[0].strip()), int(data[1]))

        if len(data) == 4:
            status.lac = data[2][1:-1]
            status.ci = data[3][1:-1]

        return status


class SignalQualityParser(ATParser):
    """
    Parser that returns a SignalQuality object.
    """

    @staticmethod
    def parse(content):
        data = utils.split_str(content[0][content[0].index(':') + 1:])
        return SignalQuality(int(data[0].strip()), int(data[1]))


class PinStatusParser(ATParser):
    """
    Parser that returns a PinStatus object.
    """

    @staticmethod
    def parse(content):
        print(content)
        return PINStatus(content[0][content[0].index(':') + 1:].strip())


class IMEIParser(ATParser):
    """
    Parser that returns a IMEI object.
    """

    @staticmethod
    def parse(content):
        return IMEI(content[0])


class SubscriberNumberParser(ATParser):
    """
    Parser that returns a SubscriberNumber object.
    """

    @staticmethod
    def parse(content):
        data = utils.split_str(content[0][content[0].index(':') + 1:])

        number = SubscriberNumber(data[1][1:-1], int(data[2]))

        if data[0].strip():
            number.alpha = data[0].strip()

        if len(data) == 5:
            number.speed = data[3]
            number.service = data[4]

        return number


class IMSIParser(ATParser):
    """
    Parser that returns an IMSI object.
    """

    @staticmethod
    def parse(content):
        mcc = content[0][:3]
        mnc = content[0][3:5]
        msin = content[0][5:]

        with open(get_apn_config_path()) as f:
            data = json.load(f)

            country = None
            iso = None
            network = None

            if mcc in data:
                country = data[mcc]['country']
                iso = data[mcc]['iso']

                if mnc in data[mcc]:
                    network = data[mcc][mnc]

            return IMSI(mcc, mnc, msin, network.strip(), country.strip(), iso)


class CallerIdentificationParser(ATParser):
    """
    Parser that returns the caller number.
    """

    @staticmethod
    def parse(content):

        data = utils.split_str(content[0][content[0].index(':') + 1:])

        if len(data) > 2:
            print(data[0])
            print(data[0].strip())
            print(data[0][1:-1])
            return CallerIdentification(data[0].strip()[1:-1], int(data[1]), data[2].strip(),
                                        int(data[3]), data[4].strip(), int(data[5]))
        else:
            return CallerIdentification(data[0].strip()[1:-1], int(data[1]))
