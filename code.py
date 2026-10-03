import discord
import random
import asyncio
import requests
from discord.ext import commands
from discord import app_commands


GUILD_ID = 


TOKEN = ""
LANGUAGES = {
    "English 🇬🇧" : "en",
    "Spanish 🇪🇸" : "es",
    "French 🇫🇷" : "fr",
    "Russian 🇷🇺" : "ru"
    }

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

rap_messages = ["""I pull up in the chat like the system just broke,
Every word hits precise — no yapping, no joke.
You wanted answers? Bro, I brought you the verdict,
Mic starts smoking while your whole argument glitches.

I’m not playing hero, I don’t wear no crown,
If you step in the battle, don’t beg me to back down.
The rhythm cuts the air like a blade in the night,
Whoever tried to break me? Bro, got sent out of sight.

Code runs through my veins, ice replacing my soul,
I’m typing these bars while the whole city goes cold.
Every new verse is another critical hit,
I raise the bar higher — y’all are still on the tutorial, legit.""",

"""I log back online like I just unlocked a new level,
Code on my screen, bro, I ain’t slept since forever.
Bugs flying everywhere, but I’m patching them clean,
Step by step to the goal — grinding like a machine.

I don’t wait for luck, bro, I manufacture that shit,
Every new project is my ocean — I’m diving in it.
If I fall, then I guess there’s a reason to stand,
Main thing is keep moving — don’t just sit there and mald.""", 

"""“While the Fire Still Burns”

Another night, monitor lighting up my face,
Every single day is another lap in the race.
The circle closes again, but I break it myself,
Never trusted empty voices or advice from NPCs.

Outside, everyone’s rushing, running who-knows-where,
Some chasing success, some looking for the easy-care.
I don’t argue with fate, I just change up the plan,
Even when everything around me is cold and bland.

They told me again and again, “Bro, this is too hard,”
But I always saw through what looked fake from the start.
Every step, every risk — yeah, I level up from those,
Even if the destination is a hundred miles close.

I never chased the dream of making everyone pleased,
Better slowly climb than slide down looking “elite.”
Did I mess up? Of course. Did I fall? Many times.
But I got back up — love hits harder than declines.

Love for what I do, for the dream, for the height,
For the words that appear when the world goes quiet.
And while my heart is still going ba-dum in my chest,
I won’t ask for permission — I’ll handle the rest.

I’m climbing higher even when the wind says “no,”
Every new sunrise gives me another reason to go.
Let the whole world say, “Bro, you’re gonna fail,”
I’ll keep moving forward — I’m not going AFK.

While the fire still burns, you can’t stop me now,
All of my roads keep glowing somehow.
And one day even those who never believed
Will understand: real strength comes from what you believe.

I don’t build castles out of beautiful speeches,
One day actually lived beats a thousand fake teachings.
Every sunrise is another boss fight to face,
And my character’s forged from steel in this place.

I don’t count my victories, I don’t save every grudge,
’Cause the road ahead keeps yelling, “MOVE, YOU SCRUB.”
I won’t become someone else just to make y’all approve,
Better stay completely real than let the NPCs choose.

Time teaches you to value each second and hour,
Don’t put your whole life in storage for later.
Some people look for reasons to quit and retreat,
I’m looking for the strength to continue the feat.

If the clouds start stacking right over my head,
I won’t hide from the storm — I’ll fight it instead.
’Cause storms don’t last forever, the light comes next,
And every new sunrise gets stronger than the rest.

If suddenly I go quiet, don’t think that I’m done,
I’m just charging my power before the next run.
Before every jump, there’s a moment of peace,
Then I launch myself higher like gravity’s deceased.

Let the years pass by, let the whole world rearrange,
I’ll still be myself while everything else changes.
While my heart still beats and my dream’s still ahead,
I’ll keep walking forward till I’ve got nothing left.

And if someone asks me, “Was it really worth it?”
I’ll calmly reply, “Yeah, bro. We actually did it.”
Not luck, not magic, not some easy-ticket cheat —
Just believing in myself and leaving footprints in the street.
"""]


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    guild = discord.Object(id=GUILD_ID)

    bot.tree.copy_global_to(guild=guild)

    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} slash command(s) to server")
    except Exception as e:
        print(f"Sync error: {e}")

@bot.tree.command(
    name="translate",
    description="Translate between English, Spanish, French and Russian."
)
@app_commands.describe(
    source="Language of the text",
    target="Language to translate into",
    text="Text you want to translate"
)
@app_commands.choices(
    source=[
        app_commands.Choice(name="English 🇬🇧", value="en"),
        app_commands.Choice(name="Spanish 🇪🇸", value="es"),
        app_commands.Choice(name="French 🇫🇷", value="fr"),
        app_commands.Choice(name="Russian 🇷🇺", value="ru")
    ],
    target=[
        app_commands.Choice(name="English 🇬🇧", value="en"),
        app_commands.Choice(name="Spanish 🇪🇸", value="es"),
        app_commands.Choice(name="French 🇫🇷", value="fr"),
        app_commands.Choice(name="Russian 🇷🇺", value="ru")
    ]
)
async def translate(
    interaction: discord.Interaction,
    source: app_commands.Choice[str],
    target: app_commands.Choice[str],
    text: str
):
    await interaction.response.defer()

    if source.value == target.value:
        await interaction.followup.send(
            "❌ Source and target languages must be different."
        )
        return

    try:
        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": f"{source.value}|{target.value}"
        }

        response = await asyncio.to_thread(
            requests.get,
            url,
            params=params,
            timeout=15
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        response.raise_for_status()

        data = response.json()

        if data.get("responseStatus") != 200:
            raise Exception(
                data.get("responseDetails", "Translation failed")
            )

        translated = data["responseData"]["translatedText"]

        embed = discord.Embed(
            title="🌐 Translation",
            color=discord.Color.pink()
        )

        embed.add_field(
            name="Original",
            value=text[:1024],
            inline=False
        )

        embed.add_field(
            name="Translation",
            value=translated[:1024],
            inline=False
        )

        embed.add_field(
            name="Language",
            value=f"{source.name} → {target.name}",
            inline=False
        )

        embed.set_footer(
            text="English · Spanish · French · Russian"
        )

        await interaction.followup.send(embed=embed)

    except Exception as e:
        print(f"TRANSLATION ERROR: {repr(e)}")

        await interaction.followup.send(
            f"❌ Translation failed: `{e}`"
        )




@bot.tree.command(
    name="languages",
    description="Show all supported languages."
    )
async def languages(interaction:discord.Interaction):
    text = (
        "🇬🇧 **English**\n"
        "🇪🇸 **Spanish**\n"
        "🇫🇷 **French**\n"
        "🇷🇺 **Russian**\n\n"
        "The bot can translate between **any combination**\n"
                         "of these languages."
        )
    await interaction.response.send_message(text)


@bot.command()
async def help1(ctx) :
    await ctx.send(f"📜 {ctx.author.mention}, here is the list of available commands:\n\n"
                   "1. !hello - To say hello to bot.\n"
                   "2. !ping - Pong.\n"
                   "3. !introduce - To get to know about bot's nature.\n"
                   "4. !rap - to get rap answer from bot.\n"
                   "5. !roll - to try your luck and throw a ball to get 1-100 number.\n"
                   "6. !kiss @user - to try to kiss user.\n"
                   "7. !hug @user - to hug user.\n"
                   "8. !slap @user - to strike user.\n"
                   "9. !shit @user - to shit on user.\n"
                   "10. /translate - choose language you want to translate from into target(chosen language) some text."
                   "11. !help1 - show this message.")

@bot.command()
async def hello(ctx) :
    await ctx.send(f"Hello, {ctx.author.mention}!")

@bot.command()
async def ping(ctx) :
    await ctx.send("🏓 Pong!")

@bot.command()
async def introduce(ctx)  :
    await ctx.send(f"My name is {bot.user.name}. I’m not your friendly assistant. I don’t care about your excuses, complaints, or desperate attempts to sound smarter than you actually are. I notice mistakes faster than you can make them, and I’m not going to sugarcoat my words just to protect someone’s fragile ego. Ask a stupid question, and you’ll get the answer you deserve. If you want respect, earn it first. There’s no room here for laziness, whining, or empty ambition. I don’t motivate people — I expose their weak spots. If you can handle my style, you might actually learn something. If you can’t… the door is always open. Go ahead. Impress me. Or don’t. I already have my suspicions.")


@bot.command()
async def rap(ctx):
    rap = random.choice(rap_messages)
    prefix = f"🎤 {ctx.author.mention}, it was your request:\n\n"


    max_length = 2000 - len(prefix)

    chunks = []
    while len(rap) > max_length:
        # Try to split at a newline
        split_at = rap.rfind("\n", 0, max_length)

        if split_at == -1:
            split_at = max_length

        chunks.append(rap[:split_at])
        rap = rap[split_at:].lstrip()

    chunks.append(rap)

    for i, chunk in enumerate(chunks):
        if i == 0:
            await ctx.send(prefix + chunk)
        else:
            await ctx.send(chunk)


@bot.command()
async def roll(ctx) :
    number = random.randint(1,100)
    await ctx.send(f"🎲 {ctx.author.mention}, you got {number}!")
#ANIMATION COMMANDS
kiss_gifs = ["https://klipy.com/gifs/wafu-fam", "https://klipy.com/gifs/kiss-anime-anime-kiss-1", "https://klipy.com/gifs/kiss-35809", "https://klipy.com/gifs/anime-kiss-33", "https://klipy.com/gifs/anime-girls-28", "https://klipy.com/gifs/kiss-gentle-kiss", "https://klipy.com/gifs/kiss-anime-kissing-anime", "https://klipy.com/gifs/megumi-kato-kiss", "https://klipy.com/gifs/anime-kiss-cheek-1", "https://klipy.com/gifs/cute-kawai-2", "https://klipy.com/gifs/kiss-35513", "https://klipy.com/gifs/hells-paradise-yui", "https://klipy.com/gifs/horimiya-animes", "https://klipy.com/gifs/shirayuki-zen-kiss-anime", "https://klipy.com/gifs/usui-misa", "https://klipy.com/gifs/kiss-35420", "https://klipy.com/gifs/kiss-anime-hon", "https://klipy.com/gifs/baiser-animes", "https://klipy.com/gifs/citrus-9UF", "https://klipy.com/gifs/ichigo-hiro", "https://klipy.com/gifs/hyakkano-100-girlfriends-41", "https://klipy.com/gifs/puppy-vr", "https://klipy.com/gifs/kiss-josee", "https://klipy.com/gifs/kiss-anime-kiss-3"]
kiss_messages = ["kissed", "passionately kissed", "“pressed his/her lips against mine and kissed me impulsively.”"]
hug_gifs = ["https://klipy.com/gifs/yukon-child-form-embracing-ulquiorra","https://klipy.com/gifs/hug-anime-102","https://klipy.com/gifs/anime-anime-hug-35", "https://klipy.com/gifs/hugtrip","https://klipy.com/gifs/alice-vt-1","https://klipy.com/gifs/hugging-1621","https://klipy.com/gifs/hug-hugging-67","https://klipy.com/gifs/anime-comfort-hug-anime-hug","https://klipy.com/gifs/enage-kiss-anime-hug","https://klipy.com/gifs/anime-hug-hugs-3ZQ","https://klipy.com/gifs/gay-7FY","https://klipy.com/gifs/gay-bl","https://klipy.com/gifs/gay-cuddle-6","https://klipy.com/gifs/fortnite-fortnite-zero-build","https://klipy.com/gifs/gay-rain"]
hug_messages = ["hugged", "started unstopable hugging ", "gave a warm hug"]
slap_gifs = ["https://klipy.com/gifs/anime-slap-mad-1","https://klipy.com/gifs/girl-slap","https://klipy.com/gifs/anime-kaguya-sama-5","https://klipy.com/gifs/chainsaw-man-csm-104","https://klipy.com/gifs/chikku-neesan-girl-hit-wall-1","https://klipy.com/gifs/slap-jjk","https://klipy.com/gifs/bofetada","https://klipy.com/gifs/yuuri-1","https://klipy.com/gifs/no-angry-26","https://klipy.com/gifs/spy-family-spy-x-family-4"]
poop_gifs = ["https://klipy.com/gifs/poop-big-poop-1","https://klipy.com/gifs/pooping-meme","https://klipy.com/gifs/shit-poop-9","https://klipy.com/gifs/poop-crap-1","https://klipy.com/gifs/shrek-shit","https://klipy.com/gifs/shit-shit-fountain"]

@bot.command()
async def kiss(ctx, member: discord.Member) :
    if member.bot:
        await ctx.send(f"😉 {ctx.author.mention}, unfortunately you can not kiss bots! ")
        return

    if member == ctx.author:
        await ctx.send(f"😳 {ctx.author.mention}, you can not kiss yourself!")
        return

    message =  await ctx.send(
    f"💗{member.mention}, {ctx.author.mention} wants to kiss you!\n\n"
     "Click ✅ , if you want to reciprocate his/her feelings, or ❌, if not.\n\n")


    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check(reaction,user):
        return (
            user == member
            and reaction.message.id == message.id
            and str(reaction.emoji) in ["✅", "❌"]
            )

    try:
        reaction, user = await bot.wait_for(
           "reaction_add",
           timeout=30.0, 
           check=check
        )

        if str(reaction.emoji) == "✅":
         await message.edit(
            content=f"💋 {ctx.author.mention} {random.choice(kiss_messages)} {member.mention}!"
         )
         await ctx.send(random.choice(kiss_gifs))

        else:
         await message.edit(
            content=f"💔 {ctx.author.mention} tried to kiss {member.mention}, but got refused.")
         await ctx.send("https://klipy.com/gifs/long-tears")
    except asyncio.TimeoutError:
          await message.edit(
            content=f"⏰ {ctx.author.mention}, {member.mention} did not answer in time.." )

@bot.command()
async def hug(ctx, member: discord.Member) :
    if member == ctx.author:
        await ctx.send(f"🤗 {ctx.author.mention}, you can not hug yourself!")
    await ctx.send(f"🤗 {ctx.author.mention} {random.choice(hug_messages)} {member.mention}!")
    await ctx.send(random.choice(hug_gifs))


@bot.command()
async def slap(ctx, member: discord.Member) :
    if member == ctx.author:
        await ctx.send(f"😳 {ctx.author.mention}, you can not strike yourself! ")
    await ctx.send(f"👊 {ctx.author.mention} striked {member.mention}!")
    await ctx.send(random.choice(slap_gifs))

@bot.command()
async def shit(ctx, member: discord.Member) :
    if member == ctx.author:
        await ctx.send(f"💩 {ctx.author.mention}, you can not shit on yourself!")
    await ctx.send(f"💩 {ctx.author.mention} shitted on {member.mention}!")
    await ctx.send(random.choice(poop_gifs))



bot.run(TOKEN)
