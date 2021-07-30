#import datetime, pytz
import random, string, os
import hashlib as h
from flask import Flask, redirect#, request, jsonify
from flask_simplelogin import SimpleLogin, login_required, is_logged_in
from threading import Thread

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
	'''dt = datetime.datetime.now( datetime.timezone.utc ).astimezone( pytz.timezone( 'Asia/Manila' ) ).strftime( '(%b %d, %Y - %X)\n' )
	ip = 'ip: ' + str( request.remote_addr )
	browser = 'user-agent: ' + str( request.headers.get( 'User-Agent' ) )
	header = 'full header request: ' + str( request.headers )
	with open( 'flask.log', 'a' ) as file:
		file.write( dt + ip + ' ' + browser + '\n' + header )'''
	return redirect( "https://stat.ddotb.tk/" )

@app.route( '/hook/' )
def hook_redirect():
	if is_logged_in( username = 'didotb' ):
		return redirect( app.config[ 'SIMPLELOGIN_HOME_URL' ] )
	return redirect( app.config[ 'SIMPLELOGIN_LOGIN_URL' ] )

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