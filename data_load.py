import os
import json
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

path = r"C:\Jinal project\PhonePe-pulse-main\pulse-master\data\aggregated\transaction\country\india\state"

data_list = []

for state in os.listdir(path):
    state_path = os.path.join(path, state)

    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)

            if os.path.isdir(year_path):
                for file in os.listdir(year_path):
                    file_path = os.path.join(year_path, file)

                    with open(file_path, "r") as f:
                        data = json.load(f)

                        if data.get("data") and data["data"].get("transactionData"):
                            for i in data["data"]["transactionData"]:
                                data_list.append({
                                    "state": state,
                                    "year": int(year),
                                    "quarter": file.replace(".json", ""),
                                    "type": i["name"],
                                    "count": i["paymentInstruments"][0]["count"],
                                    "amount": i["paymentInstruments"][0]["amount"]
                                })

df = pd.DataFrame(data_list)

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

for index, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO aggregated_transaction
        (state, year, quarter, transaction_type, count, amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            row["state"],
            row["year"],
            int(row["quarter"]),
            row["type"],
            row["count"],
            row["amount"]
        )
    )

conn.commit()

print("Data inserted successfully")