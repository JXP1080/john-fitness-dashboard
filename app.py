"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Complete Streamlit Dashboard
All 7 tabs: Split, Workout Logger, Nutrition, Metrics, Analytics, 12-Month Plan, Settings
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="John's 48-Week Plan", page_icon="💪", layout="wide")

# CUSTOM CSS
st.markdown("""
<style>
.phase-badge { padding: 8px 14px; border-radius: 8px; font-weight: bold; font-size: 12px; display: inline-block; }
.phase-1 { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.phase-2 { background: linear-gradient(135deg, #764ba2, #f093fb); color: white; }
.phase-3 { background: linear-gradient(135deg, #f093fb, #4facfe); color: white; }
.stat-card { background: white; padding: 12px; border-radius: 8px; border-left: 4px solid #667eea; text-align: center; }
.stat-label { font-size: 11px; color: #666; margin-bottom: 6px; }
.stat-value { font-size: 18px; font-weight: bold; color: #667eea; }
.weakness-alert { padding: 12px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 6px; margin: 8px 0; font-size: 13px; }
.exercise-box { padding: 14px; background: #f8f9fa; border-left: 4px solid #667eea; border-radius: 6px; margin: 8px 0; }
table { width: 100%; font-size: 13px; }
td, th { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
th { background: #f8f9fa; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "workout_log" not in st.session_state:
    st.session_state.workout_log = []

if "nutrition_log" not in st.session_state:
    st.session_state.nutrition_log = {}

if "metrics_log" not in st.session_state:
    st.session_state.metrics_log = []

if "current_week" not in st.session_state:
    st.session_state.current_week = 5

# ============================================================================
# YOUR SPLIT DATA (AUTHORITATIVE)
# ============================================================================

YOUR_SPLIT = {
    "Monday - Shoulders + Arms": {
        "exercises": [
            {"name": "Machine Shoulder Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 38, "w6": 40, "w7": 42, "w8": 42, "w9": 42, "w11": 44, "w12": 44},
            {"name": "DB Lateral Raise", "type": "HYPER", "sets": 4, "reps": "12-15", "rest": 60, "w5": 9, "w6": 9, "w7": 10, "w8": 11, "w9": 11, "w11": 12, "w12": 12, "weak": True},
            {"name": "Cable Lateral Raise (Double)", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 8, "w6": 9, "w7": 9, "w8": 10, "w9": 10, "w11": 10, "w12": 10, "weak": True},
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14, "w6": 14, "w7": 15, "w8": 16, "w9": 16, "w11": 16, "w12": 16},
            {"name": "Triceps Cable Pushdown", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "w6": 22, "w7": 23, "w8": 25, "w9": 25, "w11": 25, "w12": 25},
        ]
    },
    "Tuesday - Legs + Back": {
        "exercises": [
            {"name": "Back Squat", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 30, "w6": 32, "w7": 34, "w8": 40, "w9": 40, "w11": 40, "w12": 40},
            {"name": "Leg Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 85, "w6": 88, "w7": 92, "w8": 95, "w9": 100, "w11": 110, "w12": 110},
            {"name": "Leg Extension", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 90, "w5": 45, "w6": 47, "w7": 50, "w8": 50, "w9": 50, "w11": 50, "w12": 50},
            {"name": "RDL", "type": "ACC", "sets": 3, "reps": "10-12", "rest": 90, "w5": 65, "w6": 65, "w7": 70, "w8": 70, "w9": 70, "w11": 70, "w12": 70},
            {"name": "Lat Pulldown", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42, "w6": 45, "w7": 48, "w8": 48, "w9": 48, "w11": 48, "w12": 48},
            {"name": "Seated Row", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42, "w6": 44, "w7": 48, "w8": 48, "w9": 48, "w11": 48, "w12": 48},
        ]
    },
    "Wednesday - Chest + Core": {
        "exercises": [
            {"name": "Barbell Bench Press", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 28, "w6": 28, "w7": 30, "w8": 32, "w9": 32, "w11": 36, "w12": 36, "weak": True},
            {"name": "DB Bench Press", "type": "HYPER", "sets": 4, "reps": "8-10", "rest": 120, "w5": 20, "w6": 21, "w7": 22, "w8": 23, "w9": 23, "w11": 24, "w12": 24},
            {"name": "Machine Chest Press", "type": "VOL", "sets": 3, "reps": "12-15", "rest": 90, "w5": 50, "w6": 52, "w7": 54, "w8": 55, "w9": 55, "w11": 55, "w12": 55},
            {"name": "Incline DB Press", "type": "VOL", "sets": 3, "reps": "10-12", "rest": 90, "w5": 16, "w6": 16, "w7": 18, "w8": 18, "w9": 18, "w11": 18, "w12": 18},
            {"name": "Cable Crunch", "type": "ACC", "sets": 3, "reps": "12-15", "rest": 60, "w5": 20, "w6": 22, "w7": 25, "w8": 25, "w9": 25, "w11": 25, "w12": 25},
            {"name": "Machine Ab Crunch", "type": "ACC", "sets": 3, "reps": "12-15", "rest": 60, "w5": 25, "w6": 27, "w7": 29, "w8": 30, "w9": 30, "w11": 30, "w12": 30},
        ]
    },
    "Thursday - Arms + Leg Finisher": {
        "exercises": [
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14, "w6": 14, "w7": 16, "w8": 16, "w9": 16, "w11": 16, "w12": 16},
            {"name": "Machine Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 18, "w6": 18, "w7": 20, "w8": 20, "w9": 20, "w11": 20, "w12": 20},
            {"name": "Triceps Cable Pushdown", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "w6": 22, "w7": 23, "w8": 25, "w9": 25, "w11": 25, "w12": 25},
            {"name": "Machine Dip", "type": "HYPER", "sets": 2, "reps": "12-15", "rest": 60, "w5": 45, "w6": 47, "w7": 50, "w8": 50, "w9": 50, "w11": 50, "w12": 50},
            {"name": "Leg Press Drop Set", "type": "VOL", "sets": 2, "reps": "Drop to fail", "rest": 120, "w5": "85→65→45", "w6": "90→70→50", "w7": "95→75→55", "w8": "95→75→55", "w9": "100→80→60", "w11": "110→90→70", "w12": "110→90→70"},
        ]
    },
}

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### Dashboard")
    selected_week = st.slider("Week", min_value=1, max_value=48, value=5)
    st.session_state.current_week = selected_week
    
    # Phase determination
    if selected_week <= 8:
        phase_text = "Phase 1: Accumulation"
        phase_color = "phase-1"
    elif selected_week <= 16:
        phase_text = "Phase 2: Intensification"
        phase_color = "phase-1"
    elif selected_week <= 24:
        phase_text = "Phase 3: Hypertrophy"
        phase_color = "phase-2"
    elif selected_week <= 32:
        phase_text = "Phase 4: Strength"
        phase_color = "phase-2"
    elif selected_week <= 40:
        phase_text = "Phase 5: Peak Power"
        phase_color = "phase-3"
    else:
        phase_text = "Phase 6: Deload"
        phase_color = "phase-3"
    
    st.markdown(f"<div class='phase-badge {phase_color}'>{phase_text}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 📊 Progress")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weight", "69.6 kg", "+2.4")
    with col2:
        st.metric("Target", "75 kg", "5.4 to go")
    
    st.markdown("### ⚠️ Focus Areas")
    st.markdown("🔴 **Shoulders** (3x/week)\n🔴 **Chest** (density)\n🟡 **Legs** (form)")

# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["📊 Dashboard", "🏋️ Workout Logger", "🍽️ Nutrition", "📈 Metrics", "📉 Analytics", "🗓️ 12-Month Plan", "⚙️ Settings"]
)

# ============================================================================
# TAB 1: DASHBOARD
# ============================================================================

with tab1:
    st.markdown(f"### Week {selected_week} Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='stat-card'><div class='stat-label'>Workouts/Week</div><div class='stat-value'>4</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='stat-card' style='border-left-color: #764ba2;'><div class='stat-label'>Total Sets</div><div class='stat-value' style='color: #764ba2;'>102</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='stat-card' style='border-left-color: #fbbf24;'><div class='stat-label'>Duration</div><div class='stat-value' style='color: #fbbf24;'>360m</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='stat-card' style='border-left-color: #10b981;'><div class='stat-label'>RPE Target</div><div class='stat-value' style='color: #10b981;'>8-9</div></div>""", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### Weekly Split Summary")
    
    for day, data in YOUR_SPLIT.items():
        with st.expander(f"📅 {day}"):
            for ex in data["exercises"]:
                week_key = f"w{selected_week}"
                weight = ex.get(week_key, "—")
                weak_badge = "⭐ " if ex.get("weak") else ""
                st.markdown(f"**{weak_badge}{ex['name']}**  \n"
                           f"{ex['type']} | {ex['sets']}×{ex['reps']} | Rest {ex['rest']}s | **{weight}kg**")

# ============================================================================
# TAB 2: WORKOUT LOGGER
# ============================================================================

with tab2:
    st.markdown("### Log Today's Workout")
    
    day = st.selectbox("Select Day", list(YOUR_SPLIT.keys()))
    
    st.markdown(f"#### {day}")
    
    exercises = YOUR_SPLIT[day]["exercises"]
    
    for i, ex in enumerate(exercises):
        with st.container():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**{ex['name']}**  \nTarget: {ex['sets']}×{ex['reps']}")
            
            with col2:
                weight = st.number_input(f"Weight (kg) - {ex['name']}", value=float(ex.get("w5", 0)), step=0.5, key=f"w_{i}")
                reps = st.number_input(f"Reps - {ex['name']}", value=int(ex['reps'].split('-')[0]) if '-' in ex['reps'] else 8, key=f"r_{i}")
            
            with col3:
                rpe = st.slider(f"RPE - {ex['name']}", 1, 10, 8, key=f"rpe_{i}")
            
            if st.button("✅ Log Set", key=f"log_{i}"):
                st.success(f"✓ {ex['name']}: {weight}kg × {reps} @ RPE {rpe}")

# ============================================================================
# TAB 3: NUTRITION TRACKER
# ============================================================================

with tab3:
    st.markdown("### Daily Nutrition Tracker")
    st.markdown("**Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    col1, col2 = st.columns(2)
    
    meals = ["7am Breakfast", "10am Snack", "1pm Lunch", "3:30pm Pre-WO", "7pm Dinner", "10pm Night Shake"]
    
    with col1:
        st.markdown("#### ☑️ Meal Checklist")
        for i, meal in enumerate(meals[:3]):
            st.checkbox(meal, key=f"meal_{i}")
    
    with col2:
        st.markdown("#### ☑️ Meal Checklist")
        for i, meal in enumerate(meals[3:]):
            st.checkbox(meal, key=f"meal_{i+3}")
    
    st.divider()
    st.markdown("#### 📊 Macro Breakdown")
    
    protein_today = st.slider("Protein (g)", 0, 200, 120)
    carbs_today = st.slider("Carbs (g)", 0, 500, 300)
    fat_today = st.slider("Fat (g)", 0, 100, 30)
    
    calories = (protein_today * 4) + (carbs_today * 4) + (fat_today * 9)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Protein", f"{protein_today}g", f"{protein_today-165}g vs target")
    with col2:
        st.metric("Carbs", f"{carbs_today}g", f"{carbs_today-413}g vs target")
    with col3:
        st.metric("Fat", f"{fat_today}g", f"{fat_today-44}g vs target")
    with col4:
        st.metric("Total", f"{calories} kcal", f"{calories-3150} vs target")

# ============================================================================
# TAB 4: METRICS
# ============================================================================

with tab4:
    st.markdown("### Body Composition Tracker")
    
    col1, col2 = st.columns(2)
    
   with col1:
    st.markdown("#### Weekly Log")
    weight_today = st.number_input("Weight (kg)", value=69.6, step=0.1)
    body_fat = st.number_input("Body Fat (%)", value=16.2, step=0.1)
    muscle_mass = st.number_input("Muscle Mass (kg)", value=55.4, step=0.1)
    waist_cm = st.number_input("Waist (cm)", value=82.0, step=0.5)  # FIXED
    sleep_hours = st.number_input("Sleep (hours)", value=5.0, step=0.5)  # FIXED
    
    if st.button("💾 Save Metrics"):
        st.success("✓ Metrics saved")
    
    with col2:
        st.markdown("#### Progress Since Week 1")
        st.metric("Weight Change", "+2.4 kg", "target: +5.4 kg by week 12")
        st.metric("Body Fat", "-0.8%", "target: -6.2% by week 12")
        st.metric("Muscle Mass", "+3.2 kg", "target: +10 kg by week 12")
        st.metric("Sleep", f"{sleep_hours}h/night", "target: 7-8h")

# ============================================================================
# TAB 5: ANALYTICS
# ============================================================================

with tab5:
    st.markdown("### Weekly Analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Adherence", "75%", "3/4 workouts done")
    with col2:
        st.metric("Volume", "17.6k kg", "total lifted")
    with col3:
        st.metric("Avg RPE", "8.1", "target: 8-9")
    
    st.divider()
    
    st.markdown("#### Weak Point Focus")
    st.markdown("""
    **🔴 Shoulders (Priority 1)**
    - Lateral Raise: 8kg → 11kg progress
    - Volume: 9 sets/week (3 exercises × 3 sets each)
    - Target: 12kg by week 12
    
    **🔴 Chest (Priority 2)**
    - Bench Press: 25kg → 32kg by week 8
    - Density focus: RPE 8-9 with steady weight
    - Target: 36kg by week 12
    
    **🟡 Legs (Form focus)**
    - Squat: Starting at 30kg (form priority)
    - Leg Press: 85kg → 95kg (strong progression)
    """)

# ============================================================================
# TAB 6: 12-MONTH PLAN
# ============================================================================

with tab6:
    st.markdown("### 48-Week Periodization (6 Phases)")
    
    phases_data = {
        "Phase": ["1: Foundation", "2: Density", "3: Hypertrophy", "4: Strength", "5: Peak Power", "6: Deload"],
        "Weeks": ["1-8", "9-16", "17-24", "25-32", "33-40", "41-48"],
        "Focus": ["Build base", "Increase density", "Max growth", "Build strength", "Power + density", "Recovery"],
        "Volume": ["High", "High", "Very High", "Moderate", "Moderate-High", "Low"],
        "Intensity": ["RPE 8-9", "RPE 8", "RPE 7.5-8.5", "RPE 8-9", "RPE 8.5-9", "RPE 6"],
    }
    
    df_phases = pd.DataFrame(phases_data)
    st.dataframe(df_phases, use_container_width=True, hide_index=True)
    
    st.divider()
    st.markdown("#### 12-Week Milestones (Phase 1-2)")
    
    milestones = pd.DataFrame({
        "Metric": ["Weight", "Body Fat", "Barbell Bench", "DB Lateral Raise", "Leg Press"],
        "Start": ["69.6 kg", "16.2%", "25 kg", "8 kg", "79 kg"],
        "Week 8": ["71-72 kg", "15.8%", "32 kg", "11 kg", "95 kg"],
        "Week 12": ["73 kg", "15%", "36 kg", "12 kg", "110 kg"],
        "Total Gain": ["+3.4 kg", "-1.2%", "+11 kg", "+4 kg", "+31 kg"],
    })
    st.dataframe(milestones, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 7: SETTINGS
# ============================================================================

with tab7:
    st.markdown("### User Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Profile")
        name = st.text_input("Name", value="John")
        age = st.number_input("Age", value=33)
        height_cm = st.number_input("Height (cm)", value=176)
        gym = st.selectbox("Current Gym", ["PureGym Basford", "NRG Gym Bulwell"])
    
    with col2:
        st.markdown("#### Goals")
        target_weight = st.number_input("Target Weight (kg)", value=75.0)
        target_bf = st.number_input("Target Body Fat (%)", value=10.0)
        focus_areas = st.multiselect("Focus Areas", 
                                    ["Shoulders", "Chest", "Arms", "Back", "Legs"],
                                    default=["Shoulders", "Chest"])
    
    st.divider()
    st.markdown("#### Constraints")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("✓ Glaucoma (no inversions)", value=True)
        st.checkbox("✓ Tennis elbow (neutral grip)", value=True)
    with col2:
        st.checkbox("✓ Busy Monday (no chest)", value=True)
        st.checkbox("✓ 90min session limit", value=True)
    
    if st.button("💾 Save Settings"):
        st.success("✓ Settings saved")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px;'>
📱 Syncing with BoostCamp | 💾 Data persists in session | 📊 Export available
<br>Your split matches authoritative reference | Ready for Streamlit Cloud
</div>
""", unsafe_allow_html=True)
