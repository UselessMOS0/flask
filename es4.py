# Si vuole realizzare un sito web per memorizzare le squadre di uno sport a scelta. 
# L'utente deve poter inserire il nome della squadra e la data di fondazione e la città.
# Deve inoltre poter effetturare delle ricerche inserendo uno dei valori delle colonne e ottenendo i dati presenti.

from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if method == 'GET':
        return  render_template('es4/index.html')
    else:
        
        return


@app.route('/data',methods=['GET'])
def data():
    team, year, city = request.args['team'],request.args['year'],request.args['city']
    df = pd.read_csv('/workspace/flask/templates/es4/dati.csv')
    data = {'team' : team , 'year' : year , 'city' : city}
    print(data)
    df = df.append(data,ignore_index=True)
    print(df)
    df.to_csv('/workspace/flask/templates/es4/dati.csv',index=False)

    return df.to_html()



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)