from services.google_sheets import GoogleSheetsService
from agents.sync_agent import SyncAgent

gs = GoogleSheetsService()
sync_agent = SyncAgent()

assignment = {
    "status": "SUCCESS",
    "pilot_id": "P001",
    "drone_id": "D001"
}

sync_agent.sync_assignment(gs, assignment)

print("Sync completed. Check Google Sheets.")
