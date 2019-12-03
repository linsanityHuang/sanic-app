import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://localhost:1338/feed') as ws:
            await ws.send_str('hello')

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print('Received: ' + msg.data)
                    if msg.data == 'close':
                        await ws.close()
                        break
                    else:
                        await ws.send_str(msg.data + '/answer')
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
