from app import app 
@app.route('/') 
@app.route('/index') 
def index():
    return '''<html>
    <head>
    	<title>Home Page</title>
    	</head>
       <body>
           <h1> adfaf</h1>
           </html>'''
