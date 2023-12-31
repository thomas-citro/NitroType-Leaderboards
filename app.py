from flask import Flask, render_template

homeTab = 'pages/top_racers_season.html'
app = Flask(__name__, template_folder='pages')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/tab/<tabName>')
def get_tab_content(tabName):
	try:
		with open(f'C:\\Projects\\Nitro Type Leaderboards\\NitroType-Leaderboards\\pages\\{tabName}.html', 'r') as file:
			content = file.read()
		return content
	except Exception as e:
		print(f"Error: {str(e)}")
		return f"Content for {tabName} not found."

if __name__ == '__main__':
	app.run()
