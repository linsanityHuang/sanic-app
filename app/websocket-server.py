from sanic import Sanic
from sanic.websocket import WebSocketProtocol

app = Sanic()


@app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = 'world!'
        print('Sending: ' + data)
        await ws.send(data)
        data = await ws.recv()
        print('Received: ' + data)
        data = 'close'
        await ws.send(data)
        data = await ws.recv()
        print('Received: ' + data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
