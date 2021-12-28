import requests
import webbrowser
import base64
import datetime
from secrets import *

SPOTIFY_GET_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"
SPOTIFY_TRACK_ANALYSIS = "https://api.spotify.com/v1/audio-analysis/"

SPOTIFY_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"

SPOTIFY_URI_REDIRECT = "https://philipnah.github.io/"
SPOTIFY_URI_REDIRECT_ENCODED = "https%3A%2F%2Fphilipnah.github.io%2F"

# see currently playing and analyse tracks 
scopes = "user-read-currently-playing"

class spotify_interactions():
	access_token = None
	refresh_token = None
	tokenExpires = datetime.datetime.now()

	def SpotifyConnect(self):
		"""
		Returns access token and refresh token in json format.
		"""
		
		if self.tokenExpires > datetime.datetime.now():
			spotify_interactions.RefreshAccessToken()
		
		# First send this url to spotify with all information
		spotify_get_url = f"{SPOTIFY_AUTHORIZE_URL}?client_id={clientID}&response_type=code&redirect_uri={SPOTIFY_URI_REDIRECT_ENCODED}&scope={scopes}"
		webbrowser.open(spotify_get_url, new=2)

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
		
		nowTime = datetime.datetime.now()

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
			print("\nAccess and refresh token received successfully\n")
			# print(response.json())
		else:
			print("\n", response.status_code, response.text)

		jsonResponse = response.json()

		# sets the expireTime of the access token
		self.tokenExpires = nowTime + datetime.timedelta(jsonResponse['expires_in'] - 10)
		self.access_token = jsonResponse['access_token']
		self.refresh_token = jsonResponse['refresh_token']

		return jsonResponse

	def RefreshAccessToken(self):

		# create client base64 string
		clientData = f"{clientID}:{clientSecret}"
		clientDataAscii = clientData.encode('ascii') 
		clientDataEncode = base64.b64encode(clientDataAscii)
		base64ClientData = clientDataEncode.decode('ascii')


		response = requests.post(SPOTIFY_ACCESS_TOKEN_URL,
			headers={"Authorization": f"Basic {base64ClientData}"},
			data={"grant_type": "refresh_token",
			"refresh_token": self.refresh_token}
		)

		self.access_token = response.json()['access_token']
		print("\nNew access token received successfully\n")


	# Music needs to be playing, otherwise the API will return HTTP status_code 204 (No content)
	def GetCurrentTrack(self):
		
		if datetime.datetime.now() > self.tokenExpires:
			spotify_interactions.refresh_token()

		response = requests.get(
			SPOTIFY_GET_TRACK_URL,
			headers={"Authorization": f"Bearer {self.access_token}"}
		)

		trackInfo = response.json()

		if response.status_code == 200:
			if trackInfo['currently_playing_type'] == 'episode':
				print("You can't get track info of podcasts, play a music track first.")
				return "Play music first"

			return {"name": trackInfo['item']['name'], "id": trackInfo['item']['id']}

		if response.status_code == 204:
			print("Nothing is playing on your spotify account right now, please try again")
		else:
			print(f"An error occurred. This was the API response: {response.status_code}")

	def GetTrackTempo(self, currentTrack):
		"""
		The current track should be inputted as dictionary with name and id. Returns track tempo.
		"""

		response = requests.get(
			SPOTIFY_TRACK_ANALYSIS + str(currentTrack['id']),
			headers={"Authorization": f"Bearer {self.access_token}"}
		).json()

		tempo = response['track']['tempo']
		return tempo



spotify_client = spotify_interactions()

# Always run SpotifyConnect() first
spotify_client.SpotifyConnect()

# print(spotify_client.GetTrackTempo(spotify_client.GetCurrentTrack()))