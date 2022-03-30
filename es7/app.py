from flask import Flask, render_template, Response, request
app = Flask(__name__)

import pandas as pd

stazioni = pd.read_csv('es7/templates/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv',sep=';')

@app.route('/', methods=['GET'])
def home():
    return  render_template('index.html')

    
@app.route('/numero', methods=['GET'])
def home():
    # numero stazioni per ogni municipio
    risultato = stazioni[['OPERATORE','MUNICIPIO']].groupby('MUNICIPIO',as_index=False).count().sort_values(by='MUNICIPIO',ascending=True)
    return  render_template('elenco.html',risultato = risultato.to_html())

    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)