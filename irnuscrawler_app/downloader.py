import aiohttp
import aiofiles
import eyed3
from eyed3.id3.frames import ImageFrame
from bs4 import BeautifulSoup
import json
import datetime
from uuid import uuid4
import os
import asyncio
import traceback
import re
import subprocess
import shutil

# Helper function to sanitize and escape file names
def sanitize_filename(filename):
    # Escape forward slashes and remove other problematic characters
    return re.sub(r'[<>:"\\|?*]', '', filename).replace('/', '\\/')

async def download_album(url, is_use_track_artist, is_use_multiple_artist, consumer):
    try:
        if not re.match(r'^https:\/\/www\.iramanusantara\.org\/release\/\d+(\/master)?$', url):
            await consumer.send(text_data=json.dumps({
                'status': 'ERROR',
                'message': 'Invalid URL, please try again.',
            }))
            return

        uuid = str(uuid4())
        os.makedirs(f'tmp-{uuid}', exist_ok=True)

        async with aiohttp.ClientSession() as session:
            html = ''
            
            async with session.get(url) as response:
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
            script_el = soup.find('script', id='__NEXT_DATA__')
            json_data = script_el.string
            data = json.loads(json_data)

            if not data['props']['pageProps']['data']:
                await consumer.send(text_data=json.dumps({
                    'status': 'ERROR',
                    'message': 'Release not found, please try again.',
                }))
                return

            data = data['props']['pageProps']['data']['attributes']
            album_title = sanitize_filename(data['record_title'])
            album_year = data['released']
            if not (album_year and album_year.isdigit()):
                album_year = ''
            album_country = data['country']
            album_artist = sanitize_filename(data['artist'][0]['artist']['data']['attributes']['artist_name'])
            album_art_url = data['record_thumbnail']['data'][0]['attributes']['url']
            album_art_extension = album_art_url.split('.')[-1]

            if is_use_multiple_artist:
                album_artist = ', '.join(sanitize_filename(artist['artist']['data']['attributes']['artist_name']) for artist in data['artist'])

            if album_artist == 'Student Power, The':
                album_artist = 'The Student Power'

            await consumer.send(text_data=json.dumps({
                'status': 'INFO',
                'album_title': album_title,
                'album_year': album_year,
                'album_country': album_country,
                'album_artist': album_artist,
                'album_art_url': album_art_url,
            }))

            cover_file_path = f'tmp-{uuid}/cover.{album_art_extension}'
            async with session.get(album_art_url) as response:
                async with aiofiles.open(cover_file_path, 'wb') as f:
                    await f.write(await response.read())

            for i, track in enumerate(data['tracklists']):
                track_title = sanitize_filename(track['title']).replace('/', '\\/')
                track_duration = datetime.timedelta(seconds=int(track['duration']))
                track_artist = ''

                if not track['file_track']['data']:
                    continue

                if is_use_track_artist and track['credits']:
                    if is_use_multiple_artist:
                        track_artist = ', '.join(
                            sanitize_filename(credits['artists']['data'][0]['attributes']['artist_name'])
                            for credits in track['credits']
                            if credits['role'] == 'Vokal'
                        ) or album_artist
                    else:
                        for credits in track['credits']:
                            if credits['role'] == 'Vokal' and not track_artist:
                                track_artist = sanitize_filename(credits['artists']['data'][0]['attributes']['artist_name'])
                                break

                if not track_artist:
                    track_artist = album_artist

                track_url = track['file_track']['data']['attributes']['url']
                track_extension = track_url.split('.')[-1]

                await consumer.send(text_data=json.dumps({
                    'status': 'PROCESS',
                    'message': f'({i + 1}/{len(data["tracklists"])}) Processing {track_artist} - {track_title} ({track_duration})',
                }))

                track_file_path = f'tmp-{uuid}/{track_title}.{track_extension}'
                async with session.get(track_url) as response:
                    async with aiofiles.open(track_file_path, 'wb') as f:
                        await f.write(await response.read())

                aud = eyed3.load(track_file_path)
                if not aud.tag:
                    aud.initTag()

                aud.tag.artist = track_artist
                aud.tag.album = album_title
                aud.tag.title = track_title
                aud.tag.track_num = i + 1

                if album_year and album_year.isdigit():
                    aud.tag.recording_date = eyed3.core.Date(int(album_year))

                aud.tag.images.set(3, open(cover_file_path, 'rb').read(), 'image/jpeg')
                aud.tag.save(version=eyed3.id3.ID3_V2_3)

            out_file_name = f'{album_artist} - {album_title}'
            if album_year:
                out_file_name += f' ({album_year})'
            
            out_file_name = sanitize_filename(out_file_name)

            await consumer.send(text_data=json.dumps({
                'status': 'PROCESS',
                'message': 'Zipping tracks...',
            }))

            zip_command = f'cd tmp-{uuid}; zip -r ../static/tmp/"{out_file_name}.zip" *'
            process = await asyncio.create_subprocess_shell(zip_command)
            await process.communicate()

            await consumer.send(text_data=json.dumps({
                'status': 'SUCCESS',
                'url': f'/static/tmp/{out_file_name}.zip',
            }))

            shutil.rmtree(f'tmp-{uuid}')
            subprocess.Popen(f'sleep 180 && rm static/tmp/"{out_file_name}.zip"', shell=True)

    except Exception as e:
        traceback.print_exc()
        await consumer.send(text_data=json.dumps({
            'status': 'ERROR',
            'message': 'An error has occurred.'
        }))
