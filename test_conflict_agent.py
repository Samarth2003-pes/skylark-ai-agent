from services.google_sheets import GoogleSheetsService
from agents.roster_agent import RosterAgent
from agents.drone_agent import DroneAgent
from agents.assignment_agent import AssignmentAgent
from agents.conflict_agent import ConflictAgent

gs = GoogleSheetsService()
roster = RosterAgent()
drone_agent = DroneAgent()
assigner = AssignmentAgent()
conflict_agent = ConflictAgent()

pilots = gs.read_sheet("pilot_roster")
drones = gs.read_sheet("drone_fleet")
missions = gs.read_sheet("missions")

mission = missions[missions["project_id"] == "PRJ001"].iloc[0]

available_pilots = roster.find_available_pilots(
    pilots,
    mission["required_skills"],
    mission["required_certs"],
    mission["location"],
    mission["start_date"]
)

available_drones = drone_agent.find_available_drones(
    drones,
    mission["required_skills"],
    mission["location"],
    mission["end_date"]
)

pilot = available_pilots.iloc[0]
drone = available_drones.iloc[0]

conflicts = conflict_agent.detect_conflicts(
    mission, pilot, drone
)

print(conflicts)
