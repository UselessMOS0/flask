from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

userLst = []

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return  render_template('es2/form.html')
    else: 
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        sex = request.form.get('Sex')
        if username != '' and pwd != '' and sex != None and pwd != request.form.get('cpwd'):
            userLst.append({'username':username, 'pwd':pwd, 'sex':sex})
            return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    


    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)