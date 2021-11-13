import urllib
from urllib.parse import urlparse
import json
import praw
from uuid import uuid4
from datetime import datetime
import time
import math
import os

# for interacting with database
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# load config
import config
import database

# logging
import logging

utilLogger = logging.getLogger()

# Set up database
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# instantiate reddit api
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# returns the top X stories based on hotness
def get_top(n=40, i=0, username=None, subreddits=config.DEFAULT_SUBREDDITS, new=False):

    # sorted by new
    if new:
        if username is not None:

            items = db.execute(
                """SELECT * FROM items WHERE subreddit in (
                    SELECT DISTINCT subreddit FROM subreddits
                    WHERE username=:username
                )
                OR subreddit in (
                    SELECT DISTINCT subreddit FROM subreddits
                    WHERE username="DEFAULT"
                )
                OR platform = 'hackernews'
                ORDER BY min_passed ASC LIMIT :n""",
                {"n": n, "username": username},
            ).fetchall()

        else:
            items = db.execute(
                """SELECT * FROM items WHERE subreddit in (
                    SELECT DISTINCT subreddit FROM subreddits
                    WHERE username='DEFAULT'
                )
                OR platform = 'hackernews'
                ORDER BY min_passed ASC LIMIT :n""",
                {"n": n},
            ).fetchall()

    # sorted by hotness
    else:
        if username is not None:
            items = db.execute(
                """SELECT * FROM items WHERE subreddit in (
                    SELECT DISTINCT subreddit FROM subreddits
                    WHERE username=:username
                )
                OR subreddit in (
                    SELECT DISTINCT subreddit FROM subreddits
                    WHERE username='DEFAULT'
                )
                OR platform = 'hackernews'
                ORDER BY hotness DESC LIMIT :n""",
                {"n": n, "username": username},
            ).fetchall()

        else:
            items = db.execute(
                """SELECT * FROM items WHERE subreddit in (
                    SELECT DISTINCT subreddit FROM subreddits
                    WHERE username='DEFAULT'
                )
                OR platform = 'hackernews'
                ORDER BY hotness DESC LIMIT :n""",
                {"n": n},
            ).fetchall()

    for item in items:
        print(item["platform"], item["title"], item["hotness"])

    return items


# returns the top n HN stories
def get_top_HN(n=50, i=0):

    # get top 500 stories
    response = urllib.request.urlopen(
        config.BASE_HN_URL + "topstories" + config.END_HN_URL
    )
    items = json.load(response)

    # split list to only get the first n items
    if n != 0:
        items = items[n * i : n * (i + 1)]

    for i, id in enumerate(items):
        response = urllib.request.urlopen(
            config.BASE_HN_URL + "item/" + str(id) + config.END_HN_URL
        )
        items[i] = json.load(response)

    return items


# returns the top n HN stories
def get_top_R(subreddit_name, n=10):

    # instantiate the subreddit - can also be multisubreddit
    subreddit = reddit.subreddit(subreddit_name)

    return subreddit.hot(limit=n)


# updates database with new submissions
def update_db():
    utilLogger.info("updating database")

    # update hackernewsitems
    update_hn_items()

    # update reddit items
    update_r_items()

    # delete all the old items (>48h) to manage db size
    db.execute("DELETE FROM items WHERE min_passed > 2880")
    db.commit()

    # update the hotness score
    update_hotness()

    return


def update_hn_items():

    # get the current hottest HackerNews posts
    hn_items = get_top_HN()

    for hn_item in hn_items:

        # sometimes these values can be empty (e.g. Ask HN posts)
        if "url" not in hn_item.keys():
            hn_item["url"] = ""
        if "descendants" not in hn_item.keys():
            hn_item["descendants"] = 0

        # calculate mins since item was posted
        now = int(time.time())  # UNIX timestamp
        post_time = hn_item["time"]
        mins = (now - post_time) // 60
        hours = mins // 60

        # process variables we aren't copying directly
        parsed_uri = urlparse(hn_item["url"])
        domain = parsed_uri.netloc.replace("www.", "")
        domain = "{uri.netloc}".format(uri=parsed_uri)
        permalink = "https://news.ycombinator.com/item?id=" + str(hn_item["id"])

        # check if item exists in database
        item_row = db.execute(
            "SELECT * FROM items WHERE id=:id", {"id": str(hn_item["id"])}
        ).fetchone()
        if item_row is None:

            # insert item into database
            db.execute(
                """INSERT INTO items
                (id,platform,title,score,by,url,permalink,domain,time,
                num_comments,min_passed,hours_passed)
                VALUES
                (:id,:platform,:title,:score,:by,:url,:permalink,:domain,
                :time,:num_comments,:min_passed,:hours_passed)""",
                {
                    "id": str(hn_item["id"]),
                    "platform": "hackernews",
                    "title": hn_item["title"],
                    "score": hn_item["score"],
                    "by": hn_item["by"],
                    "url": hn_item["url"],
                    "permalink": permalink,
                    "domain": domain,
                    "time": hn_item["time"],
                    "min_passed": mins,
                    "hours_passed": hours,
                    "num_comments": hn_item["descendants"],
                },
            )
            db.commit()

        # update votecount & hotness
        else:
            db.execute(
                """UPDATE items
                SET title=:title,score=:score,num_comments=:num_comments,
                min_passed=:min_passed,hours_passed=:hours_passed
                WHERE id=:id""",
                {
                    "id": str(hn_item["id"]),
                    "title": hn_item["title"],
                    "score": hn_item["score"],
                    "num_comments": hn_item["descendants"],
                    "min_passed": mins,
                    "hours_passed": hours,
                },
            )
            db.commit()

    return


def update_r_items():

    # get list of subreddits we have to update
    subreddits = db.execute("SELECT DISTINCT subreddit FROM subreddits").fetchall()
    subreddits = set([subreddit[0] for subreddit in subreddits])

    for subreddit in list(subreddits):
        update_subreddit(subreddit)

    return


def update_subreddit(subreddit):
    print("updating subreddit: " + subreddit)

    # get the current top reddit items
    r_items = get_top_R(subreddit)

    for r_item in r_items:

        # calculate mins since item was posted
        now = datetime.now()
        post_time = datetime.fromtimestamp(r_item.created_utc)
        mins = (now - post_time).total_seconds() // 60
        hours = mins // 60

        # process variables we aren't copying directly
        parsed_uri = urlparse(r_item.url)
        parsed_uri = parsed_uri._replace(netloc=parsed_uri.netloc.replace("www.", ""))
        domain = "{uri.netloc}".format(uri=parsed_uri)
        permalink = "https://www.reddit.com/" + str(r_item.permalink)
        subscribers = reddit.subreddit(subreddit).subscribers

        # check if item exists in database
        item_row = db.execute(
            "SELECT * FROM items WHERE id=:id", {"id": r_item.id}
        ).fetchone()
        if item_row is None:

            # insert item into database
            db.execute(
                """INSERT INTO items
                (id,platform,title,score,by,url,permalink,domain,
                time,num_comments,upvote_ratio,stickied,subreddit,
                subscribers,min_passed, hours_passed)
                VALUES
                (:id,:platform,:title,:score,:by,:url,:permalink,
                :domain,:time,:num_comments,:upvote_ratio,:stickied,
                :subreddit,:subscribers,:min_passed,:hours_passed)""",
                {
                    "id": r_item.id,
                    "platform": "reddit",
                    "title": r_item.title,
                    "score": r_item.score,
                    "by": r_item.author.name,
                    "url": r_item.url,
                    "permalink": permalink,
                    "domain": domain,
                    "time": r_item.created_utc,
                    "num_comments": r_item.num_comments,
                    "upvote_ratio": r_item.upvote_ratio,
                    "hours_passed": hours,
                    "stickied": int(r_item.stickied),
                    "subreddit": subreddit,
                    "subscribers": subscribers,
                    "min_passed": mins,
                },
            )

            db.commit()

        else:
            # update the item
            db.execute(
                """UPDATE items
                SET title=:title,score=:score,num_comments=:num_comments,
                min_passed=:min_passed,hours_passed=:hours_passed
                WHERE id=:id""",
                {
                    "id": r_item.id,
                    "title": r_item.title,
                    "score": r_item.score,
                    "stickied": int(r_item.stickied),
                    "num_comments": r_item.num_comments,
                    "upvote_ratio": r_item.upvote_ratio,
                    "hours_passed": hours,
                    "min_passed": mins,
                },
            )
            db.commit()

    update_hotness()
    return


# update the hotness of all posts in database
def update_hotness():

    items = db.execute("SELECT * FROM items").fetchall()

    for item in items:
        hotness = get_hotness(item)

        db.execute(
            "UPDATE items SET hotness=:hotness where id=:id",
            {"hotness": hotness, "id": item["id"]},
        )

    db.commit()

    return


# get a hotness score for a given post (to determine display order)
def get_hotness(item):
    # NEEDS WORK!
    # TODO: weight repeated submission from same subreddit lower
    relative_reddit_weight = 1
    subreddit_size_penalizer_compensation = 10e4 # insert average subreddit size here or similar
    curve_width = 360

    # score scales with: upvotes
    time_penalizer = 2 / (1 + math.exp((-item["min_passed"]-360) / curve_width)) - 1
    if item["platform"] == "reddit":
        subreddit_size_penalizer = item["subscribers"]
        # sigmoid scale score with time passed
        hotness = (relative_reddit_weight * item["score"] * subreddit_size_penalizer_compensation) / (
            time_penalizer * subreddit_size_penalizer
        )

    # weight the hackernews items differently
    elif item["platform"] == "hackernews":
        hotness = item["score"] / (time_penalizer)

    return hotness


# utility function to turn sqlalchemy results into standard lists
def sqla_to_list(sqlalchemy_res):
    output = []
    for i in sqlalchemy_res:
        output.append(i[0])
    return output
