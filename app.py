from flask import Flask

app = Flask(__name__)

@app.route('/')
def print_welcome_message():
  return 'Nitro Type Leaderboards'

if __name__ == '__main__':
  app.run()
