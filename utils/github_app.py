import requests
import time
import jwt
import os

app_id = '903588'
installation_id = '51026556'
private_key = os.environ.get("GITHUB_APP_PRIVATE_KEY_1")

def generate_jwt():
	payload = {
		'iat': int(time.time()),
		'exp': int(time.time()) + (10 * 60),  # JWT expiration time (10 minutes)
		'iss': app_id
	}
	encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')
	return encoded_jwt

def get_installation_access_token():
	jwt_token = generate_jwt(app_id, private_key)
	headers = {
		'Authorization': f'Bearer {jwt_token}',
		'Accept': 'application/vnd.github.v3+json'
	}
	url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
	response = requests.post(url, headers=headers)
	response_data = response.json()
	return response_data['token']

def list_repo_contents(owner, repo, path, access_token):
	headers = {
		'Authorization': f'token {access_token}',
		'Accept': 'application/vnd.github.v3+json'
	}
	url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
	response = requests.get(url, headers=headers)
	return response.json()

def list_all_files(owner, repo, path='', access_token=None, files=[]):
	contents = list_repo_contents(owner, repo, path, access_token)
	for item in contents:
		if item['type'] == 'file':
			files.append(item['path'])
		elif item['type'] == 'dir':
			list_all_files(owner, repo, item['path'], access_token, files)