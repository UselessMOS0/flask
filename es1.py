from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def es1():
    return  render_template('es1.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)