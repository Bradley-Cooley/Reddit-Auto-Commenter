"""
This is Reddit Auto Commenter! v1.0
For comments, stalking concerns, etc. please contact /u/SnufflesTheAnteater
https://github.com/Bradley-Cooley/Reddit-Auto-Commenter.git
"""

import praw
import time
from collections import deque

print("Reddit Auto Commenter only affects the last 10 comments a user has made. Because of reddit api limits, time between replies could take awhile. For bug reports and the like, please contact /u/SnufflesTheAnteater.")
user_name = raw_input("\nWhat is your reddit username?")
target_name = raw_input("Which user would you like to automatically reply to?")
comment_distance = int(raw_input("To how many recent comments would you like to reply?"))
user_comment = raw_input("What would you like your comment to say?")

# Attributes
already_done = set()
queue = deque([])
flag = True

# Setup praw and login
user_agent = ('Reddit-Auto-Commenter/1.0 by SnufflesTheAnteater'
              'https://github.com/Bradley-Cooley/Reddit-Auto-Commenter.git')
r = praw.Reddit(user_agent)
r.login(user_name)
print("Logged in.")
target = r.get_redditor(target_name)
user = r.get_redditor(user_name)

while flag == True:
    comments = target.get_comments(limit=comment_distance)
    if queue:
        try:
            current_reply = queue.popleft()
            current_reply.reply(user_comment)
            print("Comment posted. %d left in queue." % len(queue))
        except praw.errors.RateLimitExceeded as e:
            queue.appendleft(current_reply)
            print('Comment rate limit exceeded, sleeping for %d seconds.' % e.sleep_time)
            time.sleep(e.sleep_time)
    for comment in comments:
        if comment.id not in already_done and comment not in queue:
            users_replied = set()
            replies = comment.replies
            for reply in replies:
                users_replied.add(reply.author.name)
            if user.name not in users_replied:
                queue.append(comment)
                already_done.add(comment.id)
                print("Comment queued.")
    time.sleep(2)

    if not queue:
        continue_run = raw_input("No comments in queue. Press enter to quit.")
        flag = False

print("Thanks for using Reddit Auto Commenter! Automatic exit will occur.")
time.sleep(3)
exit
