import utils
import pandas as pd
import os

def test_logic():
    print("Testing CSV Load...")
    df = utils.load_csv("test_participants.csv")
    assert df is not None
    assert len(df) == 2
    print("CSV Load OK")

    print("Testing Deduplication...")
    participants = []
    new_p = utils.deduplicate_participants(df, participants)
    assert len(new_p) == 2
    participants.extend(new_p)
    
    # Try adding same again
    new_p_2 = utils.deduplicate_participants(df, participants)
    assert len(new_p_2) == 0
    print("Deduplication OK")

    print("Testing Export...")
    teams = {"Team Alpha": ["tommaso.giacomello@studbocconi.it"]}
    export_df = utils.export_teams_to_csv(teams, participants)
    assert len(export_df) == 1
    assert export_df.iloc[0]['Full Name'] == "Tommaso Giacomello"
    print("Export OK")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_logic()
