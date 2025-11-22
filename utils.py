import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

STATE_FILE = "hackathon_state.json"

def load_state():
    """Loads the application state from a JSON file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"participants": [], "teams": {}}

def save_state(state):
    """Saves the application state to a JSON file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def load_csv(file):
    """Loads participants from a CSV file."""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

def deduplicate_participants(new_df, current_participants):
    """
    Deduplicates participants based on Email.
    Returns a list of new unique participants (as dicts).
    """
    existing_emails = {p.get('Email') for p in current_participants}
    new_participants = []
    
    # Convert DataFrame to list of dicts for easier processing
    records = new_df.to_dict('records')
    
    for record in records:
        email = record.get('Email')
        if email and email not in existing_emails:
            # Add a unique ID if needed, or just use Email as key
            # For now, we just append the record
            # Clean up NaN values which are common in pandas imports
            clean_record = {k: (v if pd.notna(v) else "") for k, v in record.items()}
            new_participants.append(clean_record)
            existing_emails.add(email)
            
    return new_participants

def export_teams_to_csv(teams, participants):
    """
    Exports teams to a CSV format.
    teams: dict {team_name: {'members': [email, ...], 'track': ...}} 
           OR old format {team_name: [email, ...]} (for backward compat if needed, but we will migrate)
    participants: list of dicts
    """
    # Create a mapping of email -> participant data
    p_map = {p.get('Email'): p for p in participants}
    
    export_data = []
    for team_name, team_data in teams.items():
        # Handle both new dict structure and old list structure
        if isinstance(team_data, dict):
            members = team_data.get('members', [])
            track = team_data.get('track', 'Unknown')
        else:
            members = team_data
            track = 'Unknown'

        for member_email in members:
            p_data = p_map.get(member_email, {})
            row = {
                "Team Name": team_name,
                "Track": track,
                "Full Name": p_data.get('Full Name', ''),
                "Email": member_email,
                "Phone": p_data.get('Phone', '')
            }
            export_data.append(row)
            
    return pd.DataFrame(export_data)
