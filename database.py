from util import *
from sqlalchemy import create_engine, exc

try:
    import secret
except ImportError:
    pass
import config
import os

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
engine = create_engine(DATABASE_URL)


def drop_tables():
    # drop table hn_items, r_items, items, subreddits, users

    # drop table hn_items
    query = "DROP TABLE IF EXISTS hn_items"
    engine.execute(query)

    # drop table r_items
    query = "DROP TABLE IF EXISTS r_items"
    engine.execute(query)

    # drop table items
    query = "DROP TABLE IF EXISTS items"
    engine.execute(query)

    # drop table subreddits
    query = "DROP TABLE IF EXISTS subreddits"
    engine.execute(query)

    # drop table users
    query = "DROP TABLE IF EXISTS users"
    engine.execute(query)


# Create tables in database if they dont exist
def create_tables():
    # create table hn_items, r_items, items, subreddits, users

    # create table hn_items
    query = "CREATE TABLE IF NOT EXISTS hn_items (id SERIAL PRIMARY KEY, type TEXT, by TEXT, time INTEGER, text TEXT, parent TEXT, url TEXT, kids TEXT, score INTEGER, title TEXT, descendants INTEGER)"
    engine.execute(query)

    # create table r_items
    query = "CREATE TABLE IF NOT EXISTS r_items (id TEXT PRIMARY KEY, title TEXT, score INTEGER, upvote_ratio NUMERIC, url TEXT, by TEXT, time INTEGER, num_comments INTEGER, stickied INTEGER, subreddit TEXT, comments_url TEXT, comments_count INTEGER)"
    engine.execute(query)

    # create table items
    query = "CREATE TABLE IF NOT EXISTS items (id TEXT PRIMARY KEY, platform TEXT, title TEXT, score INTEGER, by TEXT, url TEXT, permalink TEXT, domain TEXT, time INTEGER, num_comments INTEGER, upvote_ratio NUMERIC, stickied INTEGER, subreddit TEXT, subscribers INTEGER, min_passed INTEGER, hours_passed INTEGER, hotness NUMERIC, comments_url TEXT, comments_count INTEGER)"
    engine.execute(query)

    # create table subreddits
    query = "CREATE TABLE IF NOT EXISTS subreddits (username TEXT, subreddit TEXT, PRIMARY KEY (username, subreddit))"
    engine.execute(query)
    # populate with default subreddits
    for subreddit in config.DEFAULT_SUBREDDITS:
        query = "INSERT INTO subreddits (username, subreddit) VALUES (%s, %s)"
        try:
            engine.execute(query, (config.DEFAULT_USERNAME, subreddit))
        except exc.IntegrityError:
            pass

    # create table users
    query = "CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, pwd_hash VARCHAR(255), salt VARCHAR(255), email VARCHAR(255), admin INTEGER)"
    engine.execute(query)


drop_tables()
create_tables()
