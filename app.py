from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, template_folder='pages')

@app.route('/')
def home():
	return redirect(url_for('top_racers'))

@app.route('/top_racers')
def top_racers():
	return render_template('top_racers.html')

@app.route('/top_teams')
def top_teams():
    return render_template('top_teams.html')

if __name__ == '__main__':
	app.run()
