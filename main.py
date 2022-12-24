import os
import praw

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime

load_dotenv()


def main():
    print(datetime.now())

    reddit = praw.Reddit(
        user_agent="transcribe-video-bot (by u/transcribe-video-bot)",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        username="transcribe-video-bot",
        password=os.getenv("PASSWORD"),
    )

    unread_messages = []
    for item in reddit.inbox.unread(limit=None):
        if isinstance(item, praw.models.Comment) and isCommentSummon(item):
            unread_messages.append(item)
            url = item.submission.url
            print(url)
            video_id = url[-11:]
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

            item.reply(transcript)

    reddit.inbox.mark_read(unread_messages)


def isCommentSummon(comment):
    """
    Returns true if the comment contains content that summons the bot.
    """
    return comment.body == "u/transcribe-video-bot"


if __name__ == "__main__":
    main()
