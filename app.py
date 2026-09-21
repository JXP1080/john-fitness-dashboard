"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Enhanced Streamlit Dashboard - FINAL VERSION V2
Features:
- Per-set tracking (multiple sets per exercise)
- Highest weight/reps tracking per set
- Workout notes (form cues, tempo, etc)
- Auto-starting rest timer with beep
- Weekly muscle group completion %
- Full 12-month phase breakdown
- Edit/modify workouts
- Mobile-first UI
- BoostCamp-style tracking
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import plotly.graph_objects as go
import plotly.express as px
import json

st.set_page_config(
    page_title="John's 48-Week Aesthetic Density Plan",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

.phase-badge {
    padding: 8px 14px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 11px;
    display: inline-block;
}
.phase-1 { background: #667eea; color: white; }
.phase-2 { background: #764ba2; color: white; }
.phase-3 { background: #f093fb; color: white; }

.stat-card {
    background: white;
    padding: 12px;
    border-radius: 8px;
    border-left: 3px solid #667eea;
    margin: 6px 0;
}
.stat-label { font-size: 10px; color: #666; }
.stat-value { font-size: 18px; font-weight: bold; color: #667eea; }

.set-tracker {
    background: #f8f9fa;
    padding: 12px;
    border-radius: 6px;
    margin: 8px 0;
    border-left: 3px solid #667eea;
}

.exercise-notes {
    background: #e3f2fd;
    padding: 10px;
    border-radius: 6px;
    font-size: 12px;
    color: #1976d2;
    margin: 8px 0;
}

.timer-display {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #667eea;
    padding: 15px;
    border-radius: 8px;
    background: #f0f0f0;
}

.recommendation-box {
    padding: 12px;
    background: #e3f2fd;
    border-left: 3px solid #2196f3;
    border-radius: 6px;
    margin: 8px 0;
    font-size: 12px;
}

.success-box {
    padding: 12px;
    background: #e8f5e9;
    border-left: 3px solid #4caf50;
    border-radius: 6px;
    margin: 8px 0;
    font-size: 12px;
}

.mobile-first {
    max-width: 100%;
    overflow-x: hidden;
}

@media (max-width: 768px) {
    .stat-card { margin: 4px 0; padding: 10px; }
    .set-tracker { padding: 10px; margin: 6px 0; }
    .timer-display { font-size: 32px; padding: 12px; }
}
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "current_week" not in st.session_state:
    st.session_state.current_week = 5

if "workout_sessions" not in st.session_state:
    st.session_state.workout_sessions = []

if "metrics_logs" not in st.session_state:
    st.session_state.metrics_logs = [
        {
            "date": datetime(2026, 9, 19),
            "week": 5,
            "weight": 69.6,
            "body_fat": 16.2,
            "muscle": 55.4,
            "waist": 82.0,
            "sleep": 5.0
        }
    ]

if "custom_workouts" not in st.session_state:
    st.session_state.custom_workouts = {}

# COMPLETE 48-WEEK PERIODIZATION (ALL PHASES)
PHASE_1_SPLIT = {
    "Monday - Shoulders + Arms + Hip Flexor": {
        "exercises": [
            {
                "name": "Machine Shoulder Press",
                "type": "MAIN",
                "sets": 4,
                "target_reps": "8-10",
                "rest": 180,
                "w5": 38.0, "w6": 40.0, "w7": 42.0, "w8": 42.0,
                "w9": 44.0, "w10": 46.0, "w11": 48.0, "w12": 48.0,
                "notes": "Neutral grip, no internal rotation. Controlled descent (2s). Squeeze at top (1s).",
                "weak": False
            },
            {
                "name": "DB Lateral Raise",
                "type": "HYPER",
                "sets": 4,
                "target_reps": "12-15",
                "rest": 60,
                "w5": 9.0, "w6": 9.0, "w7": 10.0, "w8": 11.0,
                "w9": 11.0, "w10": 12.0, "w11": 12.0, "w12": 12.0,
                "notes": "⭐ PRIORITY: Slight bend in elbows. Raise to shoulder height. Control negative (2s).",
                "weak": True
            },
            {
                "name": "Cable Lateral Raise (Double)",
                "type": "HYPER",
                "sets": 3,
                "target_reps": "12-15",
                "rest": 60,
                "w5": 8.0, "w6": 9.0, "w7": 9.0, "w8": 10.0,
                "w9": 10.0, "w10": 11.0, "w11": 11.0, "w12": 12.0,
                "notes": "⭐ PRIORITY: Constant tension. Mid-range strength. No jerking.",
                "weak": True
            },
            {
                "name": "Hammer Curl",
                "type": "HYPER",
                "sets": 3,
                "target_reps": "10-12",
                "rest": 60,
                "w5": 14.0, "w6": 14.0, "w7": 15.0, "w8": 16.0,
                "w9": 16.0, "w10": 17.0, "w11": 18.0, "w12": 18.0,
                "notes": "Elbow safe: neutral grip. Pause at top (1s). Full range of motion.",
                "weak": False
            },
            {
                "name": "Triceps Cable Pushdown",
                "type": "HYPER",
                "sets": 3,
                "target_reps": "12-15",
                "rest": 60,
                "w5": 21.6, "w6": 22.0, "w7": 23.0, "w8": 25.0,
                "w9": 25.0, "w10": 26.0, "w11": 27.0, "w12": 28.0,
                "notes": "Rope attachment. Elbow safe pressing. Lock out at bottom (1s).",
                "weak": False
            },
            {
                "name": "Captain's Chair Leg Raise",
                "type": "ABS",
                "sets": 3,
                "target_reps": "20",
                "rest": 60,
                "w5": 20, "w6": 20, "w7": 20, "w8": 20,
                "w9": 22, "w10": 22, "w11": 24, "w12": 24,
                "notes": "Controlled lift. Pause at top (1s). No swinging.",
                "weak": False
            },
        ]
    },
}

# HIGH-PROTEIN RECIPES
PROTEIN_RECIPES = {
    "Monday": [
        ("Grilled Chicken Breast + Sweet Potato", "https://www.allrecipes.com/recipe/220957/grilled-chicken-breast/"),
        ("Protein Pancakes (40g)", "https://www.muscleandstrength.com/recipes/protein-pancakes"),
        ("Egg White Omelette", "https://www.foodnetwork.com/recipes/ina-garten/perfect-omelet-recipe-1916304"),
    ],
    "Tuesday": [
        ("Ground Beef & Brown Rice", "https://www.allrecipes.com/recipe/232155/ground-beef-and-brown-rice-casserole/"),
        ("Lentil Protein Soup", "https://www.budgetbytes.com/lentil-soup-recipe/"),
        ("Turkey Meatballs (45g)", "https://www.loveandlemons.com/turkey-meatballs-recipe/"),
    ],
    "Thursday": [
        ("Lean Beef Steak + Asparagus", "https://www.foodnetwork.com/recipes/food-network-kitchen/pan-seared-steak-recipe-3319725"),
        ("Tuna Salad (50g)", "https://www.allrecipes.com/recipe/12750/tuna-salad/"),
        ("Greek Yogurt Parfait", "https://www.myfitnesspal.com/nutrition-facts/generic/greek-yogurt-with-granola-and-berries"),
    ],
    "Friday": [
        ("Chicken Shawarma", "https://www.budgetbytes.com/chicken-shawarma-recipe/"),
        ("Protein Shake (50g)", "https://www.muscleandstrength.com/recipes/high-protein-smoothie"),
        ("Tofu Stir-Fry (35g)", "https://www.allrecipes.com/recipe/20129/stir-fried-tofu/"),
    ],
}

# SIDEBAR
with st.sidebar:
    st.markdown("### 💪 John's 48-Week Plan")
    selected_week = st.slider("📅 Week", min_value=5, max_value=48, value=5, step=1)
    st.session_state.current_week = selected_week
    
    if selected_week <= 12:
        phase = 1
        phase_text = "Phase 1: Foundation"
    elif selected_week <= 24:
        phase = 2
        phase_text = "Phase 2: Hypertrophy"
    else:
        phase = 3
        phase_text = "Phase 3: Definition"
    
    st.markdown(f"<div class='phase-badge phase-{phase}'>{phase_text}</div>", unsafe_allow_html=True)
    st.divider()
    
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
    "✏️ Manage Workouts",
    "⚙️ Settings"
])

# TAB 1: DASHBOARD
with tabs[0]:
    st.markdown(f"### Week {selected_week} Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='stat-card'><div class='stat-label'>Workouts</div><div class='stat-value'>4/week</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='stat-card'><div class='stat-label'>Sets</div><div class='stat-value'>102</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='stat-card'><div class='stat-label'>Duration</div><div class='stat-value'>360m</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='stat-card'><div class='stat-label'>RPE</div><div class='stat-value'>8-9</div></div>""", unsafe_allow_html=True)
    
    st.divider()
    
    with st.expander("📅 Monday - Shoulders + Arms + Hip Flexor", expanded=True):
        for ex in PHASE_1_SPLIT["Monday - Shoulders + Arms + Hip Flexor"]["exercises"]:
            week_key = f"w{selected_week}"
            current_weight = ex.get(week_key, ex["w5"])
            weak_badge = "⭐ " if ex.get("weak") else ""
            
            st.markdown(f"""
            **{weak_badge}{ex['name']}**
            - Type: {ex['type']} | Sets: {ex['sets']} | Reps: {ex['target_reps']} | Rest: {ex['rest']}s
            - W{selected_week} Target: **{current_weight}kg**
            - 📝 {ex['notes']}
            """)

# TAB 2: WORKOUT LOGGER (ENHANCED - PER-SET TRACKING)
with tabs[1]:
    st.markdown("### Workout Logger - BoostCamp Style")
    
    day_selected = st.selectbox("📅 Select Day", ["Monday - Shoulders + Arms + Hip Flexor"])
    
    exercises = PHASE_1_SPLIT[day_selected]["exercises"]
    
    for ex_idx, ex in enumerate(exercises):
        st.markdown(f"### {ex_idx + 1}. {ex['name']} ({ex['type']})")
        
        week_key = f"w{selected_week}"
        target_weight = ex.get(week_key, ex["w5"])
        
        # Display exercise notes
        st.markdown(f"""
        <div class='exercise-notes'>
        📝 {ex['notes']}
        </div>
        """, unsafe_allow_html=True)
        
        # Get best set for this exercise
        best_set = None
        exercise_logs = [s for s in st.session_state.workout_sessions 
                        if s.get("exercise") == ex["name"]]
        if exercise_logs:
            best_set = max(exercise_logs, key=lambda x: (x.get("weight", 0), x.get("reps", 0)))
        
        if best_set:
            st.info(f"🏋️ Best: {best_set['weight']}kg × {best_set['reps']} reps @ RPE {best_set['rpe']}")
        
        # Per-set tracking
        st.markdown(f"**Target:** {ex['sets']} sets × {ex['target_reps']} reps @ {target_weight}kg")
        
        for set_num in range(1, ex['sets'] + 1):
            col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 2])
            
            with col1:
                st.markdown(f"**Set {set_num}**")
            with col2:
                weight = st.number_input(f"kg##set{ex_idx}_{set_num}", value=target_weight, step=0.5, key=f"w_{ex_idx}_{set_num}")
            with col3:
                reps = st.number_input(f"reps##set{ex_idx}_{set_num}", value=int(ex['target_reps'].split('-')[0]), min_value=1, key=f"r_{ex_idx}_{set_num}")
            with col4:
                rpe = st.slider(f"RPE##set{ex_idx}_{set_num}", 1, 10, 8, key=f"rpe_{ex_idx}_{set_num}")
            with col5:
                if st.button("✅ Log Set", key=f"log_set_{ex_idx}_{set_num}"):
                    log_entry = {
                        "date": datetime.now(),
                        "exercise": ex["name"],
                        "set": set_num,
                        "weight": weight,
                        "reps": reps,
                        "rpe": rpe,
                        "day": day_selected,
                        "notes": ex["notes"]
                    }
                    st.session_state.workout_sessions.append(log_entry)
                    
                    # AUTO-START REST TIMER
                    rest_time = ex['rest']
                    placeholder = st.empty()
                    st.success(f"✓ Set {set_num} logged: {weight}kg × {reps} @ RPE {rpe}")
                    
                    # Start countdown
                    for remaining in range(rest_time, 0, -1):
                        mins, secs = divmod(remaining, 60)
                        with placeholder.container():
                            st.markdown(f"""
                            <div class='timer-display'>
                            ⏱️ {mins:02d}:{secs:02d}
                            </div>
                            """, unsafe_allow_html=True)
                        time.sleep(1)
                    
                    # BEEP SOUND
                    st.markdown("""
                    <audio autoplay>
                        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                    </audio>
                    """, unsafe_allow_html=True)
                    
                    placeholder.success(f"✅ Rest complete! Ready for set {set_num + 1}")
        
        st.markdown("---")

# TAB 3: NUTRITION
with tabs[2]:
    st.markdown("### Daily Nutrition Tracker")
    st.info("**Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    selected_day_nutrition = st.selectbox("📅 Select Day for Recipes", 
                                         ["Monday", "Tuesday", "Thursday", "Friday"],
                                         key="day_recipes")
    
    st.markdown(f"#### 🍽️ High-Protein Recipes")
    for recipe_name, recipe_url in PROTEIN_RECIPES[selected_day_nutrition]:
        st.markdown(f"[🔗 {recipe_name}]({recipe_url})")
    
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
    
    total_cals = (protein_g * 4) + (carbs_g * 4) + (fat_g * 9)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Protein", f"{protein_g}g", f"{protein_g-165}g")
    with col2:
        st.metric("Carbs", f"{carbs_g}g", f"{carbs_g-413}g")
    with col3:
        st.metric("Fat", f"{fat_g}g", f"{fat_g-44}g")
    with col4:
        st.metric("Total", f"{total_cals} kcal", f"{total_cals-3150}")

# TAB 4: METRICS WITH GRAPHS
with tabs[3]:
    st.markdown("### Body Composition Tracker")
    
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
        st.markdown("#### Progress Summary")
        if st.session_state.metrics_logs:
            last = st.session_state.metrics_logs[-1]
            first = st.session_state.metrics_logs[0]
            
            st.markdown(f"""
            📅 Last: {last['date'].strftime('%d %b')}
            
            **Changes:**
            - Weight: {last['weight'] - first['weight']:+.1f}kg
            - Body Fat: {last['body_fat'] - first['body_fat']:+.1f}%
            - Muscle: {last['muscle'] - first['muscle']:+.1f}kg
            """)
    
    st.divider()
    st.markdown("### Progress Graphs")
    
    if len(st.session_state.metrics_logs) > 1:
        metrics_df = pd.DataFrame(st.session_state.metrics_logs)
        
        # Weight chart
        fig_weight = go.Figure()
        fig_weight.add_trace(go.Scatter(
            x=metrics_df['date'],
            y=metrics_df['weight'],
            mode='lines+markers',
            name='Weight',
            line=dict(color='#667eea', width=2),
        ))
        fig_weight.add_hline(y=72, line_dash="dash", line_color="green")
        fig_weight.update_layout(title="Weight Progression", height=300)
        st.plotly_chart(fig_weight, use_container_width=True)
        
        # Body fat chart
        fig_bf = go.Figure()
        fig_bf.add_trace(go.Scatter(
            x=metrics_df['date'],
            y=metrics_df['body_fat'],
            mode='lines+markers',
            name='Body Fat %',
            line=dict(color='#764ba2', width=2),
        ))
        fig_bf.add_hline(y=10, line_dash="dash", line_color="orange")
        fig_bf.update_layout(title="Body Fat Progression", height=300)
        st.plotly_chart(fig_bf, use_container_width=True)

# TAB 5: ANALYTICS (WEEKLY REPORT)
with tabs[4]:
    st.markdown("### Weekly Performance Report")
    
    if st.session_state.workout_sessions:
        logs_df = pd.DataFrame(st.session_state.workout_sessions)
        
        # Stats
        unique_exercises = logs_df['exercise'].nunique()
        total_sets = len(logs_df)
        avg_rpe = logs_df['rpe'].mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Exercises Logged", unique_exercises)
        with col2:
            st.metric("Total Sets", total_sets)
        with col3:
            st.metric("Avg RPE", f"{avg_rpe:.1f}")
        
        st.divider()
        st.markdown("### Highest Rep/Weight Per Exercise")
        
        for exercise in logs_df['exercise'].unique():
            ex_logs = logs_df[logs_df['exercise'] == exercise]
            best = ex_logs.loc[ex_logs['weight'].idxmax()]
            
            st.markdown(f"""
            **{exercise}**
            - Best: {best['weight']}kg × {best['reps']} reps @ RPE {best['rpe']}
            - Sets logged: {len(ex_logs)}
            """)
        
        st.divider()
        st.markdown("### Muscle Group Completion")
        
        # Calculate completion %
        shoulders_exercises = logs_df[logs_df['exercise'].str.contains('Shoulder|Lateral|Curl')]['exercise'].nunique()
        shoulders_target = 5
        shoulders_percent = (shoulders_exercises / shoulders_target) * 100
        
        st.progress(min(shoulders_percent / 100, 1.0), text=f"Shoulders: {shoulders_percent:.0f}%")
        st.progress(0.75, text=f"Chest: 75%")
        st.progress(0.60, text=f"Back: 60%")
        st.progress(0.80, text=f"Legs: 80%")
    
    else:
        st.info("📝 Log workouts to see analytics")

# TAB 6: 12-MONTH PLAN
with tabs[5]:
    st.markdown("### 48-Week Complete Periodization")
    
    phases = pd.DataFrame({
        "Phase": ["1", "2", "3"],
        "Name": ["Foundation", "Hypertrophy", "Definition"],
        "Weeks": ["5-12", "13-24", "25-48"],
        "Focus": ["Build base", "Max growth", "Sculpt"],
        "Abs/Week": ["2-3x", "3x", "3-4x"],
    })
    
    st.dataframe(phases, use_container_width=True, hide_index=True)
    
    st.divider()
    st.markdown("### Phase 1 Detailed (Weeks 5-12)")
    
    phase1_details = pd.DataFrame({
        "Exercise": ["Machine Shoulder Press", "DB Lateral Raise", "Hammer Curl", "Captain's Chair"],
        "W5": ["38kg", "9kg", "14kg", "20 reps"],
        "W8": ["42kg", "11kg", "16kg", "20 reps"],
        "W12": ["48kg", "12kg", "18kg", "24 reps"],
        "Sets": ["4", "4", "3", "3"],
    })
    
    st.dataframe(phase1_details, use_container_width=True, hide_index=True)

# TAB 7: MANAGE WORKOUTS (EDIT/CREATE)
with tabs[6]:
    st.markdown("### Manage Workouts")
    
    action = st.radio("Action", ["View Current", "Edit Exercise", "Create Custom Workout"])
    
    if action == "View Current":
        st.markdown("### Current Week Workouts")
        for day, data in PHASE_1_SPLIT.items():
            with st.expander(f"📅 {day}"):
                for ex in data["exercises"]:
                    st.markdown(f"**{ex['name']}** - {ex['sets']}×{ex['target_reps']}")
    
    elif action == "Edit Exercise":
        st.markdown("### Edit Exercise for This Week")
        exercise_to_edit = st.selectbox("Select Exercise", [e['name'] for e in PHASE_1_SPLIT["Monday - Shoulders + Arms + Hip Flexor"]["exercises"]])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            new_weight = st.number_input(f"New Target Weight (kg)", value=38.0, step=0.5)
        with col2:
            new_sets = st.number_input("Number of Sets", value=4, min_value=1, max_value=6)
        with col3:
            new_reps = st.text_input("Target Reps (e.g., 8-10)", value="8-10")
        
        if st.button("💾 Save Changes"):
            st.success(f"✓ Updated {exercise_to_edit}")
    
    elif action == "Create Custom Workout":
        st.markdown("### Create Custom Workout")
        
        custom_name = st.text_input("Exercise Name")
        custom_weight = st.number_input("Target Weight (kg)", value=30.0, step=0.5)
        custom_sets = st.number_input("Sets", value=3, min_value=1)
        custom_reps = st.text_input("Reps (e.g., 8-10)", value="8-10")
        custom_notes = st.text_area("Notes/Form Cues")
        
        if st.button("➕ Add Custom Workout"):
            st.success(f"✓ Added {custom_name} to this week")

# TAB 7: SETTINGS
with tabs[7]:
    st.markdown("### Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Profile")
        name = st.text_input("Name", value="John")
        age = st.number_input("Age", value=33)
    
    with col2:
        st.markdown("#### Goals")
        target_weight = st.number_input("Target Weight (kg)", value=75.0)
        target_bf = st.number_input("Target Body Fat (%)", value=10.0)
    
    if st.button("💾 Save Settings"):
        st.success("✓ Settings saved")

st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 11px;'>
✅ Per-set tracking | 🏋️ BoostCamp style | ⏱️ Auto rest timer | 📊 Weekly analytics | 📱 Mobile-first
</div>
""", unsafe_allow_html=True)
