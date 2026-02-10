Skylark Drones – Drone Operations Coordinator AI Agent

1. Overview

The goal of this project was to build an AI agent that can act as a Drone Operations Coordinator, handling pilot availability, drone inventory, mission assignments, and conflict resolution. The system was designed to reduce manual coordination by reasoning over live operational data and making safe, explainable decisions.

2. Key Assumptions

Google Sheets as Source of Truth
Google Sheets was assumed to be the primary operational database because:

It is easy for non-technical users to update

It supports real-time collaboration

It satisfies the requirement for two-way sync

Rule-based Agentic Reasoning
Instead of using machine learning, the system uses rule-based reasoning because:

The problem is deterministic (skills, certifications, availability)

Decisions must be explainable

Safety and correctness are more important than prediction

Single Pilot + Single Drone per Mission
Each mission is assumed to require exactly:

One pilot

One drone
This simplifies coordination logic and avoids partial assignments.

Location Matching Is Mandatory
Pilots and drones must be in the same location as the mission to avoid unrealistic assignments.

3. Architecture Decisions
Agent-based Design

The system was split into multiple logical agents, each responsible for a single concern:

Roster Agent – Handles pilot availability, skills, certifications, and location

Drone Agent – Handles drone availability, capabilities, location, and maintenance

Assignment Agent – Combines valid pilots and drones into assignments

Conflict Agent – Detects invalid or unsafe assignments

Urgent Reassignment Agent – Handles high-priority mission overrides

Sync Logic – Writes updates back to Google Sheets

Although implemented in a single file for simplicity, the design follows a modular agentic approach.

4. Handling Ambiguity
Mapping Mission Skills to Drone Capabilities

Mission requirements such as Mapping do not directly match drone capabilities like LiDAR or RGB.
To handle this ambiguity, a capability mapping rule was introduced:

Mapping → LiDAR or RGB

Inspection → RGB

Thermal → Thermal

This decision reflects real-world operational reasoning instead of simple string matching.

5. Conflict Detection Strategy

The Conflict Agent checks for the following conditions before finalizing an assignment:

Pilot is not available

Pilot lacks required certifications

Pilot location mismatch

Drone location mismatch

Drone under maintenance

If any conflict is detected, the assignment is safely rejected with a clear explanation.

6. Urgent Reassignment Interpretation

Interpretation:
Urgent missions are allowed to override lower-priority assignments.

Implementation:
When a mission is marked as Urgent and no free resources are available:

The agent looks for pilots and drones currently assigned to lower-priority missions

Frees one pilot and one drone

Reassigns them to the urgent mission

Returns a clear explanation of the reassignment

This reflects how real operations teams prioritize critical missions.

7. Trade-offs Made

Single-file implementation was chosen for simplicity and clarity, even though the system can be modularized further.

No ML models were used to ensure transparency and deterministic behavior.

Simple selection strategy (first valid match) was used instead of optimization to keep the system reliable and explainable.

8. What I Would Improve with More Time

Add assignment history tracking

Add time-based overlap detection using start/end dates

Implement optimization strategies (load balancing, fairness)

Add authentication and role-based access

Deploy with persistent backend storage instead of Sheets

9. Conclusion

This project demonstrates how an agentic AI system can manage complex coordination tasks by reasoning over structured data, handling edge cases, and making explainable decisions. The design prioritizes correctness, safety, and real-world usability over complexity.