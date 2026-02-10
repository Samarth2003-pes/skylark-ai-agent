class SyncAgent:
    def sync_assignment(self, gs, assignment):
        if assignment["status"] != "SUCCESS":
            return False

        # Update pilot status
        gs.update_cell_by_id(
            "pilot_roster",
            "pilot_id",
            assignment["pilot_id"],
            "status",
            "Assigned"
        )

        # Update drone status
        gs.update_cell_by_id(
            "drone_fleet",
            "drone_id",
            assignment["drone_id"],
            "status",
            "Assigned"
        )

        return True
