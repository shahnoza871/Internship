import logging
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import executor
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

from transformers import pipeline


summarization = pipeline("summarization")


# Then you have to initialize bot and dispatcher instances.
API_TOKEN = "6154664932:AAFnsf-hzepvQCnUO-vdGzfvZ4Pdue8cGwA"

# logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def is_valid_url(url):
    return re.match(r"^https?://", url)


def extract_video_id(url):
    # if url.startswith(('youtu', 'www')):
    #     url = "http://" + url

    query = urlparse(url)

    if "youtube" in query.hostname:
        if query.path == "/watch":
            return parse_qs(query.query)["v"][0]
        elif query.path.startswith(("/embed", "/v/")):
            return query.path.split("/")[2]
    elif "youtu.be" in query.hostname:
        # is used to remove the first character (which is typically the leading slash /) from the "PATH" component of the URL
        return query.path[1:]
    else:
        raise ValueError


def extract_text(video_id):
    txt = YouTubeTranscriptApi.get_transcript(video_id)
    # joins each item (dictionary) in the txt list together into a single string with space " " between each item.
    text = " ".join([item["text"] for item in txt])
    # await message.reply(f"Here is the text of the video you provided: \n{text}")
    return text

def split_txt(txt):
    if len(txt) > 6000:
        chunks = []
        while chunk_size > 6000:
            chunk_size = len(txt)/2
        for i in range(0, len(txt), chunk_size):
            chunk = txt[i:i + chunk_size]
            chunks.append(chunk)
        return chunks
    else:
        return txt

# This handler will be called when the user sends the `/start` command
@dp.message_handler(commands=["start"])
async def on_start(message: types.Message):
    await message.reply(
        "Hello, I am your bot! \nSend me a URL of a YouTube video and I will give you a short description of it."
    )


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def url_received(message: types.Message):
    url = message.text
    if not is_valid_url(url):
        await message.reply(
            "Invalid URL. Please, sent a valid URL."  # if URL is not valid
        )

    try:
        video_id = extract_video_id(url)
        # await message.reply(video_id)
    except Exception as error:
        await message.reply(
            "Sorry, something went wrong. Please make sure you send a valid YouTube video link."  # if could not extract video ID
        )

    try:
        txt = extract_text(video_id)
    except Exception as error:
        await message.reply(
            "The video doesn not have captions. Please, send the link of a video that has captions."
        )

    try:
        chunks = split_txt(txt)
        for i in chunks:
            short_txts = []
            short_txts.append(summarization(i)[0]["summary_text"])
        short_txt = " ".join(short_txts)
        await message.reply(f"Here is the summary of the video: \n\n{short_txt}")
    except Exception as error:
        await message.reply(
            "The video is too long. Please, send the link of a shorter video."
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


# https://youtu.be/fQUeDdaVoWo
# https://youtu.be/Ywec1MbeQDk

# too long: https://youtu.be/eIho2S0ZahI
