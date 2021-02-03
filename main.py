import asyncio
from argparse import ArgumentParser

import urwid

from client import User
from user_interface import LoginMenu, MainWidget

# Order of imports is important, first you import default libraries (e.g. asyncio, argparse, and so on)
# Then after empty line - 3rd party libraries, in this case urwid
# Last imports are always internal files from project.


def main(args):
    # First we crate server.
    user_client = User()

    main_widget = MainWidget(None)
    login_menu = LoginMenu(user_client, main_widget)
    main_widget.change_main_widget(login_menu)

    # Urwid-asyncio mumbo jumbo, tl;dr is that
    # you need to run both urwid interface and server backend
    # at the same time so first you initialize (but not start)
    # Urwid loop
    aloop = asyncio.get_event_loop()
    ev_loop = urwid.AsyncioEventLoop(loop=aloop)
    loop = urwid.MainLoop(main_widget, event_loop=ev_loop)

    # And here you specify that alongside urwid you run server
    # All is set up - here execution starts
    loop.run()


if __name__ == '__main__':
    # Here we define options that can be passed via console while running this app
    # All arguments defined here are optional because we specified default values
    argument_parser = ArgumentParser(description='First stage of simple web chat')
    argument_parser.add_argument('--host', help='On which address should it run', default='127.0.0.1')
    argument_parser.add_argument('--port', help='On which port should it run', default=2137)

    # Here parsing happens, if user provides wrong args, it breaks here.
    args = argument_parser.parse_args()

    # We pass args to the main function
    main(args)
