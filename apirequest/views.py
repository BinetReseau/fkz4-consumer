from django.shortcuts import render
from django.http import *
from requests_oauthlib import OAuth2Session

#Oauth variables
#These variables identify the application and are provided by Frankiz admins when you register the app
client_id = "test"
client_secret = "azertyuiop"
#Uri where the client is redirected on this app once it has logged in on the auth site. This uri must be registered by Frankiz admins
redirect_uri = "http://localhost:8001/apirequest/auth_code_given/"
#Rights required by the application
#Possible rights are: read
scope = ['read']

#Urls used to get the authorization and token
auth_url = 'http://localhost:8000/o/authorize/'
token_url = 'http://localhost:8000/o/token'

def make_oauth_object(token = None):
	if token:
		return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope, token = token)
	else:
		return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

def index(request):
	"""
	Index page performing authentication if needed and showing data from the api if the user is authenticated
	"""
	#Logged in
	if 'oauth_token' in request.session:
		oauth = make_oauth_object(request.session(request.session['oauth_token']))
		r = oauth.get('http://localhost:8000/api/student/1/.json')
		return HttpResponse('Authenticated :) <br/>' + r)
	#Not logged in
	else:
		oauth = make_oauth_object()
		authorization_url, state = oauth.authorization_url(auth_url)
		#Redirect the user to the authentication site, where he can log in if needed
		return HttpResponseRedirect(authorization_url)

def auth_code_given(request):
	"""
	View receiving the token and redirecting to the index after saving the token in the session
	"""
	authorization_code = request.GET.get('code')
	oauth =  make_oauth_object()
	token = oauth.fetch_token(token_url,
    	authorization_response=authorization_code, client_secret=client_secret)
	request.session['oauth_token'] = token
	#Redirecting to the index page
	return HttpResponseRedirect('http://localhost:8001/apirequest/')



