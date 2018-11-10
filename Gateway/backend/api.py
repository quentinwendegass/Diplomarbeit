import requests
from pyee import EventEmitter
from backend.sse import SSE
from utils import logger, AnsiEscapeSequence
import uuid


class API(EventEmitter):
    """
    Wrapper to send requests to the REST-API.
    """

    def __init__(self, username, password, _id=None, host='https://api.da.digitalsubmarine.com/v1'):
        super(API, self).__init__()
        self.auth = (username, password)
        self.host = host

        # Create an new sse connection, that emits the incoming push notifications on the API object
        self.sse = SSE(self)

        if _id is None:
            # TODO: Get IMEI instead of setting a random uuid
            self.id = str(uuid.uuid4())
            self.post_gateway()
        else:
            self.id = _id

        logger.info('Gateway', 'IMEI({})'.format(self.id))

    def start(self):
        """
        Start the sse thread.

        :return: nothing
        """

        self.sse.start()

    def close(self):
        """
        Close the sse thread.

        :return: noting
        """

        self.sse.close()

    def get_gateway(self):
        return self._request('/gateway/' + self.id, requests.get)

    def get_gateways(self):
        return self._request('/gateways', requests.get)

    def post_gateway(self):
        return self._request('/gateway', requests.post, {'imei': self.id})

    def delete_gateway(self):
        return self._request('/gateway/' + self.id, requests.delete)

    def put_gateway(self, signal_strength=None):
        body = {}
        if signal_strength:
            body['signalStrength'] = signal_strength

        return self._request('/gateway/' + self.id, requests.put, body)

    def get_user(self):
        return self._request('/user', requests.get)

    def put_user(self, first_name=None, last_name=None, password=None):
        body = {}
        if first_name:
            body['firstName'] = first_name
        if last_name:
            body['lastName'] = last_name
        if password:
            body['password'] = password

        return self._request('/user', requests.put, body)

    def _request(self, path, method, body=None):
        """
        Sends a http request to the server with a given http method
        and returns the json body in a dict

        :param path: path of the endpoint
        :param method: http method from requests module
        :param body: json data in form of a dict
        :type path: str
        :type method: request function
        :type body: dict
        :return: body of the response and status code in a tuple
        :returns: dict
        """

        if type(body) is not dict and body is not None:
            error = ValueError('Body has to be of type dict!')
            logger.error('API', error.args[0])
            raise error

        if body is None:
            response = method(self.host + path, auth=self.auth)
        else:
            response = method(self.host + path, auth=self.auth, json=body)

        data = response.json()
        status_code = AnsiEscapeSequence.BOLD + str(response.status_code) + AnsiEscapeSequence.DEFAULT
        path = AnsiEscapeSequence.UNDERLINE + path + AnsiEscapeSequence.DEFAULT
        logger.debug('API', 'Finished request ' + path + ' with status code ' + status_code)
        return data, response.status_code
