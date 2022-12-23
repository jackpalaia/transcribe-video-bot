import os
import praw

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()


def main():
    reddit = praw.Reddit(
        user_agent="transcribe-video-bot (by u/transcribe-video-bot)",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        username="transcribe-video-bot",
        password=os.getenv("PASSWORD"),
    )

    subreddit = reddit.subreddit("test")
    for comment in subreddit.stream.comments(skip_existing=True):
        if isCommentValid(comment):
            url = comment.submission.url
            video_id = url.split("=")[1]
            transcript_list = []
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id=video_id)
            except:
                continue

            transcript = "Here is your transcription:\n\n>"
            for part in transcript_list:
                text = part['text'].replace("\n", " ").replace(
                    " !", "!").replace(" ?", "?") + " "
                transcript += text
            transcript += "\n\n*This action was performed by a bot. Please contact u/MangoToothpaste if there are any issues.*"

            comment.reply(transcript)


def isCommentValid(comment):
    """
    Returns true if the comment contains content that summons the bot.
    """
    return comment.body == "u/transcribe-video-bot"


if __name__ == "__main__":
    main()
