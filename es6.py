from flask import Flask, render_template, Response, request
from string import Template
app = Flask(__name__)

import geopandas as gpd
import io 
import contextily as ctx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

province = gpd.read_file('/workspace/flask/templates/es6/ProvCM01012021_g_WGS84.zip')
regioni = gpd.read_file('/workspace/flask/templates/es6/Reg01012021_g_WGS84.zip')
comuni = gpd.read_file('/workspace/flask/templates/es6/Com01012021_g_WGS84.zip')

@app.route('/', methods=['GET'])
def home():
  return  render_template('es6/index.html',regioni=regioni.DEN_REG)

@app.route('/province', methods=['GET'])
def provroute():
  global provinceReg
  ureg = request.args['uReg']
  provinceReg = province[province.within(regioni[regioni.DEN_REG == ureg].geometry.squeeze())]
  return render_template('es6/regione.html', provinceReg = provinceReg.DEN_PROV, ureg = ureg)

@app.route('/comuni', methods=['GET'])
def comroute():
  uprov = request.args['provincia']
  comProv = comuni[comuni.within(provinceReg[provinceReg.DEN_PROV == uprov].geometry.squeeze())]
  return render_template('es6/comuni.html', comProv = comProv.COMUNE.sort_values(ascending=True), uprov = uprov)


#@app.route('/comune.png', methods=['GET'])
#def mplcom():
#    ucom = 

#    fig, ax = plt.subplots(figsize = (12,8))

#    ucom.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
#    contextily.add_basemap(ax=ax) 

#    output = io.BytesIO()
#    FigureCanvas(fig).print_png(output)
#    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)