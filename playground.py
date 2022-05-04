# import math
# for i in range(1, 2880, 10):
#     item = {"min_passed": i}
#     time_penalizer = 1 / (1 + math.exp((-item["min_passed"]-100) / (60 * 12))) ** 2
#     print(f"{(i/60):.2f}h score: {time_penalizer:.2f}")


import util
util.update_db()

# subreddits = ["news", "politics", "carsfuckingdragons"]
    
# import util
# import secret
# import praw
# import os

# # instantiate reddit api
# reddit = praw.Reddit(
#     client_id=os.getenv("REDDIT_CLIENT_ID"),
#     client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
#     user_agent=os.getenv("REDDIT_USER_AGENT"),
# )

# print('RUNNING')
# import time
# start = time.time()
# for subreddit_name in subreddits:
#     print(reddit.subreddit(subreddit_name).subscribers)
#     # subreddit = reddit.subreddit(subreddit_name)
#     # print(subreddit)
#     # hot = subreddit.hot(limit=40)
#     # print(hot)
#     # for submission in hot:
#     #     print(submission.title, submission.score, submission.id, submission.url, submission.subscribers)
# end = time.time()
# # average time
# print(f"{(end-start)/len(subreddits):.2f}s")

# print("\nRUN 2 \n")

# # start = time.time()
# # for subreddit in subreddits:
# #     posts = util.get_top_R(subreddit)
# # end = time.time()
# # print(f"{(end-start):.2f}s")
# # # Average
# # print(f"{(end-start)/len(subreddits):.2f}s")