from django.shortcuts import render
from django.http import *
from requests_oauthlib import OAuth2Session


class Frankiz:
	#Urls used to get the authorization and token
	auth_url = 'http://localhost:8000/o/authorize/'
	token_url = 'http://localhost:8000/o/token/'

	#Rights required by the application
	#Possible rights are: read
	scope = ['read']

	def make_oauth_object(token = None):
		if token:
			return OAuth2Session(client_id, token = token)
		else:
			return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=Frankiz.scope)

	def authorization_url():
		return auth_url



#Oauth variables
#These variables identify the application and are provided by Frankiz admins when you register the app
client_id = "test"
client_secret = "azertyuiop"
#Uri where the client is redirected once it has logged in on the auth site. This uri must be registered by Frankiz admins
redirect_uri = "http://localhost:8001/apirequest/auth_code_given/"


def index(request):
	"""
	Index page performing authentication if needed and showing data from the api if the user is authenticated
	"""
	#Logged in
	if 'oauth_token' in request.session:
		oauth = Frankiz.make_oauth_object(request.session['oauth_token'])
		r = oauth.get('http://localhost:8000/api/group/1/.json')
		return HttpResponse('Authenticated :) <br/>' + r.content.decode("utf-8"))
	#Not logged in
	else:
		oauth = Frankiz.make_oauth_object()
		authorization_url, state = oauth.authorization_url(Frankiz.authorization_url())
		#Redirect the user to the authentication site, where he can log in if needed
		return HttpResponseRedirect(authorization_url)

def auth_code_given(request):
	"""
	View receiving the token and redirecting to the index after saving the token in the session
	"""
	authorization_code = request.build_absolute_uri(request.get_full_path())
	oauth =  Frankiz.make_oauth_object()
	token = oauth.fetch_token(Frankiz.token_url,
    	authorization_response=authorization_code, client_secret=client_secret)
	request.session['oauth_token'] = token
	#Redirecting to the index page
	return HttpResponseRedirect('http://localhost:8001/apirequest/')

def request(request, url):
	"""
	View used to make a test request to the api
	"""
	#Logged in?
	if 'oauth_token' in request.session:
		oauth = Frankiz.make_oauth_object(request.session['oauth_token'])
		r = oauth.get('http://localhost:8000/api/' + url)
		return HttpResponse(r.content.decode("utf-8"))
	else:
		return HttpResponseRedirect('http://localhost:8001/apirequest/')



