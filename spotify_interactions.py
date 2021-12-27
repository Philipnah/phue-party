import requests
import base64
import datetime
from secrets import *

SPOTIFY_GET_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"

class spotify_interactions():
	access_token = "BQA16-fin1asMjEGV1CqBBPkvG0v_MJ8V3OnQgANZbo6mwoTeC2UU_SPIHhMmp-srv43Wx8pAkHCtcCgu0D32wqs5yIPFXZG1LeUI1P5s2nDziukSD6L6ant3_MnWtaQjgd396QPzprNxsKWjPNV7hD_AJlhlgk"
	tokenExpires = datetime.datetime.now()

	def EstablishContact(self):
		"""Returns 'access token', when clientID and clientSecret are sent to spotify."""
		authURL = "https://accounts.spotify.com/api/token"
		
		message = f"{clientID}:{clientSecret}"
		messageAscii = message.encode('ascii') 
		messageEncode = base64.b64encode(messageAscii)
		base64Message = messageEncode.decode('ascii')

		authHeaders = {"Authorization": "Basic " + base64Message}
		authData = {"grant_type": "client_credentials"}

		nowTime = datetime.datetime.now()
		response = requests.post(authURL, headers=authHeaders, data=authData).json()
		
		self.tokenExpires = nowTime + datetime.timedelta(response['expires_in'] - 10)
		self.access_token = response['access_token']

		return response['access_token']

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
# print(spot.EstablishContact())
print(spot.GetCurrentTrack())