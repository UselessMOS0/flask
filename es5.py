# realizzare un sito web che restituisca la mappa dei quartieri di milano
# ci deve essere una homepage con un link "quartieri di milano": cliccando su questo link
# si deve visualizzare la mappa dei quartieri di milano 

from flask import Flask, render_template, send_file, make_response, url_for, Response, request
app = Flask(__name__)

import geopandas as gpd
import io 
import contextily as ctx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

districts = gpd.read_file('/workspace/flask/templates/es5/ds964_nil_wm-20220322T110843Z-001.zip')
print(districts)

@app.route('/', methods=['GET'])
def home():
    return render_template('es5/index.html')

@app.route('/districts.png', methods=['GET'])
def district():
    fig, ax = plt.subplots(figsize=(10,9))

    districts.to_crs(epsg=3857).plot(ax=ax, alpha=.5)
    ctx.add_basemap(ax=ax)

    result = io.BytesIO()
    FigureCanvas(fig).print_png(result)

    return Response(result.getvalue(),mimetype='image/png')

@app.route('/userdistrict', methods=['GET'])
def user_district():
    fig, ax = plt.subplots(figsize=(10,9))

    districts[districts.NIL == u_distr.upper()].to_crs(epsg=3857).plot(ax=ax, alpha=.5)
    ctx.add_basemap(ax=ax)

    result = io.BytesIO()
    FigureCanvas(fig).print_png(result)

    return Response(result.getvalue(),mimetype='image/png')

@app.route('/quartieri', methods=("POST", "GET"))
def mpl():
    return render_template('es5/plot.html')

@app.route('/quartiereUtente', methods=['GET'])
def u_mpl():
    global u_distr
    u_distr = request.args['user_district']
    return render_template('es5/plot1.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)