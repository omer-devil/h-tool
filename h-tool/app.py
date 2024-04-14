from flask import Flask,request,render_template,redirect
from blueprint.app.app import app_bp
app = Flask(__name__)

app.register_blueprint(app_bp)

if __name__ == "__main__":
    app.run(debug=True)
