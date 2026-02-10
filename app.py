from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------------------
# GOOGLE SHEETS SERVICE
# ---------------------------
class GoogleSheetsService:
    def __init__(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scope
        )
        self.client = gspread.authorize(creds)

    def read_sheet(self, sheet_name):
        sheet = self.client.open(sheet_name).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        df = df.replace("â€“", None)
        df = df.replace("", None)
        return df

    def update_cell_by_id(self, sheet_name, id_column, row_id, update_column, value):
        sheet = self.client.open(sheet_name).sheet1
        records = sheet.get_all_records()

        for idx, record in enumerate(records, start=2):
            if record[id_column] == row_id:
                col_index = sheet.find(update_column).col
                sheet.update_cell(idx, col_index, value)
                return True
        return False


# ---------------------------
# PILOT AGENT
# ---------------------------
class RosterAgent:
    def find_available_pilots(self, pilots, skill, certs, location):
        df = pilots[
            (pilots["status"] == "Available") &
            (pilots["location"] == location) &
            (pilots["skills"].str.contains(skill, case=False, na=False))
        ]

        for cert in certs.split(","):
            df = df[df["certifications"].str.contains(cert.strip(), case=False, na=False)]

        return df


# ---------------------------
# DRONE AGENT
# ---------------------------
class DroneAgent:
    def find_available_drones(self, drones, skill, location):
        capability_map = {
            "Mapping": ["LiDAR", "RGB"],
            "Inspection": ["RGB"],
            "Thermal": ["Thermal"]
        }

        required_caps = capability_map.get(skill, [])

        df = drones[
            (drones["status"] == "Available") &
            (drones["location"] == location)
        ]

        df = df[df["capabilities"].apply(
            lambda c: any(cap in c for cap in required_caps)
        )]

        return df


# ---------------------------
# ASSIGNMENT AGENT
# ---------------------------
class AssignmentAgent:
    def assign(self, mission, pilots, drones):
        if pilots.empty:
            return {"status": "FAILED", "reason": "No available pilot"}
        if drones.empty:
            return {"status": "FAILED", "reason": "No available drone"}

        pilot = pilots.iloc[0]
        drone = drones.iloc[0]

        return {
            "status": "SUCCESS",
            "project_id": mission["project_id"],
            "pilot_id": pilot["pilot_id"],
            "pilot_name": pilot["name"],
            "drone_id": drone["drone_id"],
            "drone_model": drone["model"]
        }


# ---------------------------
# CONFLICT AGENT
# ---------------------------
class ConflictAgent:
    def detect(self, mission, pilot, drone):
        conflicts = []

        if pilot["location"] != mission["location"]:
            conflicts.append("Pilot location mismatch")

        if drone["location"] != mission["location"]:
            conflicts.append("Drone location mismatch")

        for cert in mission["required_certs"].split(","):
            if cert.strip() not in pilot["certifications"]:
                conflicts.append(f"Missing certification: {cert.strip()}")

        if drone["status"] == "Maintenance":
            conflicts.append("Drone under maintenance")

        return conflicts


# ---------------------------
# URGENT REASSIGNMENT AGENT
# ---------------------------
class UrgentAgent:
    def handle(self, mission, pilots, drones):
        if mission["priority"] != "Urgent":
            return {"status": "IGNORED"}

        p = pilots[pilots["status"] == "Assigned"]
        d = drones[drones["status"] == "Assigned"]

        if p.empty or d.empty:
            return {"status": "FAILED", "reason": "No resources to reassign"}

        return {
            "status": "REASSIGN",
            "pilot_id": p.iloc[0]["pilot_id"],
            "drone_id": d.iloc[0]["drone_id"]
        }


# ---------------------------
# FASTAPI APP
# ---------------------------
app = FastAPI()
gs = GoogleSheetsService()

roster = RosterAgent()
drone_agent = DroneAgent()
assigner = AssignmentAgent()
conflict_agent = ConflictAgent()
urgent_agent = UrgentAgent()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.lower()

    pilots = gs.read_sheet("pilot_roster")
    drones = gs.read_sheet("drone_fleet")
    missions = gs.read_sheet("missions")

    if "assign" in msg:
        for _, mission in missions.iterrows():
            if mission["project_id"].lower() in msg:
                ap = roster.find_available_pilots(
                    pilots,
                    mission["required_skills"],
                    mission["required_certs"],
                    mission["location"]
                )

                ad = drone_agent.find_available_drones(
                    drones,
                    mission["required_skills"],
                    mission["location"]
                )

                assignment = assigner.assign(mission, ap, ad)

                if assignment["status"] != "SUCCESS":
                    return {"response": assignment}

                conflicts = conflict_agent.detect(
                    mission, ap.iloc[0], ad.iloc[0]
                )

                if conflicts:
                    return {"response": conflicts}

                gs.update_cell_by_id("pilot_roster", "pilot_id",
                                     assignment["pilot_id"], "status", "Assigned")

                gs.update_cell_by_id("drone_fleet", "drone_id",
                                     assignment["drone_id"], "status", "Assigned")

                return {
                    "response": f"Assigned {assignment['pilot_name']} with drone {assignment['drone_model']} to {assignment['project_id']}"
                }

    if "urgent" in msg:
        urgent_mission = missions[missions["priority"] == "Urgent"].iloc[0]
        return {"response": urgent_agent.handle(urgent_mission, pilots, drones)}

    return {"response": "I did not understand your request"}
