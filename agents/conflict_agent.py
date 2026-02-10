class ConflictAgent:
    def detect_conflicts(self, mission, pilot, drone):
        conflicts = []

        # Pilot availability
        if pilot["status"] != "Available":
            conflicts.append("Pilot is not available")

        # Certification mismatch
        required_certs = mission["required_certs"].split(",")
        for cert in required_certs:
            if cert.strip() not in pilot["certifications"]:
                conflicts.append(f"Pilot missing certification: {cert.strip()}")

        # Location mismatch
        if pilot["location"] != mission["location"]:
            conflicts.append("Pilot location mismatch")

        if drone["location"] != mission["location"]:
            conflicts.append("Drone location mismatch")

        # Maintenance check
        if drone["status"] == "Maintenance":
            conflicts.append("Drone under maintenance")

        return conflicts
