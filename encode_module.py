import os
import asyncio

async def prepare(mkv, encodeid):
    os.rename(mkv, f"{encodeid}.mkv")
async def encode(mkv, ass, encodeid):
    if ass == ".ass":
        raise Exception("no ass file provided")
    try:
        await prepare(mkv, encodeid)
    except:pass
    os.system(f'ffmpeg -i "{encodeid}.mkv" -vf ass="{encodeid}.ass" -c:v libx264 -profile:v main -level:v 4.1 -crf 17 -preset veryfast -c:a aac -b:a 192k "{encodeid}.mp4"')

    return f"{encodeid}.mp4"