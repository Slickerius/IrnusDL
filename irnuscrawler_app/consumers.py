import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from irnuscrawler_app.downloader import download_album

class DownloadConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    await self.accept()
  async def disconnect(self, close_code):
    raise StopConsumer()
  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    url = text_data_json['url']

    is_use_track_artist = bool(text_data_json['is_use_track_artist'])
    is_use_multiple_artist = bool(text_data_json['is_use_multiple_artist'])

    await download_album(url, is_use_track_artist, is_use_multiple_artist, self)