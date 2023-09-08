# importing libraries
import pymongo
import pandas as pd
import json

# mongodb client
client = pymongo.MongoClient(
    "mongodb+srv://NilutpalDAS992:s729TiAxVqw01pG@cluster0.xxk1zfm.mongodb.net/?retryWrites=true&w=majority"
)

# daatset file path
DATA_FILE_PATH = r"D:\Data Science\Python_Projects\medical_insurance\Medical-Insurance-Prediction-Data-Science-Project\insurance.csv"

# dataset name
DATABASE_NAME = "INSURANCE"

# dataset folder name
COLLECTION_NAME = "INSURANCE_PROJECT"


if __name__ == "__main__":
    # reading the dataset
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns : {df.shape}")

    # resetting the index
    df.reset_index(drop=True, inplace=True)

    # transposing and converting it into json format
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    # uploading the transposed dataset into mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
