"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Complete Streamlit Dashboard - Production Ready
UPDATED: Session storage for workout history + live analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# PAGE CONFIG
st.set_page_config(
    page_title="John's 48-Week Aesthetic Density Plan",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS
st.markdown("""
<style>
.phase-badge {
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 12px;
    display: inline-block;
    margin-bottom: 12px;
}
.phase-1 { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.phase-2 { background: linear-gradient(135deg, #764ba2, #f093fb); color: white; }
.phase-3 { background: linear-gradient(135deg, #f093fb, #4facfe); color: white; }
.stat-card {
    background: white;
    padding: 14px 16px;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    text-align: center;
}
.stat-label { font-size: 11px; color: #666; margin-bottom: 8px; }
.stat-value { font-size: 20px; font-weight: bold; color: #667eea; }
.weakness-alert {
    padding: 14px;
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    border-radius: 6px;
    margin: 12px 0;
    font-size: 13px;
    color: #856404;
}
.progress-box {
    background: #e8f5e9;
    padding: 12px;
    border-left: 4px solid #4caf50;
    border-radius: 6px;
    margin: 8px 0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE - UPDATED WITH WORKOUT HISTORY
# ============================================================================

if "current_week" not in st.session_state:
    st.session_state.current_week = 5

if "workout_history" not in st.session_state:
    st.session_state.workout_history = {}  # Format: {exercise_name: {"weight": X, "reps": Y, "rpe": Z, "date": datetime}}

if "weekly_logs" not in st.session_state:
    st.session_state.weekly_logs = []  # List of all logged sessions

# ============================================================================
# YOUR SPLIT DATA (AUTHORITATIVE)
# ============================================================================

YOUR_SPLIT = {
    "Monday - Shoulders + Arms": {
        "exercises": [
            {"name": "Machine Shoulder Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 38.0, "w8": 42.0},
            {"name": "DB Lateral Raise", "type": "HYPER", "sets": 4, "reps": "12-15", "rest": 60, "w5": 9.0, "w8": 11.0, "weak": True},
            {"name": "Cable Lateral Raise (Double)", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 8.0, "w8": 10.0, "weak": True},
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "w8": 16.0},
            {"name": "Triceps Cable Pushdown", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "w8": 25.0},
        ]
    },
    "Tuesday - Legs + Back": {
        "exercises": [
            {"name": "Back Squat", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 30.0, "w8": 40.0},
            {"name": "Leg Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 85.0, "w8": 95.0},
            {"name": "Leg Extension", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 90, "w5": 45.0, "w8": 50.0},
            {"name": "RDL", "type": "ACC", "sets": 3, "reps": "10-12", "rest": 90, "w5": 65.0, "w8": 70.0},
            {"name": "Lat Pulldown", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0, "w8": 48.0},
            {"name": "Seated Row", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0, "w8": 48.0},
        ]
    },
    "Wednesday - Chest + Core": {
        "exercises": [
            {"name": "Barbell Bench Press", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 28.0, "w8": 32.0, "weak": True},
            {"name": "DB Bench Press", "type": "HYPER", "sets": 4, "reps": "8-10", "rest": 120, "w5": 20.0, "w8": 23.0},
            {"name": "Machine Chest Press", "type": "VOL", "sets": 3, "reps": "12-15", "rest": 90, "w5": 50.0, "w8": 55.0},
            {"name": "Incline DB Press", "type": "VOL", "sets": 3, "reps": "10-12", "rest": 90, "w5": 16.0, "w8": 18.0},
            {"name": "Cable Crunch", "type": "ACC", "sets": 3, "reps": "12-15", "rest": 60, "w5": 20.0, "w8": 25.0},
            {"name": "Machine Ab Crunch", "type": "ACC", "sets": 3, "reps": "12-15", "rest": 60, "w5": 25.0, "w8": 30.0},
        ]
    },
    "Thursday - Arms + Leg Finisher": {
        "exercises": [
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "w8": 16.0},
            {"name": "Machine Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 18.0, "w8": 20.0},
            {"name": "Triceps Cable Pushdown", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "w8": 25.0},
            {"name": "Machine Dip", "type": "HYPER", "sets": 2, "reps": "12-15", "rest": 60, "w5": 45.0, "w8": 50.0},
            {"name": "Leg Press Drop Set", "type": "VOL", "sets": 2, "reps": "Drop to fail", "rest": 120, "w5": "85→65→45", "w8": "95→75→55"},
        ]
    },
}

# ============================================================================
# SIDEBAR
# ============================================================================

with
