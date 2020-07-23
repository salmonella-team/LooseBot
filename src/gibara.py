from discord.ext import commands

import setting

GIBARA_TOKEN = setting.GIBARA_TOKEN
MAKE_CHANNEL_CATEGORY_ID = setting.MAKE_CHANNEL_CATEGORY_ID

bot = commands.Bot(command_prefix="/gibara ")

@bot.command()
async def make2ch(ctx, *args):
    category_id = int(MAKE_CHANNEL_CATEGORY_ID)
    category = ctx.guild.get_channel(category_id)
    print(category)
    if len(args) < 2:
        new_channel = await ctx.guild.create_text_channel(name=args[0], category=category)
    else:
        await ctx.send("引数が不正")

bot.run(GIBARA_TOKEN)