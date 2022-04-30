import discord, os, asyncio, pytz, datetime, random, sys, re
from collections import deque
from discord.ext import commands, tasks
from discord.commands import Option
from discord_together import DiscordTogether, errors as dte
from simple_rng import roll
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
bot = commands.Bot( command_prefix=listener, intents=discord.Intents.all(), owner_id=int(os.environ['discord_user_db']), strip_after_prefix=True )

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

# main vca function
async def act_app(vcid, app_name=None):
	try:
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
			return f'Join the Voice Chat Activity: {vcal}\nValid only for 5 minutes.'
		elif vcal is None:
			return f'Invalid app code: `{app_name}`'
		else:
			raise dte.BotMissingPerms
	except AttributeError:
		return 'Join a VC first!'
	except dte.BotMissingPerms:
		return '`I can\'t seem to create an invite link.\nMake sure users are allowed to make an invite link to the VC.\n(Check VC permissions)`'

async def bot_startled(author:str):
	if author != os.environ['discord_user_db']:
		return emote(False, "bij") + ' what? <@' + author + '>'
	elif author == os.environ['discord_user_db']:
		return 'eyy <@' + author + '>! what\'s up'
	else:
		await debug(msg='author id: ' + author)
		return 'Command broke, check debug channel, and console.'

async def debug( cmsg:str = None, pmsg:int = None, cid:int = int( os.environ[ 'discord_channel_debug' ] ) ):
	if pmsg is not None:
		switcher = {
			0:"InfNo:0: Process ended",
			1:"InfNo:1: Process started",
			2:"InfNo:2: Waiting for minutes to turn 00",
			3:"InfNo:3: Weather loop started",
			4:"InfNo:4: Weather animation sent"
		}
		message = switcher.get( pmsg, "Warning: Error getting pre-determined message" )
	elif cmsg is not None:
		message = "Custom: " + cmsg
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
		channel = bot.get_channel( int( os.environ[ 'discord_channel_vii_weather' ] ) )

		if hours == 9 or hours == 13:
			await debug(pmsg=1)
			weather.weather('latest')
			async with channel.typing():
				await asyncio.sleep(11)
			await channel.send("__2 hour interval__ mid-day daily weather images", file = discord.File('out.mp4'))

		if hours % 4 == 3:
			await debug( pmsg = 1 )
			weather.weather( 'latest' )
			async with channel.typing():
				await asyncio.sleep(11)
			await channel.send(  "__4 hour interval__ daily weather images", file = discord.File( 'out.mp4' ) )

		if os.path.exists(weather.target):
			await debug( pmsg = 4 )
			weather.clean()
			await debug( pmsg = 0 )

	@sched_weather.before_loop
	async def sched_weather_before():
		minutes = int( datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '%M' ) )
		seconds = int( datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '%S' ) )
		wait = 3600 - ( ( ( minutes + 1 ) * 60 ) + ( seconds - 30 ) ) # wait for 30 secs early before an absolute hour
		print("weather waiting")
		await asyncio.sleep( wait )
		await bot.wait_until_ready()

@bot.event
async def on_ready():
	print(f'logged in as {bot.user}')

	name = "\'db help\'"
	act = discord.ActivityType.streaming

	activity = discord.Activity( name=name, details='Testing', type=act )
	await bot.change_presence(activity=activity, status=discord.Status.streaming)

	bot.vca = await DiscordTogether(os.getenv( 'TOKEN' ))

@bot.event
async def on_message(msg):
	msgCont = []
	msgCont = msg.content.lower().split(' ')

	mTrigA = (cont for cont in msgCont if cont in msgTrigA)
	mTrig = (cont for cont in msgCont if cont in msgTrig)
	mYep = (cont for cont in msgCont if cont in msgYEP)

	if (msg.author == bot.user) and ((msg.channel.id == int(os.environ['discord_channel_vii_weather']) and msg.attachments)) or (msg.channel.id == int(os.environ['discord_channel_vii_days_before_xmas'])):
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
		if ( cont in msg.content.lower() ) and str( msg.author.id ) != os.environ[ 'discord_user_db' ]:
			await msg.channel.send(content="no u.", reference=msg, mention_author=True)

	if 'new pc' in msg.content.lower():
		await msg.channel.send(content=emote(False, "mmmseks") + emote(False, "mmmseks") + emote(False, "mmmseks"), reference=msg, mention_author=True)
		await msg.add_reaction(emoji=emote(False, "mmmseks"))

	details = f"```{str(datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ))}\n# Author: {msg.author.name}\n# Server Name: {msg.guild.name}\n# Channel Name: {msg.channel.name}\n\n{msg.content}```"
	if msg.guild.id != int(os.environ['discord_guild_REDACTED_1_server']) and msg.guild.id != int(os.environ['discord_guild_beaneyboo_server']) and msg.guild.id != int(os.environ['discord_guild_debug_server']):
		if msg.attachments:
			channel = bot.get_channel(int(os.environ['discord_channel_images_archive']))
			for i in msg.attachments:
				await channel.send(details, file=await i.to_file())
		if not msg.attachments:
			channel = bot.get_channel(int(os.environ['discord_channel_text_archive']))
			await channel.send(details)

	if msg.guild.id == int(os.environ['discord_guild_foxy_server']):
		channel = bot.get_channel(int(os.environ['discord_channel_foxy_archive']))
		if msg.attachments:
			for i in msg.attachments:
				att = await i.to_file()
				await channel.send(details, file=att)
		if not msg.attachments:
			await channel.send(details)

	if msg.guild.id == int(os.environ['discord_guild_beaneyboo_server']) and (msg.channel.id != int(os.environ['discord_channel_beaneyboo_mods_priv']) and msg.channel.id != int(os.environ['discord_channel_beaneyboo_moderator_only']) and msg.channel.id != int(os.environ['discord_channel_beaneyboo_msg_archiving'])):
		channel = bot.get_channel(int(os.environ['discord_channel_beaneyboo_msg_archiving']))
		if msg.attachments:
			for i in msg.attachments:
				att = await i.to_file()
				await channel.send(details, file=att)
		if not msg.attachments:
			await channel.send(details)

	if msg.channel.id in [int(os.environ['discord_channel_beaneyboo_announcement'])]:
		await asyncio.sleep(3)
		await msg.publish()

	else: # process discord.ext.commands
		await bot.process_commands(msg)

##
## BOT COMMANDS ##
##

@bot.command( name='troll', hidden=True )
async def troll(ctx):
	#cnl = bot.get_channel( int( os.environ['discord_channel_vii_days_before_xmas'] ) )
	msg = f"<@{os.environ['discord_user_db']}> gae."
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
	await debug( cmsg="Requested weather command" )
	await ctx.send( content="Please wait 15 seconds. Generating __requested__ images.", reference=ctx.message, mention_author=True )
	weather.weather( 'latest' )
	async with ctx.typing():
		await asyncio.sleep(30)
	await ctx.edit(content="Please use weather command sparingly. Bot might get banned for using too much resource.", file=discord.File('out.mp4'))
	await debug( pmsg=4 )
	weather.clean()
	await debug( pmsg=0 )

@bot.command( name='bitch', aliases=['bij'], hidden=True )
async def bitch_react(ctx):
	await ctx.reply(content=await bot_startled(str(ctx.author.id)), mention_author=False)

@bot.command( name='vca', description='Start Discord Together / Voice Chat Activities' )
async def vca(ctx, app_name=None):
	if (app_name != 'list') and (app_name is not None):
		await ctx.reply(await act_app(ctx.author.voice.channel.id, app_name), delete_after=300.0)
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
			await ctx.reply(embed=embed, mention_author=True)

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
	await ctx.reply(content=roll(divd[0],divd[1],divd[2]), mention_author=False)

@bot.command(name="debug", description="Send a test debug message")
async def command_debug(ctx, *, message:str=None):
	await ctx.reply(content="Check debug channel.", mention_author=False)
	await on_command_error(ctx, error=message if message is not None else "Test error")

##
## SLASH COMMANDS ##
##

@bot.slash_command(name="test")
async def test(ctx):
	embed = discord.Embed(title="Embed test", description=":p", colour=discord.Colour(0xd6b4d8))
	await ctx.respond(content="test", embeds=[embed], ephemeral=True)

@bot.slash_command(name="hidden")
async def hidden_test(ctx):
	await ctx.respond(content="d: sapnu puas", ephemeral=True)

'''@slash.context_menu(name="context", target=3, guild_ids=[int(os.environ['discord_guild_debug_server'])])
async def context_test(ctx):
	print( ctx.data )
	await ctx.send("check console", ephemeral=True)'''

@bot.slash_command(name="vca")
async def slash_vca(
	ctx,
	app_name: Option(str, "Enter the app name", choices=[
		'youtube', 'poker', 'chess',
		'betrayal', 'fishing', 'letter-league',
		'word-snack', 'sketch-heads', 'spellcast',
		'awkword', 'checkers'], default=None)
):
	await ctx.respond(await act_app(ctx.author.voice.channel.id, app_name), delete_after=300.0)

@bot.slash_command(name="weather", description="Generate weather images.")
async def slash_weather(ctx, action='latest'):
	if 'weather' not in sys.modules:
		await ctx.respond(content="Weather module was not imported. Please check console for problems.")
		return None
	else:
		if action == 'clean':
			weather.clean()
			await ctx.respond(content="Cache of weather images has been cleared.", ephemeral=True)
		elif action == 'latest':
			await debug( cmsg="Requested weather command" )
			await ctx.respond( content="Please wait 15 seconds. Generating __requested__ images." )
			weather.weather(action)
			async with ctx.typing():
				await asyncio.sleep(10)
			await ctx.edit(content="Please use weather command sparingly. Bot might get banned for using too much resource.", file=discord.File('out.mp4'))
			await debug( pmsg=4 )
			weather.clean()
			await debug( pmsg=0 )

@bot.slash_command(name="announcement", description="Send an announcement to a channel.")
async def slash_announcement(ctx, content:str, test:bool, colour:int=0xffb9d2, channel:str=None):
	embed = discord.Embed(title="Announcement", description=f"Author: {ctx.author}", colour=int(colour))
	#embed.set_thumbnail(url=ctx.author.display_avatar)
	embed.add_field(name="Content:", value=content)
	embed.set_footer(text=f"Published: {datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone('Asia/Manila')).strftime('%b %d, %Y :: %I.%M.%S %p')}")
	if (channel is not None) and (test is False):
		cnl = bot.get_channel(int(channel))
		if(cnl.permissions_for(cnl.guild.get_member(ctx.author.id)).send_messages):
			await cnl.send(embed=embed)
			await ctx.respond(content="Message sent")
		else:
			raise commands.MissingPermissions()
	else:
		await ctx.respond(embed=embed, ephemeral=False if test==False else True)

@bot.slash_command(name="debug", description="Send a test debug message.")
async def slash_debug(ctx, message:str=None):
	await ctx.respond(content="Check debug channel.", ephemeral=True)
	await on_command_error(ctx, error=message if message is not None else "Test error")

@bot.slash_command(name="init")
async def slash_init(ctx):
	ctx.respond("Refreshing commands.", ephemeral=True)

@bot.slash_command(name="shutdown", description="Shutdown bot.", hidden=True)
async def slash_shutdown(ctx, reason=None, schedule=5, silent:bool=None):
	try:
		shutdown_sched = int(schedule)
	except ValueError as e:
		await ctx.respond(e, ephemeral=True)
		return None
	embed = discord.Embed(title=f"Scheduled Shutdown", description=f"Shutdown in {shutdown_sched} seconds.", colour=int(0xffb9d2))
	embed.add_field(name="Reason:", value=reason if reason is not None else "No reason stated.")
	embed.set_footer(text=f"Scheduled by: {ctx.author}")
	await ctx.respond(embed=embed, ephemeral=True if silent==True else False)
	await asyncio.sleep(shutdown_sched)
	await bot.close()

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
		embed = discord.Embed(title="Error in command", description=f"Command: {ctx.command}")
		embed.add_field(name="Details:", value=f"{error}")
		embed.set_footer(text=f"Usage: {ctx.command} {ctx.command.signature}")
		await ctx.send(embed=embed, reference=ctx.message, mention_author=False, ephemeral=True)
	else:
		debug_cnl = bot.get_channel(int(os.environ['discord_channel_debug']))
		embed = discord.Embed(title="Unhandled custom pycord error", description=f"Command: {ctx.command}")
		embed.add_field(name="Details:", value=f"{error}")
		embed.set_footer(text=f"Message: {ctx.message.content if ctx.message is not None else error}")
		await ctx.send(embed=embed, reference=ctx.message, mention_author=False)
		await debug_cnl.send(content=f"Message URL: {ctx.message.jump_url}" if ctx.message is not None else f"Message: {error}", embed=embed)

###
### RUN EVERYTHING ###
###

if 'weather' in sys.modules:
	sched_weather.start()
if 'keep_alive' in sys.modules:
	keep_alive()

try:
	loop = asyncio.get_event_loop()
	bot_loop = loop.create_task(bot.start(os.getenv('TOKEN')))
	loops = asyncio.gather(bot_loop, loop=loop)
	loop.run_until_complete(loops)
except KeyboardInterrupt:
	loop.run_until_complete(bot.close())
finally:
	loop.close()

'''if 'weather' in sys.modules:
	sched_weather.cancel()
	sched_weather.stop()'''
#bot.run(os.getenv( 'TOKEN' ))
