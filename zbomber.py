from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
from time import sleep
import random

# zoom bot object
class ZBot():
    def __init__(self, uname='Satoru Gojo', link=None, zid=None, pwd=None):
        self.uname = uname
        self.link = link
        self.zid = zid
        self.pwd = pwd
        self.cookie_clicked = False
        self.generate_driver()

    # creates and sets the selenium browser driver
    def generate_driver(self):
        chrome_options = Options()
        # preventing popup (attempt) (update: attempt failed)
        prefs = {
            "profile.default_content_setting_values.notifications" : 2,
            "profile.sandbox_external_protocol_blocked": True,
            "external_protocol_dialog.show_always_open_checkbox": False,
        }
        chrome_options.add_experimental_option("prefs",prefs)
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)
        # used to wait for elements to load before trying to access them
        wait_time = 5
        self.wait = WebDriverWait(self.driver, wait_time)
        return

    # TODO modify and test this, doesn't actually work im guessing
    # connect using id and password
    def id_connect(self):
        # ? Opening the website
        self.driver.get(
            f"https://zoom.us/wc/{self.zid}/join?from=join&_x_zm_rtaid=ws81SA1uSGuB2O6_Sekbbg.1690523013218.d0e8a870b0195ee064d41de484bdd657&_x_zm_rhtaid=508"
        )

        # ? Entering password
        pwd_box = driver.find_element(By.ID, "input-for-pwd")
        pwd_box.clear()
        pwd_box.send_keys(self.pwd)
        return

    # TODO have this work on windows (tested on linux)
    # presses enter to get rid of browser zoom prompt
    # browser prompts can't be handled by selenium, only by the operating system
    def dismiss_popup(self):
        sleep(.5)
        keyboard = Controller()
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        return

    # prepare the bot up until joining the meeting
    def meeting_init(self):

        # open the zoom meeting in browser
        if self.link != None:
            self.driver.get(self.link)
        elif self.zid != None and self.pwd != None:
            self.id_connect()
        else:
            print('missing credentials, stopping...')
            return False

        # removing zoom browser popup
        self.dismiss_popup()

        # remove cookie banner
        if not self.cookie_clicked:
            cookie_xpath = '/html/body/div[4]/div[3]/div/div/div[1]/button'
            cookie = self.wait.until(EC.element_to_be_clickable((By.XPATH, cookie_xpath)))
            cookie.click()
            self.cookie_clicked = True

        # click launch meeting to reveal browser link
        join_xpath = '/html/body/div[2]/div[2]/div/div[1]/div'
        join = self.wait.until(EC.element_to_be_clickable((By.XPATH, join_xpath)))
        join.click()

        # remove zoom browser popup AGAIN
        self.dismiss_popup()

        # click join meeting through the browser
        join_browser = '/html/body/div[2]/div[2]/div/div[2]/h3[2]/span/a'
        join = self.wait.until(EC.element_to_be_clickable((By.XPATH, join_browser)))
        join.click()

        # switching to iframe to access fillable elements
        iframe_xpath = '/html/body/div[1]/div[1]/div/iframe'
        iframe = self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_xpath)))

        # enter name
        name_xpath = '/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/div/input'
        name = self.wait.until(EC.element_to_be_clickable((By.XPATH, name_xpath)))
        name.clear()
        name.send_keys(self.uname)

    # join the meeting and open the chat window
    def join_meeting(self):

        # join meeting
        join_xpath = '/html/body/div[2]/div[2]/div/div[1]/div/div[2]/button'
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, join_xpath)))
        button.click()

        # return driver frame to parent (might not be necessary? idk idc)
        self.driver.switch_to.default_content()

        # opens the chat window
        iframe_xpath = '/html/body/div[1]/div[2]/div/iframe'
        iframe = self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_xpath)))
        try:
            # chat button visible
            chat_btn_xpath = '//*[@id="foot-bar"]/div[2]/div[3]/div/button'
            chat_btn = self.driver.find_element(By.XPATH, chat_btn_xpath)
            chat_btn.click()
            chat_btn.click()
        except:
            # chat button not visible, open chat from more
            # faster wait
            wait = WebDriverWait(self.driver, 2)
            more_xpath = '//div[@feature-type="more"]'
            more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, more_xpath)))
            more_btn.click()
            more_btn.click()

            # chat button from more
            # sometimes more needs 1 click, sometimes it needs 2, idk
            chat_btn_xpath = '//span[contains(text(), "Chat")]'
            try:
                chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, chat_btn_xpath)))
                chat_btn.click()
            except:
                more_btn.click()
                chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, chat_btn_xpath)))
                chat_btn.click()
        return

    # send a message in chat
    def send_chat(self, msg):
        try: 
            chat_xpath = '//*[@id="wc-container-right"]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]'
            chat_box = self.driver.find_element(By.XPATH, chat_xpath)
        except:
            chat_xpath = '//div[@contenteditable="true"]'
            chat_box = self.wait.until(EC.element_to_be_clickable((By.XPATH, chat_xpath)))
        chat_box.click()
        chat_box.send_keys(msg)
        chat_box.send_keys(Keys.ENTER)
        return

    # leave the current meeting
    def leave(self):
        # leave button is alwasys last?
        leave_xpath = '//div[@id="foot-bar"]/div[last()]/button'
        leave_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, leave_xpath)))
        leave_btn.click()
        leave_xpath = '//button[contains(text(), "Leave Meeting")]'
        leave_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, leave_xpath)))
        leave_btn.click()
        return

    # rejoin a meeting
    def rejoin(self):
        try:
            # if the browser doesn't exist just make a new one
            self.driver.close()
        finally:
            # generate a new name? or keep the same
            self.generate_driver()
            self.meeting_init()
            self.join_meeting()
            return

    # kill the browser
    def die(self):
        # attempt to leave?
        # kill browser
        try:
            self.driver.close()
        finally:
            return

    # TODO rename in meeting
    def rename(self):
        return

class ZBomber():
    def __init__(self, num_bots=1, link=None, zid=None, zpwd=None, uname_file=None):
        self.num_bots = num_bots
        self.link = link
        self.zid = zid
        self.zpwd = zpwd
        self.uname_file = uname_file
        self.bots = []

        # TODO get unames from file
        if uname_file == None or True:
            self.unames = ['Satoru Gojo', 'Joe Brandon', 'Hasan Piker', 'Kay Dot', 'Child Keem', 'Manny Heffley', 
                           'Heinz Doofenshmirtz', 'Elongated Muskrat', 'A'*50]

        # used for testing with tui
        self.tmp = None

    # create all bots and initializes bots
    # TODO reset bots when num_bots change
    def create_bots(self):
        print('starting create bots')

        if len(self.bots) < self.num_bots:
            print('adding bots')
            for i in range(len(self.bots), self.num_bots):
                uname = self.unames[i%len(self.unames)]
                bot = ZBot(uname=uname, link=self.link)
                self.bots.append(bot)
        else:
            print('killing bots')
            while len(self.bots) > self.num_bots:
                # kill the bot
                bot = self.bots.pop(len(self.bots)-1)
                bot.die()

    # get list of bot unames
    def get_unames(self):
        unames = []
        for bot in self.bots:
            unames.append(bot.uname)
        return unames
    
    # prepares all bots to join the meeting
    def init_bots(self):
        for bot in self.bots:
            bot.meeting_init()

    # have all bots join the meeting
    def join_all(self):
        for bot in self.bots:
            bot.join_meeting()

    # repeatedly send a message from all bots
    def spam(self, msg, num_msgs=50):
        for i in range(num_msgs):
            try:
                self.bots[i%self.num_bots].send_chat(msg)
            except:
                # bot was kicked? maybe keep track and remove from list/restart
                # could probably do this in a subprocess to keep the spam going,
                # but the need for enter to be pressed by the os could make things
                # complicated
                self.bots[i%self.num_bots].rejoin()
                continue
        return

    # have all bots leave the meeting
    def retreat(self):
        for bot in self.bots:
            try:
                bot.leave()
            except:
                print(bot.uname, "can't retreat!")
                continue
        return
    
    def kill_all(self):
        for bot in self.bots:
            bot.die()

def main():
    # TODO 
    # implement id/pass zoom meetings
    # deal with waiting rooms
    # add ability for bots to sign up with temp emails
    # get vars from user input
    #   maybe tui mode and cmdline mode
    # better error handling
    # add more bot orders and make them more efficient
    #   send orders through threads maybe

    # set the target link
    link = 'https://us05web.zoom.us/j/86760623751?pwd=bDKOH7gaQCkYTnNL3BZr8APRg9s31S.1'
    num_bots = 1
    startup_time = 3

    if link == '':
        print('set the invite link in main')
        return

    # note that if the window is too small, it might make clicking buttons impossible (for some reason)
    # only a problem with me i think bc bspwm is not normal
    print('zbomber starting in',startup_time,'seconds with',num_bots,'bots. prepare yourself...')
    sleep(startup_time)

    # initializing bot controller
    zbomber = ZBomber(num_bots=num_bots, link=link)

    # joins meeting and opens chat window
    zbomber.create_bots()
    zbomber.init_bots()
    zbomber.join_all()

    # for now set your orders here
    # this sends 30 total messages split between all bots and then they all leave
    zbomber.spam('FREE PALESTINE', 10)
    zbomber.retreat()

    print('increasing bots to 2')
    zbomber.num_bots = 2
    zbomber.create_bots()
    zbomber.init_bots()
    zbomber.join_all()
    zbomber.spam('FREE PALESTINE 2', 10)
    zbomber.retreat()

    print('decreasing bots to 1')
    zbomber.num_bots = 1
    zbomber.create_bots()
    zbomber.init_bots()
    zbomber.join_all()
    zbomber.spam('FREE PALESTINE 3', 10)
    zbomber.retreat()

    return

if __name__ == "__main__":
    main()
