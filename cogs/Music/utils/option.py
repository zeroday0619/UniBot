"""
Powered By ZERODAY BOT
copyright (C) 2019 All Rights Reserved Zeroday Cha
Closed Source | Uni Bot Project 한정 Project ZERODAY 소스 공유
"""
import discord

def ytdl_format_options_a():
    ytdl_format_options = {
        'format': 'bestaudio',
        'outtmpl': 'download/%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'audio-quality': 0,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
    }
    return ytdl_format_options

def ffmpeg_options_a():
    options={'options': '-vn'}
    return options


ytdl_format_options = ytdl_format_options_a()
ffmpeg_options = ffmpeg_options_a()
embed_ERROR = ((discord.Embed(title="Music", description='```css\n재생하고있는 Music 이 없습니다.\n```',
                              color=discord.Color.blurple())).add_field(name="INFO", value="stable"))

embed_queued = ((discord.Embed(title="Music", description='```css\n현재 대기중인 노래가 더 이상 없습니다.\n```',
                              color=discord.Color.blurple())).add_field(name="INFO", value="stable"))
embed_value = ((discord.Embed(title="Music", description='```css\n1에서 100 사이의 값을 입력하십시오.\n```',
                              color=discord.Color.blurple())).add_field(name="INFO", value="stable"))