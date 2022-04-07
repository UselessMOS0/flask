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

linee['linea'] = linee.linea.astype(int)
linee['lung_km'] = linee.lung_km.astype(float)
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

    lineeminmax = linee[(linee.lung_km > minim) & (linee.lung_km < maxim)].sort_values(by='linea',ascending=True)
    return render_template('elenco.html',tabella = lineeminmax.to_html())

#es 2 -----------------------------------------------------------------------------------------------------------------------------


@app.route('/ricerca', methods=['GET'])
def ricerca():
    return render_template('ricerca.html')

    
@app.route('/elencolinee', methods=['GET'])
def elencolinee():
    quartiere = quartieri[quartieri.NIL.str.contains(request.args['u_quart'].upper())]
    lineequart = linee[linee.intersects(quartiere.geometry.squeeze())]

    return render_template('elencolinee.html',tabella = lineequart.sort_values(by='linea', ascending=True).to_html())



#es 2 -----------------------------------------------------------------------------------------------------------------------------


@app.route('/scelta', methods=['GET'])
def scelta():
    return render_template('scelta.html',linee = linee['linea'].drop_duplicates().sort_values(ascending=True))


@app.route('/mappa', methods=['GET'])
def mappa():
    global u_linea
    u_linea = int(request.args['u_linea'])
    return render_template('mappa.html')

@app.route('/mappa.png', methods=['GET'])
def mappampl():
    print(u_linea,type(u_linea))
    fig, ax = plt.subplots(figsize=(10,10))
    quartieri.to_crs(3857).plot(alpha=.5,ax=ax)
    linee[linee.linea==u_linea].to_crs(3857).plot(ax=ax,color='b')
    
    ctx.add_basemap(ax=ax)

    output=io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(),mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)