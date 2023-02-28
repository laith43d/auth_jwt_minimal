from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity


class User( object ):
    def __init__( self, id, username, password ):
        self.id = id
        self.username = username
        self.password = password

    def __str__( self ):
        return f"User(id='{self.id}')"


user = User( 1, 'user', 'pass' )


def authenticate( username, password ):
    if username == user.username and password == user.password:
        return user


def identity():
    return user


app = Flask( __name__ )
app.debug = True
app.config[ 'SECRET_KEY' ] = 'super-secret'

jwt = JWT( app, authenticate, identity )


# send cors headers
@app.after_request
def after_request( response ):
    response.headers.add( 'Access-Control-Allow-Origin', '*' )
    if request.method == 'OPTIONS':
        response.headers[ 'Access-Control-Allow-Methods' ] = 'DELETE, GET, POST, PUT'
        if headers := request.headers.get('Access-Control-Request-Headers'):
            response.headers[ 'Access-Control-Allow-Headers' ] = headers
    return response


@app.route( '/unprotected' )
def unprotected():
    return jsonify( {
        'message': 'This is an unprotected resource.'
    } )


@app.route( '/protected' )
@jwt_required()
def protected():
    return jsonify( {
        'message'         : 'This is a protected resource.',
        'current_identity': str( current_identity )
    } )


app.run()
