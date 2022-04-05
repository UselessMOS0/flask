from flask import Flask, render_template, Response, request, redirect, url_for
app = Flask(__name__)

import pandas as pd
import geopandas as gpd
import io 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import contextily as ctx

stazioni = pd.read_csv('templates/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv',sep=';')
stazionigeo = gpd.read_file('https://dati.comune.milano.it/dataset/7fae4996-02e1-4a80-8794-9ec22454041b/resource/eec5e0ef-2622-443e-a2e4-8b066af2e093/download/ds710_coordfix_ripetitori_radiofonici_milano_160120_loc_final.geojson')
quartieri = gpd.read_file('/workspace/flask/templates/es5/ds964_nil_wm-20220322T110843Z-001.zip')
print(quartieri)

@app.route('/', methods=['GET'])
def home():
    return  render_template('index.html')

@app.route('/redirect', methods=['GET'])
def redir():
    if request.args['opt'] == '1':
        return redirect(url_for('numero'))
    elif request.args['opt'] == '2':
        return redirect(url_for('input'))
    else:
        return redirect(url_for('dropdown'))

    
@app.route('/numero', methods=['GET'])
def numero():
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
    global u_quart, stazioni_quartiere
    u_quart = quartieri[quartieri.NIL.str.contains(request.args['quartiere'])]
    stazioni_quartiere = stazionigeo[stazionigeo.within(u_quart.geometry.squeeze())]
    return  render_template('elenco1.html',stazioni_quart = stazioni_quartiere.to_html())
    

@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize=(10,10))

    u_quart.to_crs(3857).plot(alpha=.5)
    stazioni_quartiere.to_crs(3857).plot(color='k',ax=ax)
    ctx.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(),mimetype='image/png')

@app.route('/dropdown', methods=['GET'])
def dropdown():
    nomi_stazioni = stazioni.OPERATORE.drop_duplicates().sort_values(ascending=True).to_list()
    return render_template('dropdown.html', stazioni = nomi_stazioni)

@app.route('/sceltastazioni', methods=['GET'])
def sceltastazioni():
    stazione = stazioni[stazioni.OPERATORE.str.contains(request.args['stazione'])]
    return render_template('vistastazione.html', stazione = stazione.to_html())

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)