from flask import Flask, render_template


app = Flask(__name__)

@app.route('/hello')
def hello_world():    
    return 'Hello World!'
    
    
if __name__ == '__main__':    
    app.run()


@app.route('/', methods=['GET', 'POST'])
def index():    
    name="HELLO"    
    return render_template('index.html',data=name)
