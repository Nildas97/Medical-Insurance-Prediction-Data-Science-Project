# importing libraries
from flask import Flask
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route("/")  # sample -> localhost:5000/
def home():
    return "this is our first docker file"


if __name__ == "__main__":
    app.run()
