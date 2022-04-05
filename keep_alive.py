#import datetime, pytz
import random, string, os, datetime, pytz
import hashlib as h
from flask import Flask, redirect, request, jsonify
from flask_simplelogin import SimpleLogin, login_required, is_logged_in
from threading import Thread
from totp import totp

def r( size:int=25, chars:str=string.ascii_uppercase + string.ascii_lowercase + string.digits ):
	return ''.join( random.SystemRandom().choice( chars ) for _ in range( size ) )

app = Flask( '' )

app.config[ 'SECRET_KEY' ] = r(128)
app.config[ 'SIMPLELOGIN_HOME_URL' ] = '/2021/05/15/' + r(5) + '/' + r() + '/'
app.config[ 'SIMPLELOGIN_LOGIN_URL' ] = '/login/'
app.config[ 'SIMPLELOGIN_LOGOUT_URL' ] = '/logout/'

def check( user ):
	if ( user.get( 'username' ) == os.environ[ 'FLASK_USER' ] ) and ( ( h.sha256( os.environ[ 'FLASK_S1' ].encode() + user.get( 'password' ).encode() + os.environ[ 'FLASK_S2' ].encode() ).hexdigest() ) == os.environ[ 'FLASK_PWD' ] ):
		return True
	return False

@app.route( '/' )
def home():
	dt = datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '(%b %d, %Y - %X)\n' )
	header = 'full header request: ' + str( request.headers )
	with open( 'flask.log', 'a' ) as file:
		file.write( f'{dt}{header}' )
	return f"<a href='/invite/'>Invite DeeBee Bot</a><br><br>Permissions:\n<ul>&bull;&emsp;Administrator (Optional)</ul><ul>&bull;&emsp;Slash Commands</ul><ul>&bull;&emsp;Start Activities</ul><ul>&bull;&emsp;Create Invite link (for Discord Together)</ul>"

@app.route('/invite/', methods=['POST','GET'])
def invite():
	'''if int(totp_data) == totp(os.environ['totp']):
		return f"https://discord.com/api/oauth2/authorize?client_id={os.environ['discord-bot_id']}&permissions={request.args.get("perms")}&scope=applications.commands%20bot"'''
	data = request.json
	return data

@app.route( '/hook/' )
def hook_redirect():
	if is_logged_in( username = 'didotb' ):
		return redirect( app.config[ 'SIMPLELOGIN_HOME_URL' ] )
	return redirect( app.config[ 'SIMPLELOGIN_LOGIN_URL' ] )

@app.route( '/deebee/' )
def bot_oauth2():
	headers = str(request.headers)
	with open('oauth2_log.debug', 'a') as log:
		log.write(headers)
		log.close()
	return "/deebee/"

@app.route( app.config[ 'SIMPLELOGIN_HOME_URL' ] )
@login_required( username = 'didotb' )
def hook():
	if is_logged_in( username = 'didotb' ):
		return "logged in as didotb"
	return redirect( app.config[ 'SIMPLELOGIN_LOGIN_URL' ] )

SimpleLogin( app = app, login_checker = check )

def run():
	app.run( host='0.0.0.0', port=8080 )

def keep_alive():
	t = Thread( target=run )
	t.start()