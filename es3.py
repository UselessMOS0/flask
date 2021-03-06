#server web che permetta di conoscere capoluoghi di regione
#l'utente inserisce il nome della regione e il programma restituisce il
#capoluogo di regione
# caricare i capoluoghi in un opportuna struttura dati
# 
# modificare poi l'es precedente per permettere all'utente di inserire
# un capoluogo e avere la regione in cui si trova
# l'utente sceglie se avere la regione o il capoluogo selezionando un radio button 

from flask import Flask, render_template, request, url_for
app = Flask(__name__)

regcap = {"Abruzzo" :"L\'Aquila",
        "Basilicata"	:"Potenza",
        "Campania"	:"Napoli","Calabria":	"Catanzaro",
        "Emilia-Romagna":"Bologna",
        "Friuli-Venezia Giulia"	:"Trieste",
        "Lazio"	:"Roma",
        "Liguria":	"Genova",
        "Lombardia":"Milano",
        "Marche":"Ancona",
        "Molise":"Campobasso",
        "Piemonte":"Torino",
        "Puglia":"Bari",
        "Sardegna":"Cagliari",
        "Sicilia":"Palermo",
        "Toscana":"Firenze",
        "Trentino-Alto Adige":"Trento",
        "Umbria":"Perugia",
        "Valle d Aosta":"Aosta",
        "Veneto":"Venezia"}

@app.route('/', methods=['GET','POST'])
def home():
  if request.method == 'GET':
    return  render_template('es3/index.html')
  else:
    input = request.form.get('input')
    srccap = int(request.form.get('opt'))

    for reg,cap in regcap.items():
      if srccap:
        if reg == input:
          return cap
      else: 
        if cap == input:
          return reg
          
    return 'errore'




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)