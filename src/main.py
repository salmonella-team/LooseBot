# main.py

import setting
import discord

import datetime
import locale
import hashlib
import requests
import os


DISCORD_TOKEN = setting.DISCORD_TOKEN
BOT_SEED = setting.BOT_SEED
MAKE_CHANNEL_CATEGORY_ID = setting.CATEGORY_ID

client = discord.Client()


# 日付を文字列で返す
def today_string() -> str:
    dt = datetime.datetime.today()
    send_message_date = dt.strftime('%Y/%m/%d(%a) %H:%M:%S')
    return send_message_date


# 日付と送信したIDを連結してハッシュ化
def get_hash_id(athor_id) -> str:
    dt = datetime.datetime.today()
    athor_id += dt.strftime('%Y/%m/%d(%a)')
    hs = hashlib.sha256(athor_id.encode()).hexdigest().upper()
    return hs


# 画像を一時的に保存する
def save_pic(pic_url, save_name):
    r = requests.get(pic_url, stream=True)
    if r.status_code == 200:
        with open(save_name, 'wb') as f:
            f.write(r.content)


# 最新のレス番号を取得
def get_res_number(message_history) -> int:
    for res_message in message_history:
        if len(res_message.embeds):
            res_num = int(res_message.embeds[0].title[0:3])
            print(res_num)
            return res_num


# 起動メッセージ
@client.event
async def on_ready():
    print("Start on {0.user}".format(client))


# チャンネル作成時に発火
@client.event
async def on_guild_channel_create(channel):
    # チャンネルの頭に☆がついていたら匿名チャンネル判定
    if channel.name[0:1] == "☆":
        res_num = 1
        send_message_date = today_string()
        hs = get_hash_id(str(BOT_SEED))
        send_message = """
        1get!!!!
                        """
        embed = discord.Embed(title=str(res_num).zfill(3) + "  腸まで届く名無しさん  " + send_message_date + "  ID:" + hs[10:17], description=send_message, color=0x000000)
        await channel.send(embed=embed)


# ここからメイン
@client.event
async def on_message(message):
    """
    Message Delete -> Send Message Anonymous User
    """

    # Botだったら反応しない
    if message.author.bot:
        return
    
    # スレ立て機能
    # argsが今の書き方だと使えないので筋肉実装
    if message.content[0:6] == "/mk2ch":
        make_channel_message = message.content.split()
        channel = client.get_channel(message.channel.id)
        if len(make_channel_message) == 2:
            category_id = int(MAKE_CHANNEL_CATEGORY_ID)
            category = channel.guild.get_channel(category_id)
            new_channel = await channel.guild.create_text_channel(name="☆" + make_channel_message[1], category=category)
        else:
            await channel.send("引数が不正です")


    channel = client.get_channel(message.channel.id)
    if channel.name[0:1] == "☆":

        # ID用の日付取得
        send_message_date = today_string()

        # 送信されたメッセージの取得
        send_message = message.content

        if len(message.attachments):
            pic_url = message.attachments[0].url
            save_name = "riamu.jpg"
            save_pic(pic_url, save_name)
            discord_img = discord.File(save_name)

        # 送信されたメッセージの削除
        await message.delete()

        # ハッシュの作成
        athor_id = str(message.author.id)
        hs = get_hash_id(athor_id)

        # レス番号の確認
        async for res_message in channel.history(limit=1000):
            if len(res_message.embeds):
                res_num = int(res_message.embeds[0].title[0:4])
                break

        if res_num == 1001:
            return
        elif res_num >= 1001:
            embed = discord.Embed(title="1001" + "  1001  " + "Over1000 Thread", description="このスレッドは１０００を超えました。\nもう書けないので、新しいスレッドを立ててくださいです。。。", color=0x000000)
            await channel.send(embed=embed)
            return

        """
        最新のメッセージの取り方を確認
        メッセージの取り方
        channel.fetch_message(733137000130936914)

        レス番号だけ取り出す
        embeds[0].title[0:3]

        表示例
        001 腸まで届く名無しさん YYYY/MMM/DD(A) %H:%M:%S ID:XXXXXXX
        テスト

        IDは個人IDと日付を連結させた文字列をハッシュ化し真ん中を切り取ったもの

        1001 1001 Over 1000Thread
        このスレッドは１０００を超えました。
        もう書けないので、新しいスレッドを立ててくださいです。。。
        """

        # レス
        res_num += 1
        embed = discord.Embed(title=str(res_num).zfill(3) + "  腸まで届く名無しさん  " + send_message_date + "  ID:" + hs[10:17], description=send_message, color=0x000000)
        await channel.send(embed=embed)

        # 画像がある場合保持
        if len(message.attachments):
            await message.channel.send(file=discord_img)
            os.remove("riamu.jpg")


client.run(DISCORD_TOKEN)