# importing libraries
import pandas as pd
import numpy as np
import pymongo
import json
import os, sys
from dataclasses import dataclass


# creating ENvironmentVariable class
@dataclass
class EnvironmentVariable:
    """
    Description:
        getting environment variable
    """

    # fetching the data
    mongo_db_url: str = os.getenv("MONGO_DB_URL")


# calling the class object
env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "expenses"
print("env_var.mongo_db_url")
