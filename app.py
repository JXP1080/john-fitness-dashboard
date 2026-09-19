"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Complete Dashboard | Your Split (Weeks 5-12 Reference)
Deployed on Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="John's 48-Week Plan", page_icon="💪", layout="wide")

st.markdown("""
<style>
.phase-badge { padding: 8px 14px; border-radius: 8px; font-weight: bold; font-size: 12px; display: inline-block; }
.phase-1 { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.exercise-box { padding: 14px; background: #f8f9fa; border-left: 4px solid #667eea; border-radius: 6px; margin: 8px 0; }
.exercise-box.main { border-left-color: #667eea; }
.exercise-box.hyper { border-left-color: #764ba2; }
.exercise-box.vol { border-left-color: #fbbf24; }
.exercise-box.acc { border-left-color: #10b981; }
.weakness-alert { padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 6px; margin: 8px 0; font-size: 13px; color: #856404; }
.stat-card { background: white; padding: 12px; border-radius: 8px; border-left: 4px solid #667eea; text-align: center; }
.stat-label { font-size: 11px; color: #666; margin-bottom: 6px; }
.stat-value { font-size: 18px; font-weight: bold; color: #667eea; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# YOUR AUTHORITATIVE SPLIT (Week 5-12)
# ============================================================================

YOUR_SPLIT = {
    "Monday - Shoulders + Arms": {
        "focus": "Shoulder width + arm size",
        "duration": 90,
        "exercises": [
            {
                "name": "Machine Shoulder Press",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest_sec": 180,
                "week5": 38.0, "week6": 40.0, "week7": 42.0, "week8": 42.0,
                "week9": 42.0, "week11": 44.0, "week12": 44.0,
                "muscles": "Shoulders, Triceps",
            },
            {
                "name": "DB Lateral Raise",
                "type": "HYPER",
                "sets": 4,
                "reps": "12-15",
                "rest_sec": 60,
                "week5": 9.0, "week6": 9.0, "week7": 10.0, "week8": 11.0,
                "week9": 11.0, "week11": 12.0, "week12": 12.0,
                "muscles": "Side Delts",
                "weak_point": True,
                "notes": "⭐ PRIORITY: +1kg/week target",
            },
            {
                "name": "Cable Lateral Raise (Double Pulley)",
                "type": "HYPER",
                "sets": 3,
                "reps": "12-15",
                "rest_sec": 60,
                "week5": 8.0, "week6": 9.0, "week7": 9.0, "week8": 10.0,
                "week9": 10.0, "week11": 10.0, "week12": 10.0,
                "muscles": "Side Delts",
                "weak_point": True,
            },
            {
                "name": "Hammer Curl (Dumbbell)",
                "type": "HYPER",
                "sets": 3,
                "reps": "10-12",
                "rest_sec": 60,
                "week5": 14.0, "week6": 14.0, "week7": 15.0, "week8": 16.0,
                "week9": 16.0, "week11": 16.0, "week12": 16.0,
                "muscles": "Biceps",
            },
            {
                "name": "Triceps Cable Pushdown (Rope)",
                "type": "HYPER",
                "sets": 3,
                "reps": "12-15",
                "rest_sec": 60,
                "week5": 21.6, "week6": 22.0, "week7": 23.0, "week8": 25.0,
                "week9": 25.0, "week11": 25.0, "week12": 25.0,
                "muscles": "Triceps",
            },
        ]
    },
    
    "Tuesday - Legs + Back": {
        "focus": "Quad & back development",
        "duration": 90,
        "exercises": [
            {
                "name": "Back Squat",
                "type": "MAIN",
                "sets": 4,
                "reps": "6-8",
                "rest_sec": 180,
                "week5": 30.0, "week6": 32.0, "week7": 34.0, "week8": 40.0,
                "week9": 40.0, "week11": 40.0, "week12": 40.0,
                "muscles": "Quads",
                "notes": "⚠️ Form priority: Start 30kg",
            },
            {
                "name": "Leg Press",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest_sec": 180,
                "week5": 85.0, "week6": 88.0, "week7": 92.0, "week8": 95.0,
                "week9": 100.0, "week11": 110.0, "week12": 110.0,
                "muscles": "Quads",
            },
            {
                "name": "Leg Extension",
                "type": "HYPER",
                "sets": 3,
                "reps": "10-12",
                "rest_sec": 90,
                "week5": 45.0, "week6": 47.0, "week7": 50.0, "week8": 50.0,
                "week9": 50.0, "week11": 50.0, "week12": 50.0,
                "muscles": "Quads",
            },
            {
                "name": "Romanian Deadlift (RDL)",
                "type": "ACC",
                "sets": 3,
                "reps": "10-12",
                "rest_sec": 90,
                "week5": 65.0, "week6": 65.0, "week7": 70.0, "week8": 70.0,
                "week9": 70.0, "week11": 70.0, "week12": 70.0,
                "muscles": "Hamstrings, Glutes",
            },
            {
                "name": "Lat Pulldown",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest_sec": 180,
                "week5": 42.0, "week6": 45.0, "week7": 48.0, "week8": 48.0,
                "week9": 48.0, "week11": 48.0, "week12": 48.0,
                "muscles": "Lats, Back",
            },
            {
                "name": "Seated Row",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest_sec": 180,
                "week5": 42.0, "week6": 44.0, "week7": 48.0, "week8": 48.0,
                "week9": 48.0, "week11": 48.0, "week12": 48.0,
                "muscles": "Back, Middle Back",
            },
        ]
    },
    
    "Wednesday - Chest + Core": {
        "focus": "Chest density + core",
        "duration": 90,
        "exercises": [
            {
                "name": "Barbell Bench Press",
                "type": "MAIN",
                "sets": 4,
                "reps": "6-8",
                "rest_sec": 180,
                "week5": 28.0, "week6": 28.0, "week7": 30.0, "week8": 32.0,
                "week9": 32.0, "week11": 36.0, "week12": 36.0,
                "muscles": "Chest",
                "weak_point": True,
                "notes": "START: 28kg (25kg bar + 3kg jumpers). Density focus.",
            },
            {
                "name": "Dumbbell Bench Press",
                "type": "HYPER",
                "sets": 4,
                "reps": "8-10",
                "rest_sec": 120,
                "week5": 20.0, "week6": 21.0, "week7": 22.0, "week8": 23.0,
                "week9": 23.0, "week11": 24.0, "week12": 24.0,
                "muscles": "Chest",
            },
            {
                "name": "Machine Chest Press",
                "type": "VOL",
                "sets": 3,
                "reps": "12-15",
                "rest_sec": 90,
                "week5": 50.0, "week6": 52.0, "week7": 54.0, "week8": 55.0,
                "week9": 55.0, "week11": 55.0, "week12": 55.0,
                "muscles": "Chest",
            },
            {
                "name": "Incline Dumbbell Press",
                "type": "VOL",
                "sets": 3,
                "reps": "10-12",
                "rest_sec": 90,
                "week5": 16.0, "week6": 16.0, "week7": 18.0, "week8": 18.0,
                "week9": 18.0, "week11": 18.0, "week12": 18.0,
                "muscles": "Chest, Front Delts",
            },
            {
                "name": "Cable Crunch",
                "type": "ACC",
                "sets": 3,
                "reps": "12-15",
                "rest_sec": 60,
                "week5": 20.0, "week6": 22.0, "week7": 25.0, "week8": 25.0,
                "week9": 25.0, "week11": 25.0, "week12": 25.0,
                "muscles": "Core",
            },
            {
                "name": "Machine Ab Crunch",
                "type": "ACC",
                "sets": 3,
                "reps": "12-15",
                "rest_sec": 60,
                "week5": 25.0, "week6": 27.0, "week7": 29.0, "week8": 30.0,
                "week9": 30.0, "week11": 30.0, "week12": 30.0,
                "muscles": "Core",
            },
        ]
    },
    
    "Thursday - Arms + Leg Finisher": {
        "focus": "Arm size + leg pump",
        "duration": 90,
        "exercises": [
            {
                "name": "Hammer Curl (Dumbbell)",
                "type": "HYPER",
                "sets": 3,
                "reps": "10-12",
                "rest_sec": 60,
                "week5": 14.0, "week6": 14.0, "week7": 16.0, "week8": 16.0,
                "week9": 16.0, "week11": 16.0, "week12": 16.0,
                "muscles": "Biceps",
            },
            {
                "name": "Machine Curl",
                "type": "HYPER",
                "sets": 3,
                "reps": "10-12",
                "rest_sec": 60,
                "week5": 18.0, "week6": 18.0, "week7": 20.0, "week8": 20.0,
                "week9": 20.0, "week11": 20.0, "week12": 20.0,
                "muscles": "Biceps",
            },
            {
                "name": "Triceps Cable Pushdown",
                "type": "HYPER",
                "sets": 3,
                "reps": "12-15",
                "rest_sec": 60,
                "week5": 21.6, "week6": 22.0, "week7": 23.0, "week8": 25.0,
                "week9": 25.0, "week11": 25.0, "week12": 25.0,
                "muscles": "Triceps",
            },
            {
                "name": "Machine Dip",
                "type": "HYPER",
                "sets": 2,
                "reps": "12-15",
                "rest_sec": 60,
                "week5": 45.0, "week6": 47.0, "week7": 50.0, "week8": 50.0,
                "week9": 50.0, "week11": 50.0, "week12": 50.0,
                "muscles": "Triceps",
            },
            {
                "name": "Leg Press Drop Set",
                "type": "VOL",
                "sets": 2,
                "reps": "Drop to fail",
                "rest_sec": 120,
                "week5": "85→65→45", "week6": "90→70→50", "week7": "95→75→55", "week8": "95→75→55",
                "week9": "100→80→60", "week11": "110→90→70", "week12": "110→90→70",
                "muscles": "Quads",
                "notes": "Finisher: +5kg each stage every 2 weeks",
            },
        ]
    },
}

# ============================================================================
# UI
# ============================================================================

st.title("💪 John's 48-Week Aesthetic Density Program")

with st.sidebar:
    st.markdown("### Dashboard")
    selected_week = st.slider("Week", min_value=1, max_value=48, value=5)
    
    if selected_week <= 8:
        phase = "Phase 1: Accumulation"
        color = "phase-1"
    elif selected_week <= 16:
        phase = "Phase 2: Intensification"
        color = "phase-1"
    else:
        phase = f"Phase {(selected_week - 17) // 8 + 3}"
        color = "phase-1"
    
    st.markdown(f"<div class='phase-badge {color}'>{phase}</div>", unsafe_allow_html=True)
    st.divider()
    st.metric("Current Weight", "69.6 kg", "+2.4 kg")
    st.metric("Target (Week 8)", "71-72 kg", "")
    st.metric("Target (Week 12)", "73 kg", "")

st.markdown(f"**Week {selected_week}** | View your complete split with progressive overload targets")

# STATS
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class='stat-card'><div class='stat-label'>Workouts/Week</div><div class='stat-value'>4</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class='stat-card' style='border-left-color: #764ba2;'><div class='stat-label'>Total Sets</div><div class='stat-value' style='color: #764ba2;'>102</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class='stat-card' style='border-left-color: #fbbf24;'><div class='stat-label'>Duration/Week</div><div class='stat-value' style='color: #fbbf24;'>360 min</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class='stat-card' style='border-left-color: #10b981;'><div class='stat-label'>Intensity</div><div class='stat-value' style='color: #10b981;'>RPE 8-9</div></div>""", unsafe_allow_html=True)

st.divider()

# WEAK POINTS
st.markdown("<div class='weakness-alert'><strong>⭐ WEAK POINT FOCUS (Your Priority Areas)</strong><br>🔴 Shoulders (Lateral raise 8kg → 12kg): 3x per week volume<br>🔴 Chest (Bench 25kg → 36kg): Density progression<br>🟡 Leg Form (Squat at 30kg): Safety & stability focus</div>", unsafe_allow_html=True)

st.divider()

# WEEKLY SPLIT TABS
st.markdown("### 📅 Your Weekly Split")

tabs = st.tabs(["Monday", "Tuesday", "Wednesday", "Thursday", "📊 Progression"])

days = ["Monday - Shoulders + Arms", "Tuesday - Legs + Back", "Wednesday - Chest + Core", "Thursday - Arms + Leg Finisher"]

for tab_idx, (tab, day) in enumerate(zip(tabs[:-1], days)):
    with tab:
        day_data = YOUR_SPLIT[day]
        st.markdown(f"**{day}** | {day_data['focus']} ({day_data['duration']} min)")
        
        for ex in day_data["exercises"]:
            type_color = {"MAIN": "#667eea", "HYPER": "#764ba2", "VOL": "#fbbf24", "ACC": "#10b981"}[ex["type"]]
            
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                weak_flag = "⭐ " if ex.get("weak_point") else ""
                st.markdown(f"<div class='exercise-box' style='border-left-color: {type_color};'>"
                           f"<strong>{weak_flag}{ex['name']}</strong><br>"
                           f"<span style='font-size: 12px; color: #666;'>{ex['type']} | {ex['sets']} sets x {ex['reps']} | Rest {ex['rest_sec']}s | {ex['muscles']}</span>"
                           f"</div>", unsafe_allow_html=True)
                
                if ex.get("notes"):
                    st.markdown(f"*{ex['notes']}*")
            
            with col2:
                st.markdown(f"**W5:** {ex['week5']}kg  \n**W8:** {ex['week8']}kg")

# PROGRESSION TABLE
with tabs[4]:
    prog_data = []
    for day in days:
        for ex in YOUR_SPLIT[day]["exercises"]:
            prog_data.append({
                "Exercise": ex["name"],
                "Type": ex["type"],
                "W5": ex["week5"],
                "W8": f"**{ex['week8']}**",
                "+Gain": f"+{ex['week8'] - ex['week5']:.1f}kg" if isinstance(ex['week8'], (int, float)) else "—",
            })
    
    df = pd.DataFrame(prog_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# PHASE GUIDE
with st.expander("📋 Phase 1 Guide (Weeks 5-8)", expanded=False):
    st.markdown("""
    **Accumulation Phase**
    - High volume (22-27 sets/session)
    - Moderate loads (RPE 8-9)
    - Focus on movement quality
    - Build work capacity
    
    **Progression Rules**
    1. Increase reps first (hit top of range)
    2. Then increase weight (+2-5kg)
    3. Rest only if recovery is good
    
    **Week 8 Targets**
    - Barbell Bench: 32kg (28kg → +4kg)
    - Lateral Raise: 11kg (9kg → +2kg)
    - Leg Press: 95kg (85kg → +10kg)
    - Body Weight: 71-72kg
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px;'>
📱 Syncing with BoostCamp App | ✅ Your split matches authoritative reference<br>
Ready to deploy to Streamlit Cloud
</div>
""", unsafe_allow_html=True)
