from django.shortcuts import render
from django.http import *
from requests_oauthlib import OAuth2Session


client_id = "test"
client_secret = "CWHpQb1d2j!oULsPQ:zt3ekStD7izej8VKTp!rl7zdPjdbDhg3Yz1@h?Q!HRFunDXugT@MXAaIk=J6FK7?KttPvkO:e2QQo=UJh9!tZ?y;4K4tdLPgnqcI=:JHjlS9cP"
redirect_uri = "http://localhost:8001/apirequest/auth_code_given/"

def index(request):
	scope = ['read']
	oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
	authorization_url, state = oauth.authorization_url('http://localhost:8000/o/authorize/')
	return HttpResponseRedirect(authorization_url)

def auth_code_given(request):
	authorization_code = request.GET.get('code')
	oauth =  OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
	token = oauth.fetch_token('http://localhost:8000/o/token',
    	authorization_response=authorization_code, client_secret=client_secret)
	request.session['token'] = token
	r = oauth.get('http://localhost:8000/api/student/1/.json')
	return HttpResponse('Authenticated :) <br/>' + r)
	#return HttpResponse('bah')



