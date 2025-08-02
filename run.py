from app import create_flask_app, create_dash_app
import os


app= create_flask_app()
dash_app= create_dash_app(app)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8020)
