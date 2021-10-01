import requests
import json

# https://2bnaovl3ad.execute-api.eu-central-1.amazonaws.com/api/get_sim_amsterdam_by_id/666
param = '666'
base_url = "https://2bnaovl3ad.execute-api.eu-central-1.amazonaws.com/api/get_sim_amsterdam_by_id/"
# test_url = "{id}"


# j = json.loads(r.text)

# print(j['im_amsterdam'][0]['tijd']['politie_meldtijd'])

def get_by_id(id):

    base_url = "https://2bnaovl3ad.execute-api.eu-central-1.amazonaws.com"
    api_point = f"/api/get_sim_amsterdam_by_id/{id}"
    r = requests.get(base_url + api_point)
    j = json.loads(r.text)
    return j['im_amsterdam'][0]['ID']


print(str(get_by_id(666)))
