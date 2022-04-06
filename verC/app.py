from flask import Flask, render_template, url_for, redirect, request, Response
app = Flask(__name__)

import geopandas as gpd
import io 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import contextily as ctx

quartieri = gpd.read_file('/workspace/flask/templates/es5/ds964_nil_wm-20220322T110843Z-001.zip')
linee = gpd.read_file('https://dati.comune.milano.it/dataset/8bfe2015-2669-4796-9940-36b3c155b258/resource/b5acc06f-65fb-4481-9428-347fd1c18096/download/tpl_percorsi.geojson').to_crs(4326)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

    
@app.route('/redir', methods=['GET'])
def redir():
    opz = request.args['scelta']
    if opz == '1':
        return redirect(url_for('valori'))
    elif opz == '2':
        return redirect(url_for('ricerca'))
    elif opz == '3':
        return redirect(url_for('scelta'))
#es 1 -----------------------------------------------------------------------------------------------------------------------------

@app.route('/valori', methods=['GET'])
def valori():
    return render_template('valori.html')

@app.route('/elenco', methods=['GET'])
def elenco():
    minim = float(min(request.args['val'],request.args['val2']))
    maxim = float(max(request.args['val'],request.args['val2']))
    
    linee['linea'] = linee.linea.astype(int)
    linee['lung_km'] = linee.lung_km.astype(float)

    lineeminmax = linee[(linee.lung_km > minim) & (linee.lung_km < maxim)].sort_values(by='linea',ascending=True)
    return render_template('elenco.html',tabella = lineeminmax.to_html())



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)