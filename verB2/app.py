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


province['AREA'] = province.geometry.area

@app.route('/', methods=['GET'])
def home():
  return  render_template('index.html')
  
@app.route('/ricerca', methods=['GET'])
def home():
  return  render_template('ricerca.html')

@app.route('/mappa', methods=['GET'])
def home():
  u_reg = regioni[regioni.REGIONE.str.contains(request.args['u_reg'])]
  lung = u_reg.geometry.length/1000
  prov_in_reg = province[province.within(u_reg.geometry.squeeze())].sort_values(by='AREA',ascending=False)['PROVINCIA']
  return render_template('mappa.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)