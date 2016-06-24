from bottle import route, run, template, get, request, post

@get('/volume/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return "<p>Your login information was correct.</p> "+username+" "+password

run(host='localhost', port=8081)
