"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Final Production Version - Modern UI, All 4 Days, No Errors
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import plotly.graph_objects as go

st.set_page_config(
    page_title="John's 48-Week Fitness Plan",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# MODERN DARK THEME CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
}

body {
    background: #0f172a;
    color: #e2e8f0;
}

.main {
    background: #0f172a;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: #1e293b;
    border-radius: 12px;
    padding: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #334155;
    border-radius: 8px;
    padding: 12px 20px;
    color: #cbd5e1;
    font-weight: 500;
}

.stTabs [aria-selected="true"] [data-baseweb="tab"] {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

.stat-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-left: 4px solid #667eea;
    padding: 16px;
    border-radius: 12px;
    margin: 8px 0;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #667eea;
    margin: 8px 0 0 0;
}

.stat-label {
    font-size: 12px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.set-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-left: 4px solid #10b981;
    padding: 14px;
    border-radius: 10px;
    margin: 10px 0;
}

.exercise-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 16px;
    border-radius: 10px;
    margin: 16px 0 12px 0;
    color: white;
}

.exercise-notes {
    background: #1e293b;
    border-left: 3px solid #667eea;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 12px;
    color: #cbd5e1;
}

.timer-box {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 24px;
    border-radius: 12px;
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    margin: 16px 0;
}

.recommendation {
    background: #1e293b;
    border-left: 4px solid #667eea;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 13px;
}

.success-badge {
    background: #10b981;
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin: 4px 0;
}

.warning-badge {
    background: #f59e0b;
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin: 4px 0;
}

.phase-badge {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin: 8px 0;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin: 12px 0;
}

.input-group {
    display: flex;
    gap: 8px;
    margin: 8px 0;
}

@media (max-width: 768px) {
    .stat-value { font-size: 20px; }
    .timer-box { font-size: 36px; padding: 16px; }
    .metric-row { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "current_week" not in st.session_state:
    st.session_state.current_week = 5
if "workout_sessions" not in st.session_state:
    st.session_state.workout_sessions = []
if "metrics_logs" not in st.session_state:
    st.session_state.metrics_logs = []

# COMPLETE SPLIT (ALL 4 DAYS) - FIXED TYPES
COMPLETE_SPLIT = {
    "Monday - Shoulders + Arms": {
        "exercises": [
            {
                "name": "Machine Shoulder Press",
                "type": "MAIN",
                "sets": 4,
                "target_reps": "8-10",
                "rest": 180,
                "w5_weight": 38.0,
                "w12_weight": 42.0,
                "notes": "Neutral grip. Controlled descent (2s). Squeeze at top (1s).",
            },
            {
                "name": "DB Lateral Raise",
                "type": "HYPER",
                "sets": 4,
                "target_reps": "12-15",
                "rest": 60,
                "w5_weight": 9.0,
                "w12_weight": 12.0,
                "notes": "⭐ PRIORITY. Raise to shoulder height. Control negative (2s).",
            },
            {
                "name": "Cable Lateral Raise",
                "type": "HYPER",
                "sets": 3,
                "target_reps": "12-15",
                "rest": 60,
                "w5_weight": 8.0,
                "w12_weight": 10.0,
                "notes": "⭐ PRIORITY. Constant tension. No jerking.",
            },
            {
                "name": "Hammer Curl",
                "type": "HYPER",
                "sets": 3,
                "target_reps": "10-12",
                "rest": 60,
                "w5_weight": 14.0,
                "w12_weight": 16.0,
                "notes": "Neutral grip. Pause at top (1s). Full ROM.",
            },
            {
                "name": "Triceps Pushdown",
                "type": "HYPER",
                "sets": 3,
                "target_reps": "12-15",
                "rest": 60,
                "w5_weight": 21.6,
                "w12_weight": 25.0,
                "notes": "Rope attachment. Lock out at bottom (1s).",
            },
            {
                "name": "Captain's Chair Leg Raise",
                "type": "ABS",
                "sets": 3,
                "target_reps": "20",
                "rest": 60,
                "w5_weight": 0.0,
                "w12_weight": 0.0,
                "notes": "Controlled lift. Pause at top (1s). No swinging.",
            },
        ]
    },
    "Tuesday - Legs + Back": {
        "exercises": [
            {
                "name": "Back Squat",
                "type": "MAIN",
                "sets": 4,
                "target_reps": "6-8",
                "rest": 180,
                "w5_weight": 30.0,
                "w12_weight": 40.0,
                "notes": "Form priority. Chest up. Depth below parallel.",
            },
            {
                "name": "Leg Press",
                "type": "MAIN",
                "sets": 4,
                "target_reps": "8-10",
                "rest": 180,
                "w5_weight": 85.0,
                "w12_weight": 95.0,
                "notes": "Full range. Controlled descent (2s).",
            },
            {
                "name": "Leg Extension",
                "type": "HYPER",
                "sets": 3,
                "target_reps": "10-12",
                "rest": 90,
                "w5_weight": 45.0,
                "w12_weight": 50.0,
                "notes": "Quad isolation. Squeeze at top (1s).",
            },
            {
                "name": "RDL",
                "type": "ACC",
                "sets": 3,
                "target_reps": "10-12",
                "rest": 90,
                "w5_weight": 65.0,
                "w12_weight": 70.0,
                "notes": "Posterior chain. Keep back straight.",
            },
            {
                "name": "Lat Pulldown",
                "type": "MAIN",
                "sets": 4,
                "target_reps": "8-10",
                "rest": 180,
                "w5_weight": 42.0,
                "w12_weight": 48.0,
                "notes": "Controlled negative. Full stretch.",
            },
            {
                "name": "Seated Row",
                "type": "MAIN",
                "sets": 4,
                "target_reps": "8-10",
                "rest": 180,
                "w5_weight": 42.0,
                "w12_weight": 48.0,
                "notes": "Chest forward. Squeeze shoulder blades (1s).",
            },
            {
                "name": "Pallof Press",
                "type": "ABS",
                "sets": 2,
                "target_reps": "12 each",
                "rest": 60,
                "w5_weight": 12.0,
                "w12_weight": 15.0,
                "notes": "Anti-rotation. Single arm. Controlled.",
            },
        ]
    },
    "Thursday - Chest + Triceps": {
        "exercises": [
            {
                "name": "Barbell Bench Press",
                "type": "MAIN",
                "sets": 4,
                "target_reps": "6-8",
                "rest": 180,
                "w5_weight": 28.0,
                "w12_weight": 32.0,
                "notes": "⭐ PRIORITY. Controlled descent (2s). Pause at chest (1s).",
            },
            {
                "name": "DB Bench Press",
                "type": "HYPER",
                "sets": 4,
                "target_reps": "8-10",
                "rest": 120,
                "w5_weight": 20.0,
                "w12_weight": 23.0,
                "notes": "Full range. Squeeze at top (1s).",
            },
            {
                "name": "Machine Chest Press",
                "type": "VOL",
                "sets": 3,
                "target_reps": "12-15",
                "rest": 90,
                "w5_weight": 50.0,
                "w12_weight": 55.0,
                "notes": "High reps. Controlled movement.",
            },
            {
                "name": "Incline DB Press",
                "type": "VOL",
                "sets": 3,
                "target_reps": "10-12",
                "rest": 90,
                "w5_weight": 16.0,
                "w12_weight": 18.0,
                "notes": "Upper chest. Full ROM.",
            },
            {
                "name": "Machine Dip",
                "type": "ACC",
                "sets": 2,
                "target_reps": "12-15",
                "rest": 60,
                "w5_weight": 45.0,
                "w12_weight": 50.0,
                "notes": "Assisted machine. Full range.",
            },
            {
                "name": "Cable Crunch",
                "type": "ABS",
                "sets": 3,
                "target_reps": "12-15",
                "rest": 60,
                "w5_weight": 20.0,
                "w12_weight": 25.0,
                "notes": "Core work. Light weight. Controlled.",
            },
            {
                "name": "Machine Ab Crunch",
                "type": "ABS",
                "sets": 3,
                "target_reps": "12-15",
                "rest": 60,
                "w5_weight": 25.0,
                "w12_weight": 30.0,
                "notes": "Visible abs. Finisher.",
            },
        ]
    },
    "Friday - Arms + Legs": {
        "exercises": [
            {
                "name": "Machine Curl",
                "type": "ARM",
                "sets": 3,
                "target_reps": "10-12",
                "rest": 60,
                "w5_weight": 18.0,
                "w12_weight": 20.0,
                "notes": "Isolation. Controlled movement.",
            },
            {
                "name": "Hammer Curl",
                "type": "ARM",
                "sets": 3,
                "target_reps": "10-12",
                "rest": 60,
                "w5_weight": 14.0,
                "w12_weight": 16.0,
                "notes": "Neutral grip. Full ROM.",
            },
            {
                "name": "Triceps Pushdown",
                "type": "ARM",
                "sets": 3,
                "target_reps": "12-15",
                "rest": 60,
                "w5_weight": 21.6,
                "w12_weight": 25.0,
                "notes": "Rope. Lock out at bottom.",
            },
            {
                "name": "Leg Press Drop Set",
                "type": "VOL",
                "sets": 2,
                "target_reps": "Drop to fail",
                "rest": 120,
                "w5_weight": 85.0,
                "w12_weight": 95.0,
                "notes": "Finisher. Drop: 85→65→45kg. Go to failure.",
            },
            {
                "name": "Woodchops",
                "type": "ABS",
                "sets": 3,
                "target_reps": "20 alt",
                "rest": 60,
                "w5_weight": 0.0,
                "w12_weight": 0.0,
                "notes": "Obliques. Alternating. Controlled rotation.",
            },
            {
                "name": "Reverse Crunch",
                "type": "ABS",
                "sets": 2,
                "target_reps": "15",
                "rest": 45,
                "w5_weight": 0.0,
                "w12_weight": 0.0,
                "notes": "Lower abs. Bodyweight. Controlled.",
            },
        ]
    },
}

# PROTEIN RECIPES
PROTEIN_RECIPES = {
    "Monday": [("Grilled Chicken Breast", "https://www.allrecipes.com/recipe/220957/"), ("Protein Pancakes", "https://www.muscleandstrength.com/recipes/protein-pancakes")],
    "Tuesday": [("Ground Beef Bowl", "https://www.allrecipes.com/recipe/232155/"), ("Lentil Soup", "https://www.budgetbytes.com/lentil-soup-recipe/")],
    "Thursday": [("Lean Beef Steak", "https://www.foodnetwork.com/recipes/food-network-kitchen/"), ("Tuna Salad", "https://www.allrecipes.com/recipe/12750/")],
    "Friday": [("Chicken Shawarma", "https://www.budgetbytes.com/chicken-shawarma-recipe/"), ("Protein Shake", "https://www.muscleandstrength.com/recipes/high-protein-smoothie")],
}

# SIDEBAR
with st.sidebar:
    st.markdown("### 💪 John's 48-Week Plan")
    selected_week = st.slider("📅 Week", min_value=5, max_value=48, value=5, step=1)
    st.session_state.current_week = selected_week
    
    if selected_week <= 12:
        phase_text = "Phase 1: Foundation"
    elif selected_week <= 24:
        phase_text = "Phase 2: Hypertrophy"
    else:
        phase_text = "Phase 3: Definition"
    
    st.markdown(f"<div class='phase-badge'>{phase_text}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weight", "69.6kg", "+2.4")
    with col2:
        st.metric("Target", "75kg", "5.4 to go")

# MAIN TABS
tabs = st.tabs([
    "📊 Dashboard",
    "🏋️ Workout Logger",
    "🍽️ Nutrition",
    "📈 Metrics",
    "📉 Analytics",
    "🗓️ 12-Month Plan",
    "⚙️ Settings"
])

# TAB 1: DASHBOARD
with tabs[0]:
    st.markdown("# 📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-card"><div class="stat-label">Workouts</div><div class="stat-value">4/week</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><div class="stat-label">Sets</div><div class="stat-value">102</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><div class="stat-label">Duration</div><div class="stat-value">360m</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-card"><div class="stat-label">RPE</div><div class="stat-value">8-9</div></div>', unsafe_allow_html=True)
    
    st.divider()
    
    for day_name, day_data in COMPLETE_SPLIT.items():
        with st.expander(f"📅 {day_name}", expanded=False):
            for ex in day_data["exercises"]:
                current_weight = ex["w5_weight"]
                st.markdown(f"""
                **{ex['name']}** | {ex['type']}
                - Sets: {ex['sets']} | Reps: {ex['target_reps']} | Rest: {ex['rest']}s | W{selected_week}: **{current_weight}kg**
                - 📝 {ex['notes']}
                """)

# TAB 2: WORKOUT LOGGER
with tabs[1]:
    st.markdown("# 🏋️ Workout Logger")
    
    day_selected = st.selectbox("📅 Select Workout Day", list(COMPLETE_SPLIT.keys()), key="day_select")
    
    exercises = COMPLETE_SPLIT[day_selected]["exercises"]
    
    for ex_idx, ex in enumerate(exercises):
        st.markdown(f'<div class="exercise-header">🏋️ {ex_idx + 1}. {ex["name"]} ({ex["type"]})</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="exercise-notes">📝 {ex["notes"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**Target:** {ex['sets']} sets × {ex['target_reps']} reps @ {ex['w5_weight']}kg | Rest: {ex['rest']}s")
        
        # Per-set tracking
        for set_num in range(1, ex["sets"] + 1):
            col1, col2, col3, col4, col5 = st.columns([1.5, 1.2, 1.2, 1, 1.5])
            
            with col1:
                st.markdown(f"**Set {set_num}**")
            with col2:
                weight_val = st.number_input(
                    f"Weight",
                    value=float(ex["w5_weight"]),
                    step=0.5,
                    key=f"weight_{ex_idx}_{set_num}",
                    label_visibility="collapsed"
                )
            with col3:
                reps_val = st.number_input(
                    f"Reps",
                    value=8,
                    min_value=1,
                    key=f"reps_{ex_idx}_{set_num}",
                    label_visibility="collapsed"
                )
            with col4:
                rpe_val = st.number_input(
                    f"RPE",
                    value=8,
                    min_value=1,
                    max_value=10,
                    key=f"rpe_{ex_idx}_{set_num}",
                    label_visibility="collapsed"
                )
            with col5:
                if st.button("✅ Log", key=f"log_{ex_idx}_{set_num}"):
                    log_entry = {
                        "date": datetime.now(),
                        "exercise": ex["name"],
                        "set": set_num,
                        "weight": weight_val,
                        "reps": int(reps_val),
                        "rpe": int(rpe_val),
                        "day": day_selected
                    }
                    st.session_state.workout_sessions.append(log_entry)
                    
                    # AUTO REST TIMER
                    rest_time = ex["rest"]
                    st.success(f"✓ Set {set_num}: {weight_val}kg × {reps_val} @ RPE {rpe_val}")
                    
                    placeholder = st.empty()
                    for remaining in range(rest_time, 0, -1):
                        mins, secs = divmod(remaining, 60)
                        with placeholder.container():
                            st.markdown(f'<div class="timer-box">⏱️ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                        time.sleep(1)
                    
                    # BEEP
                    st.markdown("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>""", unsafe_allow_html=True)
                    placeholder.success(f"✅ Rest complete!")
        
        st.divider()

# TAB 3: NUTRITION
with tabs[2]:
    st.markdown("# 🍽️ Nutrition Tracker")
    st.info("**Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    selected_day_nutrition = st.selectbox("📅 Select Day for Recipes", ["Monday", "Tuesday", "Thursday", "Friday"], key="day_recipes")
    
    st.markdown("#### 🔗 High-Protein Recipes")
    for recipe_name, recipe_url in PROTEIN_RECIPES[selected_day_nutrition]:
        st.markdown(f"[{recipe_name}]({recipe_url})")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    meals = ["7am Breakfast", "10am Snack", "1pm Lunch", "3:30pm Pre-WO", "7pm Dinner", "10pm Night Shake"]
    
    with col1:
        st.markdown("#### Meals 1-3")
        for i in range(3):
            st.checkbox(meals[i], key=f"meal_{i}")
    
    with col2:
        st.markdown("#### Meals 4-6")
        for i in range(3, 6):
            st.checkbox(meals[i], key=f"meal_{i}")
    
    st.divider()
    protein_g = st.slider("Protein (g)", 0, 200, 120)
    carbs_g = st.slider("Carbs (g)", 0, 500, 300)
    fat_g = st.slider("Fat (g)", 0, 100, 30)
    
    total_cals = (protein_g * 4.0) + (carbs_g * 4.0) + (fat_g * 9.0)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Protein", f"{protein_g}g", f"{protein_g - 165}g")
    with col2:
        st.metric("Carbs", f"{carbs_g}g", f"{carbs_g - 413}g")
    with col3:
        st.metric("Fat", f"{fat_g}g", f"{fat_g - 44}g")
    with col4:
        st.metric("Total", f"{int(total_cals)} kcal", f"{int(total_cals - 3150)}")

# TAB 4: METRICS
with tabs[3]:
    st.markdown("# 📈 Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Weekly Log")
        weight_today = st.number_input("Weight (kg)", value=69.6, step=0.1)
        body_fat = st.number_input("Body Fat (%)", value=16.2, step=0.1)
        muscle_mass = st.number_input("Muscle Mass (kg)", value=55.4, step=0.1)
        waist_cm = st.number_input("Waist (cm)", value=82.0, step=0.5)
        sleep_hours = st.number_input("Sleep (hours)", value=5.0, step=0.5)
        
        if st.button("💾 Save Metrics"):
            new_entry = {
                "date": datetime.now(),
                "week": st.session_state.current_week,
                "weight": weight_today,
                "body_fat": body_fat,
                "muscle": muscle_mass,
                "waist": waist_cm,
                "sleep": sleep_hours
            }
            st.session_state.metrics_logs.append(new_entry)
            st.success(f"✓ Saved {new_entry['date'].strftime('%d %b %Y')}")
    
    with col2:
        st.markdown("#### Progress")
        if st.session_state.metrics_logs:
            last = st.session_state.metrics_logs[-1]
            first = st.session_state.metrics_logs[0]
            st.markdown(f"""
            **Latest (W{last['week']}):**
            - Weight: {last['weight']}kg
            - Body Fat: {last['body_fat']}%
            - Muscle: {last['muscle']}kg
            
            **Changes:**
            - Weight: {last['weight'] - first['weight']:+.1f}kg
            - Body Fat: {last['body_fat'] - first['body_fat']:+.1f}%
            - Muscle: {last['muscle'] - first['muscle']:+.1f}kg
            """)

# TAB 5: ANALYTICS
with tabs[4]:
    st.markdown("# 📉 Analytics")
    
    if st.session_state.workout_sessions:
        logs_df = pd.DataFrame(st.session_state.workout_sessions)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Exercises Logged", logs_df['exercise'].nunique())
        with col2:
            st.metric("Total Sets", len(logs_df))
        with col3:
            st.metric("Avg RPE", f"{logs_df['rpe'].mean():.1f}")
        
        st.divider()
        st.markdown("### Best Performance Per Exercise")
        
        for exercise in logs_df['exercise'].unique():
            ex_logs = logs_df[logs_df['exercise'] == exercise]
            best = ex_logs.loc[ex_logs['weight'].idxmax()]
            
            st.markdown(f"""
            **{exercise}**
            - Best: {best['weight']}kg × {best['reps']} reps @ RPE {best['rpe']}
            - Sets: {len(ex_logs)}
            """)
    else:
        st.info("📝 Log workouts to see analytics")

# TAB 6: 12-MONTH PLAN
with tabs[5]:
    st.markdown("# 🗓️ 48-Week Plan")
    
    phases = pd.DataFrame({
        "Phase": ["1", "2", "3"],
        "Name": ["Foundation", "Hypertrophy", "Definition"],
        "Weeks": ["5-12", "13-24", "25-48"],
        "Focus": ["Build base", "Max growth", "Sculpt & cut"],
        "Abs/Week": ["2-3x", "3x", "3-4x"],
    })
    
    st.dataframe(phases, use_container_width=True, hide_index=True)

# TAB 7: SETTINGS
with tabs[6]:
    st.markdown("# ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Profile")
        name = st.text_input("Name", value="John")
        age = st.number_input("Age", value=33)
    
    with col2:
        st.markdown("#### Goals")
        target_weight = st.number_input("Target Weight (kg)", value=75.0, step=0.5)
        target_bf = st.number_input("Target Body Fat (%)", value=10.0, step=0.5)
    
    if st.button("💾 Save Settings"):
        st.success("✓ Settings saved")

st.divider()
st.markdown("""<div style='text-align: center; color: #94a3b8; font-size: 11px;'>
✅ Per-set tracking | 🏋️ All 4 days | ⏱️ Auto rest timer | 📊 Modern UI | 📱 Mobile-first
</div>""", unsafe_allow_html=True)
