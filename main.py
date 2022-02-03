import discord, os, asyncio, pytz, datetime, random, sys, re
from collections import deque
from discord.ext import commands, tasks
from discord_together import DiscordTogether, errors as dte

try:
	import weather
except:
	print( "weather.py is missing. Bot will not be able to use weather command." )
	pass
try:
	from keep_alive import keep_alive
except:
	print( "keep_alive.py is missing. Although optional, UptimeRobot will not be able to monitor bot uptime status." )
	pass

listener = "db ", "deebee ", "DB ", "DEEBEE ", "Db ", "DeeBee ", "Deebee "
greeting = ['hello', 'hi']
positive = ['true', 't']
negative = ['false', 'f']
mf = ['motherfucker', 'modafaka', 'motherfuka', 'madafaka', 'mdfk', 'mfkr']
msgTrigA = ['wiggle', 'popcat', 'catjam', 'new pc', 'blobdance', 'pepeds']
msgTrig = ['bij', 'bitch']
msgYEP = ['sock', 'cock', 'rock', 'dock', 'duck', 'stock', 'clock', 'croc', 'lock', 'knock', 'mock', 'jock']
dicelist = {'d','r'}
bot = commands.Bot( command_prefix=listener, intents=discord.Intents.all(), owner_id=int(os.environ['discord-user_d.b']), strip_after_prefix=True )

def emote(animated, emojiName):
	eName = emojiName.lower()
	for i in bot.emojis:
		j = str(i)
		if animated is True:
			if eName in j.lower() and '<a:' in j.lower():
				return j
		elif animated is False:
			if eName in j.lower() and '<a:' not in j.lower():
				return j
		else:
			return "Argument `animated` is missing."
	if animated == False:
		return "`Error retrieving emote. Check name or spelling.`"
	elif animated == True:
		return "`Error retriving animated emote. Check name or spelling.`"

# actually fixed this using RegEx
def roll(start:int, kind:str=None, stop:int=None):
	out:int = 0
	if start <= 0 or stop <= 0:
		return 'Cannot roll ' +start+ ' amount of dice with '+stop+' amount of sides.'
	if kind is None:
		return f'Invalid input: missing argument \'kind\''
	elif kind == 'd':
		if start <= 9999:
			for i in range(1,start+1):
				out:int = out + random.randint(1,stop)
			return out
		else:
			return f'Not enough memory to calculate {str(start)} amount of dice.'
	#elif kind == 'r':
		# insert stuff later

async def bot_startled(author:str):
	if author != os.environ['discord-user_d.b']:
		return emote(False, "bij") + ' what? <@' + author + '>'
	elif author == os.environ['discord-user_d.b']:
		return 'eyy <@' + author + '>! what\'s up'
	else:
		await debug(msg='author id: ' + author)
		return 'Command broke, check debug channel, and console.'

async def debug( msg:str = None, pre_msg:int = None, cid:int = int( os.environ[ 'discord-channel_debug' ] ) ):
	if pre_msg is not None:
		switcher = {
			0:"InfNo:0: Process ended",
			1:"InfNo:1: Process started",
			2:"InfNo:2: Waiting for minutes to turn 00",
			3:"InfNo:3: Weather loop started",
			4:"InfNo:4: Weather animation sent"
		}
		message = switcher.get( pre_msg, "Warning: Error getting pre-determined message" )
	elif msg is not None:
		message = "Custom: " + msg
	else:
		message = "Warning: Generic debug message"

	channel = bot.get_channel( cid )
	ts = datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '(%b %d, %Y - %X): ' )
	await channel.send( "`" + ts + message + "`" )
	return

## 
## SCHEDULERS ##
##

if 'weather' in sys.modules:
	@tasks.loop( hours=1 )
	async def sched_weather():
		hours = int( datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '%H' ) )
		print( "Another hour has passed: " + str( hours + 1 ) )
		channel = bot.get_channel( int( os.environ[ 'discord-channel_vii-weather' ] ) )

		if hours == 9 or hours == 13:
			await debug(pre_msg=1)
			weather.weather('latest')
			async with channel.typing():
				await asyncio.sleep(30)
			await channel.send("__2 hour interval__ mid-day daily weather images", file = discord.File('out.mp4'))

		if hours % 4 == 3:
			await debug( pre_msg = 1 )
			weather.weather( 'latest' )
			async with channel.typing():
				await asyncio.sleep( 30 )
			await channel.send(  "__4 hour interval__ daily weather images", file = discord.File( 'out.mp4' ) )

		if os.path.exists(weather.target):
			await debug( pre_msg = 4 )
			weather.clean()
			await debug( pre_msg = 0 )

	@sched_weather.before_loop
	async def before():
		minutes = int( datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '%M' ) )
		seconds = int( datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '%S' ) )
		wait = 3600 - ( ( ( minutes + 1 ) * 60 ) + ( seconds - 30 ) )
		print("weather waiting")
		await asyncio.sleep( wait )
		await bot.wait_until_ready()

@bot.event
async def on_ready():
	print(f'logged in as {bot.user}')

	name = "\'db help\'"
	act = discord.ActivityType.listening

	activity = discord.Activity( name=name, details='Testing', type=act )
	await bot.change_presence( activity=activity, status=discord.Status.online, afk=False )

	bot.vca = await DiscordTogether(os.getenv( 'TOKEN' ))

@bot.event
async def on_message(msg):
	msgCont = []
	msgCont = msg.content.lower().split(' ')

	mTrigA = (cont for cont in msgCont if cont in msgTrigA)
	mTrig = (cont for cont in msgCont if cont in msgTrig)
	mYep = (cont for cont in msgCont if cont in msgYEP)

	if (msg.author == bot.user) and ((msg.channel.id == int(os.environ['discord-channel_vii-weather']) and msg.attachments)) or (msg.channel.id == int(os.environ['discord-channel_vii_days-before-xmas'])):
		await asyncio.sleep(3)
		await msg.publish()

	# if message author is itself or another bot, ignore it
	if msg.author == bot.user or msg.author.bot:
		return
	if not (msg.content.startswith(listener)):
		for cont in mTrigA:
			if cont == 'wiggle':
				if msg.reference is None:
					await msg.add_reaction(emoji=emote(True, cont))
				elif msg.reference is not None:
					refmsg = await msg.channel.fetch_message(msg.reference.message_id)
					await refmsg.add_reaction(emoji=emote(True, cont))
			elif cont in {'blobdance', 'pepeds'}:
				await msg.channel.send(
						emote(True, cont) + emote(True, cont) + emote(True, cont))
			else:
				await msg.channel.send(emote(True, cont))
		for cont in mTrig:
			cont = 'bij' if cont == 'bitch' else cont
			await msg.add_reaction(emoji=emote(False, cont))
		for cont in mYep:
			await msg.add_reaction(emoji=emote(False, 'yep'))

	if (bot.user in msg.mentions) or ("bitches" in msg.content.lower()):
		await msg.channel.send(content=await bot_startled(str(msg.author.id)), reference=msg, mention_author=True)

	for cont in mf:
		if ( cont in msg.content.lower() ) and str( msg.author.id ) != os.environ[ 'discord-user_d.b' ]:
			await msg.channel.send(content="no u.", reference=msg, mention_author=True)

	if 'new pc' in msg.content.lower():
		await msg.channel.send(content=emote(False, "mmmseks") + emote(False, "mmmseks") + emote(False, "mmmseks"), reference=msg, mention_author=True)
		await msg.add_reaction(emoji=emote(False, "mmmseks"))

	details = f"```{str(datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ))}\n# Author: {msg.author.name}\n# Server Name: {msg.guild.name}\n# Channel Name: {msg.channel.name}\n\n{msg.content}```"
	if msg.guild.id != int(os.environ['discord-guild_migs-server']) and msg.guild.id != int(os.environ['discord-guild_beaneyboo-server']) and msg.guild.id != int(os.environ['discord-guild_db-server']):
		if msg.attachments:
			channel = bot.get_channel(int(os.environ['discord-channel_images-archive']))
			for i in msg.attachments:
				await channel.send(details, file=await i.to_file())
		if not msg.attachments:
			channel = bot.get_channel(int(os.environ['discord-channel_text-archive']))
			await channel.send(details)

	if msg.guild.id == int(os.environ['discord-guild_foxy-server']):
		channel = bot.get_channel(int(os.environ['discord-channel_foxy-archive']))
		if msg.attachments:
			for i in msg.attachments:
				att = await i.to_file()
				await channel.send(details, file=att)
		if not msg.attachments:
			await channel.send(details)

	if msg.guild.id == int(os.environ['discord-guild_beaneyboo-server']) and (msg.channel.id != int(os.environ['discord-channel_beaneyboo-mods-priv']) and msg.channel.id != int(os.environ['discord-channel_beaneyboo-moderator-only']) and msg.channel.id != int(os.environ['discord-channel_beaneyboo-msg-archiving'])):
		channel = bot.get_channel(int(os.environ['discord-channel_beaneyboo-msg-archiving']))
		if msg.attachments:
			for i in msg.attachments:
				att = await i.to_file()
				await channel.send(details, file=att)
		if not msg.attachments:
			await channel.send(details)

	if msg.channel.id in [int(os.environ['discord-channel_beaneyboo-announcement'])]:
		await asyncio.sleep(3)
		await msg.publish()

	else: # process discord.ext.commands
		await bot.process_commands(msg)

##
## BOT COMMANDS ##
##

@bot.command( name='troll', hidden=True )
async def troll(ctx):
	#cnl = bot.get_channel( int( os.environ['discord-channel_vii_days-before-xmas'] ) )
	msg = f"<@{os.environ['discord-user_d.b']}> gae."
	await ctx.send(content=msg)

@bot.command( name='hello', aliases=['hi'], description="Greet user with Hello!" )
async def bot_greet(ctx):
	await ctx.send(content='Hello!', reference=ctx.message, mention_author=True)

@bot.command( name='guild', description="Return the current Server ID. For debugging.", hidden=True )
async def guild(ctx, channel_id:int=None):
	if channel_id is None:
		await ctx.send(str(ctx.message.guild.id))
	else:
		chn = bot.get_channel(channel_id)
		if chn is not None:
			await chn.send(content="``` ```")

@bot.command( name='emote', description="Send any emote from servers the bot is in." )
async def send_emote(ctx, name:str, animated:bool = False):
	await ctx.send( emote( animated, name ) )

'''@bot.command( name='sticker', enabled=False, hidden=True, description="Send any sticker from servers the bot is in." )
async def send_sticker(ctx, name:str):
	await ctx.send(  )'''

@bot.command( name='weather', description="Send animated weather satelite images as mp4 video file." )
async def send_weather(ctx):
	if 'weather' not in sys.modules:
		await ctx.send(content="Weather module was not imported. Please check console for problems.")
		return None
	await debug( msg="Requested weather command" )
	await ctx.send( content="Please wait 1 minute. Generating __requested__ images.", delete_after=33.0, reference=ctx.message, mention_author=False )
	weather.weather( 'latest' )
	async with ctx.typing():
		await asyncio.sleep(30)
	await ctx.send(content="Please use weather command sparingly. Bot might get banned for using too much resource.", file=discord.File('out.mp4'), reference=ctx.message, mention_author=True)
	await debug( pre_msg=4 )
	weather.clean()
	await debug( pre_msg=0 )

@bot.command( name='bitch', aliases=['bij'], hidden=True )
async def bitch_react(ctx):
	await ctx.send(content=await bot_startled(str(ctx.author.id)), reference=ctx.message, mention_author=False)

@bot.command( name='vca', description='Start Discord Together / Voice Chat Activities' )
async def vca(ctx, app_name=None):
	if (app_name != 'list') and (app_name is not None):
		try:
			vcid = ctx.author.voice.channel.id
			valid_app = [['youtube', 'yt', 'wt'], ['poker', 'pn'], 'chess', 'betrayal', 'fishing', ['letter-league', 'lt'], ['word-snack', 'ws'], ['sketch-heads', 'sh'], ['spellcast', 'sc'], 'awkword', 'checkers']

			if app_name in valid_app[0]:
				vcal = await bot.vca.create_link(vcid, 'youtube', max_age=300)
			elif app_name in valid_app[1]:
				vcal = await bot.vca.create_link(vcid, 'poker', max_age=300)
			elif app_name in valid_app[2]:
				vcal = await bot.vca.create_link(vcid, 'chess', max_age=300)
			elif app_name in valid_app[3]:
				vcal = await bot.vca.create_link(vcid, 'betrayal', max_age=300)
			elif app_name in valid_app[4]:
				vcal = await bot.vca.create_link(vcid, 'fishing', max_age=300)
			elif app_name in valid_app[5]:
				vcal = await bot.vca.create_link(vcid, 'letter-league', max_age=300)
			elif app_name in valid_app[6]:
				vcal = await bot.vca.create_link(vcid, 'word-snack', max_age=300)
			elif app_name in valid_app[7]:
				vcal = await bot.vca.create_link(vcid, 'sketch-heads', max_age=300)
			elif app_name in valid_app[8]:
				vcal = await bot.vca.create_link(vcid, 'spellcast', max_age=300)
			elif app_name in valid_app[9]:
				vcal = await bot.vca.create_link(vcid, 'awkword', max_age=300)
			elif app_name in valid_app[10]:
				vcal = await bot.vca.create_link(vcid, 'checkers', max_age=300)
			else:
				vcal = None

			if vcal is not None:
				await ctx.send(f'Join the Voice Chat Activity: {vcal}\nValid only for 5 minutes.', delete_after=300.0)
			elif vcal is None:
				await ctx.send(f'Invalid app code: `{app_name}`')
		except AttributeError:
			await ctx.send('Join a VC first!')
		except dte.BotMissingPerms:
			await ctx.send('`I can\'t seem to create an invite link.\nMake sure users are allowed to make an invite link to the VC.\n(Check VC permissions)`')
	elif (app_name == 'list') or (app_name is None):
			embed=discord.Embed(title="Discord Together Applications", description="Available applications for Discord Together")
			embed.add_field(name="Watch Together", value="[yt, youtube, wt]", inline=False)
			embed.add_field(name="Poker Night", value="[poker, pn]", inline=False)
			embed.add_field(name="Chess in the Park", value="[chess]", inline=False)
			embed.add_field(name="Betrayal.io", value="[betrayal]", inline=False)
			embed.add_field(name="Fishington.io", value="[fishing]", inline=False)
			embed.add_field(name="Letter League", value="[letter-league, lt]", inline=False)
			embed.add_field(name="Word Snack", value="[word-snack, ws]", inline=False)
			embed.add_field(name="Sketch Heads", value="[sketch-heads, sh]", inline=False)
			embed.add_field(name="SpellCast", value="[spellcast, sc]", inline=False)
			embed.add_field(name="Awkword", value="[awkword]", inline=False)
			embed.add_field(name="Checkers in the Park", value="[checkers]", inline=False)
			embed.set_footer(text="Example: `db vca youtube` to start a Watch Together session.")
			await ctx.send(embed=embed, reference=ctx.message, mention_author=True)

'''@bot.command(name='embed', description="Manually send an embed message.")
async def manual_embed(ctx)'''

@bot.command( name='roll', description="Roll a dice." )
async def roll_cmd(ctx, dice_notation:str):
	dice = dice_notation.lower()
	try:
		divd = deque([int(temp) if temp.isdigit() else temp for temp in re.match(r'([a-z]+)([0-9]+)',dice).groups()])
		divd.appendleft(1)
	except AttributeError:
		try:
			divd = deque([int(temp) if temp.isdigit() else temp for temp in re.match(r'([0-9]+)([a-z]+)([0-9]+)',dice).groups()])
		except AttributeError:
			raise commands.BadArgument("Bad argument: Invalid input.\nUse simple dice notation. Algebraic expressions not yet supported.")
	if divd[1] not in dicelist:
		raise commands.BadArgument(f"BadArgument: Invalid dice type.\n\'{divd[1]}\' is not a valid type of dice.")
	await ctx.send(content=roll(divd[0],divd[1],divd[2]), reference=ctx.message, mention_author=False)

##
## SLASH COMMANDS ##
##

'''@slash.slash(name="test")
async def test(ctx: SlashContext):
	embed = discord.Embed(title="Embed test", description=":p", colour=discord.Colour(0xd6b4d8))
	await ctx.send(content="test", embeds=[embed])

@slash.context_menu(name="apps test", target=3)
async def ctx_menu_test(ctx: SlashContext):
	embed = discord.Embed(title="Apps test", description="yep, another test, but this time from Apps menu :p BTW, there's a \"hidden\" command ;)", colour=discord.Colour(0xd6b4d8))
	await ctx.send(content="yes, this is a test.. again", embeds=[embed])

@slash.slash(name="hidden")
async def hidden_test(ctx: SlashContext):
	await ctx.send(content="d: sapnu puas", hidden=True)

@slash.context_menu(name="context", target=3, guild_ids=[int(os.environ['discord-guild_db-server'])])
async def context_test(ctx: MenuContext):
	print( ctx.data )
	await ctx.send("check console", hidden=True)

@slash.slash(name="vca")
async def slash_vca(ctx: SlashContext, app='list'):
	await vca(ctx, app)
	await ctx.send('vca test')'''
##
## ERROR HANDLER(S) ##
##

@bot.event
async def on_command_error(ctx, error):
	bad_cmd = (commands.MissingRequiredArgument, commands.BadArgument, commands.BadBoolArgument, commands.TooManyArguments)

	if isinstance(error, commands.CommandNotFound):
		await ctx.send( f"`{error}`", delete_after=5.0, reference=ctx.message, mention_author=False )
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have permission to use this command.", delete_after=5.0, reference=ctx.message, mention_author=True)
	elif isinstance(error, commands.BotMissingPermissions):
		await ctx.send("I can\'t seem to create an invite link :/")
	elif isinstance(error, bad_cmd):
		await ctx.send(f"""```md
Error in command
{error}
# Message will delete after 15 seconds.

<Usage: {ctx.command} {ctx.command.signature}>
```""", delete_after=15.0, reference=ctx.message, mention_author=False)
	else:
		await ctx.send(f"""```md
General ext.commands error
{error}
<Command: {ctx.command}>
<Message: {ctx.message.content}>```""", delete_after=15.0, reference=ctx.message, mention_author=False)

###
### RUN EVERYTHING ###
###

if 'weather' in sys.modules:
	sched_weather.start()
if 'keep_alive' in sys.modules:
	keep_alive()

loop = asyncio.get_event_loop()
bot_loop = loop.create_task(bot.start(os.getenv('TOKEN'), bot=True))
loops = asyncio.gather(bot_loop, loop=loop)
loop.run_until_complete(loops)

#bot.run(os.getenv( 'TOKEN' ))