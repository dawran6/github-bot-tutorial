import os

import aiohttp
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp


router = routing.Router()


@router.register('issues', action='opened')
async def issue_opened_event(event, gh, *args, **kwargs):
    pass


async def main(request):
    body = await request.read()

    secret = os.getenv('GH_SECRET')
    oauth_token = os.getenv('GH_TOKEN')

    event = sansio.Event.from_http(request.headers, body, secret=secret)

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, 'dawran6', oauth_token=oauth_token)
        await router.dispatch(event, gh)

    return web.Response(status=200)


if __name__ == '__main__':
    app = web.Application()
    app.router.add_post('/', main)
    port = os.environ.get('PORT')
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
