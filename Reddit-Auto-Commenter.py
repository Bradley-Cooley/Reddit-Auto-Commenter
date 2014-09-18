"""

"""

import praw
import time
from collections import deque

print("Reddit Auto Commenter takes 12 minutes between each reply, and only affects the last 10 comments a user has made. You must leave the program running until 'Up to date' is printed. Also, this program not guaranteed to work correctly.")
user_name = raw_input("What is your reddit username?")
target_name = raw_input("Which user would you like to automatically reply to?")
user_comment = raw_input("What would you like your comment to say?")

# Attributes
already_done = set()
queue = deque([])
flag = True

# Setup praw and login
user_agent = ('Dedicated to promoting the knowledge of Warlizards origin story by /u/SnufflesTheAnteater')
r = praw.Reddit(user_agent)
r.login(user_name)
print("Logged in as " + user_name)
target = r.get_redditor(target_name)

while flag == True:
    comments = target.get_comments(limit=10)
    if queue:
        try:
            queue.popleft().reply(user_comment)
            print("Comment posted. %d left in queue." % len(queue))
        except praw.errors.RateLimitExceeded as e:
            print('Comment rate limit exceeded, sleeping for %d seconds.' % e.sleep_time)
            time.sleep(e.sleep_time)
    for comment in comments:
        if comment.id not in already_done and comment not in queue:
            users_replied = set()
            replies = comment.replies
            for comment in replies:
                users_replied.add(comment.author.name)
            if user_name not in users_replied:
                queue.append(comment)
                already_done.add(comment.id)
                print("Comment queued.")
    time.sleep(2)

    if not queue:
        continue_run = raw_input("No comments in queue. Y to quit, N to continue.")
        if not(continue_run == 'Y' or 'y'):
            flag = False

print("Thanks for using Reddit Auto Commenter! Automatic exit will occur.")
time.sleep(3)
exit
