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
        cpwd = request.form.get('cpwd')
        if username != '' and pwd != '' and sex != '' and pwd == cpwd:
            userLst.append({'username':username, 'pwd':pwd, 'sex':sex})
            return redirect(url_for('login'))
        else:
            return f'errore {username,pwd,cpwd,sex}'


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('es2/welcome.html')
    else:
        username = request.form.get('username')
        pwd = request.form.get('pwd')

        for user in userLst:
            if username == user['username']:
                if pwd == user['pwd']:
                    return 'loggato'
                else:
                    return 'password errata'
        
        return 'utente non trovato' 



    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)