from time import sleep, perf_counter
from random import uniform
class instabot:
    """The instabot class has been revised for InstaBot 2.4"""

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

    
        def check_action(self):
        """This function makes sure that you have met all the requirements to execute an actions"""
        if self.override == True or self.actionsdone <= self.limitperhour:
            return True
        else:
            return False

    def number_of_posts_followers_and_following(self, forwho):
        """returns an array with 3 integers in it. The format is : [numberofposts, followernumber, followingnumber]"""
        from Static_Functions import Filtering_Information
        from time import perf_counter

        #It is debatable if opening a url is counted as an action. I am not going to include it as an action

        w = "https://www.instagram.com/" + forwho + "/"
        if self.browser.current_url != w:
            self.browser.get(w)

        if self.broken_link():
            return False
        #The stats variable is a list which stores the follower, following and post number as
        #integers in the form [ posts, followers, following]
        try:
            stats = self.browser.find_elements_by_class_name("-nal3")
        except:
            stats = [0]

        start=perf_counter()
        now=perf_counter()
        # Waiting for the page to load:
        while len(stats) < 3 and now-start<self.loop_time_out:
            try:
                stats = self.browser.find_elements_by_class_name("-nal3")

            except:
                stats = [0]
            now=perf_counter()

        if now-start>=self.loop_time_out:
            if self.broken_link():
                return False
            elif self.broken_link(): #check one more time
                return False
            else:
                return self.number_of_posts_followers_and_following(forwho=forwho)

        numberofposts = stats[0].text
        followernumber = stats[1].text
        followingnumber = stats[2].text

        numberofposts = Filtering_Information.filter_stat(numberofposts)
        followernumber = Filtering_Information.filter_stat(followernumber)
        followingnumber = Filtering_Information.filter_stat(followingnumber)


        return [numberofposts, followernumber, followingnumber]

    
    
        def scrolldown(self, numpeople, classname="FPmhX"):
        """This function is made to scroll down the list of followers/following for a person. It can be tweaked to
        become a regular automatic scroller.
        After scrolling all the way down, it return an array of the people that it has scrolled through."""
        try:
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains

            thingtodo = ActionChains(self.browser) #we need to create a separate action chains object due to the bugs
            # with the send_keys function
            
            #The tab key is pressed multiple times to make sure that the window is in focus.
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()
            thingtodo.send_keys(Keys.TAB).perform()


            now = self.browser.find_elements_by_class_name(classname)
            while len(now) <= numpeople - 4: #scrolling until all of the elements have loaded
                now = self.browser.find_elements_by_class_name(classname) #updating the variable that stores the elements
                thingtodo.send_keys(Keys.END).perform()
                sleep(self.scrollsleep)

                
            
            #converting every element into text:
            now = self.browser.find_elements_by_class_name(classname)
            final = []
            for i in now:
                final.append(i.text)


            return final

        except:
            #If something goes wrong in the process, try the function again.
            return self.scrolldown(numpeople=numpeople,classname=classname)

    def follower_following_int(self, person):
        """This function returns an array with two integers (the number of people following the person,
        and the number of people that the person is following). [followernumber,followingnumber]."""


        if self.check_action()==False:
            return False

        w="https://www.instagram.com/" + person + "/" #creating the url for person
        if self.browser.current_url!=w:
            self.browser.get(w)

        if self.broken_link():
            return False
        sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

        stats = self.number_of_posts_followers_and_following(person)
        followers = stats[1]
        following = stats[2]
        return [followers,following]
    
    
        def getstat(self, person, followersorfollowing,how_many_people=None):

        """This function will return an array of people."""
        w = "https://www.instagram.com/" + person
        self.browser.get(w)
        from time import sleep

        if how_many_people==None:

            followers_and_following=self.follower_following_int(person=person)
            followers = followers_and_following[0]
            following = followers_and_following[1]
        else:
            followers=how_many_people
            following=how_many_people

        # The buttons variable stores the buttons in the form : [posts, followers, following]
        # The while loop waits for the 3 buttons to load
        buttons = self.browser.find_elements_by_class_name("-nal3")
        while len(buttons) < 3:
            buttons = self.browser.find_elements_by_class_name("-nal3")

        sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

        if followersorfollowing == "followers":
            buttons[1].click()

            return self.scrolldown(followers, "FPmhX")

        elif followersorfollowing == "following":
            buttons[2].click()

            return self.scrolldown(following, "FPmhX")

        else:
            return False

    def findwhohasnotfollowedback(self, who, write_to_document=True, followers=None, following=None):
        """This function finds the list of people who have not followed back for any given person."""
        import os
        from Static_Functions import Writing_Analysis_Files

        if following is None:
            following = []
        if followers is None:
            followers = []

        if followers==[]:
            followers = self.getstat(who, "followers")
            self.browser.get("https://www.instagram.com/" + who)
        if followers == False:
            return False

        if following==[]:
             following = self.getstat(who, "following")
        if following == False:
            return False

        no_follow_back = []

        for i in following:
            if i not in followers:
                no_follow_back.append(i)
        original=os.getcwd()

        os.chdir(Writing_Analysis_Files.path)
        peopledone = os.listdir(os.getcwd())
        isthere = False
        for i in peopledone:

            if i == who:
                isthere = True
                break
        update=[]
        for i in followers:
            if i not in [""," ","  ","   "]:
                update.append(i)
        followers = update

        new_update=[]
        for i in following:
            if i not in [""," ","  ","   "]:
                new_update.append(i)
        following=new_update

        os.chdir(original)
        if write_to_document:
            if not isthere:
                Writing_Analysis_Files.write_list_for_new_user(who, followers, following, no_follow_back)

            else:
                Writing_Analysis_Files.write_list_for_old_user(who, followers, following, no_follow_back)

        print(who,followers,following,no_follow_back)
        return no_follow_back

    def filter_celebrities(self,array_of_people,celeb_follower_limit=50000):
        update=[]
        for person in array_of_people:
            if self.follower_following_int(person)[0]<=celeb_follower_limit:
                update.append(person)

        return update

    @staticmethod
    def processperson(person):
        from Static_Functions import Processing_Stats
        return Processing_Stats.who_has_unfollowed(person)

    def follow(self, person):
        """The 'follow' function follows a person. """
        from time import perf_counter
        self.browser.get("https://www.instagram.com/" + person)
        self.wait_for_page()
        if self.broken_link():
            return False
        buttons = self.browser.find_elements_by_class_name("sqdOP")  # This is an array that will store only one html
        # element. We are storing it in an array so that we wait until the array is non-empty.

        if len(buttons) > 0:
            if "follow"!=buttons[0].text.lower():
                return False
        start=perf_counter()
        now=perf_counter()
        buttons = self.browser.find_elements_by_class_name("_5f5mN") #the buttons
        buttons_alternative=self.browser.find_elements_by_class_name("y3zKF") #The buttons if the account is private

        while len(buttons) < 1 and len(buttons_alternative)<1 and now-start<self.loop_time_out:
            buttons = self.browser.find_elements_by_class_name("_5f5mN")
            buttons_alternative = self.browser.find_elements_by_class_name("y3zKF")
            sleep(uniform(self.added_sleep, self.added_sleep + self.interval))
            now = perf_counter()

        sleep(uniform(self.added_sleep, self.added_sleep + self.interval))
        if len(buttons)<1:
            buttons=buttons_alternative

        if "follow" not in buttons[0].text.lower(): #making sure the buttons is the follow button
            return False
        if self.check_action()==False:
            return False


        # if now-start>=self.loop_time_out:
        #     if self.broken_link():
        #         return False
        #     elif self.broken_link(): #checking again
        #         return False
        #     else:
        #         return self.follow(person=person)


        buttons[0].click()
        self.browser.implicitly_wait(1)
        self.actionsdone += 1

        print("Followed " + str(person) )
        return True


    def unfollow(self, person):
        """The 'unfollow' function unfollows a given person. """
        from time import sleep
        from random import randint

        can_I=self.follow(person) #this function is enough to get you half the way. After this, all you need to do is
        # confirm that you want to unfollow the person

        if can_I==False:
            return False

        #Confirming that we want to unfollow:

        buttons = self.browser.find_elements_by_class_name("aOOlW")

        while len(buttons) < 1:
            buttons = self.browser.find_elements_by_class_name("BY3EC")
            sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

        #Here, we are just double checking to make sure everything is in order. A time out will be added to all while
        # loops to make sure they don't last forever.
        if len(buttons) > 1:
            sleep(randint(1, 2))
            buttons[0].click()

            return True
        else:
            return False
    def likeposts(self, person, howmany):
        """Since I rarely use the post liking function, this function has NOT been revised for Instabot2.1 . It does not
        count the amount of posts that have been liked."""

        from time import sleep
        from random import randint
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains

        thingtodo = ActionChains(self.browser) #we need to create a separate action chains object due to the bugs
        w="https://www.instagram.com/" + person + "/"
        if self.browser.current_url!=w:
            self.browser.get(w)

        if self.broken_link():
            return False

        sleep(randint(2, 5))

        posts = self.browser.find_elements_by_class_name("_9AhH0")
        # MAKING SURE THERE ARE ENOUGH POSTS SPECIFIED:
        n=0
        while len(posts) < howmany:
            thingtodo.send_keys(Keys.PAGE_DOWN).perform()
            posts = self.browser.find_elements_by_class_name("_9AhH0")
            n+=1
            if n%10==0:
                from selenium.webdriver.common.action_chains import ActionChains

                thingtodo = ActionChains(self.browser)  # we need to create a separate action chains object due to the bugs
            sleep(uniform(self.added_sleep, self.added_sleep + self.interval))

        posts[0].click()
        sleep(randint(1, 3))

        for i in range(0, howmany):
            sleep(randint(1, 4))
            stuff = self.browser.find_elements_by_class_name("_8-yf5")
            while len(stuff) < 8:
                stuff = self.browser.find_elements_by_class_name("_8-yf5")
            stuff[7].click()
            sleep(randint(1, 4))
            rightarrow = self.browser.find_element_by_class_name("coreSpritedRightPaginationArrow")
            rightarrow.click()
