from src import app
from db_setup import soft_db_setup

if __name__ == "__main__":
    # set up missing tables if there are any
    soft_db_setup()
    app.run(host="0.0.0.0", debug=True)
