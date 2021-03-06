

def followed_back(followers,following):
    """Returns a list of people who have followed back."""
    f_back=[]
    for person in following:
        if person in followers:
            f_back.append(person)
    return f_back

def no_follow_back(followers,following):
    """Returns a list of users that have not followed back"""
    nof=[]
    for person in following:
        if person not in followers:
            nof.append(person)
    return nof

def we_no_follow_back(followers,following):
    miss=[]
    for person in followers:
        if person not in following:
            miss.append(person)
    return miss


def filterfromstuff(string, list_to_filter_out):

    new = ""

    for i in string:
        if i not in list_to_filter_out:
            new += i

    return new

def findlist(file_name, username):
    """Reads the file named generate_file_name, under the directory for given user.
    RETURNS: [ARRAY_OF_FOLLOWERS,ARRAY_OF_FOLLOWING,ARRAY_OF_PEOPLE_WHO_HAVENT_FOLLOWED_BACK]   """
    global path

    backslash = "\ "
#SPECYFIYING PATH:
    backslash = backslash[0:-1]
    modulename = path
    modulename = modulename[0:-1]
    modulename += username
    firstpath = modulename + backslash + file_name

    folderfirst = open(firstpath, "r")

    fstring = str(folderfirst.read())

    wheretoslice = []
    n = 0
    for i in fstring:

        if i == "[" or i == "]":
            wheretoslice.append(n)

        n += 1

    folderfirst.close()
    beginnine = wheretoslice[0]
    end = wheretoslice[1]
    followers = fstring[beginnine:end + 1]
    beginnine = wheretoslice[2]
    end = wheretoslice[3]
    following = fstring[beginnine:end]

    nofollow = fstring[wheretoslice[4]:wheretoslice[5]]

    filter_out=[" ", "[", "]", "'"]
    followers=filterfromstuff(followers,filter_out)
    nofollow=filterfromstuff(nofollow,filter_out)
    following=filterfromstuff(following,filter_out)

    followers=followers.split(",")
    following=following.split(",")
    nofollow=nofollow.split(",")

    return [followers,following,nofollow]


def who_has_unfollowed(username, index1=0, index2=-1):
    """This function analyzes who has unfollowed a given account between records index1 and index2. """
    import os
    global path

    pathtogo=path[0:-1]

    pathtogo=pathtogo+username
    # CHECKING TO SEE IF A FILE OF THIS PERSON EXISTS:
    try:
        os.chdir(pathtogo)
    except FileNotFoundError:
        return("There are no records/files of this person. ")

    records=os.listdir()



    first=records[index1]
    last=records[index2]
    firstfilelist=findlist(first,username)
    lastfilelist=findlist(last,username)

    followerfirst=firstfilelist[0]
    followerlast=lastfilelist[0]

    people_who_have_unfollowed=[]

    for person in followerfirst:
        if person not in followerlast:
            people_who_have_unfollowed.append(person)

    followingfirst = firstfilelist[1]
    followinglast= lastfilelist[1]
    lastman=[]
    for person in people_who_have_unfollowed:
        if person in followinglast:
            lastman.append(person)
    people_who_have_unfollowed=lastman
    return(people_who_have_unfollowed)

def risk_evaluation(post_number,follower_number,following_number):
    """This function returns an integer depending on the input. The smaller the value returned, the less risky the
    decision to follow a given person with these statistics are. I.e. the lower the value this function returns,
    the better it is. """
    # relationship_score=follower_number+following_number #The higher, the better
    # reciprocal=follower_number/following_number #The lower, the better.
    #
    # activity=follower_number/(following_number+post_number) #the lower, the better
    #
    # return activity*reciprocal/relationship_score

    #The k1,k2,k3,a and b values could be skewed to have different effects for instance, k1 can be decreased to tell
    # the bot to value active users over users who have lots of followers.
    k1=1
    k2=1
    k3=-1
    a=k1*post_number+k2*follower_number+k3*following_number #the lower, the better
    if a<0:
        a=-1/a
    try:
        b=follower_number/following_number #also needs to be low
    except ZeroDivisionError:
        b=100000000000000000000000
    return a*b


def order_accounts(array):
    """Sorts a given array in the format [ [account, risk], [account2, risk2] ... ] depending on the risk values of
    each sub-array within the main array. Returns an array in the same format with the values of the risk for each
    sub-array in ascending order."""

    for p in range(len(array)):
        for i in range(len(array)-1):
            if array[i][1]>array[i+1][1]:
                array[i],array[i+1]=array[i+1],array[i]
    return array

#
# yes=[risk_evaluation(1,22,256),
# risk_evaluation(0,15,215),
# risk_evaluation(0,15,215),
# risk_evaluation(2,14,35),
# risk_evaluation(0,146,337),
# risk_evaluation(1,5,35)]
#
# no=[
#     risk_evaluation(0,454,452),
#     risk_evaluation(12, 13, 127),
#     risk_evaluation(200, 3123, 2947),
#     risk_evaluation(29, 330, 99),
#     risk_evaluation(9, 29, 129),
#     risk_evaluation(41, 69, 113),
#     risk_evaluation(0,10,50)
# ]
# yt=0
# for i in yes:
#     yt+=i
#
# nt=0
# for i in no:
#     nt+=i
# print(yt/len(yes))
# print(nt/len(no))
#
# print()
# print('YES')
# for i in yes:
#     print(i)
#
# print('NO:')
# print()
# for i in no:
#     print(i)
# print('ALL:')
# print()
#
# all=[]
# for i in yes:
#     all.append(i)
# for i in no:
#     all.append(i)
#
# all=sorted(all)
# for i in all:
#     if i in yes:
#         print("YES")
#     elif i in no:
#         print("NO")
