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

@app.route('/', methods=['GET'])
def home():
  return  render_template('index.html')
  



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)