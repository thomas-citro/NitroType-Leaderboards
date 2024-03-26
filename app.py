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


if __name__ == '__main__':
	app.run()