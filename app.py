from flask import Flask, render_template

homeTab = 'pages/top_racers_season.html'
app = Flask(__name__, template_folder='pages')

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

if __name__ == '__main__':
	app.run()