import asyncio

HOST = '192.168.0.183'
PORT = '1410'


class User:

    def __init__(self):
        self.username = None
        self.password = None
        self.reader = None
        self.writer = None
        self.callback = lambda msg: None

    async def log_in(self, username, password):
        self.username = username
        self.password = password
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
        self.writer.write(f'{self.username}\n{self.password}\n'.encode('UTF-8'))
        await self.writer.drain()
        asyncio.create_task(self.reader_job())

    def write_message(self, addressee, msg):
        self.writer.write(f'{addressee}\n{msg}\x00'.encode('UTF-8'))

    async def read_message(self):
        msg = await self.reader.readuntil(b'\x00')
        return msg.decode('UTF-8')

    async def log_out(self):
        self.writer.close()
        self.writer.wait_closed()

    async def reader_job(self):
        while not self.reader.at_eof():
            await self.writer.drain()
            msg = await self.read_message()
            self.callback(msg)


async def main():
    user = User('leo', 'kociak69')
    await user.log_in()
    await asyncio.gather(*asyncio.all_tasks())

if __name__ == '__main__':
    asyncio.run(main())
