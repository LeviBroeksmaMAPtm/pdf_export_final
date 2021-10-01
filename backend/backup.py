from chalicelib.my_functions import search
from chalice import Chalice
import json

app = Chalice(app_name="python_lambda_levi")
app.debug = True

lst = [
    {
        "longitude": "52.93",
        "latidude": "5.21",
        "modaliteit": "fiets",
        "id": "ID987",
        "naam_user": "Levi",
    },
    {
        "longitude": "50.13",
        "latidude": "5.93",
        "modaliteit": "auto",
        "id": "ID297",
        "naam_user": "Levi",
    },
    {
        "longitude": "51.93",
        "latidude": "5.91",
        "modaliteit": "voetganger",
        "id": "ID957",
        "naam_user": "Martijn",
    },
]

@app.route("/")
def index():
    output = json.dumps(lst)
    print(output)
    return output


@app.route("/count-points/upload", methods=['POST'])
def add_countpoint():
    newRow = {}
    data = app.current_request.json_body

    try:
        if(data["longitude"] != "" and data["latitude"] != "" and data["modaliteit"] != ""):
            newRow = {
                "longitude": data["longitude"],
                "latitude": data["latitude"],
                "modaliteit": data["modaliteit"],
                "id": data["id"],
                "naam_user": data["naam_user"]
            }
            # check for empty fields and replace if necessary
            if(newRow["id"] == ""):
                newRow["id"] = "n.v.t."
            if(newRow["naam_user"] == ""):
                newRow["naam_user"] = "n.v.t."

        to_be_replace = str(search(newRow, lst))

        lst.append(newRow)
        return to_be_replace

    except Exception as e:
        return{"message": "correct data is missing: " + str(e) + " can't be empty"}

# WAT MOET IK NOG DOEN

# [] Zorgen dat ik meer dan een dictionary tegelijk kan uploaden (dus een list van dictionaries)
# [] Check of newRow identiek is aan een dict in lst
    # [] Check moet worden gedaan advh longitude, latitude en modaliteit, als alle drie overeenkomen mag deze worden vervangen, anders: nieuwe aanmaken
# [] Als newRow identiek is aan een dict in lst, vervang
# [] Is newRow niet identiek aan een van de dicts in lst, append
# [] Ik moet ervoor zorgen dat niet allen per dict kan worden ge-upload, maar ook een list van dicts
