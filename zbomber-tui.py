from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, Button, \
TextBox, Widget, FileBrowser, Label, DropdownList, PopUpDialog, RadioButtons
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from random import randint
from time import sleep
import zbomber as zb
import sys

# theme for the views
# monochrome
theme = 'green'

# validator for checking if s is a postive number
def is_num(s):
    try:
        x = int(s)
        return x >= 0
    except:
        return False

class SettingsView(Frame):
    def __init__(self, screen, zbomber):
        super(SettingsView, self).__init__(screen, 
                                           screen.height,
                                           screen.width,
                                           hover_focus=True, 
                                           on_load=self.reload_values,
                                           title="ZBomber Settings")
        # bot controller
        self.zbomber = zbomber

        # color
        self.set_theme(theme)

        # input num, and links
        layout = Layout([5])
        self.add_layout(layout)
        num_bots_inp = Text("Number of Bots:", "num_bots", validator=is_num)
        num_bots_inp.value = "4"
        layout.add_widget(num_bots_inp)
        layout.add_widget(Text("Zoom Link:", "link"))
        zid = Text("Meeting ID (optional):", "zid")
        layout.add_widget(zid)
        pwd = Text("Meeting Password (optional):", "pwd")
        layout.add_widget(pwd)

        # username list
        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout2)
        layout2.add_widget(Label("Username List:"))
        # only shows txt files
        browser = FileBrowser(8, '.', name="uname_file", file_filter=".*.txt$")
        layout2.add_widget(browser)

        # will enable once implemented
        browser.disabled = True
        pwd.disabled = True
        zid.disabled = True

        # navigation
        layout3 = Layout([100])
        self.add_layout(layout3)
        layout3.add_widget(Divider())
        layout3.add_widget(Button("Menu", self.menu_view), 0)

        # what this?
        self.fix()
        return

    # reload previously set values
    def reload_values(self):
        self.data = self.zbomber.tui_data
        return

    # pass input to zbomber then switch to menu
    def menu_view(self):
        self.save()
        inp = self.data
        try:
            self.zbomber.num_bots = int(inp['num_bots'])
        except:
            self.zbomber.num_bots = 1
        self.zbomber.link = inp['link']
        self.zbomber.zid = inp['zid']
        self.zbomber.pwd = inp['pwd']
        self.zbomber.uname_file = inp['uname_file']
        self.zbomber.tui_data = inp
        self.zbomber.refresh_bots()
        raise NextScene("Menu")

class BotListView(Frame):
    def __init__(self, screen, zbomber):
        super(BotListView, self).__init__(screen, 
                                           screen.height,
                                           screen.width,
                                           hover_focus=True, 
                                           on_load=self.update_list,
                                           title="Bot List")
        self.zbomber = zbomber
        self.set_theme(theme)

        # bot list
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._list_view = ListBox(Widget.FILL_FRAME, self.get_list(),
                            name="bot_index", add_scroll_bar=True)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())

        # navigation and editing
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Edit", self.bot_view), 0)
        layout2.add_widget(Button("Menu", self.menu_view), 1)
        self.fix()
        return

    # return a list of active bot names
    def get_list(self):
        active_bots = []
        unames = self.zbomber.get_unames()
        for i in range(len(unames)):
            active_bots.append((unames[i], i+1))
        return active_bots

    # updates the list of names on load
    def update_list(self):
        self._list_view.options = self.get_list()

    def bot_view(self):
        self.save()
        self.zbomber.curr_bot = self.data["bot_index"] - 1
        raise NextScene("Bot")

    def menu_view(self):
        self.save()
        raise NextScene("Menu")

class MenuView(Frame):
    def __init__(self, screen, zbomber):
        super(MenuView, self).__init__(screen, 
                                           screen.height,
                                           screen.width,
                                           hover_focus=True, 
                                           title="Menu")
        self.set_theme(theme)
        self.zbomber = zbomber

        # TODO space this better
        layout = Layout([100])
        self.add_layout(layout)
        self.add_padding(layout, screen)
        layout.add_widget(Button("Settings", self.settings_view))
        layout.add_widget(Label(""))
        layout.add_widget(Label(""))
        layout.add_widget(Button("Bots", self.bot_list_view))
        layout.add_widget(Label(""))
        layout.add_widget(Label(""))
        layout.add_widget(Button("Commands", self.commands_view))
        layout.add_widget(Label(""))
        layout.add_widget(Label(""))
        layout.add_widget(Button("Quit", self.quit))
        self.layout = layout
        self.fix()

    def add_padding(self, layout, screen):
        vert_pad = screen.height // 3
        for i in range(vert_pad):
            layout.add_widget(Label(""))
        return

    def settings_view(self):
        raise NextScene("Settings")

    def commands_view(self):
        raise NextScene("Commands")

    def bot_list_view(self):
        raise NextScene("Bot List")

    # bring up the quit popup
    def quit(self):
        buttons = ["No", "Yes"]
        # setting theme to global theme doesn't show text?
        self._scene.add_effect(PopUpDialog(self._screen, "Are you sure?", buttons, on_close=self.exit))
        return

    # end the program
    def exit(self, option):
        if option == 1:
            # destroy the bots, won't leave meetings
            self.zbomber.kill_all()
            raise StopApplication('User presed quit')
        else:
            return

class BotView(Frame):
    def __init__(self, screen, zbomber):
        super(BotView, self).__init__(screen, 
                                           screen.height,
                                           screen.width,
                                           hover_focus=True, 
                                           on_load=self.load_bot,
                                           title="Bot")
        self.set_theme(theme)
        self.zbomber = zbomber
        self._screen = screen

        # bot info
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Text("Bot Name:", "uname"))
        # can't figure out updating status labels without crashing?

        # individual bot commands
        layout2 = Layout([1, 99], fill_frame=True)
        self.add_layout(layout2)
        layout2.add_widget(Button("Start", self.start))
        layout2.add_widget(Button("Prepare for Bombing", self.prepare))
        layout2.add_widget(Button("Join Meeting", self.join))
        layout2.add_widget(Button("Leave Meeting", self.leave))
        layout2.add_widget(Button("Kill", self.kill))
        # send message?

        # navigation
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Divider())
        layout2.add_widget(Divider(), 1)
        layout2.add_widget(Button("Cancel", self.cancel), 0)
        layout2.add_widget(Button("Save", self.save_bot), 1)
        self.fix()
        return

    # get information on selected bot
    def load_bot(self):
        self.bot = self.zbomber.get_curr_bot()
        values = {"uname": self.bot.uname}
        self.data = values
        return

    def start(self, opt=-1):
        if opt == 0:
            return
        elif opt == 1:
            self.bot.start()
        buttons = ["No", "Yes"]
        msg = "Start " + self.bot.uname + "?"
        if opt == -1:
            self._scene.add_effect(PopUpDialog(self._screen, msg, buttons, on_close=self.start))
        return

    def prepare(self, opt=-1):
        if opt == 0:
            return
        elif opt == 1:
            self.bot.meeting_init()
        buttons = ["No", "Yes"]
        msg = "Prepare for Bombing?"
        if opt == -1:
            self._scene.add_effect(PopUpDialog(self._screen, msg, buttons, on_close=self.prepare))
        return

    def join(self, opt=-1):
        if opt == 0:
            return
        elif opt == 1:
            self.bot.join_meeting()
        buttons = ["No", "Yes"]
        msg = "Join Meeting?"
        if opt == -1:
            self._scene.add_effect(PopUpDialog(self._screen, msg, buttons, on_close=self.join))
        return

    def leave(self, opt=-1):
        if opt == 0:
            return
        elif opt == 1:
            self.bot.leave()
        buttons = ["No", "Yes"]
        msg = "Leave Meeting?"
        if opt == -1:
            self._scene.add_effect(PopUpDialog(self._screen, msg, buttons, on_close=self.leave))
        return

    def kill(self, opt=-1):
        if opt == 0:
            return
        elif opt == 1:
            self.bot.die()
        buttons = ["No", "Yes"]
        msg = "Kill " + self.bot.uname + "?"
        if opt == -1:
            self._scene.add_effect(PopUpDialog(self._screen, msg, buttons, on_close=self.kill))
        return

    # go back to bot list view without saving
    def cancel(self):
        self.save()
        self.zbomber.tmp = self.data
        raise NextScene("Bot List")

    # save information and return to list
    def save_bot(self):
        self.save()
        bot = self.zbomber.get_curr_bot()
        bot.uname = self.data["uname"]
        raise NextScene("Bot List")

class CommandsView(Frame):
    def __init__(self, screen, zbomber):
        super(CommandsView, self).__init__(screen, 
                                           screen.height,
                                           screen.width,
                                           hover_focus=True, 
                                           on_load=self.load_defaults,
                                           title="Commands")
        self.zbomber = zbomber

        # command buttons
        self.set_theme(theme)
        layout = Layout([100])
        self.add_layout(layout)
        self.spam_count = Text("Number of Messages (spam):", "num_msgs", validator=is_num)
        self.spam_msg = TextBox(5, "Spam Message:", "spam_msg")
        cmds = ["Start Bots", "Prepare for Bombing", "Join", "Spam", "Retreat", "Kill Bots"]
        cmd_opts = []
        for i in range(len(cmds)):
            cmd_opts.append((cmds[i], i+1))
        layout.add_widget(RadioButtons(cmd_opts, name="cmd", on_change=self.update_widgets))

        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout2)
        layout2.add_widget(self.spam_count)
        layout2.add_widget(self.spam_msg)

        # navigation and execution
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Divider())
        layout2.add_widget(Divider(), 1)
        layout2.add_widget(Button("Execute", self.confirm_cmd), 0)
        layout2.add_widget(Button("Menu", self.menu_view), 1)

        self.fix()
        return

    # enable/disable widgets based on selected command
    def update_widgets(self):
        self.save()
        if 'cmd' in self.data and self.data['cmd'] == 4:
            self.spam_count.disabled = False
            self.spam_msg.disabled = False
        else:
            self.spam_count.disabled = True
            self.spam_msg.disabled = True


    # load default values into fields
    def load_defaults(self):
        self.data = {'cmd': 1, 'num_msgs': '50', 
                     'spam_msg': ['FROM THE RIVER TO THE SEA', 
                                  'PALESTINE WILL BE FREE']
                     }
        return

    # read radio button and execute
    def execute_cmd(self, opt):
        if opt == 0:
            return
        # radio buttons starts index at 1
        self.save()
        data = self.data
        if data['cmd'] == 1:
            self.zbomber.start_bots()
        elif data['cmd'] == 2:
            self.zbomber.prepare_bots()
        elif data['cmd'] == 3:
            self.zbomber.join_all()
        elif data['cmd'] == 4:
            try:
                num_msgs = int(data['num_msgs'])
            except:
                msg = "Input a valid number!"
                buttons = ["OK"]
                self._scene.add_effect(PopUpDialog(self._screen, msg, buttons))
                return
            spam_msg = ' '.join(data['spam_msg'])
            self.zbomber.spam(spam_msg, num_msgs)
        elif data['cmd'] == 5:
            self.zbomber.retreat()
        elif data['cmd'] == 6:
            self.zbomber.kill_all()
        return

    # asks for confirmation before executing cmd
    def confirm_cmd(self):
        self.save()
        opt = self.data['cmd']
        buttons = ["No", "Yes"]
        msg = ""
        if opt == 1:
            msg = "Start Bots?"
        elif opt == 2:
            msg = "Prepare for Bombing?"
        elif opt == 3:
            msg = "Join Meeting?"
        elif opt == 4:
            msg = "Start Spamming?"
        elif opt == 5:
            msg = "Retreat?"
        elif opt == 6:
            msg = "Kill All Bots?"
        self._scene.add_effect(PopUpDialog(self._screen, msg, buttons, on_close=self.execute_cmd))
        return

    def menu_view(self):
        raise NextScene("Menu")

# render the scenes homie
def render(screen, scene, zbomber):
    scenes = [
            Scene([SettingsView(screen, zbomber)], -1, name="Settings"),
            Scene([BotListView(screen, zbomber)], -1, name="Bot List"),
            Scene([MenuView(screen, zbomber)], -1, name="Menu"),
            Scene([BotView(screen, zbomber)], -1, name="Bot"),
            Scene([CommandsView(screen, zbomber)], -1, name="Commands")
            ]
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)
    return

def main():
    zbomber = zb.ZBomber()

    # more rendering shit
    last_scene = None
    while True:
        try:
            Screen.wrapper(render, catch_interrupt=True, arguments=[last_scene, zbomber])
            # testing
            print('zbomber.tmp', zbomber.tmp)
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

if __name__ == '__main__':
    main()

