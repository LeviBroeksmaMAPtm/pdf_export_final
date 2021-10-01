from pathlib import Path
from fpdf import FPDF
import requests
import json


def search(newData, list):
    for row in list:
        if row["longitude"] == newData["longitude"]:
            return row


def create_new_row(data, row):
    if data["longitude"] != "" and data["latitude"] != "" and data["modaliteit"] != "":
        row = {
            "longitude": data["longitude"],
            "latitude": data["latitude"],
            "modaliteit": data["modaliteit"],
            "id": data["id"],
            "naam_user": data["naam_user"],
        }
        # check for empty fields and replace if necessary
        if row["id"] == "":
            row["id"] = "n.v.t."
        if row["naam_user"] == "":
            row["naam_user"] = "n.v.t."


def get_by_id(id):
    base_url = "https://2bnaovl3ad.execute-api.eu-central-1.amazonaws.com"
    api_point = f"/api/get_sim_amsterdam_by_id/{id}"
    r = requests.get(base_url + api_point)
    j = json.loads(r.text)
    data = j["im_amsterdam"][0]
    # print(j["im_amsterdam"][0]["tijd"])
    return data["tijd"]["vri_meldtijd_storing"]


def temp_test_function(id):
    print(get_by_id(id))


def build_pdf(id):
    base_url = "https://2bnaovl3ad.execute-api.eu-central-1.amazonaws.com"
    api_point = f"/api/get_sim_amsterdam_by_id/{id}"
    r = requests.get(base_url + api_point)
    j = json.loads(r.text)
    data = j["im_amsterdam"]

    for row in data:
        id_alert = row["ID"]
        time_alert = row["tijd"]["tijd_melding"]
        origin_alert = row["herkomst_melding"]
        type_of_incident = row["im"]["type"]
        creator = row["operator"]
        notes = row["im"]["im_opmerking_incident"]
        swis_needed = row["swis"]["swis_benodigd"]
        swis_time = row["tijd"]["swis_tijd_aansturing"]
        swis_directed = row["swis"]["swis_aangestuurd"]
        swis_ride_type = row["swis"]["swis_rit_type"]
        swis_remaining_time = row["swis"]["swis_restduur"]
        swis_delay = row["swis"]["swis_vertraag"]
        police_notified = row["politie"]["gemeld"]
        police_notification_time = row["tijd"]["politie_meldtijd"]
        police_needed = row["politie"]["inzet_benodigd"]
        police_remark = row["politie"]["inzet_beschrijving"]
        city_notified = row["stadwerken"]["gemeld"]
        city_notification_time = row["tijd"]["stadwerken_meldtijd"]
        city_needed = row["stadwerken"]["inzet_benodigd"]
        city_remark = row["stadwerken"]["inzet_beschrijving"]
        no_impact = row["impact"]["geen_impact"]
        traffic_jams = row["impact"]["filevorming"]
        lane_closed = row["impact"]["rijstrook_dicht"]
        road_closed = row["impact"]["wegdicht"]
        unsafe = row["impact"]["onveilig"]
        delay_time = row["impact"]["inschatting_vertraging_tijd"]
        delay_distance = row["impact"]["inschatting_vertraging_lengte"]
        salvage_needed = row["berging"]["nodig"]
        salvage_category = row["berging"]["weg_categorie"]
        salvage_by = row["berging"]["door"]
        salvage_id = row["berging"]["LCM_id"]
        salvage_time_request = row["tijd"]["berging_meldtijd_bij_LCM"]
        scenario_management = row["scenario"]["nodig"]
        type_scenario_management = row["scenario"]["type"]
        scenario_management_in_tune = row["scenario"]["inzet_afgestemd"]
        scenario_id = row["scenario"]["id"]
        scenario_initiated = row["tijd"]["scenario_tijd_in"]
        scenario_terminated = row["tijd"]["scenario_tijd_uit"]
        completed = row["compleetheid"]["rating"]
        discuss = row["bespreken"]["bespreken"]
        discuss_remark = row["bespreken"]["bespreken_opmerking"]

        # REGELS HIERONDER ZIJN PAS NODIG WANNEER ER DAADWERKELIJK AFBEELDINGEN WORDEN OPGESLAGEN
        # images = row["afbeeldingen"]
        # width = 210

        # PAGINA AANMAKEN
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()

        # TITEL INSTELLEN
        pdf.set_font("Arial", "B", 16)
        pdf.cell(
            ln=1,
            h=10,
            align="L",
            w=0,
            txt=f"Rapportage incident: {id_alert}, datum: {time_alert}",
        )

        # ALGEMENE GEGEVENS
        pdf.set_font("Arial", "", 12)
        pdf.cell(ln=1, h=5, w=20, txt=f"Aangemaakt door: {creator}")
        pdf.cell(ln=1, h=5, w=20, txt=f"Tijdstip melding: {time_alert}")
        pdf.cell(ln=1, h=5, w=20, txt=f"Type incident: {type_of_incident}")
        pdf.cell(ln=1, h=5, w=20, txt=f"Herkomst melding: {origin_alert}")

        if notes != "":
            pdf.multi_cell(h=5, w=0, txt=f"Opmerking: {notes}")
        else:
            pdf.multi_cell(h=5, w=0, txt="Opmerking: Geen opmerking meegegeven.")

        # SWIS

        if swis_needed != "0":
            pdf.cell(ln=1, h=5, w=20, txt="sWIS aansturing:")
            pdf.cell(ln=1, h=5, w=20, txt="")
            pdf.cell(ln=1, h=5, w=20, txt="sWIS nodig: Ja")
            pdf.cell(ln=1, h=5, w=20, txt=f"Tijd van aansturing: {swis_time}")
            pdf.cell(ln=1, h=5, w=20, txt=f"Aangestuurde sWIS: {swis_directed}")
            pdf.cell(ln=1, h=5, w=20, txt=f"Type rit: {swis_ride_type}")
            pdf.cell(
                ln=1,
                h=5,
                w=20,
                txt=f"Geschatte restduur: {swis_remaining_time} minuten",
            )
            pdf.cell(ln=1, h=5, w=20, txt=f"Reden vertraging: {swis_delay}")
            if swis_needed == "0":
                pdf.cell(ln=1, h=5, w=20, txt="sWIS nodig: Nee")
            pdf.cell(
                ln=1,
                h=5,
                w=20,
                txt="-------------------------------------------------------------------------------------------------------------------------------------",
            )

        # POLITIE

        if police_notified == "0":
            pdf.cell(ln=1, h=5, w=20, txt="Politie geïnformeerd: Nee")
        else:
            pdf.cell(ln=1, h=5, w=20, txt="Politie geïnformeerd: Ja")
        if police_notified != "":
            pdf.cell(ln=1, h=5, w=20, txt=f"Tijd melding: {police_notification_time}")
        if police_notified != "0" and police_needed == "0":
            pdf.cell(ln=1, h=5, w=20, txt=f"Inzet politie benodigd: Nee")
        else:
            pdf.cell(ln=1, h=5, w=20, txt=f"Inzet politie benodigd: Ja")
        if police_notified != "0" and police_needed != "0":
            pdf.multi_cell(h=5, w=20, txt=f"Opmerking inzet politie: {police_remark}")

        # STADWERKEN

        if city_notified == "0":
            pdf.cell(ln=1, h=5, w=20, txt="Stadwerken geïnformeerd: Nee")
        else:
            pdf.cell(ln=1, h=5, w=20, txt="Stadwerken geïnformeerd: Ja")
        if city_notified != "0":
            pdf.cell(ln=1, h=5, w=20, txt=f"Tijd melding: {city_notification_time}")
        if city_notified != "0" and city_needed == "0":
            pdf.cell(ln=1, h=5, w=20, txt=f"Inzet politie benodigd: Nee")
        else:
            pdf.cell(ln=1, h=5, w=20, txt=f"Inzet politie benodigd: Ja")
        if city_notified != "0" and city_needed != "0":
            pdf.multi_cell(h=5, w=20, txt=f"Opmerking inzet politie: {city_remark}")
        pdf.cell(
            ln=1,
            h=5,
            w=20,
            txt="-------------------------------------------------------------------------------------------------------------------------------------",
        )

        # VERKEERSBEELD

        pdf.cell(ln=1, h=5, w=20, txt="Omschrijving verkeersbeeld:")
        pdf.cell(ln=1, h=5, w=20, txt="")
        if no_impact == "0":
            pdf.cell(ln=1, h=5, w=20, txt="[ ] Geen impact")
        else:
            pdf.cell(ln=1, h=5, w=20, txt="[x] Geen impact")
        if traffic_jams == "0":
            pdf.cell(ln=1, h=5, w=20, txt="[ ] Filevorming")
        else:
            pdf.cell(ln=1, h=5, w=20, txt="[x] Filevorming")

        if lane_closed == "0":
            pdf.cell(ln=1, h=5, w=20, txt="[ ] Rijstrook dicht")
        else:
            pdf.cell(ln=1, h=5, w=20, txt="[x] Rijstrook dicht")
        if road_closed == "0":
            pdf.cell(ln=1, h=5, w=20, txt="[ ] Weg dicht")
        else:
            pdf.cell(ln=1, h=5, w=20, txt="[x] Weg dicht")
        if unsafe == "0":
            pdf.cell(ln=1, h=5, w=20, txt="[ ] Verkeersonveilige situatie")
        else:
            pdf.cell(ln=1, h=5, w=20, txt="[x] Verkeersonveilige situatie")
        pdf.cell(
            ln=1,
            h=5,
            w=20,
            txt="-------------------------------------------------------------------------------------------------------------------------------------",
        )

        # VERTRAGING / LENGTE WACHTRIJ

        pdf.cell(ln=1, h=5, w=20, txt="Inschatting vertraging / wachtrijlengte:")
        pdf.cell(ln=1, h=5, w=20, txt="")
        if delay_time != "0":
            pdf.cell(
                ln=1,
                h=5,
                w=20,
                txt=f"De verwachte vertraging is: {delay_time} minuten",
            )
        else:
            pdf.cell(ln=1, h=5, w=20, txt="Geen vertraging")
        if delay_distance != "0":
            pdf.cell(
                ln=1,
                h=5,
                w=20,
                txt=f"De lengte van de wachtrij bedraagt: {delay_distance} meter",
            )
        else:
            pdf.cell(ln=1, h=5, w=20, txt="Geen wachtrij")
        pdf.cell(
            ln=1,
            h=5,
            w=20,
            txt="-------------------------------------------------------------------------------------------------------------------------------------",
        )

        # BERGING DETAILS

        pdf.cell(ln=1, h=5, w=20, txt="Berging details:")
        pdf.cell(ln=1, h=5, w=20, txt="")
        if salvage_needed != "0":
            if salvage_id != "":
                pdf.cell(ln=1, h=5, w=20, txt=f"Berging ID: {salvage_id}")
            else:
                pdf.cell(ln=1, h=5, w=20, txt=f"Berging ID: Gegevens ontbreken")
            if salvage_needed != "":
                pdf.cell(ln=1, h=5, w=20, txt="Berging noodzakelijk: Ja")
            else:
                pdf.cell(ln=1, h=5, w=20, txt=f"Berging nodig: Gegevens ontbreken")
            if salvage_category != "":
                pdf.cell(ln=1, h=5, w=20, txt=f"Berging categorie: {salvage_category}")
            else:
                pdf.cell(ln=1, h=5, w=20, txt=f"Berging categorie: Gegevens ontbreken")
            if salvage_by != "":
                pdf.cell(ln=1, h=5, w=20, txt=f"Berging door: {salvage_by}")
            else:
                pdf.cell(ln=1, h=5, w=20, txt=f"Berging door: Gegevens ontbreken")
            if salvage_time_request != "":
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt=f"Berging gemeld bij LCM om: {salvage_time_request}",
                )
            else:
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt=f"Berging gemeld bij LCM om: Gegevens ontbreken",
                )
        else:
            pdf.cell(ln=1, h=5, w=20, txt="Berging noodzakelijk: Nee")
        pdf.cell(
            ln=1,
            h=5,
            w=20,
            txt="-------------------------------------------------------------------------------------------------------------------------------------",
        )

        # SCENARIO MANAGEMENT

        if scenario_management != "0":
            pdf.cell(ln=1, h=5, w=20, txt="Scenario management:")
            pdf.cell(ln=1, h=5, w=20, txt="")
            pdf.cell(ln=1, h=5, w=20, txt="Inzet scenario noodzakelijk: Ja")
            if scenario_id != "":
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt=f"Scenarionaam / Schakelingnummer: {scenario_id}",
                )
            else:
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt="Scenarionaam / Schakelingnummer: Gegevens ontbreken",
                )
            if type_scenario_management != "":
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt=f"Type scenario: {type_scenario_management}",
                )
            else:
                pdf.cell(ln=1, h=5, w=20, txt="Type scenario: Gegevens ontbreken")
            if scenario_management_in_tune != "" and scenario_management_in_tune == "0":
                pdf.cell(ln=1, h=5, w=20, txt=f"Inzet afgestemd: Nee")
            elif (
                scenario_management_in_tune != "" and scenario_management_in_tune == "1"
            ):
                pdf.cell(ln=1, h=5, w=20, txt=f"Inzet afgestemd: Ja")
            else:
                pdf.cell(ln=1, h=5, w=20, txt="Inzet afgestemd: Gegevens ontbreken")
            if type_scenario_management != "":
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt=f"Type scenario: {type_scenario_management}",
                )
            else:
                pdf.cell(ln=1, h=5, w=20, txt="Type scenario: Gegevens ontbreken")
            if scenario_initiated != "":
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt=f"Scenario ingeschakeld om: {scenario_initiated}",
                )
            else:
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt="Scenario ingeschakeld om: Gegevens ontbreken",
                )
            if scenario_terminated != "":
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt=f"Scenario uitgeschakeld om: {scenario_terminated}",
                )
            else:
                pdf.cell(
                    ln=1,
                    h=5,
                    w=20,
                    txt="Scenario uitgeschakeld om: Gegevens ontbreken",
                )
            pdf.cell(
                ln=1,
                h=5,
                w=20,
                txt="-------------------------------------------------------------------------------------------------------------------------------------",
            )

        if completed != "":
            pdf.cell(ln=1, h=5, w=20, txt=f"Tijd afgerond: {completed}")
        else:
            pdf.cell(ln=1, h=5, w=20, txt="Dit incident is nog niet volledig afgerond.")
        if discuss == "1":
            pdf.cell(ln=1, h=5, w=20, txt=f"Graag bespreken in volgend overleg: Ja")
            pdf.multi_cell(h=5, w=0, txt=f"Opmerkingen: {discuss_remark}")
        else:
            pdf.cell(ln=1, h=5, w=20, txt=f"Graag bespreken in volgend overleg: Nee")

        # IMAGES

        # if images != "":
        #     for image in images:
        #         pdf.add_page()
        #         pdf.image(image, 12, 12, width - 24)

    # return pdf.output(f'./resources/{timestamp}.pdf', 'F')
    file_name = f"tmp/{id}.pdf"
    # contents = pdf.output(dest="F", name=file_name)
    pdf.output(dest="F", name=file_name)


def download_pdf(id):
    file_out = f"Export {id}.pdf"

    return Path(f"/tmp/{file_out}")
