import os
import praw

from dotenv import load_dotenv

load_dotenv()

signals = ["transcribe", "transcription"]
validUrls = ["youtube", "youtu.be"]


def main():

    # Set up Reddit instance
    reddit = praw.Reddit(
        user_agent="transcribe-video-bot (by u/transcribe-video-bot)",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        username="transcribe-video-bot",
        password=os.getenv("PASSWORD"),
    )

    subreddit = reddit.subreddit("test")
    for comment in subreddit.stream.comments():
        if isCommentValid(comment):
            print(comment.permalink)
            comment.reply("hello!")


# Returns true if the comment is a valid signal.
# Checks if the comment contains a signal string,
# if the comment is on a post that is a video,
# and if the comment was not made by a bot.
def isCommentValid(comment):
    return (
        any(s in comment.body for s in signals)
        and (
            comment.submission.is_video
            or any(url in comment.submission.url for url in validUrls)
        )
        and "bot" not in comment.body
    )


if __name__ == "__main__":
    main()
