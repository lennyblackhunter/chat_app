import urwid
import asyncio as aio
import sys


class MainWidget(urwid.WidgetWrap):

    def __init__(self, main_widget):
        super().__init__(main_widget)

    def change_main_widget(self, new_main_widget):
        self._w = new_main_widget


# This represents graphical chat that interacts with user
# See that the connection with server is minimal, namely we're using
# just two functions to create it - set_output and write_msg
class ChatWindow(urwid.WidgetWrap):

    def __init__(self, user_client):
        self.history = urwid.Text('')
        input_box = urwid.Edit(multiline=True)
        user_client.callback = lambda txt: self.append_msg(txt)

        def _callback(widget, oldtext):
            newtext = input_box.edit_text

            # If user pressed enter, write using chat_server and append to history
            if newtext and newtext[-1] == '\n':
                user, msg = newtext.split(':')
                user_client.write_message(user, msg)
                new_text = self.history.text
                if new_text:
                    new_text += '\n'
                self.history.set_text(new_text + input_box.edit_text[:-1])
                input_box.edit_text = ""

        # The meaning of this line is - every time something changes in edit box
        # run function _callback
        urwid.connect_signal(input_box, 'postchange', _callback)
        self.pile = urwid.Pile([self.history, input_box])
        super().__init__(self.pile)

    def append_msg(self, txt):
        self.history.set_text(self.history.text + f"\nother user: {txt}")


class LoginMenu(urwid.WidgetWrap):

    def __init__(self, user, main_widget):
        self.menu_box = self.menu('koty')
        self.user = user
        self.main_widget = main_widget
        super().__init__(self.menu_box)

    def menu(self, title):
        body = [urwid.Text(title, align='center'), urwid.Divider()]
        username = urwid.Edit(caption='username: ')
        password = urwid.Edit(caption='password: ')
        body += [username, password]

        def _callback():
            user = username.get_text()[0][10:]
            pswd = password.get_text()[0][10:]
            aio.create_task(self.user.log_in(user, pswd))
            chat_window = ChatWindow(self.user)
            whole_window = urwid.Filler(chat_window, valign='bottom')
            self.main_widget.change_main_widget(whole_window)

        button = urwid.Padding(urwid.Button('ok', on_press=_callback), align='center', min_width=6, width=6)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))


if __name__ == '__main__':
    main = urwid.Padding(LoginMenu(), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                        align='center', width=('relative', 60),
                        valign='middle', height=('relative', 60),
                        min_width=20, min_height=9)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
