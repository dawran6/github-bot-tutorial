import os

import aiohttp
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp


router = routing.Router()


@router.register('pull_request', action='opened')
async def issue_opened_event(event, gh, *args, **kwargs):
    url = event.data["pull_request"]["url"]

    await gh.patch(url, data={"labels": 'help wanted'})


@router.register('issues', action='opened')
async def issue_opened_event(event, gh, *args, **kwargs):
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})


@router.register('issues', action='closed')
async def issue_merged_event(event, gh, *args, **kwargs):
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the PR @{author}! (I'm a bot)."
    await gh.post(url, data={"body": message})


@router.register('issue_comment', action='created')
async def issue_commented_event(event, gh, *args, **kwargs):
    url = event.data["comment"]["url"]
    await gh.post(f'{url}/reactions', data={"content": '+1'}, accept='application/vnd.github.squirrel-girl-preview+json')


async def main(request):
    body = await request.read()

    secret = os.getenv('GH_SECRET')
    oauth_token = os.getenv('GH_AUTH')

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

