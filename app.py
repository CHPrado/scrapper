from flask import Flask
from scrapper import ZapImoveis

app = Flask(__name__)

@app.route('/')
def hello():
  scrapper = ZapImoveis() 
  return scrapper.navegar()

if __name__ == '__main__':
  app.run(debug=True)