import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

MBTI_indexes = {
    "INTJ": 0,
    "INTP": 1,
    "ENTJ": 2,
    "ENTP": 3,

    "INFJ": 4,
    "INFP": 5,
    "ENFJ": 6,
    "ENFP": 7,

    "ISTJ": 8,
    "ISFJ": 9,
    "ESTJ": 10,
    "ESFJ": 11,

    "ISTP": 12,
    "ISFP": 13,
    "ESTP": 14,
    "ESFP": 15,
}

# reference: https://open.spotify.com/user/pq8w5snqhyu97x4x4kmsmaxup/playlists
MBTI_playlists = [
  ['4acQIuCN9aeFBCpr9vubVd', '6ocmyGGftkUZHJ0n9awpic', '1WzuaRUxekhPMBZEsszcSe', '34zlRD1iOauOEarXeioIkF', '0Ip95waV5jsOSvOZn10DTc'],
  ['55tWFSrWv5N132X6zHIO5v', '7a1NapcyZ2e8Bmox6V0MSH', '5EfNQZ8IDMbCgdbBYy8pXO', '54YCS9D2dr1AisRScAx8gl', '2JVtayh4spaHi3762hoJWQ'],
  ['2MiqxSFSTyJFBMBXnBHYH4', '0F30ijpg50ABLb5ohmtmp3', '3i2sBpBI7VKznMsvl7UH6j', '0Tbo6gBc7zsI8X2x04isvi', '7jmnBH2b8DFCEayotoAgAd'],
  ['1EzjgL6RF95f5QoZ7GhXUE', '4ScfRJB3qcMUKdJ5mOZUB0', '5Ic6h1cZIT0MIe8qmyxhC1', '1hBpfY9PYUjgVOEvyzqkTU', '3dsXsupZkWBN6xVGoi6DuL'],

  ['7AKVZtpDloU0tsf8f26gKN', '2J1Xdogu9HbBxJvrutXGNi', '39oj6TOAf9CPaPjQD9NmM5', '2HTkX7Q03qo3jrPvfz1XCy', '3IEPeg2dfjXiRuAketmy8M'],
  ['11gIBNBNUbpiM8WwKrMp8i', '7haMzDleVTr4uAltOPveEJ', '3jdYow8s08PgEKYwXL2uX0', '6MmxNmITZDpdOd1jlwQOxx', '4F5VDfTrksyhuT0wbuAE5V'],
  ['4gtLRPzwpUXXrYi3uIiMgP', '4AE4DBt4YjJJ8v4Hk9myWl', '4w5Rr4z1YrrRwt2qtgtgcl', '5XCk4WUE71D7m8CkV5g5oG', '6IYbjtqjOOVeq9hjyll0R2'],
  ['70OTqsaDO26cpTwFZbGNRb', '5J3tDgBRt4BkebL1N9ykZU', '1rfeszkxZKbJyq44hF2voC', '758jPdwPa3EdtXgrpx5URY', '7rcEnzK6DANSoBhf7GMwSi'],
  
  ['4qhJjuTNmmAwRoFAER1Wxr', '0EctXmIqa6mA4uLo5TojBT', '2AxqeM4iZrKp93SHznEJpl', '3Nn0M9rF3X5umZzMojv9CL', '6ZwvfVF1CHP0p4IBag8ONw'],
  ['0lYllEZHsSAuVE0bBsYTvA', '5O6UX2oYe51o2VBT804788', '0dZkJnJuZHZbgSEPVgxiXV', '0eymdBMDZ3edB8LWG0w5MU', '4jlZ5ehLh6sV1qrf0eef5K'],
  ['4vZIQ9H9u0XORVSTPk04T4', '5JJAGSC9jMsBicBVTIKuyw', '1s59H8zfMEUPQx0Wvk5TI9', '2UAj0iBYYQcXm3gD9bcjM9', '3K71TN0WJioIYr2jCUZFYi'],
  ['6PsawaiOyvzoNX6h6B8DUE', '6VfTmFmtJUSQhyQFsQvOsI', '24WCUtRtXmIeKbYiyc1Oyn', '2ndIXL3CGNGzvrm2QRgzdT', '5gNrnzaUo5WppTpwWprXBW'],
  
  ['1o7ufSKxAiLyiiyJwtx6ij', '0uU0Sn7IehlZujmz10cnlV', '6hT9flu2FlKbieK9g8G7Ln', '2AuZrRinHETn7Xu151eXaz', '0uU0Sn7IehlZujmz10cnlV'],
  ['3BFf4l51YQqpDxg10f4ZCy', '5bQ62NFhoBa2qMsC2BVrZW', '2quLJKoTXbcbcHP43QWer4', '4QcaVYy1RXPkGBw8soOwT8', '76XDJfQ6hw05ZImpYNbgNX'],
  ['52Nr2jMtUOgmHKAFPLQ6Jb', '65r8dT97EcHxBl2pW0jhzx', '3Lwgk3xP0UNPKZRQM9kBQV', '481IlgiH0qyhSE5gGnLh15', '5nkqr7vgFYYGnDRQlsDv0k'],
  ['6DjPVCftL0PANfY69Wh7ux', '5fxEXREieENyuznU1Icr7w', '3RW3FHxSWLiJ8iFrxOOiMH', '0sf2ZiHCo5FmtPdOnACzZi', '4pi2j0t6uT4YtBXnT2gAa4'],
]

index = 15 # change this
MBTI_keys = list(MBTI_indexes.keys())
print(index, MBTI_keys[index])

arr = []
data_size = 0
for playlist_uri in MBTI_playlists[index]:
  time.sleep(1)
  response = sp.playlist(playlist_uri)
  songs_in_playlist = response["tracks"]["items"]
  id_arr = [ele["track"]["id"] for ele in songs_in_playlist]
  features = sp.audio_features(id_arr)
  data_size = data_size + len(features)
  print(data_size)
  for feature in features:
    arr.append(
      str(feature["acousticness"]) + ',' 
      + str(feature["danceability"]) + ',' 
      + str(feature["energy"]) + ',' 
      + str(feature["instrumentalness"]) + ',' 
      + str(feature["key"]) + ',' 
      + str(feature["liveness"]) + ',' 
      + str(feature["loudness"]) + ',' 
      + str(feature["speechiness"]) + ',' 
      + str(feature["tempo"]) + ',' 
      + str(feature["time_signature"]) + ',' 
      + str(feature["valence"]) + ',' 
      + str(index) + '\n'
    )

csv = open("data/data_{}_{}_{}.csv".format(str(index), MBTI_keys[index], len(arr)), "w")
csv.write("acousticness,danceability,energy,instrumentalness,key,liveness,loudness,speechiness,tempo,time_signature,valence,mbti\n")
for record in arr:
  csv.write(record)

# with open("data.txt", "w") as f:
#   print(data)
#   f.write(str(data))

# print(sp.audio_features("3CnUGF7phvydXWBJUBDDP6")[0])