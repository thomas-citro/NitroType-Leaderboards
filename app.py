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
		#with open(f'pages\\{tabName}.html', 'r', encoding='utf-8') as file:
		#	content = file.read()
		#return content
	except Exception as e:
		#print(f"Error: {str(e)}")
		return f"Content for {tabName} not found.\nError: {str(e)}"

if __name__ == '__main__':
	app.run()
