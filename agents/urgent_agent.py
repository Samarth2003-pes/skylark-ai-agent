class UrgentReassignmentAgent:
    def handle_urgent_mission(
        self,
        mission,
        pilots_df,
        drones_df
    ):
        if mission["priority"] != "Urgent":
            return None

        # Find assigned but movable pilots
        candidate_pilots = pilots_df[pilots_df["status"] == "Assigned"]

        # Find assigned but movable drones
        candidate_drones = drones_df[drones_df["status"] == "Assigned"]

        if candidate_pilots.empty or candidate_drones.empty:
            return {
                "status": "FAILED",
                "reason": "No resources to reassign"
            }

        # Pick first reassignment candidates
        pilot = candidate_pilots.iloc[0]
        drone = candidate_drones.iloc[0]

        return {
            "status": "REASSIGN",
            "pilot_id": pilot["pilot_id"],
            "drone_id": drone["drone_id"],
            "note": "Reassigned from lower priority mission"
        }
