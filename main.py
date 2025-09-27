import asyncio
import os
import random

import discord
import requests
from discord.ext import commands

import drive
import lock_unit
import torrent
import util
import encode_module

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
token = ""
encq = []

def randomize():
    while True:
        x = f"{random.randint(0, 1000)}"
        if not x in encq:
            encq.append(x)
            return x


@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')


@bot.command()
async def encode(ctx: discord.ext.commands.Context, param: str, attachment: discord.Attachment):
    if not ctx.author.id in [719601957852938360, 944246988575215627]:
        await ctx.reply("Sorry, you're not a sigma.")
    outfilepath = randomize()
    try:
        if attachment == None:
            await ctx.send("provide an attachment (.ass)")
            return
        if param == None:
            await ctx.send("provide a nyaa link")
            return
        message = await ctx.send(f"Waiting in EncodelockQ\n-# rmlock:{outfilepath}")

        while not lock_unit.lock(outfilepath):
            await asyncio.sleep(5)
        for i in util.find_addt_s():
            if i != "abcdef":
                try:
                    os.remove(i)
                except:
                    pass

        file_bytes = await attachment.read()
        with open(f"{outfilepath}.ass", "wb") as f:
            f.write(file_bytes)
        try:
            response = requests.get(param)
            if response.status_code == 200:
                with open(f"{outfilepath}.torrent", "wb") as f:
                    f.write(response.content)
            else:
                lock_unit.rmlock(outfilepath)
                raise Exception(response.status_code)

            await message.edit(content=f"Linki verilen .torrent dosyası indirildi.\nTorrent içeriği indirilmeye çalışılıyor...\n-# rmlock:{outfilepath}")
        except Exception as e:
            await message.edit(content=f"Linki verilen .torrent dosyası indirilemedi. \nÇalıştığından emin olun.\n-# rmlock:{outfilepath}")
            print(e)
            lock_unit.rmlock(outfilepath)
            return

        #await torrent.get_torrent(f"{outfilepath}.torrent", f"{outfilepath}.mkv")

        newd = util.find_addt_f()
        print(newd)
        await message.edit(content=f"Torrent içeriği nyaa'dan başarıyla alındı.\nEncode'a geçiliyor.\nparametreler: {newd} {outfilepath}.ass {outfilepath} crf17\n-# rmlock:{outfilepath}")
        uploadq = await encode_module.encode(mkv=newd, ass=f"{outfilepath}.ass", encodeid=outfilepath)
        outlink = await asyncio.to_thread(drive.upload, filepath=f"{outfilepath}.mp4", mimetype="video/mp4", outfilepath=f"{outfilepath}-{param.split("/")[-1].split(".torrent")[0]}")
        if outlink == False:

            await message.edit(content=f"Gdrive'a yüklerken bir sorun oluştu. \nDosyalar temizleniyor.\n-# rmlock:{outfilepath}")
            raise Exception("uploaderror")
        await message.edit(content=f"{outlink}\n-# rmlock:{outfilepath}")
        lock_unit.rmlock(outfilepath)
    except Exception as e:
        print(e)
        try:
            await message.edit(content=f"Bir sorun oluştu. -#rmlock:{outfilepath}")
        except:pass
        lock_unit.rmlock(outfilepath)




@bot.command()
async def gdrive_test(ctx, param: str, attachment: discord.Attachment):
    if attachment == None:
        await ctx.send("provide an attachment")
        return
    if param == None:
        await ctx.send("provide a mimetype")
        return
    outfilepath = randomize()
    file_bytes = await attachment.read()

    # Dosyayı kaydet
    with open(f"{outfilepath}.tmp", "wb") as f:
        f.write(file_bytes)
    try:
        drive.upload(f"{outfilepath}.tmp", mimetype=param, outfilepath=f"{outfilepath}.{"mp4" if param == "video/mp4" else "txt"}")

        await ctx.send(f"{outfilepath}.tmp upload 0")
    except Exception as e:
        print(e)
        await ctx.send(f"{outfilepath}.tmp upload 1")

# Token ile botu başlat
bot.run(token)