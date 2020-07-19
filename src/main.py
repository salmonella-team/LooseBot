# main.py

# とりあえず単体のメッセージルームに対応

from discord import channel
import setting
import discord

import datetime
import locale
import hashlib

DISCORD_TOKEN = setting.DISCORD_TOKEN
DEBUG_ROOM_ID = setting.DEBUG_ROOM_ID
DEBUG_SEND_ROOM_ID = setting.DEBUG_SEND_ROOM_ID

locale.setlocale(locale.LC_TIME, 'ja_JP')


client = discord.Client()

num = 1
def today_string() -> str:
    dt = datetime.datetime.today()
    send_message_date = dt.strftime('%Y/%m/%d(%a) %H:%M:%S')
    return send_message_date

def get_hash_id(athor_id) -> str:
    dt = datetime.datetime.today()
    athor_id += dt.strftime('%Y/%m/%d(%a)')
    hs = hashlib.sha256(athor_id.encode()).hexdigest()
    return hs

@client.event
async def on_ready() -> str:
    """
    Start on Discord Bot


    print UserName
    """
    print("Start on {0.user}".format(client))
    return client

@client.event
async def on_guild_channel_create(channel):
    if channel.name[0:1] == "☆":
        res_num = 1
        send_message_date = today_string()
        hs = get_hash_id(str(87631876321))
        send_message = """
        1get!!!!
                        """
        embed = discord.Embed(title=str(res_num).zfill(3) + "  腸まで届く名無しさん  " + send_message_date + "  ID:" + hs.upper()[10:17], description=send_message, color=0x000000)
        await channel.send(embed=embed)


@client.event
async def on_message(message):
    """
    Message Delete -> Send Message Anonymous User
    """

    global num

    if message.author.bot:
        return
    
    channel = client.get_channel(message.channel.id)
    print(channel.name)
    if channel.name[0:1] == "☆":

        # ID用の日付取得
        send_message_date = today_string()

        # 送信されたメッセージの取得
        send_message = message.content

        # 送信されたメッセージの削除
        await message.delete()

        # チャンネルをフェッチ
        # channel = client.get_channel(int(DEBUG_SEND_ROOM_ID))

        # ハッシュの作成
        athor_id = str(message.author.id)
        hs = get_hash_id(athor_id)

        """
        表示例
        001 腸まで届く名無しさん YYYY/MMM/DD(A) %H:%M:%S ID:XXXXXXX
        テスト

        IDは個人IDと日付を連結させた文字列をハッシュ化し真ん中を切り取ったもの
        """ 


        # レス番号の確認

        async for res_message in channel.history(limit=1):
            res_num = int(res_message.embeds[0].title[0:3])

        channel = client.get_channel(message.channel.id)

        """
        最新のメッセージの取り方を確認
        メッセージの取り方
        channel.fetch_message(733137000130936914)
        
        レス番号だけ取り出す
        embeds[0].title[0:3]
        """
        res_num += 1
        embed = discord.Embed(title=str(res_num).zfill(3) + "  腸まで届く名無しさん  " + send_message_date + "  ID:" + hs.upper()[10:17], description=send_message, color=0x000000)
        await channel.send(embed=embed)
        pass

client.run(DISCORD_TOKEN)