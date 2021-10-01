from chalicelib.helper_functions import download_pdf
from chalicelib.helper_functions import build_pdf
from chalicelib.helper_functions import temp_test_function
# from chalicelib.helper_functions import search
from chalice import Chalice, Response

# import time
import json

# import os
# import requests
# import urllib.request

# from chalicelib.helper_functions import download_pdf

app = Chalice(app_name="python_lambda_levi")
app.debug = True

lst = [
    {
        "longitude": "52.93",
        "latitude": "5.21",
        "modaliteit": "fiets",
        "id": "ID987",
        "naam_user": "Levi",
    },
    {
        "longitude": "50.13",
        "latitude": "5.93",
        "modaliteit": "auto",
        "id": "ID297",
        "naam_user": "Levi",
    },
    {
        "longitude": "51.93",
        "latitude": "5.91",
        "modaliteit": "voetganger",
        "id": "ID957",
        "naam_user": "Martijn",
    },
]

fake_db = [
    {
        "id": "610",
        "type": "werk in uitvoering",
        "created_by": "sWIS",
        "origin_alert": "sWIS",
        "aantekening_incident": "Dit is een voorbeeld aantekening, ook deze heb ik langer gemaakt zodat ik kan zien of er niets van de pagian wordt afgedrukt als deze langer dan een regel zijn.",
        "swis_nodig": "0",
        "swis_tijd_aansturing": "2021-09-29 07:30:00",
        "swis_aangestuurd": "Gilbert Troenaredje",
        "swis_rit_type": "Pechgeval",
        "swis_restduur": "60",
        "swis_vertraag": "Pech met vervoermiddel",
        "gemeld_politie": "0",
        "gemeld_stadwerken": "0",
        "geen_impact": "0",
        "filevorming": "0",
        "rijstrook_dicht": "0",
        "wegdicht": "0",
        "onveilig": "0",
        "inschatting_vertraging_lengte": "100",
        "inschatting_vertraging_tijd": "60",
        "berging_nodig": "0",
        "berging_door": "",
        "berging_weg_categorie": "Rest",
        "berging_id": "LCM.123",
        "berging_tijd_melding": "2021-09-29 07:00:00",
        "scenario_management": "0",
        "type_scenario_management": "Uitstroom verhogen",
        "scenario_management_afgestemd": "0",
        "scenario_id": "Id123",
        "scenario_ingeschakeld": "2021-09-28 18:30:00",
        "scenario_uitgeschakeld": "2021-09-28 20:00:00",
        "afgerond": "2021-09-28 18:30:00",
        "bespreken": "0",
        "bespreken_opmerking": "Ook dit is een voorbeeld opmerking. Maar dit keer iets langer om te kijken wat er gebeurt met de PDF.",
        "afbeeldingen": [
            "./resources/pexels-pixabay-48125.jpeg",
            "./resources/pexels-alexandr-podvalny-1031698.jpg",
            "./resources/pexels-mikechie-esparagoza-1600757.jpg",
        ],
    },
    {
        "id": "611",
        "type": "Overig",
        "created_by": "sWIS",
        "origin_alert": "sWIS",
        "aantekening_incident": "",
        "aantekening_incident": "Dit is een voorbeeld aantekening",
        "swis_nodig": "1",
        "gemeld_politie": "0",
        "gemeld_stadwerken": "1",
        "geen_impact": "1",
        "filevorming": "0",
        "rijstrook_dicht": "0",
        "wegdicht": "0",
        "onveilig": "0",
        "inschatting_vertraging_lengte": "500",
        "inschatting_vertraging_tijd": "0",
        "berging": "0",
        "scenario_management": "0",
        "type_scenario_management": "Instroom beperken",
        "scenario_management_afgestemd": "1",
        "scenario_id": "T666",
        "afgerond": "",
        "bespreken": "0",
        "bespreken_opmerking": "",
    },
]


@app.route("/")
def index():
    output = json.dumps(lst)
    return output


@app.route("/count-points/upload", methods=["POST"])
def add_countpoint():
    data = app.current_request.json_body
    newList = data

    try:
        for row in newList:
            newRow = {}
            if (
                row["longitude"] != ""
                and row["latitude"] != ""
                and row["modaliteit"] != ""
            ):
                newRow = {
                    "longitude": row["longitude"],
                    "latitude": row["latitude"],
                    "modaliteit": row["modaliteit"],
                    "id": row["id"],
                    "naam_user": row["naam_user"],
                }
                if newRow["id"] == "":
                    newRow["id"] = "n.v.t."
                if newRow["naam_user"] == "":
                    newRow["naam_user"] = "n.v.t."
            lst.append(newRow)
        return lst
    except Exception as e:
        return {"message": "correct data is missing: " + str(e) + " can't be empty"}


@app.route("/export_pdf/download/{id}", cors=True)
def create_pdf(id):

    # Hier met requests data ophalen op basis van endpoint die in JavaScript wordt opgehaald
    # temp_test_function(id)

    build_pdf(id)

    file_out_path = download_pdf(id)

    return str(file_out_path)
