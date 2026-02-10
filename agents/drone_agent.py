import pandas as pd


class DroneAgent:
    def find_available_drones(
        self,
        drones_df: pd.DataFrame,
        required_skill: str,
        location: str,
        end_date: str
    ) -> pd.DataFrame:

        # Mission → required drone capability mapping
        capability_map = {
            "Mapping": ["LiDAR", "RGB"],
            "Inspection": ["RGB"],
            "Thermal": ["Thermal"]
        }

        required_caps = capability_map.get(required_skill, [])

        # Filter by availability and location
        filtered = drones_df[
            (drones_df["status"] == "Available") &
            (drones_df["location"] == location)
        ]

        # Capability match (ANY required capability)
        filtered = filtered[
            filtered["capabilities"].apply(
                lambda caps: any(cap in caps for cap in required_caps)
            )
        ]

        return filtered
