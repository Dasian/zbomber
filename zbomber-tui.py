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
        nums = []
        for i in range(1, 11):
            nums.append((str(i),i))
        layout.add_widget(DropdownList(nums, label="Number of Bots:", name="num_bots"))
        layout.add_widget(Text("Zoom Link:", "link"))
        layout.add_widget(Text("Meeting ID (optional):", "zid"))
        layout.add_widget(Text("Meeting Password (optional):", "pwd"))

        # username list
        layout2 = Layout([100], fill_frame=True)
        self.add_layout(layout2)
        layout2.add_widget(Label("Username List:"))
        # only shows txt files
        browser = FileBrowser(8, '.', name="uname_file", file_filter=".*.txt$")
        browser.disabled = False
        layout2.add_widget(browser)

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
        self.zbomber.num_bots = inp['num_bots']
        self.zbomber.link = inp['link']
        self.zbomber.zid = inp['zid']
        self.zbomber.pwd = inp['pwd']
        self.zbomber.uname_file = inp['uname_file']
        self.zbomber.tui_data = inp
        raise NextScene("Menu")

class BotListView(Frame):
    def __init__(self, screen, zbomber):
        super(BotListView, self).__init__(screen, 
                                           screen.height,
                                           screen.width,
                                           hover_focus=True, 
                                           on_load=self.get_list,
                                           title="Bot List")
        self.zbomber = zbomber
        self.set_theme(theme)

        self._list_view = ListBox(Widget.FILL_FRAME, self.get_list(),
                            name="bots", add_scroll_bar=True)

        # bot list
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
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

    def bot_view(self):
        raise NextScene("Bot")

    def menu_view(self):
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

# TODO have this do something
class BotView(Frame):
    def __init__(self, screen, zbomber):
        super(BotView, self).__init__(screen, 
                                           screen.height,
                                           screen.width,
                                           hover_focus=True, 
                                           on_load=self.get_bot,
                                           title="Bot")
        self.set_theme(theme)

        # bot info
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Bot Name:", "bot name"))
        # is active?
        # current activity?

        # navigation
        layout2 = Layout([100, 1])
        self.add_layout(layout2)
        layout2.add_widget(Divider())
        layout2.add_widget(Button("Back", self.bot_list_view), 0)
        layout2.add_widget(Button("Menu", self.menu_view), 1)
        self.fix()
        return

    # TODO get information for selected bot
    def get_bot(self):
        return

    def bot_list_view(self):
        raise NextScene("Bot List")

    def menu_view(self):
        raise NextScene("Menu")

class CommandsView(Frame):
    def __init__(self, screen, zbomber):
        super(CommandsView, self).__init__(screen, 
                                           screen.height,
                                           screen.width,
                                           hover_focus=True, 
                                           title="Commands")
        self.zbomber = zbomber

        # command buttons
        # TODO add spam message and number
        self.set_theme(theme)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        cmds = ["Create Bots", "Prepare for Bombing", "Join", "Spam", "Retreat"]
        cmd_opts = []
        for i in range(len(cmds)):
            cmd_opts.append((cmds[i], i+1))
        layout.add_widget(RadioButtons(cmd_opts, name="cmd"))

        # navigation and execution
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Divider())
        layout2.add_widget(Divider(), 1)
        layout2.add_widget(Button("Execute", self.execute_cmd), 0)
        layout2.add_widget(Button("Menu", self.menu_view), 1)

        self.fix()
        return

    # read radio button and execute
    # possible ask for confirmation?
    def execute_cmd(self):
        self.save()
        # radio buttons starts index at 1
        data = self.data
        if data['cmd'] == 1:
            self.zbomber.create_bots()
        elif data['cmd'] == 2:
            self.zbomber.init_bots()
        elif data['cmd'] == 3:
            self.zbomber.join_all()
        elif data['cmd'] == 4:
            self.zbomber.spam('FREE PALESTINE!!', 10)
        elif data['cmd'] == 5:
            self.zbomber.retreat()
        return

    def menu_view(self):
        raise NextScene("Menu")

# render the scenes homie
def demo(screen, scene, zbomber):
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
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene, zbomber])
            # testing
            print('zbomber.tui_data', zbomber.tui_data)
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == '__main__':
    main()

