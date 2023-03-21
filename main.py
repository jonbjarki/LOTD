import discord
import os
import datetime
from discord.ext import commands, tasks
from songs import Songs
from json import load
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
# TOKEN = os.getenv("LOTD_TOKEN")
configFile = "config.json"
TOKEN = None

# Channel to spit output the Lyric of the day
lotd_channel = 1085337400517070920
bot_spam_channel = 1085340266535321700

# Fetches data from config
with open(configFile, "r") as f:
    data = load(f)
    TOKEN = data["token"]
    lotd_channel = data["lotd_channel"]
    bot_spam_channel = data["bot_spam_channel"]


songs = Songs()

# Time when to refresh LOTD
LOTD_time = datetime.time(hour=5, tzinfo=datetime.timezone.utc)


def new_lotd_message(lyric, last_answer):
    """
    Returns properly formatted message for displaying the LOTD
    """
    output = ""
    bot_channel = bot.get_channel(bot_spam_channel)
    if last_answer != None:
        output += f"The answer to the **last** LOTD was: ||{last_answer['name']}||"

    return output + "\n" + f"**The Lyric Of The Day**\n\n♪ {lyric} ♪\n\nMake your guess in {bot_channel.mention} using !guess (song)"


def get_new_lyric():
    """
    Gets a new random lyric and returns formatted string for displaying the lyric
    """
    last_correct_answer = songs.get_answer()
    lyric = songs.get_random_lyric()

    return new_lotd_message(lyric, last_correct_answer)


class MyCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.new_lyric.start()

    def cog_unload(self) -> None:
        self.new_lyric.cancel()

    @tasks.loop(time=LOTD_time)
    async def new_lyric(self):
        # Outputs a new LOTD at a specific time every day
        channel = bot.get_channel(lotd_channel)

        await channel.send(get_new_lyric())


@bot.event
async def on_ready():
    await bot.add_cog(MyCog(bot))  # starts listening for when to reset LOTD
    print('Bot is ready.')


@bot.command()
# ID Is AK's Role
@commands.has_any_role("Mods", "Lil Mods", 810115393871544350)
async def newlyric(ctx):
    """
    Resets the LOTD and outputs it
    """
    await ctx.send(get_new_lyric())


@newlyric.error
async def lotd_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You do not have permission to use this command")


@bot.command()
async def lotd(ctx):
    lyric = songs.get_lyric()
    if lyric is not None:
        await ctx.send("The current LOTD is: \n" + f"♪ {lyric} ♪")
    else:
        await ctx.send("There is currently no lyric, generate a new one with !newlyric")


@bot.command()
async def guess(ctx, *, answer):
    """
    Allows a person to guess the LOTD
    """
    todays_song = songs.todays_song
    if todays_song == None:
        await ctx.send("There is no lyric of the day")
        return
    for song in songs.songs:
        if song["ID"] == todays_song:
            if answer.lower() == song["name"].lower():
                await ctx.send(f"Correct! {ctx.author.mention} has guessed todays lyric")
                try:
                    await ctx.message.delete()
                except:
                    print("I do not have delete permissions")
            else:
                await ctx.send("Incorrect :( Try again!")
            return
    print("Something went wrong")


@guess.error
async def guess_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to give an answer")

if __name__ == "__main__":
    if TOKEN == None:
        print("No Token Found")
    else:
        bot.run(TOKEN)
