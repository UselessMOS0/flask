#

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

dfRegioni = gpd.read_file('/workspace/flask/templates/es6/Reg01012021_g_WGS84.zip')

@app.route('/', methods=['GET'])
def home():
    print(dfRegioni)   
    return  render_template('index.html', regioni = dfRegioni.DEN_REG)

@app.route('/quartieri', methods=['GET'])
def quartieri():
    return render_template('quartieri.html')

@app.route('/quartieri.png',methods=['GET'])
def mplQrt():
    fig, axs = plt.subplots(2)

    axs[0] = 


    return Response()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)