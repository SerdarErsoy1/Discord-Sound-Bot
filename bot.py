import asyncio
import discord
import requests
import yt_dlp

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=",",
    intents=intents
)

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
}

FFMPEG_PATH = r"C:\Users\shuku\Desktop\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe"

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")

    @classmethod
    async def from_url(cls, url, *, loop=None):

        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(url, download=False)
        )

        if "entries" in data:
            data = data["entries"][0]

        return cls(
            discord.FFmpegPCMAudio(
            data["url"],
            executable=FFMPEG_PATH,
            **FFMPEG_OPTIONS
        ),
            data=data
        )


@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yaptık")
    print("Bot hazır!")


@bot.command()
async def hello(ctx):
    await ctx.send(
        f"Merhaba! Ben {bot.user}, bir Discord sohbet botuyum!"
    )


@bot.command(name="bilgi")
async def bilgi(ctx):

    response = requests.get(
        "https://catfact.ninja/fact"
    )

    data = response.json()

    bilgi_fact = data.get("fact")

    await ctx.send(bilgi_fact)


@bot.command()
async def heh(ctx, count_heh: int = 5):

    if count_heh > 50:
        count_heh = 50

    await ctx.send("he" * count_heh)


@bot.command()
async def join(ctx):

    if ctx.author.voice is None:
        await ctx.send("Önce bir ses kanalına gir.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

    await ctx.send(f"🔊 {channel.name} kanalına girdim.")


@bot.command()
async def yt(ctx, *, query):

    if ctx.author.voice is None:
        await ctx.send("Önce bir ses kanalına gir.")
        return

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    await ctx.send("🔎 Şarkı aranıyor...")

    try:

        player = await YTDLSource.from_url(
            query,
            loop=bot.loop
        )

        ctx.voice_client.play(
            player,
            after=lambda e:
            print(f"Player error: {e}") if e else None
        )

        await ctx.send(
            f"🎵 Şimdi çalıyor: **{player.title}**"
        )

    except Exception as e:

        await ctx.send(
            f"❌ Şarkı oynatılırken hata oluştu:\n`{e}`"
        )


@bot.command()
async def stop(ctx):

    if ctx.voice_client is None:
        await ctx.send("Bot ses kanalında değil.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    await ctx.voice_client.disconnect()

    await ctx.send("⏹️ Müzik durduruldu.")


@bot.command()
async def pause(ctx):

    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Müzik duraklatıldı.")
    else:
        await ctx.send("Şu anda müzik çalmıyor.")


@bot.command()
async def resume(ctx):

    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Müzik devam ediyor.")
    else:
        await ctx.send("Müzik duraklatılmış değil.")


@bot.command()
async def volume(ctx, volume: int):

    if ctx.voice_client is None:
        await ctx.send("Bot ses kanalında değil.")
        return

    if ctx.voice_client.source is None:
        await ctx.send("Şu anda müzik çalmıyor.")
        return

    if volume < 0 or volume > 200:
        await ctx.send("Ses seviyesi 0-200 arasında olmalı.")
        return

    ctx.voice_client.source.volume = volume / 100

    await ctx.send(
        f"🔊 Ses seviyesi **{volume}%** olarak ayarlandı."
    )


bot.run("Tokeninizi buraya girin")
