from flask import Flask, render_template, url_for
import random

app = Flask(__name__)

imglist = ['/static/images/meteo/cloudy.jpg',
          '/static/images/meteo/rain.jpg',
          '/static/images/meteo/sunny.jpg']

weatherlst = ['nuvoloso','piovoso','soleggiato']

frasilst = [{'autore':'Johann Wolfgang von Goethe','frase' : 'Il dubbio cresce con la conoscenza.'},
        {'autore':'Luis Sepùlveda','frase' : 'Vola solo chi osa farlo.'},
        {'autore':'Lucio Anneo Seneca','frase' : 'Se vuoi essere amato, ama.'},
        {'autore':'Voltaire','frase' : 'Chi non ha bisogno di niente non è mai povero.'},
        {'autore':'Confucio','frase' : "Non importa quanto vai piano, l' importante è non fermarsi."},
        {'autore':'Steve Jobs','frase' : 'Siate affamati, siate folli.'},
        {'autore':'Walt Disney','frase' : 'Pensa, credi, sogna e osa.'},
        {'autore':'Mark Twain','frase' : 'Il segreto per andare avanti è iniziare.'}]

@app.route('/', methods=['GET'])
def es1():
    return  render_template('es1/es1.html')

@app.route('/meteo', methods=['GET'])
def meteo():
    i = random.randrange(0,3)
    return render_template('es1/meteo.html',img = imglist[i], weather = weatherlst[i])

@app.route('/frasicelebri', methods=['GET'])
def frasi():
    i = random.randrange(0,len(frasilst))
    return render_template('es1/frasi.html',frase = frasilst[i]['frase'] , autore = frasilst[i]['autore'])

@app.route('/quantomanca', methods=['GET'])
def cdscuola():
    return render_template('es1/countd.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)