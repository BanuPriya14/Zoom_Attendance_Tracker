import requests
import json

# API credentials
api_key = 'mhZARgRdRwipKD9siNdjWA'
api_secret = 'KW4VCwg3TT2WfsRLjbb-lw'

# Generate JWT token
import jwt
import datetime

token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # Token expires in 1 hour
token_payload = {
    'iss': api_key,
    'exp': token_exp
}
jwt_token = jwt.encode(token_payload, api_secret, algorithm='HS256')

# Meeting ID for which you want to get attendees
meeting_id = '88321453048'

# API endpoint
url = f'https://api.zoom.us/v2/report/meetings/{meeting_id}/participants'

# Headers
headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Content-Type': 'application/json'
}

# Make GET request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    attendees = response.json()
    print(json.dumps(attendees, indent=4))
else:
    print(f'Failed to retrieve attendees. Status code:{response.status_code}, Error: {response.text}')