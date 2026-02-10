from services.google_sheets import GoogleSheetsService
from agents.urgent_agent import UrgentReassignmentAgent

gs = GoogleSheetsService()
urgent_agent = UrgentReassignmentAgent()

pilots = gs.read_sheet("pilot_roster")
drones = gs.read_sheet("drone_fleet")
missions = gs.read_sheet("missions")

urgent_mission = missions[missions["priority"] == "Urgent"].iloc[0]

result = urgent_agent.handle_urgent_mission(
    urgent_mission,
    pilots,
    drones
)

print(result)
