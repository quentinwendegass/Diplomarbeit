from gateway.networking import WebRTC, Role
from gateway.utils import logger, Level
from gateway.core import set_config, get_config
import asyncio
import sys

logger.level = Level.DEBUG

CALL_TIMER = 10

set_config('config.ini')
config = get_config()
USERNAME = config['Auth']['user']
PASSWORD = config['Auth']['password']
HOST = config['Server']['signalinghost']


async def test(role):
    con = WebRTC(USERNAME, PASSWORD, HOST, debug=True)
    con.on('connectionClosed', asyncio.get_event_loop().stop)
    con.start_call(role)
    if CALL_TIMER > 0:
        await asyncio.sleep(CALL_TIMER)
        con.stop_call()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'offer':
            asyncio.ensure_future(test(Role.OFFER))

        elif sys.argv[1] == 'answer':
            asyncio.ensure_future(test(Role.ANSWER))

        else:
            raise ValueError('No proper role!')
    else:
        asyncio.ensure_future(test(Role.OFFER))

    asyncio.get_event_loop().run_forever()
