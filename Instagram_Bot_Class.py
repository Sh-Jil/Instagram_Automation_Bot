from time import sleep, perf_counter
from random import uniform
class instabot:
    """The __init__ function has been revised for InstaBot 2.2"""

    def __init__(self, usrnm="", psw="", login=True, limitperhour=5):
        if login:
            from selenium import webdriver
            # from selenium.webdriver.common.action_chains import ActionChains
            from datetime import datetime

            self.browser = webdriver.Chrome(r"chromedriver\chromedriver.exe")

            #We have to create a separate ActionChains object each time we need to use ActionChains. This is due to
            # the fact that the send_keys function under ActionChains has a bug that can only be fixed by making a
            # different object each time ActionChains is used

            #self.thingtodo = ActionChains(self.browser)
            self.usrnm = usrnm
            self.psw = psw
            self.scrollsleep=1


            #The actiondone variable stores the amount of actions done in order to make sure
            #the limit per hour is not surpassed.
            self.actionsdone = 0
            self.limitperhour = limitperhour
            self.benchmark_time = datetime.now()
            self.override=False

            self.added_sleep=0
            self.interval=0

            self.loop_time_out=10 #How many seconds the program will wait until the loop times out

            self.dm_hashes={}
        else:
            self.usrnm=self.usrnm

    def wait_for_page(self):
        """This function waits for the page to load."""
        page_main = self.browser.find_elements_by_css_selector("html")
        started=perf_counter()

        while len(page_main) < 1 and perf_counter()-started<self.loop_time_out: #wait
            page_main = self.browser.find_elements_by_css_selector("html") #update to see if it has loaded

        sleep(self.added_sleep)
        if len(page_main)<1:
            return False

        else:
            return True
    def broken_link(self,wait_for=None):
        """This function checks to see if the visited website is a broken link. Sometimes the bot will try to visit a user, but the user has closed that account.
        In that case, in order to avoid an infinite loop, we first check to see if the site is valid."""
        self.wait_for_page()
        if wait_for==None:
            wait_for=self.loop_time_out

        broken=self.browser.find_elements_by_css_selector("html")
        start=perf_counter()

        while perf_counter()-start<wait_for and len(broken)<1:
            self.browser.find_elements_by_css_selector("html")

        if "isn't available" in broken[0].text:
            return True
        else:
            return False

    def signin(self):
        """This function logs in to the account specified. The signin function also closes the 'turn notifications on' window"""


        from random import randint,uniform
        from selenium.webdriver.common.keys import Keys
        from time import sleep

        self.browser.get("https://www.instagram.com/")
        sleep(randint(3, 5))

        usernameplace = self.browser.find_elements_by_name("username")
        while len(usernameplace) < 1:
            usernameplace = self.browser.find_elements_by_name("username")

        usernameplace[0].click()
        sleep(uniform(0,1))
        usernameplace[0].send_keys(self.usrnm)
        sleep(uniform(0,1))

        passwordplace = self.browser.find_elements_by_name("password")
        while len(passwordplace) < 1:
            passwordplace = self.browser.find_elements_by_name("password")
        sleep(uniform(0,1.5))

        passwordplace[0].send_keys(self.psw)
        sleep(uniform(0,1.5))
        passwordplace[0].send_keys(Keys.ENTER)
        usernameplace = self.browser.find_elements_by_name("username")

        #WE WAIT UNTIL THE SITE HAS LOADED OUR PAGE:
        while len(usernameplace) > 0:
            usernameplace = self.browser.find_elements_by_name("username")
        sleep(1)

        if self.browser.current_url == "https://www.instagram.com/accounts/onetap/?next=%2F":
            options = self.browser.find_elements_by_class_name("sqdOP")
            while len(options) < 2:
                options = self.browser.find_elements_by_class_name("sqdOP")
            sleep(randint(1, 2))
            options[1].click()

        notnow = self.browser.find_elements_by_class_name("HoLwm")

        while len(notnow) < 1:
            notnow = self.browser.find_elements_by_class_name("HoLwm")
        sleep(randint(0, 2))
        notnow[0].click()



