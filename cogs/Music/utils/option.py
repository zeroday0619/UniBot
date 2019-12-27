import discord

def ytdl_format_options_a():
    ytdl_format_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
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
                              color=discord.Color.blurple())).add_field(name="INFO", value="BETA"))

embed_queued = ((discord.Embed(title="Music", description='```css\n현재 대기중인 노래가 더 이상 없습니다.\n```',
                              color=discord.Color.blurple())).add_field(name="INFO", value="BETA"))
embed_value = ((discord.Embed(title="Music", description='```css\n1에서 100 사이의 값을 입력하십시오.\n```',
                              color=discord.Color.blurple())).add_field(name="INFO", value="BETA"))