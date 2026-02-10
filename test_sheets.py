from services.google_sheets import GoogleSheetsService

gs = GoogleSheetsService()

print("Pilot Roster:")
print(gs.read_sheet("pilot_roster"))

print("\nDrone Fleet:")
print(gs.read_sheet("drone_fleet"))

print("\nMissions:")
print(gs.read_sheet("missions"))

