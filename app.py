from flask import Flask, render_template
import json
import os

homeTab = 'pages/top_racers_season.html'
app = Flask(__name__, template_folder='pages')

filePath = os.path.join(app.root_path, 'data', 'users_in_lbs.json')
with open(filePath, 'r') as file:
	usersInLbs = json.load(file)

filePath = os.path.join(app.root_path, 'data', 'teams_in_lbs.json')
with open(filePath, 'r') as file:
	teamsInLbs = json.load(file)

teams = teamsInLbs.keys()
teams = [team for team in teams if team.isupper()]
usernames = usersInLbs.keys()
users = []
for username in usernames:
	users.append({'username': username, 'display_name': usersInLbs[username]['display_name']})

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
		return render_template(f'last_data_update_timestamp.html')
	except Exception as e:
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