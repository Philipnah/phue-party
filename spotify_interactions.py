import requests
import webbrowser
import base64
import datetime
from secrets import *

SPOTIFY_GET_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"
SPOTIFY_URI_REDIRECT = "https://philipnah.github.io/"
SPOTIFY_URI_REDIRECT_ENCODED = "https%3A%2F%2Fphilipnah.github.io%2F"
SPOTIFY_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"

# see currently playing and analyse tracks 
scopes = "user-read-currently-playing"

class spotify_interactions():
	access_token = None
	tokenExpires = datetime.datetime.now()

	def SpotifyConnect(self):
		"""
		Returns access token and refresh token
		"""
		
		# First send this url to spotify with all information
		spotify_get_url = f"{SPOTIFY_AUTHORIZE_URL}?client_id={clientID}&response_type=code&redirect_uri={SPOTIFY_URI_REDIRECT_ENCODED}&scope={scopes}"
		webbrowser.open(spotify_get_url,new=2)

		# receive response from spotify
		returnedURL = input("Copy and paste the url from your browser here: ")

		# isolates the access_token from url
		returnedAccessToken = returnedURL.split("code=")[1]
		
		# create client base64 string
		clientData = f"{clientID}:{clientSecret}"
		clientDataAscii = clientData.encode('ascii') 
		clientDataEncode = base64.b64encode(clientDataAscii)
		base64ClientData = clientDataEncode.decode('ascii')

		# get access token and refresh token
		response = requests.post(
			SPOTIFY_ACCESS_TOKEN_URL,
			headers={"Authorization": f"Basic {base64ClientData}",
				"Content-Type": "application/x-www-form-urlencoded"
			},
			data={
				"grant_type":"authorization_code",
				"code": returnedAccessToken,
				"redirect_uri": SPOTIFY_URI_REDIRECT,
			}
		)

		if response.status_code == 200:
			print("\nrequests was successful!\n")
			print(response.json())
		else:
			print("\n", response.status_code, response.text)
		
		# authURL = "https://accounts.spotify.com/api/token"
		
		# message = f"{clientID}:{clientSecret}"
		# messageAscii = message.encode('ascii') 
		# messageEncode = base64.b64encode(messageAscii)
		# base64Message = messageEncode.decode('ascii')

		# authHeaders = {"Authorization": "Basic " + base64Message}
		# authData = {"grant_type": "client_credentials"}

		# nowTime = datetime.datetime.now()
		# response = requests.post(authURL, headers=authHeaders, data=authData).json()
		
		# self.tokenExpires = nowTime + datetime.timedelta(response['expires_in'] - 10)
		# self.access_token = response['access_token']

		# return response['access_token']

	# Music needs to be playing, otherwise the API will return HTTP status_code 204 (No content)
	def GetCurrentTrack(self):
		# access_token = self.EstablishContact()
		# if datetime.datetime.now() > self.tokenExpires:
			# EstablishContact()

		response = requests.get(
			SPOTIFY_GET_TRACK_URL,
			headers={"Authorization": f"Bearer {self.access_token}"}
		)

		trackInfo = response.json()

		if response.status_code == 200:
			return {"name": trackInfo['item']['name'], "id": trackInfo['item']['id']}

		if response.status_code == 204:
			print("Nothing is playing on your spotify account right now, please try again")
		else:
			print(f"An error occurred. This was the API response: {response.status_code}")

	def GetTrackTempo(self, currentTrack):
		# The current track should be inputted as dictionary with name and id
		pass


spot = spotify_interactions()
print(spot.SpotifyConnect())
# print(spot.GetCurrentTrack())