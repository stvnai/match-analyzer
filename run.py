from app import create_flask_app, create_dash_app
import os


flask_app= create_flask_app()
dash_app= create_dash_app(flask_app)

if __name__ == "__main__":

    flask_app.run(host="0.0.0.0",debug=True)
