# Team Maker App

A local Python application built with Streamlit to manage hackathon participants, organize them into teams, and track their progress.

## 🚀 Features
- **Smart CSV Import**: Upload participant data from Google Sheets. The app automatically deduplicates entries based on email to prevent double-counting.
- **Interactive Team Building**:
    - **Search & Filter**: Find participants by name, skills, or motivation. Filter by "In Team" or "No Team" status.
    - **Team Management**: Create teams with auto-generated names (e.g., "Team 1").
    - **Tracks**: Assign teams to specific tracks (**ML** 🤖 or **Entrepreneurship** 🚀) with visual color coding.
    - **Size Limits**: Enforces a maximum of 5 members per team.
- **Data Persistence**: All changes are automatically saved to a local `hackathon_state.json` file. You can close and reopen the app without losing data.
- **Export**: Download the final team formations as a clean CSV file, ready for sharing.

## 📂 Project Structure

The project consists of the following key files:

- **`app.py`**: The main entry point of the application. It handles the User Interface (UI) using Streamlit, manages session state, and coordinates interactions between the user and the data.
- **`utils.py`**: Contains utility functions for backend logic:
    - `load_csv`: Reads and cleans the uploaded CSV.
    - `deduplicate_participants`: Logic to ensure unique participants.
    - `save_state` / `load_state`: Handles reading/writing to the JSON database.
    - `export_teams_to_csv`: Formats the team data for export.
- **`hackathon_state.json`**: A JSON file that acts as a local database. It stores the list of participants and the current team structures. **Do not edit this manually** unless you know what you are doing.
- **`requirements.txt`**: Lists the Python libraries required to run the app.

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher installed on your system.

### Steps
1.  **Download** this folder to your computer.
2.  Open a **Terminal** (Mac/Linux) or **Command Prompt** (Windows).
3.  Navigate to the folder:
    ```bash
    cd /path/to/team-maker
    ```
4.  (Optional but Recommended) Create and activate a virtual environment:
    - **Mac/Linux**:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    - **Windows**:
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```
5.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ How to Run
1.  In the terminal, inside the project folder, run:
    ```bash
    streamlit run app.py
    ```
2.  A new tab will open in your default web browser with the app.

## 📖 Usage Guide

### 1. Import Data
- Go to the **Sidebar**.
- Upload your participants CSV file.
- Click **Import Participants**. The app will tell you how many new people were added.

### 2. Manage Teams
- Switch to the **Teams** tab.
- Click **Create New Team**. A new team (e.g., "Team 1") will appear.
- **Assign a Track**: Select "ML" or "Entrepreneurship" using the radio buttons on the team card. The card color will change (Blue for ML, Red for Entrepreneurship).

### 3. Assign Participants
- Switch to the **Participants** tab.
- Use the search bar to find a person.
- On their card, use the dropdown menu to select a team.
- **Note**: You cannot add a person to a team that already has 5 members.

### 4. Export
- In the **Sidebar**, click **Export Teams**.
- A `hackathon_teams.csv` file will be downloaded containing: `Team Name`, `Track`, `Full Name`, `Email`, `Phone`.

## ❓ Troubleshooting
- **App won't start**: Ensure you have activated your virtual environment and installed requirements.
- **Changes not showing**: The app usually updates automatically, but you can try refreshing the browser page.
- **"Team is full"**: You cannot add more than 5 members to a team. Remove a member first if you need to swap someone in.
