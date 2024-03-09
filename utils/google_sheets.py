import os

from dotenv import load_dotenv
import pandas as pd
import pygsheets


load_dotenv()

SERVICE_FILE = os.getenv("SERVICE_FILE")
TABLE_ID = os.getenv("TABLE_ID")

gc = pygsheets.authorize(service_file=SERVICE_FILE)

a, b = 2, 1


def add_user_to_sheets(data: dict):
    global a
    global b
    df = pd.DataFrame(data, index=[0])

    sh = gc.open_by_key(TABLE_ID)

    wks = sh[0]

    values = df.values.tolist()

    for i in range(len(values)):
        wks.update_values(crange=(a, b), values=[values[i]])
        a += 1
