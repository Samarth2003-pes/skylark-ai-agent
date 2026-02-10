from services.google_sheets import GoogleSheetsService
from agents.drone_agent import DroneAgent

gs = GoogleSheetsService()
drone_agent = DroneAgent()

drones = gs.read_sheet("drone_fleet")
missions = gs.read_sheet("missions")

mission = missions[missions["project_id"] == "PRJ001"].iloc[0]

result = drone_agent.find_available_drones(
    drones,
    mission["required_skills"],
    mission["location"],
    mission["end_date"]
)

print(result)
