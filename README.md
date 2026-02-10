Skylark Drones – Drone Operations Coordinator AI Agent
🚁 Project Overview

Skylark Drones operates multiple drone missions across different locations, pilots, and drone types. Coordinating pilots, drones, and missions manually is error-prone and time-consuming.

This project implements an AI-powered Drone Operations Coordinator that:

Manages pilot rosters

Tracks drone inventory

Assigns pilots and drones to missions

Detects conflicts

Handles urgent mission reassignments

Syncs all updates with Google Sheets in real time

The system exposes a conversational API that allows users to interact with the coordinator using natural language.

🧠 Key Features
✅ Roster Management

Query pilots by skills, certifications, and location

Track availability (Available / Assigned / On Leave)

Update pilot status (synced back to Google Sheets)

✅ Drone Inventory Management

Query drones by capability, location, and availability

Detect maintenance constraints

Update drone status in Google Sheets

✅ Assignment Coordination

Match pilots and drones to missions

Enforce skill, certification, and location constraints

Prevent invalid or unsafe assignments

✅ Conflict Detection

Prevent double booking

Detect certification mismatches

Detect pilot–drone location mismatches

Prevent assignment of drones under maintenance

✅ Urgent Reassignment

Urgent missions can override lower-priority assignments

Automatically frees resources if required

Provides clear reassignment explanation

🏗️ Architecture Overview

The system follows an agentic design, where each responsibility is handled by a logical agent:

GoogleSheetsService – Reads/Writes live data

Roster Agent – Pilot filtering & availability checks

Drone Agent – Drone filtering & readiness checks

Assignment Agent – Combines pilots + drones

Conflict Agent – Validates assignments

Urgent Agent – Handles priority-based reassignment

FastAPI Layer – Conversational interface

Although implemented in a single FastAPI app, the design is modular and extensible.

📊 Data Source

The system uses Google Sheets as a real-time operational database:

pilot_roster

drone_fleet

missions

All updates made by the AI agent are written back to Google Sheets, enabling seamless human–AI collaboration.

🛠️ Tech Stack

Python 3.13

FastAPI – API & conversational interface

Uvicorn – ASGI server

Pandas – Data processing

gspread + oauth2client – Google Sheets integration

Google Cloud Service Account – Secure authentication

🚀 How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/Samarth2003-pes/skylark-ai-agent
cd skylark-ai-agent

2️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
python -m pip install -r requirements.txt

🔐 Google Sheets Credentials Setup

This project uses a Google Cloud Service Account to access Google Sheets.

⚠️ For security reasons, the credentials.json file is NOT included in this repository.

To run the application locally:

Create a Google Cloud service account

Enable the following APIs:

Google Sheets API

Google Drive API

Download the service account key as credentials.json

Place credentials.json in the project root directory (local only)

Share all Google Sheets with the service account email (Editor access)

4️⃣ Start the server
python -m uvicorn app:app --reload

🔗 Live Demo

This application is designed to be run locally due to secure Google Sheets credentials.

After starting the server, the interactive API documentation (Swagger UI) is available at:

http://127.0.0.1:8000/docs


All functionality, including mission assignment, conflict detection, and urgent reassignment, can be tested using the /chat endpoint from this interface.

💬 Example Chat Requests
Assign resources
{
  "message": "Assign resources for PRJ001"
}

Handle urgent mission
{
  "message": "Handle urgent mission"
}

🧪 Testing

The repository includes standalone test scripts to validate each agent:

test_roster_agent.py

test_drone_agent.py

test_assignment_agent.py

test_conflict_agent.py

test_sync_agent.py

test_urgent_agent.py

📌 Notes

The system intentionally fails safely if no valid assignment exists

All decisions are explainable and deterministic

Google Sheets remains the single source of truth

📄 License

This project was developed as part of a technical assignment for Skylark Drones.