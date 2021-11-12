# HackerReddit

I love both HackerNews and Reddit. They both have a fast, minimalist website design, they both have great communities and great content.

So, my project is to have a unified way of viewing these two!

How it works: By default, you will see a mix of top HN posts and posts of a few default subreddits, all mixed in the same page. If you
wish to sign up, you can also customize the list of subreddits that will appear on your frontpage. *Future: You will also be able to weight different news sources according to your preferences. E.g. give Hackernews a weight of 0.5x, and /r/cats maybe a 2x)*

Of course, you can navigate to the original HN/Reddit post at any time by simply clicking the comment section. You can also view the
profile of the author or the link itself. Most other text is also interactable, e.g. you can go to the original subreddit, or check out all HN posts on that specific domain, etc...

### Future Improvements:
- additional news-sources (e.g. RSS-feeds)
- custom weighing of news sources/subreddits (user-chosen weights)
- upvote functionality directly from HackerReddit using Oauth2
- automatically subscribe to subreddits when authenticating with Reddit account

### Files:

Under /templates are all the html templates:
- layout.html: layout file, extends all other files. Navbar, login functionality, footer
- index.html: newsfeed
- error.html: errorhandler
- login.html: Login as well as registering functionality
- ...

- /static you can find the images and css stylesheets and js files

- /logs logs are stored here

- data.db: database (SQLite) 

- requirements.txt: Python dependencies

- util.py: Utilities module, takes care of handling the API's and loading the data

- config.py: Configuration file

# Architecture

Since getting the data from HN/Reddit every time a user loads the website is way too slow, we have to cache the data in our own database. For this, every 5 minutes we get the top 50 Hackernews stories as well as the top 10 reddit stories in every subreddit that our users are subscribed to. 

Also, when a user subscribes to a subreddit that is not cached, we launch a new update request for that specific subreddit.

