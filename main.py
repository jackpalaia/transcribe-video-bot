import os
import praw

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

signals = ["transcribe", "transcription"]
validUrls = ["youtube", "youtu.be"]


def main():
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
            url = comment.submission.url
            video_id = url.split("=")[1]
            transcript_list = []
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id=video_id)
            except:
                continue
            
            transcript = "Here is your transcription:\n\n"
            for part in transcript_list:
                text = part['text'].replace("\n", " ").replace(" !", "!").replace(" ?", "?") + " "
                transcript += text
            transcript += "\n\nThis action was performed by a bot. Please contact u/MangoToothpaste if there are any issues."
            
            comment.reply(transcript)
                    
            # Reply with the video transcription



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
        and comment.submission.author is not None
    )


if __name__ == "__main__":
    main()
