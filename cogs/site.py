import settings 
from core import Bot, HiddenCog, Logger
from discord.ext import commands
import requests
import re
import dateparser
import datetime


class Site(HiddenCog, command_attrs = dict(hidden = True)):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_id = None
        self.csrf = None

    async def cog_check(self, context: commands.Context):
        return await self.bot.is_owner(context.message.author)

    async def api_login(self):
        self.login_id = None
        self.csrf = None 
        try:
            data = {
                'email_address': settings.USERNAME,
                'password': settings.PASSWORD
            }
            response = requests.post(f'{settings.API_ENDPOINT}/login/', data = data)
            text = response.headers['Set-Cookie']
            self.login_id = re.findall("sessionid=\w+;", text)[0].strip(";")[10:]
            self.csrf = re.findall("csrftoken=\w+;", text)[0].strip(";")[10:]
        except Exception as e:
            print(e)

    async def get_api(self, endpoint: str, query: str = None):
        try:
            cookies = {'sessionid': self.login_id}
            response = requests.get(f'{settings.API_ENDPOINT}/{endpoint}/' if query is None else f'{settings.API_ENDPOINT}/{endpoint}/{query}/', cookies = cookies)
            return response
        except Exception as e:
            print(e)

    async def post_api(self, endpoint: str, data: dict):
        try:
            cookies = {'sessionid': self.login_id, 'csrftoken': self.csrf}
            headers = {'X-CSRFToken': self.csrf}
            response = requests.post(f'{settings.API_ENDPOINT}/{endpoint}/', data = data, cookies = cookies, headers = headers)
            return response
        except Exception as e:
                print(e)
    
    async def search_api(self, endpoint: str, query: str):
        try:
            cookies = {'sessionid': self.login_id}
            response = requests.get(f'{settings.API_ENDPOINT}/{endpoint}/?search={query}', cookies = cookies)
            return response
        except Exception as e:
            print(e)
    

    @commands.command(name = 'login')
    async def _login(self, context: commands.Context, *args, **kwargs):
        await self.api_login()
        await context.send('Successfully Logged In')

    
    @commands.command(name = 'search')
    async def _search(self, context: commands.Context, endpoint: str, term: str, *args, **kwargs):
        if self.login_id is None:
            await self.api_login()
        response = await self.search_api(endpoint, term)
        if response.status_code == 200:
            return await context.send(response.json())
        
    
    @commands.command(name = 'book')
    async def _book(self, context: commands.Context, student: str, *date: str, **kwargs):
        if self.login_id is None:
            await self.api_login()

        response = await self.search_api('users', student)
        results = response.json()
        found = None
        matches = [data for data in results if data["is_staff"] == False]
        match len(matches):
            case 0:
                return await context.send("User not found!")
            case 1:
                found = matches[0]
            case _:
                return await context.send("Multiple users found!")

        start_time = dateparser.parse(" ".join(date))
        end_time = start_time + datetime.timedelta(hours = 1)
        student_id = found['id']

        data = {
            'student': student_id,
            'start_time': start_time,
            'end_time': end_time
        }
        response = await self.post_api('bookings', data)
        if response.status_code in [200, 201, 202]:
            return await context.send(f"Booking made successfully for {found['first_name']}!")
        



async def setup(bot: Bot):
    await bot.add_cog(
        Site(
            bot,
            Logger('site', 'site.log')()
        )
    )

