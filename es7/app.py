from flask import Flask, render_template, Response, request
app = Flask(__name__)

import pandas as pd
import geopandas as gpd
import io 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

stazioni = pd.read_csv('templates/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv',sep=';')
stazionigeo = gpd.read_file('templates/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv')

@app.route('/', methods=['GET'])
def home():
    return  render_template('index.html')

    
@app.route('/numero', methods=['GET'])
def num():
    global risultato
    # numero stazioni per ogni municipio
    risultato = stazioni[['OPERATORE','MUNICIPIO']].groupby('MUNICIPIO',as_index=False).count().sort_values(by='MUNICIPIO',ascending=True)
    return  render_template('elenco.html',risultato = risultato.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
    fig, ax = plt.subplots(figsize=(10,10))

    ax.bar(risultato.MUNICIPIO,risultato.OPERATORE)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(),mimetype='image/png')

@app.route('/input', methods=['GET'])
def input():
    return  render_template('input.html')
    

@app.route('/ricerca', methods=['GET'])
def ricerca():

    return
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)