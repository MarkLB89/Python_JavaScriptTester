from flask import Flask
from routes import routes  # Import the routes Blueprint

app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
