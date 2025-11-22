import streamlit as st
import pandas as pd
import utils

# Page Config
st.set_page_config(page_title="Team Maker", layout="wide")

# Initialize Session State
if 'participants' not in st.session_state:
    state = utils.load_state()
    st.session_state['participants'] = state.get('participants', [])
    # Migrate old teams structure if necessary
    loaded_teams = state.get('teams', {})
    migrated_teams = {}
    for t_name, t_data in loaded_teams.items():
        if isinstance(t_data, list):
            migrated_teams[t_name] = {'members': t_data, 'track': 'Unassigned'}
        else:
            migrated_teams[t_name] = t_data
    st.session_state['teams'] = migrated_teams

def save_current_state():
    state = {
        "participants": st.session_state['participants'],
        "teams": st.session_state['teams']
    }
    utils.save_state(state)
    # st.toast("State saved successfully!") # Reduced noise

# Sidebar
with st.sidebar:
    st.title("Team Maker Tools")
    
    uploaded_file = st.file_uploader("Upload Participants CSV", type=['csv'])
    if uploaded_file:
        if st.button("Import Participants"):
            df = utils.load_csv(uploaded_file)
            if df is not None:
                new_p = utils.deduplicate_participants(df, st.session_state['participants'])
                if new_p:
                    st.session_state['participants'].extend(new_p)
                    save_current_state()
                    st.success(f"Imported {len(new_p)} new participants.")
                else:
                    st.info("No new participants found.")

    st.divider()
    if st.button("Save State"):
        save_current_state()
        st.success("State saved!")

    if st.button("Export Teams"):
        df_teams = utils.export_teams_to_csv(st.session_state['teams'], st.session_state['participants'])
        csv = df_teams.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Teams CSV",
            data=csv,
            file_name='hackathon_teams.csv',
            mime='text/csv',
        )
        
    if st.button("Reset App"):
        if st.button("Confirm Reset?"):
            st.session_state['participants'] = []
            st.session_state['teams'] = {}
            save_current_state()
            st.rerun()

# Main Area
st.title("Hackathon Team Maker")

tab1, tab2 = st.tabs(["Participants", "Teams"])

with tab1:
    st.header("Participants")
    
    # Search and Filter
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_term = st.text_input("Search Participants", placeholder="Name, Skills, Motivation...")
    with col_filter:
        filter_status = st.selectbox("Filter by Status", ["All", "In Team", "No Team"])
    
    # Filter logic
    filtered_participants = st.session_state['participants']
    
    # 1. Text Search
    if search_term:
        term = search_term.lower()
        filtered_participants = [
            p for p in filtered_participants 
            if term in str(p.get('Full Name', '')).lower() or
               term in str(p.get('Degree Program', '')).lower() or
               term in str(p.get('Motivation', '')).lower() or
               term in str(p.get('First Track', '')).lower()
        ]
    
    # 2. Status Filter
    if filter_status != "All":
        # Build a set of emails currently in teams
        in_team_emails = set()
        for t_data in st.session_state['teams'].values():
            in_team_emails.update(t_data['members'])
            
        if filter_status == "In Team":
            filtered_participants = [p for p in filtered_participants if p.get('Email') in in_team_emails]
        elif filter_status == "No Team":
            filtered_participants = [p for p in filtered_participants if p.get('Email') not in in_team_emails]

    st.caption(f"Showing {len(filtered_participants)} participants")
    
    # Display Cards (Grid Layout)
    cols = st.columns(3)
    for idx, p in enumerate(filtered_participants):
        with cols[idx % 3]:
            # Determine Status
            in_team = False
            current_team = None
            for t_name, t_data in st.session_state['teams'].items():
                if p.get('Email') in t_data['members']:
                    in_team = True
                    current_team = t_name
                    break
            
            card_border = True
            with st.container(border=card_border):
                # Header with Status Badge
                if in_team:
                    st.markdown(f"**{p.get('Full Name', 'Unknown')}** :white_check_mark:")
                    st.caption(f"In Team: {current_team}")
                else:
                    st.markdown(f"**{p.get('Full Name', 'Unknown')}** :warning:")
                    st.caption("No Team")

                # Key Info
                st.text(f"{p.get('Degree Program', 'N/A')} - {p.get('Year of Study', '')}")
                st.markdown(f"*{p.get('First Track', 'N/A')}*")
                
                # Expander for details
                with st.expander("View Details"):
                    st.write(f"**Email:** {p.get('Email')}")
                    st.write(f"**Phone:** {p.get('Phone')}")
                    st.write(f"**Motivation:** {p.get('Motivation')}")
                    if p.get('LinkedIn'):
                        st.markdown(f"[LinkedIn]({p.get('LinkedIn')})")
                    if p.get('GitHub'):
                        st.markdown(f"[GitHub]({p.get('GitHub')})")
                    if p.get('CV (Drive Link)'):
                        st.markdown(f"[CV]({p.get('CV (Drive Link)')})")

                # Add to Team Action
                if not in_team:
                    # Filter teams that are not full (< 5 members)
                    available_teams = [
                        t_name for t_name, t_data in st.session_state['teams'].items()
                        if len(t_data['members']) < 5
                    ]
                    
                    if available_teams:
                        selected_team = st.selectbox(f"Add to...", ["Select..."] + available_teams, key=f"add_{idx}")
                        if selected_team != "Select...":
                            st.session_state['teams'][selected_team]['members'].append(p.get('Email'))
                            save_current_state()
                            st.toast(f"Added to {selected_team}")
                            st.rerun()
                    else:
                        st.caption("No available teams (create one or free up space)")
                else:
                    if st.button("Remove from Team", key=f"rem_card_{idx}"):
                        st.session_state['teams'][current_team]['members'].remove(p.get('Email'))
                        save_current_state()
                        st.rerun()

with tab2:
    st.header("Teams Management")
    
    # Auto-generate Team Name
    if st.button("Create New Team"):
        # Find first available Team N
        i = 1
        while f"Team {i}" in st.session_state['teams']:
            i += 1
        new_team_name = f"Team {i}"
        st.session_state['teams'][new_team_name] = {'members': [], 'track': 'Unassigned'}
        save_current_state()
        st.success(f"Created {new_team_name}")
        st.rerun() # Refresh to show new team immediately

    st.divider()

    # Display Teams
    # Sort teams by name naturally
    sorted_teams = sorted(st.session_state['teams'].items(), key=lambda x: int(x[0].split(' ')[1]) if 'Team ' in x[0] else x[0])
    
    for team_name, team_data in sorted_teams:
        members = team_data['members']
        track = team_data.get('track', 'Unassigned')
        
        # Visual distinction for tracks
        track_color = "#e0e0e0" # Default gray
        track_emoji = "⚪"
        if track == "ML":
            track_color = "#e3f2fd" # Light Blue
            border_color = "#2196f3" # Blue
            track_emoji = "🤖"
        elif track == "Entrepreneurship":
            track_color = "#ffebee" # Light Red
            border_color = "#f44336" # Red
            track_emoji = "🚀"
        else:
            border_color = "#9e9e9e"

        with st.container(border=True):
            # Custom Header with Color
            st.markdown(
                f"""
                <div style="
                    background-color: {track_color}; 
                    padding: 10px; 
                    border-radius: 5px; 
                    border-left: 5px solid {border_color};
                    margin-bottom: 10px;
                    color: #000000; /* Force black text for contrast on light background */
                ">
                    <h3 style="margin: 0; padding: 0; color: #000000;">{team_name} {track_emoji}</h3>
                    <p style="margin: 0; color: {border_color}; font-weight: bold;">{track} Track</p>
                    <p style="margin: 0; font-size: 0.8em; color: #333333;">{len(members)}/5 Members</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            c2 = st.container()
            if c2.button("Delete Team", key=f"del_{team_name}"):
                del st.session_state['teams'][team_name]
                save_current_state()
                st.rerun()
            
            # Track Selection
            new_track = st.radio(
                "Change Track", 
                ["Unassigned", "ML", "Entrepreneurship"], 
                index=["Unassigned", "ML", "Entrepreneurship"].index(track),
                key=f"track_{team_name}",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            if new_track != track:
                st.session_state['teams'][team_name]['track'] = new_track
                save_current_state()
                st.rerun()

            # Members List
            for member_email in members:
                member = next((p for p in st.session_state['participants'] if p.get('Email') == member_email), None)
                if member:
                    m_col1, m_col2 = st.columns([4, 1])
                    m_col1.write(f"👤 {member.get('Full Name')} ({member.get('Degree Program')})")
                    if m_col2.button("Remove", key=f"rem_{team_name}_{member_email}"):
                        st.session_state['teams'][team_name]['members'].remove(member_email)
                        save_current_state()
                        st.rerun()
