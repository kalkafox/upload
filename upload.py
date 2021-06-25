from aiohttp import web
import aiohttp
from rich.progress import Progress
from rich import inspect
from rich.logging import RichHandler
import io
import json
import logging

logging.basicConfig(handlers=[RichHandler()], level=logging.DEBUG)

log = logging.getLogger('rich')
log.info("Assembled rich.")

defaults = {
    'tld': 'i.kalka.io',
    'proto': 'https',
    'directory': '/var/www/upload/'
}

keys = json.loads(open(f'{defaults.get("directory")}keys.json').read())

async def check_url(url):
    pass

async def handle_upload(request):
    h = request.headers
    print(defaults.get('tld'))
    proto = h.get('proto') or defaults.get('proto')
    tld = h.get('tld') or defaults.get('tld')
    key = h.get('key') or None
    directory = f'{defaults.get("directory")}{tld}/'
    if key is None:
        return web.Response(text="You are missing a key.")
    if key not in keys:
        return web.Response(text="Your key was not correct.")
    reader = aiohttp.MultipartReader.from_response(request)
    filedata = None
    metadata = None
    filename = None
    while True:
        part = await reader.next()
        try:
            filename = part.filename
            log.info(filename)
        except AttributeError:
            break
        try:
            filedata = await part.read(decode=False)
        except AttributeError:
            break
    filedir = f'{directory}{filename}'
    url = f'{proto}://{tld}/{filename}'
    if filedata:
        with open(filedir, 'wb') as f:
            f.write(filedata)
    if metadata:
        inspect(metadata)
    return web.Response(text=url)

def add_route(app, uri, func):
    app.add_routes([web.post(uri, func)])
    log.info(f"Added {uri}.")

def assemble_web():
    log.info("Assembling web...")
    app = web.Application()
    log.info(f"Assembled web as {app}")
    add_route(app, '/upload', handle_upload)
    return app

def initialize_web(app):
    log.info("Initializing web...")
    web.run_app(app, sock=)

def main():
    app = assemble_web()
    log.info(app)
    try:
        initialize_web(app)
    except KeyboardInterrupt:
        log.info("We're halting, m'boys!")

main()

