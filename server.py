import asyncio
from logging import getLogger, basicConfig, INFO

from users_database import UsersDatabase

basicConfig(level=INFO)
logger = getLogger(__name__)


class ActiveUsers:

    def __init__(self):
        self.users = dict()
        self.database = UsersDatabase()

    def log_in(self, username, password, user_writer):
        if self.database.login_user(username, password):
            self.users[username] = user_writer
            return True
        else:
            return False

    def log_out(self, username):
        self.users.pop(username)


class MyServer:

    def __init__(self, host='127.0.0.1', port=2137):
        self.host = host
        self.port = port
        self.active_users = ActiveUsers()
        self.users = self.active_users.users

    # def random_txt(self):
    # return './some_trash/' + ''.join(choices('qwertyuiopasdfghjklzxcvbn', k=10)) + '.txt'

    async def send_mail(self, reader):
        while not reader.at_eof():
            addressee = (await reader.readline())[:-1].decode('UTF-8')
            print(addressee)
            if addressee == '':
                continue
            addressee_writer = self.users[addressee]
            msg = await reader.readuntil(b'\x00')
            print(msg)
            addressee_writer.write(msg)
            await addressee_writer.drain()

    async def handler(self, reader, writer):
        with open('./miau.txt', 'r') as welcome_file:
            welcome = welcome_file.read()
        writer.write(welcome.encode('UTF-8') + b'\x00')
        await writer.drain()
        username = (await reader.readline())[:-1].decode('UTF-8')
        password = (await reader.readline())[:-1].decode('UTF-8')
        logger.info(f'Username {username} connected with password "{password}"')

        if not self.active_users.log_in(username, password, writer):
            writer.close()
            print("Wrong password, closing connection")
            await writer.wait_closed()
            print("Connection closed")
            return
        try:
            await self.send_mail(reader)
        except ConnectionResetError:
            logger.error(f'User {username} disconnected.')
        self.active_users.log_out(username)

    async def server(self):
        serv = await asyncio.start_server(self.handler, host='127.0.0.1', port=1410)
        async with serv:
            await serv.serve_forever()


my_server = MyServer()
asyncio.run(my_server.server())
