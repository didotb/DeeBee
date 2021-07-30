import discord, os, asyncio, pytz, datetime, random, sys
from discord.ext import commands, tasks
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

listener = "db ", "deebee "
intents = discord.Intents.default()
intents.members = True
greeting = ['hello', 'hi']
positive = ['true', 't']
negative = ['false', 'f']
mf = ['motherfucker', 'modafaka', 'motherfuka', 'madafaka']
msgTrigA = ['wiggle', 'popcat', 'catjam', 'new pc', 'blobdance', 'pepeds']
msgTrig = ['bij', 'bitch']
msgYEP = ['sock', 'cock', 'rock', 'dock', 'duck', 'stock', 'clock', 'croc', 'lock', 'knock', 'mock', 'jock']
bot = commands.Bot( command_prefix=listener, intents=intents, owner_id=int(os.environ['discord-user_d.b']), strip_after_prefix=True )

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
			return "argument: animated not initialized"
	if animated == False:
		return "`Error retrieving emote. Check name or spelling.`"
	elif animated == True:
		return "`Error retriving animated emote. Check name or spelling.`"

def roll(start, stop):
	if start == '':
		start = 1
	if stop == '':
		return 'Error in command argument. -> second argument is empty.'
	try:
		fi = int(start)
	except ValueError:
		return 'Error in command argument. -> '+start+' is not a valid integer.'
	try:
		si = int(stop)
	except ValueError:
		return 'Error in command argument. -> '+stop+' is not a valid integer.'
	out:int = 0
	if fi <= 0 or si <= 0:
		return 'Cannot roll ' +start+ ' amount of dice with '+stop+' amount of sides.'
	if fi <= 9999:
		for i in range(1,fi+1):
			out:int = out + random.randint(1,si)
		return out
	else:
		return 'Not enough memory. -> '+str(fi)

async def bot_startled(author:str):
	if author != os.environ['discord-user_d.b']:
		return emote(False, "bij") + ' what? <@' + author + '>'
	elif author == os.environ['discord-user_d.b']:
		return 'eyy <@' + author + '>! what\'s up'
	else:
		await debug(msg='author id: ' + author)
		return 'Command has broken, check debug channel, and console.'

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

if 'weather' in sys.modules:
	@tasks.loop( hours=1 )
	async def sched_weather():
		hours = int( datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '%H' ) )
		print( "Another hour has passed: " + str( hours + 1 ) )
		channel = bot.get_channel( int( os.environ[ 'discord-channel_vii-weather' ] ) )

		if hours % 2 == 1 and (10 <= hours <= 14):
			await debug(pre_msg=1)
			weather.weather('latest')
			async with channel.typing():
				await asyncio.sleep(30)
			await channel.send("__2 hour interval__ mid-day daily weather images", file = discord.File('out.mp4'))
			await debug(pre_msg=4)
			weather.clean()
			await debug(pre_msg=0)

		if hours % 4 == 3:
			await debug( pre_msg = 1 )
			weather.weather( 'latest' )
			async with channel.typing():
				await asyncio.sleep( 30 )
			await channel.send(  "__4 hour interval__ daily weather images", file = discord.File( 'out.mp4' ) )
			await debug( pre_msg = 4 )
			weather.clean()
			await debug( pre_msg = 0 )

	@sched_weather.before_loop
	async def before():
		minutes = int( datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '%M' ) )
		seconds = int( datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '%S' ) )
		wait = 3600 - ( ( ( minutes + 1 ) * 60 ) + ( seconds - 30 ) )
		await asyncio.sleep( wait )
		await bot.wait_until_ready()

@bot.event
async def on_ready():
	print('logged in as {0.user}'.format(bot))

	name = "db help"
	act = discord.ActivityType.listening

	activity = discord.Activity( name=name, details='Testing', type=act )
	await bot.change_presence( activity=activity, status=discord.Status.online, afk=False )

@bot.event
async def on_message(msg):
	msgCont = []
	msgCont = msg.content.lower().split(' ')

	mTrigA = (cont for cont in msgCont if cont in msgTrigA)
	mTrig = (cont for cont in msgCont if cont in msgTrig)
	mYep = (cont for cont in msgCont if cont in msgYEP)

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

	if msg.guild.id != int(os.environ['discord-guild_migs-server']) and msg.guild.id != int(os.environ['discord-guild_beaneyboo-server']) and msg.guild.id != int(os.environ['discord-guild_db-server']):
		details = '`'+ str(datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) )) +'`\n# Author: `'+ msg.author.name +'`\n# Server Name: `'+ msg.guild.name +'`\n# Channel Name: `'+ msg.channel.name +'`\n'+ msg.content
		if msg.attachments:
			channel = bot.get_channel(int(os.environ['discord-channel_images-archive']))
			for i in msg.attachments:
				await channel.send(content=details, file=await i.to_file())
		if not msg.attachments:
			channel = bot.get_channel(int(os.environ['discord-channel_text-archive']))
			await channel.send(content=details)

	if msg.guild.id == int(os.environ['discord-guild_beaneyboo-server']) and (msg.channel.id != int(os.environ['discord-channel_beaneyboo-mods-priv']) and msg.channel.id != int(os.environ['discord-channel_beaneyboo-moderator-only']) and msg.channel.id != int(os.environ['discord-channel_beaneyboo-msg-archiving'])):
		channel = bot.get_channel(int(os.environ['discord-channel_beaneyboo-msg-archiving']))
		details = '`'+ str(datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) )) +'`\n# Author: `'+ msg.author.name +'` Channel Name: `'+ msg.channel.name +'`\n'+ msg.content
		if msg.attachments:
			for i in msg.attachments:
				att = await i.to_file()
				await channel.send(content=details, file=att)
		if not msg.attachments:
			await channel.send(content=details)

	if msg.channel.id == int(os.environ['discord-channel_beaneyboo-announcement']):
		await asyncio.sleep(3)
		await msg.publish()

	else: # process discord.ext.commands
		await bot.process_commands(msg)

##
## BOT COMMANDS ##
##

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

@bot.command( name='sticker', enabled=False, hidden=True, description="Send any sticker from servers the bot is in." )
async def send_sticker(ctx, name:str):
	await ctx.send(  )

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

@bot.command( name='roll', description="Roll a dice." )
async def roll_cmd(ctx, dice:str):
	splint = dice.split('d')
	await ctx.send(content=roll(splint[0],splint[1]), reference=ctx.message, mention_author=False)

##
## ERROR HANDLERS ##
##

@send_emote.error
async def send_emote_error(ctx, error):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( content = '`' + str(error) + ' Try db help emote for help`', delete_after=5.0, reference=ctx.message, mention_author = True )
	if isinstance( error, commands.BadBoolArgument ):
		await ctx.send( content = '`' + str(error) + '`', delete_after=5.0, reference=ctx.message, mention_author = True )

###
### RUN EVERYTHING ###
###

if 'weather' in sys.modules:
	sched_weather.start()
if 'keep_alive' in sys.modules:
	keep_alive()
bot.run(os.getenv( 'TOKEN' ))
