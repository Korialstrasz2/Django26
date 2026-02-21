import asyncio
import contextlib
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.ping_task = asyncio.create_task(self.send_heartbeat())

    async def disconnect(self, close_code):
        if hasattr(self, 'ping_task'):
            self.ping_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.ping_task

    async def receive_json(self, content, **kwargs):
        event = content.get('event')
        if event == 'echo':
            await self.send_json({'event': 'echo', 'payload': content.get('payload', '')})

    async def send_heartbeat(self):
        sequence = 0
        while True:
            await asyncio.sleep(2)
            sequence += 1
            await self.send_json({'event': 'ping', 'message': 'heartbeat', 'sequence': sequence})
