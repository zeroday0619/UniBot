
import discord
import time
import codecs
import json
import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


def color_header(str):
    return '\033[95m' + str + '\033[0m'

prefix = color_header('UniBot || ')

client = discord.Client(
    # max_messages = "",
    # loop = "",
    # proxy = "",
    # proxy_auth = "",
    # shard_id = "",
    # shard_count = "",
    # guild_subscriptions = True,
    #if guild_subscriptions = False
        #disable event list:
            #on_member_update()
            #on_member_join()
            #on_member_remove()
            #on_typing_start()
            #
)

@client.event
async def on_ready():
    """
    봇이 실행되었을때 발생하는 이벤트, 봇이 켜졌다는 신호의 이벤트임.
    :return:
    """
    print(prefix + "Uni Bot이 실행되고 있습니다!")
    print(prefix + "Bot Name: {}".format(client.user.name))
    print(prefix + "Join Server(Guild) List:")
    for g in client.guilds:
        print(prefix + "\t- " + g.name)

@client.event
async def on_message(message):
    """
    client으로부터 메시지가 수신되었을때 발생하는 이벤트
    :param message:
    :return:
    """
    if message.author == client.user:
        return

    if message.content.startswith('!test'):
        await message.channel.send('Hello!')
    if message.content.startswith('!botinfo'):
        await message.channel.send(id) #작동 X
    # if message.content.startswith('!test'):
    #     await client.send_message(message.channel, 'test!!!!')

    # elif message.content.startswith('!say'):
    #     await client.send_message(message.channel, 'leave message')
    #     msg = await client.wait_for_message(timeout=15.0, author=message.author)
    #
    #     if msg is None:df
    #         await client.send_message(message.channel, '15초내로 입력해주세요. 다시시도: !say')
    #         return
    #     else:
    #         await client.send_message(message.channel, msg.content)


@client.event
async def on_member_join(member):
    """
    guild 에 member 가 접속했을때 발생하는 이벤트
    :param member:
    :return:
    """
    await member.channel.send('{} 님이 서버에 참가하셨습니다!'.format(member))

@client.event
async def on_member_remove(member):
    """
    guild에서 member가 퇴장, 강퇴, 밴이 되었을대 발생하는 이벤트
    :param member:
    :return:
    """
    await member.channel.send('{} 님이 서버에서 퇴장하셨습니다!'.format(member))

@client.event
async def on_guild_join(guild):
    """
    client(유니봇)이 guild 에 접속했을 때 발생하는 이벤트
    :param guild:
    :return:
    """
    print(prefix + "{} 서버에 입장하였습니다.".format(guild))

@client.event
async def on_guild_remove(guild):
    """
    client(유니봇)이 guild 에서 나가거나, 강퇴당하거나, 밴이 되었을때 발생하는 이벤틑
    :param guild: guild
    :return:
    """
    print(prefix + "{} 서버에 퇴장하였습니다.".format(guild))

client.run('NjAxNjE0MTAwNDUxMjk1MjQy.XaGNdA.y_K5WeoZIrO0Nzs0g6UVLyi9Jg8')

