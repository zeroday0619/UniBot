from Util import *

@bot.event
async def on_member_join(member):
    """
    guild 에 member 가 접속했을때 발생하는 이벤트
    :param member:
    :return:
    """
    await member.channel.send('{} 님이 서버에 참가하셨습니다!'.format(member))

@bot.event
async def on_member_remove(member):
    """
    guild에서 member가 퇴장, 강퇴, 밴이 되었을대 발생하는 이벤트
    :param member:
    :return:
    """
    await member.channel.send('{} 님이 서버에서 퇴장하셨습니다!'.format(member))


@bot.event
async def on_guild_join(guild):
    """
    client(유니봇)이 guild 에 접속했을 때 발생하는 이벤트
    :param guild:
    :return:
    """
    print(prefix + "{} 서버에 입장하였습니다.".format(guild))

@bot.event
async def on_guild_remove(guild):
    """
    client(유니봇)이 guild 에서 나가거나, 강퇴당하거나, 밴이 되었을때 발생하는 이벤틑
    :param guild: guild
    :return:
    """
    print(prefix + "{} 서버에 퇴장하였습니다.".format(guild))