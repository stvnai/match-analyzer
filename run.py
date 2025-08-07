from app import create_flask_app, create_dash_match_analyzer, create_dash_torque_analyzer, create_dash_main
import os


app= create_flask_app()
match_app= create_dash_match_analyzer(app)
torque_app= create_dash_torque_analyzer(app)
dash_main= create_dash_main(app)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8020, debug=True)
