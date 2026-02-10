class AssignmentAgent:
    def assign_resources(self, mission, pilots_df, drones_df):
        if pilots_df.empty:
            return {
                "status": "FAILED",
                "reason": "No available pilot"
            }

        if drones_df.empty:
            return {
                "status": "FAILED",
                "reason": "No available drone"
            }

        # Simple strategy: pick first available pilot and drone
        pilot = pilots_df.iloc[0]
        drone = drones_df.iloc[0]

        return {
            "status": "SUCCESS",
            "project_id": mission["project_id"],
            "pilot_id": pilot["pilot_id"],
            "pilot_name": pilot["name"],
            "drone_id": drone["drone_id"],
            "drone_model": drone["model"]
        }
