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
stazioni = gpd.read_file('https://dati.comune.milano.it/dataset/7fae4996-02e1-4a80-8794-9ec22454041b/resource/eec5e0ef-2622-443e-a2e4-8b066af2e093/download/ds710_coordfix_ripetitori_radiofonici_milano_160120_loc_final.geojson').to_crs(4326)
print(quartieri.crs,stazioni.crs)


@app.route('/', methods=['GET'])
def home():
    return  render_template('index.html')

#es 1 -----------------------------------------------------------------------------------------------------------------------------

@app.route('/sceltaQuartiere', methods=['GET'])
def sceltaQuartiere():
    return  render_template('scelta.html', quartieri = quartieri.NIL.sort_values(ascending=True))

    
@app.route('/quartierestaz', methods=['GET'])
def quartierestaz():
    u_quart = request.args['scelta']
    stquart = stazioni[stazioni.within(quartieri[quartieri.NIL == u_quart].geometry.squeeze())]
    print(stquart)
    return  render_template('quartstaz.html',stazioni = stquart.OPERATORE)

#es 2 -----------------------------------------------------------------------------------------------------------------------------

@app.route('/ricerca', methods=['GET'])
def ricerca():
    return  render_template('ricerca.html')

@app.route('/mappa', methods=['GET'])
def mappa():
    global userQuart
    userQuart = quartieri[quartieri.NIL.str.contains(request.args['u_quart'])]
    
    return render_template('mappa.html')

    
@app.route('/mappa.png', methods=['GET'])
def mlpmappa():
    fig, ax = plt.subplots(figsize=(10,10))
    
    userQuart.to_crs(3857).plot(alpha=.5,ax=ax)
    stazioni[stazioni.within(userQuart.geometry.squeeze())].to_crs(3857).plot(color='k',ax=ax)
    ctx.add_basemap(ax=ax)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(),mimetype='image/png')

#es 3 -----------------------------------------------------------------------------------------------------------------------------

@app.route('/grafico', methods=['GET'])
def grafico():
    global data

    data = stazioni[['MUNICIPIO','OPERATORE']].groupby('MUNICIPIO',as_index=False).count().sort_values(by='MUNICIPIO',ascending=True)

    return  render_template('grafico.html',tabella = data.to_html())

    
@app.route('/grafico.png', methods=['GET'])
def mlpgrafico():

    fig,ax = plt.subplots(figsize=(10,10))

    ax.bar(data.MUNICIPIO,data.OPERATORE)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return  Response(output.getvalue(),mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)