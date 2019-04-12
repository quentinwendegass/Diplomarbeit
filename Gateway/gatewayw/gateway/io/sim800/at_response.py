from enum import IntEnum, Enum

import attr

#
# TODO: Typecheck attributes
#


class ATResponse:
    pass


@attr.s
class IMEI(ATResponse):
    """
    Wrapper class for IMEI.
    """

    imei = attr.ib()


@attr.s
class IMSI(ATResponse):
    """
    Data class for IMSI.
    """

    mcc = attr.ib()
    mnc = attr.ib()
    msin = attr.ib()
    network = attr.ib()
    country = attr.ib()
    iso = attr.ib()


class PINStatus(Enum):
    """
    Enum for the pin status.
    """

    Ready = 'READY'
    Pin = 'SIM PIN'
    Puk = 'SIM PUK'
    PHPin = 'PH_SIM PIN'
    PHPuk = 'PH_SIM PUK'
    Pin2 = 'SIM PIN2'


@attr.s
class NetworkStatus(ATResponse):
    """
    Data class for the network status.

    The attribute names are the same as in the at-commands documentation
    (https://www.elecrow.com/download/SIM800%20Series_AT%20Command%20Manual_V1.09.pdf).
    Furthermore a enum for the actual status is defined within this class.
    """

    class Status(IntEnum):
        """
        Enum for the network status.
        """

        NotRegistered = 0
        RegisteredHome = 1
        Searching = 2
        Denied = 3
        Unknown = 4
        RegisteredRoaming = 5

    # Names defined like in the at-commands documentation
    n = attr.ib()
    stat = attr.ib()
    lac = attr.ib(default=None)
    ci = attr.ib(default=None)

    def __attrs_post_init__(self):
        """
        Sets self.stat to a Status object after the initialization.

        :return: nothing
        """

        self.stat = self.Status(self.stat)


@attr.s
class SignalQuality(ATResponse):
    """
    Data class for the signal quality.

    The attribute names are the same as in the at-commands documentation
    (https://www.elecrow.com/download/SIM800%20Series_AT%20Command%20Manual_V1.09.pdf).
    """

    rssi = attr.ib()
    ber = attr.ib()


@attr.s
class SMS(ATResponse):
    """
    Data class for a sms.
    """

    class Status(Enum):
        Unread = 'REC UNREAD'
        Read = 'REC READ'
        Unsent = 'STO UNSENT'
        Sent = 'STO SENT'

    index = attr.ib()
    status = attr.ib()
    address = attr.ib()
    message = attr.ib()
    address_name = attr.ib(default=None)
    time = attr.ib(default=None)

    def __attrs_post_init__(self):
        """
        Sets status to a Status object after the initialization.

        :return: nothing
        """

        self.status = self.Status(self.status)


@attr.s
class SubscriberNumber(ATResponse):
    """
    Data class for subscriber number.
    """

    number = attr.ib()
    type = attr.ib()
    alpha = attr.ib(default=None)
    speed = attr.ib(default=None)
    service = attr.ib(default=None)


@attr.s
class CallerIdentification(ATResponse):
    """
    Data class for caller identification (AT+CLIP)
    """

    number = attr.ib()
    type = attr.ib()
    subaddr = attr.ib(default=None)
    satype = attr.ib(default=None)
    alphaId = attr.ib(default=None)
    cli_validity = attr.ib(default=None)
