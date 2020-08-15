import asyncio
import websockets
import json

msg = \
    {
        "method": "public/subscribe",
        "params": {
            "channels": [
                "trades.future.BTC.100ms"
            ]
        },
        "jsonrpc": "2.0",
        "id": 16
    }


async def call_api(msg):
    async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
        await websocket.send(msg)
        deals_cache = list()
        while websocket.open:
            response = await websocket.recv()
            json_string = json.loads(response)
            try:
                print(json_string['params']['data'][0]['timestamp'],
                      json_string['params']['data'][0]['price'],
                      json_string['params']['data'][0]['amount'])
                if len(deals_cache) < 1000:
                    deals_cache.append(dict(ts=json_string['params']['data'][0]['timestamp'],
                                            price=json_string['params']['data'][0]['price'],
                                            amount=json_string['params']['data'][0]['amount']))
                else:
                    get_average(deals_cache)
                    with open('./results/deals.json', 'a') as json_file:
                        json_file.writelines(f'{row}\n' for row in deals_cache)
                        deals_cache.clear()
            except KeyError:
                pass


def get_average(_list):
    count = 0
    counts = int(len(_list) * 0.98)
    deals_summ = 0
    amount_summ = 0
    for row in _list:
        count += 1
        deals_summ += row.get('price')
        amount_summ += row.get('amount')
        if count >= counts:
            print(row)
    print(f'average trade: {deals_summ / count}')
    print(f'average amount: {amount_summ / count}')


asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
