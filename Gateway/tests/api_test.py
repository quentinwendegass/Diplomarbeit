from backend import API
from utils import logger, AnsiEscapeSequence, Level


def run():
    api = API('quentin@wendegass.com', 'test123', 'wed')

    @api.on('test')
    def test_notification(data):
        logger.info('Test', 'Received notification {}'.format(str(data)))

    @api.on('connectionStateChange')
    def on_connection_state_change(state):
        state = AnsiEscapeSequence.UNDERLINE + state + AnsiEscapeSequence.DEFAULT
        logger.info('Connection State', 'Connection state changed to ' + state)

    @api.on('connectionFailed')
    def on_connection_failed(error):
        logger.error('Connection', 'An error occurred (' + error['error'] + ')')

    @api.on('connectionAborted')
    def on_connection_aborted():
        logger.error('Connection', 'Connection was aborted!')

    @api.on('connectionRefused')
    def on_connection_refused():
        logger.error('Connection', 'Can not connect to host!')

    @api.once('connect')
    def on_connect():
        logger.info('Connection', 'Connected with host!')
        logger.log('Tests[Put User]', 'Response = ' + str(api.put_user('Quentin', 'Wendegass')))
        logger.log('Tests[Get User]', 'Response = ' + str(api.get_user()))
        logger.log('Tests[Post Gateway]', 'Response = ' + str(api.post_gateway()))
        logger.log('Tests[Put Gateway]', 'Response = ' + str(api.put_gateway(4423)))
        logger.log('Tests[Get Gateway]', 'Response = ' + str(api.get_gateway()))
        logger.log('Tests[Delete Gateway]', 'Response = ' + str(api.delete_gateway()))
        logger.log('Tests[Get Gateways]', 'Response = ' + str(api.get_gateways()))

    api.start()


if __name__ == '__main__':
    logger.level = Level.DEBUG

    try:
        run()
    except Exception as e:
        print(e)