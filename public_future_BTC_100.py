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
                print(json_string['params']['data'][0]['timestamp'], json_string['params']['data'][0]['price'],
                      json_string['params']['data'][0]['amount'])
                if len(deals_cache) < 3:
                    print(deals_cache)
                    deals_cache.append(dict(ts=json_string['params']['data'][0]['timestamp'],
                                            price=json_string['params']['data'][0]['price'],
                                            amount=json_string['params']['data'][0]['amount']))
                else:
                    # TODO: вывод средней цены и объема алогоритма с начала работы, последние 20 сделок
                    with open('./results/deals.json', 'w') as json_file:
                        # TODO: добавление строк с новой строки
                        json.dump(deals_cache, json_file)
                        deals_cache.clear()
                        print('записано')

                    # print(dict(ts=json_string['params']['data'][0]['timestamp'],
                    #            price=json_string['params']['data'][0]['price'],
                    #            amount=json_string['params']['data'][0]['amount']))
            except KeyError:
                pass
            # print(json_string)
            # print(response)


asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
