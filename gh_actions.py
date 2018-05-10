import os
import asyncio

import aiohttp
from gidgethub.aiohttp import GitHubAPI


async def create_issue():
    async with aiohttp.ClientSession() as session:
        gh = GitHubAPI(session, 'dawran6', oauth_token=os.getenv('GH_AUTH'))
        await gh.post('/repos/mariatta/strange-relationship/issues',
                  data={
                      'title': 'Mayday! Too many problems!',
                      'body': 'Mayday!',
                  })


async def comment_on_issue():
    async with aiohttp.ClientSession() as session:
        gh = GitHubAPI(session, 'dawran6', oauth_token=os.getenv('GH_AUTH'))
        await gh.post('/repos/mariatta/strange-relationship/issues/83/comments',
                data={'body':'hooray'})


async def react_to_issue():
    async with aiohttp.ClientSession() as session:
        gh = GitHubAPI(session, 'dawran6', oauth_token=os.getenv('GH_AUTH'))
        await gh.post('/repos/mariatta/strange-relationship/issues/83/reactions',
                data={'content':'hooray'},
                accept='application/vnd.github.squirrel-girl-preview+json')


async def close_issue():
    async with aiohttp.ClientSession() as session:
        gh = GitHubAPI(session, 'dawran6', oauth_token=os.getenv('GH_AUTH'))
        await gh.post('/repos/mariatta/strange-relationship/issues/83')


async def main():
    await react_to_issue()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
