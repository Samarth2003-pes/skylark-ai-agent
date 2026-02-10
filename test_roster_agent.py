from services.google_sheets import GoogleSheetsService
from agents.roster_agent import RosterAgent

gs = GoogleSheetsService()
roster = RosterAgent()

pilots = gs.read_sheet("pilot_roster")
missions = gs.read_sheet("missions")

mission = missions[missions["project_id"] == "PRJ001"].iloc[0]

result = roster.find_available_pilots(
    pilots,
    mission["required_skills"],
    mission["required_certs"],
    mission["location"],
    mission["start_date"]
)

print(result)

