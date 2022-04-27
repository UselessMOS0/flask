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

regioni = gpd.read_file('/workspace/flask/verB2/static/Reg01012021_g_WGS84.zip')
province = gpd.read_file('/workspace/flask/verB2/static/ProvCM01012021_g_WGS84.zip').to_crs(32632)
ripgeo = gpd.read_file('/workspace/flask/verB2/static/RipGeo01012021_g_WGS84.zip').to_crs(32632)

province['AREA'] = province.geometry.area

@app.route('/', methods=['GET'])
def home():
  return  render_template('index.html')
  
@app.route('/ricerca', methods=['GET'])
def ricerca():
  return  render_template('ricerca.html')

@app.route('/mappa', methods=['GET'])
def mappa():
  global u_reg
  u_reg = regioni[regioni.DEN_REG.str.contains(request.args['u_reg'])]
  lung = u_reg.geometry.length/1000
  prov_in_reg = province[province.within(u_reg.geometry.squeeze())].sort_values(by='AREA',ascending=False)['DEN_PROV']
  return render_template('mappa.html',lung = lung, prov = prov_in_reg)

@app.route('/scelta', methods=['GET'])
def scelta():
  return render_template('scelta.html', ripartizioni = ripgeo["DEN_RIP"])

@app.route('/scelta2', methods=['GET'])
def scelta2():
  reg_in_rip = regioni[regioni.within(ripgeo[ripgeo.DEN_RIP == request.args['u_rip']].geometry.squeeze())]['DEN_REG'].sort_values(ascending=True)
  return render_template('scelta2.html',reg = reg_in_rip)

@app.route('/seleziona', methods=['GET'])
def seleziona():
  return render_template('seleziona.html', ripartizioni = ripgeo["DEN_RIP"])

@app.route('/seleziona2', methods=['GET'])
def seleziona2():
  reg_in_rip = regioni[regioni.within(ripgeo[ripgeo.DEN_RIP == request.args['u_rip']].geometry.squeeze())]['DEN_REG'].sort_values(ascending=True)
  return render_template('seleziona2.html', reg = reg_in_rip)

@app.route('/mappa.png', methods=['GET'])
def mpl():
  fig , ax = plt.subplots(figsize=(10,10))

  u_reg.to_crs(3857).plot(ax=ax,facecolor='none',edgecolor='r')
  ctx.add_basemap(ax=ax)
  
  output=io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(),mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)