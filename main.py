import discord, os, asyncio, pytz, datetime, random, sys, requests
from html.parser import HTMLParser
from discord import default_permissions
from discord.ext import commands, tasks
from discord.commands import Option
from discord_together import DiscordTogether, errors as dte
from simple_rng import roll_parser
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

valid_app = {'youtube':'youtube','yt':'youtube','wt':'youtube','poker':'poker','pn':'poker','chess':'chess','betrayal':'betrayal','fishing':'fishing','letter-league':'letter-league','lt':'letter-league','word-snack':'word-snack','ws':'word-snack','sketch-heads':'sketch-heads','sh':'sketch-heads','spellcast':'spellcast','sc':'spellcast','awkword':'awkword','checkers':'checkers','blazing-8s':'blazing-8s','b8':'blazing-8s','land-io':'land-io','putt-party':'putt-party','bobble-league':'bobble-league','ask-away':'ask-away'}
listener = "db ", "deebee ", "DB ", "DEEBEE ", "Db ", "DeeBee ", "Deebee "
greeting = ['hello', 'hi']
positive = ['true', 't']
negative = ['false', 'f']
msgTrigA = ['wiggle', 'jiggle', 'popcat', 'catjam', 'new pc', 'blobdance', 'pepeds', 'cum']
msgTrig = ['bij', 'bitch']
msgYEP = ['sock', 'cock', 'rock', 'dock', 'duck', 'stock', 'clock', 'croc', 'lock', 'knock', 'mock', 'jock']
hp = HTMLParser()
bot = commands.Bot( command_prefix=listener, intents=discord.Intents.all(), owner_id=int(os.environ['discord_user_db']), strip_after_prefix=True )

# emote searcher
async def emote(animated, emojiName):
	eName = emojiName.lower()
	for i in bot.emojis:
		j = str(i)
		##
		## match case for 3.10
		##
		if animated is True and eName in j.lower() and '<a:' in j.lower():
			return j
		elif animated is False and eName in j.lower() and '<a:' not in j.lower():
			return j
	return "`Error retrieving emote. Check name or spelling.`"

# main vca function
async def act_app(vcid, app_name=None):
	try:
		vcal = await bot.vca.create_link(vcid,valid_app.get(app_name, None),max_age=300)
		if vcal is not None:
			return f'Join the Voice Chat Activity: {vcal}\nValid only for 5 minutes.'
	except dte.InvalidArgument:
		if isinstance(app_name,int):
			return 'Invalid Custom Application ID'
		return 'Invalid or misspelled application name'
	except dte.BotMissingPerms:
		return '`I can\'t seem to create an invite link.\nMake sure I\'m allowed to make an invite link to the VC.\n(Check VC permissions)`'
	except dte.ConnectionError:
		return 'Error while contacting Discord API. Contact @d.b#3031'
	except AttributeError as e:
		return e

async def bot_startled(author:str):
	if author != os.environ['discord_user_db']:
		return await emote(False, "bij") + ' what? <@' + author + '>'
	elif author == os.environ['discord_user_db']:
		return 'eyy <@' + author + '>! what\'s up'
	else:
		await debug(msg='author id: ' + author)
		return 'Command broke, check debug channel, and console.'

async def debug(cmsg:str=None, pmsg:int=None, cid:int=int(os.environ['discord_channel_debug'])):
	if pmsg is not None:
		switcher = {
			0:"Info:0: Process ended",
			1:"Info:1: Process started",
			2:"Info:2: Waiting for absolute hour",
			3:"Info:3: Weather loop started",
			4:"Info:4: Weather animation sent",
			5:"Info:5: Restart initiated but failed due to invalid variable value",
			6:"Info:6: Restart initiated"
		}
		message = switcher.get( pmsg, "Warning: Error getting pre-determined message" )
	elif cmsg is not None:
		message = "Custom: " + cmsg
	else:
		message = "Warning: Generic debug message"

	channel = bot.get_channel( cid )
	ts = datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '(%b %d, %Y - %X): ' )
	await channel.send( "`" + ts + message + "`" )
	print(f"sent to debug channel: {message}")
	return

## 
## SCHEDULERS ##
##

"""@tasks.loop(time=[datetime.time(tzinfo=datetime.timezone(datetime.timedelta(hours=8)), hour=datetime.datetime.now().hour, minute=m) for m in range(0,59)])
async def loop_time_test():
	print("it works?")
	cnl = bot.get_channel(800385956741382186)
	await cnl.send(f"Current minute is: {datetime.datetime.now().minute}")

@loop_time_test.before_loop
async def loop_time_test_before():
	print("loop time test before started")
	print(f"\nis_running: {loop_time_test.is_running()}\nhours: {loop_time_test.hours}\nminutes: {loop_time_test.minutes}\nseconds: {loop_time_test.seconds}\ntime: {loop_time_test.time}\ncurrent_loop: {loop_time_test.current_loop}\nnext_iteration: {loop_time_test.next_iteration}\n")
	await bot.wait_until_ready()"""

if 'weather' in sys.modules:
	@tasks.loop(hours=1) #time=[datetime.time(h,0,0,0,tzinfo=datetime.timezone(datetime.timedelta(hours=8))) for h in [0,4,8,10,12,14,16,20]]
	async def sched_weather():
		dt = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone('Asia/Manila'))
		hours = int(dt.strftime('%H'))
		await debug(cmsg=f"(weather): Another hour has passed: {hours}")
		channel = bot.get_channel( int( os.environ[ 'discord_channel_vii_weather' ] ) )

		if hours in [0,4,8,10,12,14,16,20]:
			await debug(cmsg="Started weather command")
			weather.weather('sw')
			async with channel.typing():
				await asyncio.sleep(5)
				await channel.send(f"Set interval daily weather images", file=discord.File('out.mp4'))

		if os.path.exists(weather.target):
			await debug(pmsg=4)
			weather.clean()
			await debug(pmsg=0)

	@sched_weather.before_loop
	async def sched_weather_before():
		dt = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone('Asia/Manila'))
		minutes = int(dt.strftime('%M'))
		seconds = int(dt.strftime('%S'))
		wait = (3600)-((minutes*60)+seconds) # wait for an absolute hour
		print("weather 'before loop' called")
		await asyncio.sleep( wait )
		await bot.wait_until_ready()

@tasks.loop(hours=1)
async def xmas_loop():
	dt = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone('Asia/Manila'))
	sept = datetime.datetime(dt.year,9,1).astimezone(pytz.timezone('Asia/Manila'))
	xmas = datetime.datetime(dt.year,12,25).astimezone(pytz.timezone('Asia/Manila'))
	start = xmas - sept
	delta = xmas - dt
	hours = int(dt.strftime('%H'))
	await debug(cmsg=f"(xmas): Another hour has passed: {hours}")
	channel = bot.get_channel(int(os.environ['discord_channel_vii_days_before_xmas']))

	if delta.days > start.days:
		return
	if hours != 0:
		return
	if delta.days+1 < 0:
		return
	if delta.days+1 == 0:
		await channel.send("**It's Christmas Day!**")
		return

	await debug(cmsg="xmas message activated")
	response = requests.get('https://opentdb.com/api.php?amount=10')
	trivia = response.json()

	if trivia['response_code'] != 0:
		await debug(cmsg=f"Error in xmas_loop: response_code returned {trivia['response_code']}. Expected 0")
		return
	picked = random.choice(trivia['results'])
	question = hp.unescape(picked['question'])
	answer = hp.unescape(picked['correct_answer'])

	await channel.send(f"@here Question: {question}\nAnswer: ||{answer}||\nAnyway, **it's {str(int(delta.days)+1)} days before Christmas!**")

@xmas_loop.before_loop
async def xmas_loop_before():
	dt = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone('Asia/Manila'))
	minutes = int(dt.strftime('%M'))
	seconds = int(dt.strftime('%S'))
	wait = (3600)-((minutes*60)+seconds) # wait for an absolute hour
	print("xmas 'before loop' called")
	await asyncio.sleep(wait)
	await bot.wait_until_ready()

##
## BOT INIT ##
##

@bot.event
async def on_ready():
	await debug(cmsg=f'logged in as {bot.user}')
	actName = "\'db help\'"
	act = discord.ActivityType.playing
	app_id = 643329811523043343
	assets = {'large_image':'698193248190988388', 'small_image':'698193246429380729', 'large_text':'Large icon test', 'small_text':'Small icon test'}
	buttons = [{'label':'Rick Roll', 'url':'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}]
	activity = discord.Activity( application_id=app_id, assets=assets, name=actName, type=act, state='Testing' )
	await bot.change_presence(activity=activity, status=discord.Status.online)
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
			if cont in {'wiggle', 'jiggle'}:
				if msg.reference is None:
					await msg.add_reaction(emoji=await emote(True, 'wiggle'))
				elif msg.reference is not None:
					refmsg = await msg.channel.fetch_message(msg.reference.message_id)
					await refmsg.add_reaction(emoji=await emote(True, cont))
			elif cont in {'blobdance', 'pepeds'}:
				thisEmote = await emote(True, cont)
				await msg.channel.send(thisEmote + thisEmote + thisEmote)
			elif ('cum' in cont) and (msg.channel.guild.id not in {os.environ['discord_guild_beaneyboo_server'],os.environ['discord_guild_foxy_server'],os.environ['discord_guild_falcon_server'],os.environ['discord_guild_anjellying_server']}):
				await msg.add_reaction(emoji=await emote(False,'potatocum'))
			else:
				await msg.channel.send(await emote(True, cont))
		for cont in mTrig:
			cont = 'bij' if cont == 'bitch' else cont
			await msg.add_reaction(emoji=await emote(False, cont))
		for cont in mYep:
			await msg.add_reaction(emoji=await emote(False, 'yep'))

	if (bot.user in msg.mentions) or ("bitches" in msg.content.lower()):
		await msg.channel.send(content=await bot_startled(str(msg.author.id)), reference=msg, mention_author=True)

	if 'new pc' in msg.content.lower():
		thisEmote = await emote(False, "mmmseks")
		await msg.channel.send(content=thisEmote + thisEmote + thisEmote, reference=msg, mention_author=True)
		await msg.add_reaction(emoji=thisEmote)

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

@bot.command(name="test",hidden=True)
async def command_test(ctx):
	await ctx.send(content=ctx.message.content)

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
	await ctx.send( await emote(animated, name) )

'''@bot.command( name='sticker', enabled=False, hidden=True, description="Send any sticker from servers the bot is in." )
async def send_sticker(ctx, name:str):
	await ctx.send(  )'''

@bot.command( name='weather', description="Send animated weather satelite images as mp4 video file." )
async def send_weather(ctx, action='sw'):
	if 'weather' not in sys.modules:
		await ctx.send(content="Weather module was not imported. Please check console for problems.")
		return None
	await debug( cmsg="Requested weather command" )
	await ctx.reply( content="Please wait 15 seconds. Generating __requested__ images.", mention_author=True )
	weather.weather( action )
	async with ctx.typing():
		await asyncio.sleep(5)
	await ctx.send(content="Please use weather command sparingly. Bot might get banned for using too much resource.", file=discord.File('out.mp4'))
	await debug( pmsg=4 )
	weather.clean()
	await debug( pmsg=0 )

@bot.command( name='bitch', aliases=['bij'], hidden=True )
async def bitch_react(ctx):
	await ctx.reply(content=await bot_startled(str(ctx.author.id)), mention_author=False)

@bot.command( name='vca', description='Start Discord Together / Voice Chat Activities' )
async def vca(ctx, app_name=None):
	try:
		vcid = ctx.author.voice.channel.id
	except AttributeError:
		await ctx.reply("Join a Voice Channel that I can see.", delete_after=10)
		return
	if (app_name != 'list') and (app_name is not None):
		await ctx.reply(await act_app(vcid, app_name), delete_after=300.0)
	elif (app_name == 'list') or (app_name is None):
		embed=discord.Embed(title="Discord Together Applications", description="Available applications for Discord Together")
		for i in list(set(valid_app.values())):
			embed.add_field(name=i, value=[k for k, v in valid_app.items() if v == i], inline=False)
		embed.set_footer(text="Example: `db vca youtube` to start a Watch Together session.")
		await ctx.reply(embed=embed, mention_author=True)

@bot.command( name='roll', description="Roll a dice." )
async def roll_cmd(ctx, dice_notation:str):
	result = roll_parser(dice_notation)
	content = f"{result['prev']} + ({result['value'] - result['initial']}) = {result['value']}" if 'initial' in result.keys() else f"{result['prev']} = {result['value']}"
	await ctx.reply(content=content, mention_author=False)

@bot.command(name="debug", description="Send a test debug message", hidden=True)
async def command_debug(ctx, *, message:str=None):
	if int(ctx.author.id) != int(os.environ['discord_user_db']):
		raise commands.MissingPermissions()
	await ctx.reply(content="Check debug channel.", mention_author=False)
	await on_command_error(ctx, error=message if message is not None else "Test error")

"""
@bot.command(name="minecraft", aliases=['mc'], description="Start Mind&Body Hurts aternos minecraft server.", guild_ids=[os.environ['discord_guild_debug_server'],os.environ['discord_guild_mindandbodyhurts_server']], hidden=True)
async def command_mc(ctx, action:str=['status','start','stop'], keep=False):
	error = False
	keep = True if keep == 'keep' else False
	embed = discord.Embed(title="Mind&Body Hurts Aternos Minecraft Server") if keep is False else discord.Embed(title="Mind&Body Hurts Aternos Minecraft Server", description="Kept alive for 15 minutes.")
	embed.set_footer(text=f"Initiated by {ctx.author}")
	try:
		if action.lower() == 'status':
			value = await ah.server_status(ah.login())
		elif action.lower() == 'start':
			await ah.server_start(ah.login())
			value = f"Starting server...\nIt takes up to 5 minutes to start the server.\nYou will be pinged once server has started.   "
		elif action.lower() == 'stop':
			await ah.server_stop(ah.login())
			value = f"Stopping server...\nIt takes up to 2 minutes to stop the server."
		embed.add_field(name="Status", value=value)
	except Exception as e:
		error = True
		embed.add_field(name="Error", value=e)
	finally:
		await ctx.reply(embed=embed, mention_author=True if error is True else False)
		if(action == 'start') and (error is False):
			startup = 'loading'
			while (startup == 'loading') or (startup == 'loading starting'):
				await asyncio.sleep(30)
				startup = await ah.server_status(ah.login())
			embed.remove_field(0)
			embed.add_field(name="Status", value=startup)
			await ctx.send(content="@here", embed=embed, reference=ctx.message, mention_author=False)
			#subprocess.run(["./afk/MinecraftClient.exe", "./afk/MinecraftClient.ini"], shell=False, check=False)
"""

##
## SLASH COMMANDS ##
##

@bot.slash_command(name="test")
async def test(ctx):
	embed = discord.Embed(title="Embed test", description=":p", colour=discord.Colour(0xd6b4d8))
	await ctx.respond(content="test", embeds=[embed], ephemeral=True)

'''@bot.slash_command(name="hidden")
async def hidden_test(ctx):
	await ctx.respond(content="d: sapnu puas", ephemeral=True)'''

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
	try:
		vcid = ctx.author.voice.channel.id
	except AttributeError:
		await ctx.respond("Join a Voice Channel that I can see.", delete_after=10)
		return
	await ctx.respond(await act_app(vcid, app_name), delete_after=300.0)

@bot.slash_command(name="weather", description="Generate weather images.")
async def slash_weather(ctx, action='sw'):
	if 'weather' not in sys.modules:
		await ctx.respond(content="Weather module was not imported. Please check console for problems.")
		return None
	if action == 'clean':
		weather.clean()
		await ctx.respond(content="Cache of weather images has been cleared.", ephemeral=True)
	else:
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
@default_permissions(moderate_members=True)
async def slash_announcement(ctx, content:str, test:bool, tag:str=['here','everyone'], colour:int=0xffb9d2, channel_id:str=None):
	embed = discord.Embed(title="Announcement", description=f"Author: {ctx.author}", colour=int(colour))
	#embed.set_thumbnail(url=ctx.author.display_avatar)
	embed.add_field(name="Content:", value=content)
	embed.set_footer(text=f"Published: {datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone('Asia/Manila')).strftime('%b %d, %Y :: %I.%M.%S %p')}")
	tag = None if isinstance(tag, list) else tag
	tag_switcher = {'here':'@here','everyone':'@everyone'}
	if (channel_id is not None) and (test is False):
		channel_id = channel_id.split(' ')
		if len(channel_id)==1:
			cnl = bot.get_channel(int(channel_id[0]))
			if(cnl.permissions_for(cnl.guild.get_member(ctx.author.id)).send_messages):
				await cnl.send(content=tag_switcher.get(tag,None),embed=embed)
				await ctx.respond(content="Announcement sent")
			else:
				raise commands.MissingPermissions()
		elif len(channel_id)>1:
			chnl_num:int = 0
			not_sent:list = []
			for chnl in channel_id:
				cnl = bot.get_channel(int(chnl))
				if(cnl.permissions_for(cnl.guild.get_member(ctx.author.id)).send_messages):
					await cnl.send(content=tag_switcher.get(tag,None),embed=embed)
					chnl_num += 1
				else:
					not_sent.append(chnl)
					pass
			not_sent = "; ".join(not_sent) if len(not_sent) > 0 else []
			respond = f"Announcement sent to {chnl_num} channels." if len(not_sent) == 0 else f"Announcement sent to {chnl_num} channels.\nCould not send to these channels: `{not_sent}`"
			await ctx.respond(content=respond)
	else:
		await ctx.respond(content=tag_switcher.get(tag,None), embed=embed, ephemeral=False if test==False else True)

@bot.slash_command(name="debug", description="Send a test debug message.")
@default_permissions(moderate_members=True, administrator=True)
async def slash_debug(ctx, message:str=None):
	await ctx.respond(content="Check debug channel.", ephemeral=True)
	await on_command_error(ctx, error=message if message is not None else "Test error")

@bot.slash_command(name="init")
async def slash_init(ctx):
	await ctx.respond("Refreshing commands.", ephemeral=True)


@bot.slash_command(name="roll")
async def slash_roll(ctx, dice_notation:str):
	result = roll_parser(dice_notation)
	content = f"{result['prev']} + ({result['value'] - result['initial']}) = {result['value']}" if 'initial' in result.keys() else f"{result['prev']} = {result['value']}"
	await ctx.respond(content=content)

@bot.slash_command(name="analyze", description="Check if link exists in Malicious Databases")
async def slash_analyze(ctx, domain:str):
	with requests.get(f"https://phish.sinking.yachts/v2/check/{domain}") as req:
		answer = f"{domain} is present in the Sinking Yachts anti-phishing list, and is therefore a *MALICIOUS* link." if req.json() is True else f"`{domain} was not found in the list. Be careful if you don't trust the link`"
		await ctx.respond(content=answer)

@bot.slash_command(name="shutdown", description="Shutdown bot.", hidden=True)
@default_permissions(moderate_members=True, administrator=True)
async def slash_shutdown(ctx, reason=None, schedule=5, silent:bool=None):
	"""
	Shutdown the bot at any given time, with any given reason.

	Parameters
	----------
	reason : str, optional
		The reason why the shutdown was scheduled.
	schedule : int, default 5
		Time in seconds to count up to before the shutdown.
	silent : bool, optional
		Switch to ``True`` if you wish to turn on ephemeral.
	"""
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

@bot.slash_command(name="restart",description="Restart bot.")
@default_permissions(moderate_members=True)
async def slash_restart(ctx, reason=None, schedule=5, silent:bool=True):
	"""
	Restart the bot at any given time, with any given reason.

	Parameters
	----------
	reason : str, optional
		The reason why the restart was scheduled.
	schedule : int, default 5
		Time in seconds to count up to before the shutdown.
	silent : bool, default True
		Switch to ``True`` if you wish to turn on ephemeral.
	"""
	try:
		restart_sched = int(schedule)
	except ValueError as e:
		await ctx.respond(e, ephemeral=True)
		await debug(pmsg=5)
		return None
	if restart_sched>=1:
		embed_title="Scheduled Restart"
		embed_descr=f"Restart in {restart_sched} seconds."
		embed_footer="Scheduled by"
	else:
		embed_title="Immediate Restart"
		embed_descr="Restarting immediately."
		embed_footer="Initiated by"
	embed = discord.Embed(title=embed_title,description=embed_descr)
	embed.add_field(name="Reason:",value=reason if reason is not None else "No reason stated.")
	embed.set_footer(text=f"{embed_footer} {ctx.author}")
	await ctx.respond(embed=embed, ephemeral=True if silent==True else False)
	await asyncio.sleep(restart_sched)
	await debug(pmsg=6)
	os.execv(sys.executable, ['python'] + sys.argv)

@bot.slash_command(name="emote",description="Send an emote then an optional message.")
async def slash_emote(ctx, emotes, msg=None, animated=False):
	animated = True if animated is True else False
	message = [await emote(animated, e) for e in emotes.lower().split()]
	if msg is not None:
		message.append(msg)
	await ctx.send(content=' '.join(message))
	await ctx.respond("sent", ephemeral=True)

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
		await ctx.send(embed=embed, reference=ctx.message, mention_author=False)
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

### BROKEN RUN METHOD 3.10
#def run():
#	if 'keep_alive' in sys.modules:
#		keep_alive()
#
#	xmas_loop.start()
#
#	async def bot_loop_gather(action:str='start'):
#		#async_tasks = set()
#		loop = asyncio.get_event_loop()
#		start_action = loop.create_task(bot.start(os.getenv('TOKEN'))) if action == 'start' else loop.create_task(bot.close())
#		start_sched_weather = loop.create_task(sched_weather.start()) if 'weather' in sys.modules else None
#
#		#async_tasks.add(start_action)
#		#start_action.add_done_callback(async_tasks)
#
#		result = await asyncio.gather(start_action,start_sched_weather)
#		return result
#	try:
#		asyncio.run(bot_loop_gather('start'))
#	except KeyboardInterrupt:
#		sched_weather.cancel()
#		xmas_loop.cancel()
#		asyncio.run(bot_loop_gather('stop'))

### Works in 3.10
async def bot_start():
	if 'weather' in sys.modules:
		sched_weather.start()
	if 'keep_alive' in sys.modules:
		keep_alive()
	xmas_loop.start()
	await bot.start(os.getenv('TOKEN'))

async def bot_stop():
	if 'weather' in sys.modules:
		sched_weather.cancel()
	xmas_loop.cancel()
	await bot.close()

async def gatherer(run_task):
	run = bot_start() if run_task == 'start' else bot_stop()
	await asyncio.gather(run)

#if __name__ == '__main__':
#	try:
#		asyncio.run(gatherer('start'))
#	except KeyboardInterrupt:
#		asyncio.run(gatherer('stop'))
#	finally:
#		print("Bot has stopped.")

### OLDER RUN METHOD THAT WORKS FOR 3.8
#def run():
#	if 'weather' in sys.modules:
#		sched_weather.start()
#	if 'keep_alive' in sys.modules:
#		keep_alive()
#	xmas_loop.start()
#
#	loop = asyncio.get_event_loop()
#	bot_loop = loop.create_task(bot.start(os.getenv('TOKEN')))
#	loops = asyncio.gather(bot_loop, loop=loop)
#	try:
#		loop.run_until_complete(loops)
#	except KeyboardInterrupt:
#		sched_weather.cancel()
#		xmas_loop.cancel()
#		loop.run_until_complete(bot.close())
#	finally:
#		loop.close()
#
#run()