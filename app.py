from flask import Flask, render_template
import json
import os

app = Flask(__name__, template_folder='pages')

filePath = os.path.join(app.root_path, 'data', 'users_in_lbs.json')
with open(filePath, 'r') as file:
	usersInLbs = json.load(file)

filePath = os.path.join(app.root_path, 'data', 'teams_in_lbs.json')
with open(filePath, 'r') as file:
	teamsInLbs = json.load(file)

filePath = os.path.join(app.root_path, 'data', 'banned_users.json')
with open(filePath, 'r') as file:
	bannedUsers = json.load(file)

filePath = os.path.join(app.root_path, 'data', 'banned_teams.json')
with open(filePath, 'r') as file:
	bannedTeams = json.load(file)

filePath = os.path.join(app.root_path, 'data', 'flagged_users.json')
with open(filePath, 'r') as file:
	flaggedUsers = json.load(file)

filePath = os.path.join(app.root_path, 'data', 'users_keywords.json')
with open(filePath, 'r') as file:
	usersKeywordsList = json.load(file)

filePath = os.path.join(app.root_path, 'data', 'active_teams_info.json')
with open(filePath, 'r') as file:
	activeTeamsInfo = json.load(file)

bannedUsers = set(bannedUsers)
bannedTeams = set(bannedTeams)
flaggedUsers = set(flaggedUsers)
teams = teamsInLbs.keys()
teams = [team for team in teams if team.isupper()]
usernames = usersInLbs.keys()
users = []
for username in usernames:
	users.append({'username': username, 'display_name': usersInLbs[username]['display_name']})
usersKeywords = []
for keyword in usersKeywordsList:
	if keyword['username'] in usernames:
		usersKeywords.append({'keyword': keyword['keyword'], 'username': keyword['username'], 'display_name': usersInLbs[keyword['username']]['display_name']})

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/tab/<tabName>')
def get_tab_content(tabName):
	try:
		return render_template(f'{tabName}.html')
	except Exception as e:
		return f"Content for {tabName} not found.\nError: {str(e)}"

@app.route('/data_update_timestamp')
def get_data_update_timestamp():
	try:
		return render_template('last_data_update_timestamp.html')
	except Exception as e:
		return "N/A"

@app.route('/get_admin_msg')
def get_admin_message():
	try:
		return render_template('admin_msg.html')
	except Exception as e:
		return "N/A"

@app.route('/get_all_flagged_botters')
def get_all_flagged_botters():
	try:
		return list(flaggedUsers)
	except Exception as e:
		return "N/A"

@app.route('/active_teams_info/<tag>')
def get_active_team_info(tag):
	if tag in activeTeamsInfo:
		return activeTeamsInfo[tag]
	else:
		return "N/A"

@app.route('/users_in_lbs/<username>')
def get_user_in_lb(username):
	if username in usersInLbs:
		return usersInLbs[username]
	else:
		return "N/A"

@app.route('/teams_in_lbs/<tag>')
def get_team_in_lb(tag):
	if tag in teamsInLbs:
		return teamsInLbs[tag]
	else:
		return "N/A"

@app.route('/is_user_banned/<username>')
def is_user_banned(username):
	isBanned = False
	isFlagged = False
	if username in bannedUsers:
		isBanned = True
	if username in flaggedUsers:
		isFlagged = True
	
	if not isBanned and not isFlagged:
		return "N"
	if isBanned and isFlagged:
		return "Y (ban+flag)"
	if isBanned and not isFlagged:
		return "Y (ban)"
	if not isBanned and isFlagged:
		return "Y (flag)"

@app.route('/is_team_banned/<tag>')
def is_team_banned(tag):
	if tag in bannedTeams:
		return "Y"
	else:
		return "N"

@app.route('/user_suggestions/<text>')
def user_suggestions(text):
	suggestions = []
	alreadySuggested = []
	numSuggestions = 0
	# username startswith txt
	for user in users:
		if numSuggestions >= 5:
			return suggestions
		if user['username'].startswith(text) and user['username'] not in alreadySuggested:
			suggestions.append(user['username'] + ' (' + user['display_name'] + ')')
			alreadySuggested.append(user['username'])
			numSuggestions += 1
	# display name startswith txt
	for user in users:
		if numSuggestions >= 5:
			return suggestions
		if user['display_name'].lower().startswith(text) and user['username'] not in alreadySuggested:
			suggestions.append(user['username'] + ' (' + user['display_name'] + ')')
			alreadySuggested.append(user['username'])
			numSuggestions += 1
	# keyword contains txt
	for keyword in usersKeywords:
		if numSuggestions >= 5:
			return suggestions
		if text in keyword['keyword'] and keyword['username'] not in alreadySuggested:
			suggestions.append(keyword['username'] + ' (' + keyword['display_name'] + ')')
			alreadySuggested.append(keyword['username'])
			numSuggestions += 1
	# username or display name contains txt
	for user in users:
		if numSuggestions >= 5:
			return suggestions
		if (text in user['username'] or text in user['display_name'].lower()) and user['username'] not in alreadySuggested:
			suggestions.append(user['username'] + ' (' + user['display_name'] + ')')
			alreadySuggested.append(user['username'])
			numSuggestions += 1
	if numSuggestions == 0:
		return "N/A"
	else:
		return suggestions

@app.route('/team_suggestions/<text>')
def team_suggestions(text):
	suggestions = []
	alreadySuggested = []
	numSuggestions = 0
	# tag startswith txt
	for team in teams:
		if numSuggestions >= 5:
			return suggestions
		if team.startswith(text) and team not in alreadySuggested:
			suggestions.append(team)
			alreadySuggested.append(team)
			numSuggestions += 1
	# tag contains txt
	for team in teams:
		if numSuggestions >= 5:
			return suggestions
		if text in team and team not in alreadySuggested:
			suggestions.append(team)
			alreadySuggested.append(team)
			numSuggestions += 1
	if numSuggestions == 0:
		return "N/A"
	else:
		return suggestions

if __name__ == '__main__':
	app.run()