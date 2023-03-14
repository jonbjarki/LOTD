import discord
import os
import datetime
from discord.ext import commands,tasks
from songs import Songs
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents)
TOKEN = os.getenv("LOTD_TOKEN")

songs = Songs()

# Channel to spit output the Lyric of the day
lotd_channel = 1085002849345339452

# Time when to refresh LOTD
LOTD_time = datetime.time(hour = 13,minute=25, tzinfo=datetime.timezone.utc)

class MyCog(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.new_lyric.start()

    def cog_unload(self) -> None:
        self.new_lyric.cancel()

    @tasks.loop(time=LOTD_time)
    async def new_lyric(self):
        # Outputs a new LOTD at a specific time every day
        output = ""
        channel = bot.get_channel(lotd_channel)
        last_correct_answer = songs.get_answer()
        lyric = songs.get_random_lyric()
        if last_correct_answer != None:
            output += f"The answer to the last LOTD was: ||{last_correct_answer['name']}||"

        await channel.send(output + "\n" + f"**The Lyric Of The Day**\n\n♪ {lyric} ♪")

@bot.event
async def on_ready():
    await bot.add_cog(MyCog(bot)) # starts listening for when to reset LOTD
    print('Bot is ready.')

@bot.command()
@commands.has_any_role("Mods", "Lil Mods", 810115393871544350) # ID Is AK's Role
async def lotd(ctx):
    """
    Resets the LOTD and outputs it
    """
    output = ""
    last_correct_answer = songs.get_answer()
    if last_correct_answer != None:
        output += f"The answer to the last LOTD was: ||{last_correct_answer['name']}||"
    lyric = songs.get_random_lyric()
    await ctx.send(output + "\n" + f"**The Lyric Of The Day**\n\n♪ {lyric} ♪")

@lotd.error
async def lotd_error(ctx,error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("You do not have permission to use this command")

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
async def guess_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("You need to give an answer")

if __name__ == "__main__":
    if TOKEN == None:
        print("No Token Found")
    else:
        bot.run(TOKEN)


