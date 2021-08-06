import os
import praw

from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    user_agent="transcribe-video-bot (by u/transcribe-video-bot)",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    username="transcribe-video-bot",
    password=os.getenv("PASSWORD"),
)

subreddit = reddit.subreddit("Videos")
for submission in subreddit.stream.submissions():
    print(submission)
