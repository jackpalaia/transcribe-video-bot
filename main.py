import os
from datetime import datetime

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

    print("Client started and Reddit instance created, accepting mentions")

    for item in reddit.inbox.stream():
        if "u/transcribe-video-bot" in item.body:
            log_file = open("log.txt", "a")

            log_file.write(f"{datetime.now()}\n")
            log_file.write(
                f"Mention from user {item.author.name} with id {item.id} at link {item.context}\n")
            url = item.submission.url
            video_id = url[-11:]
            transcript_list = []
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(
                    video_id=video_id)
            except:
                continue

            transcript = "Here is your transcription:\n\n>"
            text = ""
            for part in transcript_list:
                text = part['text'].replace("\n", " ").replace(
                    " !", "!").replace(" ?", "?") + " "
                transcript += text
            transcript += "\n\n*This action was performed by a bot. Please contact u/MangoToothpaste if there are any issues.*"

            item.reply(transcript)
            log_file.write(
                f"Mention with id {item.id} replied to with transcript '{' '.join(text.split()[:10])}...'\n")
            item.mark_read()

            log_file.write("\n")
            log_file.close()


if __name__ == "__main__":
    main()
