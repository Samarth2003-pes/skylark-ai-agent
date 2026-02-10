import pandas as pd


class RosterAgent:
    def find_available_pilots(
        self,
        pilots_df: pd.DataFrame,
        required_skill: str,
        required_certs: str,
        location: str,
        start_date: str
    ) -> pd.DataFrame:

        # Only available pilots in same location
        filtered = pilots_df[
            (pilots_df["status"] == "Available") &
            (pilots_df["location"] == location)
        ]

        # Skill match
        filtered = filtered[
            filtered["skills"].str.contains(required_skill, case=False, na=False)
        ]

        # Certification match (at least one required cert)
        for cert in required_certs.split(","):
            filtered = filtered[
                filtered["certifications"].str.contains(cert.strip(), case=False, na=False)
            ]

        return filtered

