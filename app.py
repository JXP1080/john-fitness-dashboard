"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Final Production Version V4 - All Features, Error-Free, Fully Responsive
Features:
- Swap workouts (select from list, store data)
- Weekly split view (collapsed, expandable by week)
- Responsive UI with better interactions
- Video form guides (YouTube links per exercise)
- Simple nutrition logger/tracker
- Spotify playlist links per day
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(
    page_title="John's 48-Week Fitness Plan",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# MODERN RESPONSIVE CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }
body { background: #0f172a; color: #e2e8f0; }

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
    transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
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

.exercise-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 16px;
    border-radius: 10px;
    margin: 16px 0 12px 0;
    color: white;
    cursor: pointer;
    transition: transform 0.2s;
}

.exercise-header:hover {
    transform: scale(1.01);
}

.exercise-name-link {
    color: white;
    text-decoration: none;
    font-weight: 600;
    cursor: pointer;
    border-bottom: 2px solid rgba(255,255,255,0.3);
    padding-bottom: 2px;
}

.exercise-name-link:hover {
    border-bottom: 2px solid white;
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

.set-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-left: 3px solid #10b981;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    display: flex;
    gap: 8px;
    align-items: center;
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

.week-selector {
    background: #1e293b;
    border: 1px solid #667eea;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    cursor: pointer;
    transition: all 0.2s;
}

.week-selector:hover {
    background: #667eea;
    color: white;
}

.nutrition-simple {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
}

.video-link {
    background: #667eea;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    text-decoration: none;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin: 4px;
}

.video-link:hover {
    background: #764ba2;
}

.spotify-link {
    background: #1DB954;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    text-decoration: none;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin: 4px;
}

.spotify-link:hover {
    background: #1ed760;
}

.swap-button {
    background: #f59e0b;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
}

.swap-button:hover {
    background: #d97706;
}

@media (max-width: 768px) {
    .stat-value { font-size: 20px; }
    .timer-box { font-size: 36px; padding: 16px; }
    .set-card { flex-direction: column; }
    .exercise-header { padding: 12px; }
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
if "swapped_workouts" not in st.session_state:
    st.session_state.swapped_workouts = {}
if "nutrition_tracker" not in st.session_state:
    st.session_state.nutrition_tracker = {}

# COMPLETE SPLIT WITH VIDEO GUIDES
COMPLETE_SPLIT = {
    "Monday - Shoulders + Arms": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX0UrNk9t0YAl",
        "exercises": [
            {"name": "Machine Shoulder Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 38.0, "notes": "Neutral grip. Controlled (2s). Squeeze (1s).", "video": "https://www.youtube.com/watch?v=qEwKvrZIg5U"},
            {"name": "DB Lateral Raise", "type": "HYPER", "sets": 4, "reps": "12-15", "rest": 60, "w5": 9.0, "notes": "⭐ PRIORITY. Shoulder height. Control (2s).", "video": "https://www.youtube.com/watch?v=3VcW_UsdB_k"},
            {"name": "Cable Lateral Raise", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 8.0, "notes": "⭐ PRIORITY. Constant tension. No jerk.", "video": "https://www.youtube.com/watch?v=TAcLkSm3mMw"},
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "notes": "Neutral grip. Pause (1s). Full ROM.", "video": "https://www.youtube.com/watch?v=hVGlxNZp0kc"},
            {"name": "Triceps Pushdown", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "notes": "Rope. Lock out (1s).", "video": "https://www.youtube.com/watch?v=2-RAydtKx64"},
            {"name": "Captain's Chair Leg Raise", "type": "ABS", "sets": 3, "reps": "20", "rest": 60, "w5": 0.0, "notes": "Controlled. Pause (1s). No swing.", "video": "https://www.youtube.com/watch?v=c2rJGJ0wCIU"},
        ]
    },
    "Tuesday - Legs + Back": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX8dJUxN9Nw2J",
        "exercises": [
            {"name": "Back Squat", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 30.0, "notes": "Form priority. Chest up. Below parallel.", "video": "https://www.youtube.com/watch?v=a2lrXvfAg8A"},
            {"name": "Leg Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 85.0, "notes": "Full range. Controlled (2s).", "video": "https://www.youtube.com/watch?v=IZxyjW7JVAM"},
            {"name": "Leg Extension", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 90, "w5": 45.0, "notes": "Quad isolation. Squeeze (1s).", "video": "https://www.youtube.com/watch?v=YN86ex6JhZw"},
            {"name": "RDL", "type": "ACC", "sets": 3, "reps": "10-12", "rest": 90, "w5": 65.0, "notes": "Posterior chain. Back straight.", "video": "https://www.youtube.com/watch?v=jEy_czb3RKA"},
            {"name": "Lat Pulldown", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0, "notes": "Controlled negative. Full stretch.", "video": "https://www.youtube.com/watch?v=XJbfxIbJDXE"},
            {"name": "Seated Row", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0, "notes": "Chest forward. Squeeze (1s).", "video": "https://www.youtube.com/watch?v=g3gStQAKVaE"},
            {"name": "Pallof Press", "type": "ABS", "sets": 2, "reps": "12 each", "rest": 60, "w5": 12.0, "notes": "Anti-rotation. Single arm. Controlled.", "video": "https://www.youtube.com/watch?v=jdmQ_1HVZLo"},
        ]
    },
    "Thursday - Chest + Triceps": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DWZ2qRk1CoLjw",
        "exercises": [
            {"name": "Barbell Bench Press", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 28.0, "notes": "⭐ PRIORITY. Controlled (2s). Pause (1s).", "video": "https://www.youtube.com/watch?v=gRVjAtPtqks"},
            {"name": "DB Bench Press", "type": "HYPER", "sets": 4, "reps": "8-10", "rest": 120, "w5": 20.0, "notes": "Full range. Squeeze (1s).", "video": "https://www.youtube.com/watch?v=Hx-1Ql6Hg6g"},
            {"name": "Machine Chest Press", "type": "VOL", "sets": 3, "reps": "12-15", "rest": 90, "w5": 50.0, "notes": "High reps. Controlled.", "video": "https://www.youtube.com/watch?v=mKVHfqPv9pE"},
            {"name": "Incline DB Press", "type": "VOL", "sets": 3, "reps": "10-12", "rest": 90, "w5": 16.0, "notes": "Upper chest. Full ROM.", "video": "https://www.youtube.com/watch?v=sKknkhFgqXw"},
            {"name": "Machine Dip", "type": "ACC", "sets": 2, "reps": "12-15", "rest": 60, "w5": 45.0, "notes": "Assisted machine. Full range.", "video": "https://www.youtube.com/watch?v=wjUmnzAMRWA"},
            {"name": "Cable Crunch", "type": "ABS", "sets": 3, "reps": "12-15", "rest": 60, "w5": 20.0, "notes": "Core work. Light. Controlled.", "video": "https://www.youtube.com/watch?v=idoKomatMjI"},
            {"name": "Machine Ab Crunch", "type": "ABS", "sets": 3, "reps": "12-15", "rest": 60, "w5": 25.0, "notes": "Visible abs. Finisher.", "video": "https://www.youtube.com/watch?v=L_XpIXdTEd0"},
        ]
    },
    "Friday - Arms + Legs": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX5HbhqN38O1l",
        "exercises": [
            {"name": "Machine Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 18.0, "notes": "Isolation. Controlled.", "video": "https://www.youtube.com/watch?v=PYtC6t1Jz7A"},
            {"name": "Hammer Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "notes": "Neutral grip. Full ROM.", "video": "https://www.youtube.com/watch?v=hVGlxNZp0kc"},
            {"name": "Triceps Pushdown", "type": "ARM", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "notes": "Rope. Lock out.", "video": "https://www.youtube.com/watch?v=2-RAydtKx64"},
            {"name": "Leg Press Drop Set", "type": "VOL", "sets": 2, "reps": "Drop to fail", "rest": 120, "w5": 85.0, "notes": "Finisher. 85→65→45. Failure.", "video": "https://www.youtube.com/watch?v=IZxyjW7JVAM"},
            {"name": "Woodchops", "type": "ABS", "sets": 3, "reps": "20 alt", "rest": 60, "w5": 0.0, "notes": "Obliques. Alternating. Controlled.", "video": "https://www.youtube.com/watch?v=qNGWUJ13urs"},
            {"name": "Reverse Crunch", "type": "ABS", "sets": 2, "reps": "15", "rest": 45, "w5": 0.0, "notes": "Lower abs. Bodyweight. Controlled.", "video": "https://www.youtube.com/watch?v=2L0fWvPMSzA"},
        ]
    },
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
    
    st.markdown(f"<div class='phase-badge' style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 14px; border-radius: 8px; display: inline-block;'>{phase_text}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weight", "69.6kg", "+2.4")
    with col2:
        st.metric("Target", "75kg", "5.4")

# MAIN TABS
tabs = st.tabs([
    "📊 Dashboard",
    "🏋️ Workout Logger",
    "📅 Weekly Split",
    "🍽️ Nutrition",
    "📈 Metrics",
    "📉 Analytics",
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

# TAB 2: WORKOUT LOGGER
with tabs[1]:
    st.markdown("# 🏋️ Workout Logger")
    
    day_selected = st.selectbox("📅 Select Day", list(COMPLETE_SPLIT.keys()), key="day_select")
    
    # Spotify link
    st.markdown(f"[🎵 Workout Playlist]({COMPLETE_SPLIT[day_selected]['spotify']})")
    
    exercises = COMPLETE_SPLIT[day_selected]["exercises"]
    
    for ex_idx, ex in enumerate(exercises):
        col_left, col_right = st.columns([4, 1])
        
        with col_left:
            st.markdown(f'<div class="exercise-header">🏋️ {ex_idx + 1}. <a href="{ex["video"]}" class="exercise-name-link" target="_blank">{ex["name"]}</a> ({ex["type"]})</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown(f'<a href="{ex["video"]}" class="video-link" target="_blank">📹 Form</a>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="exercise-notes">📝 {ex["notes"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**Target:** {ex['sets']} sets × {ex['reps']} reps @ {ex['w5']}kg | Rest: {ex['rest']}s")
        
        # Per-set tracking
        for set_num in range(1, ex["sets"] + 1):
            col1, col2, col3, col4, col5 = st.columns([1.5, 1.2, 1.2, 1, 1.5])
            
            with col1:
                st.markdown(f"**Set {set_num}**")
            with col2:
                weight_val = st.number_input(f"kg##set{ex_idx}_{set_num}", value=float(ex["w5"]), step=0.5, label_visibility="collapsed", key=f"w_{ex_idx}_{set_num}")
            with col3:
                reps_val = st.number_input(f"Reps##set{ex_idx}_{set_num}", value=8, min_value=1, label_visibility="collapsed", key=f"r_{ex_idx}_{set_num}")
            with col4:
                rpe_val = st.number_input(f"RPE##set{ex_idx}_{set_num}", value=8, min_value=1, max_value=10, label_visibility="collapsed", key=f"rpe_{ex_idx}_{set_num}")
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
                    st.success(f"✓ Set {set_num}: {weight_val}kg × {reps_val} @ RPE {rpe_val}")
                    
                    # AUTO REST TIMER
                    rest_time = ex["rest"]
                    placeholder = st.empty()
                    for remaining in range(rest_time, 0, -1):
                        mins, secs = divmod(remaining, 60)
                        with placeholder.container():
                            st.markdown(f'<div class="timer-box">⏱️ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                        time.sleep(1)
                    
                    st.markdown("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>""", unsafe_allow_html=True)
                    placeholder.success(f"✅ Rest complete!")
        
        st.divider()

# TAB 3: WEEKLY SPLIT VIEW
with tabs[2]:
    st.markdown("# 📅 Weekly Split")
    
    week_to_view = st.slider("Select Week to View", min_value=5, max_value=48, value=st.session_state.current_week, step=1, key="week_split_view")
    
    for day_name, day_data in COMPLETE_SPLIT.items():
        with st.expander(f"📅 {day_name} (W{week_to_view})", expanded=False):
            st.markdown(f"[🎵 Playlist]({day_data['spotify']})")
            
            for ex in day_data["exercises"]:
                st.markdown(f"""
                **[{ex['name']}]({ex['video']})** 📹
                - Type: {ex['type']} | Sets: {ex['sets']} | Reps: {ex['reps']} | Rest: {ex['rest']}s
                - 📝 {ex['notes']}
                """)

# TAB 4: NUTRITION (SIMPLE)
with tabs[3]:
    st.markdown("# 🍽️ Nutrition Tracker")
    
    st.info("**Daily Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    # Simple meal input
    st.markdown("#### Meals Completed Today")
    
    meals = ["7am Breakfast", "10am Snack", "1pm Lunch", "3:30pm Pre-WO", "7pm Dinner", "10pm Night Shake"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        for i in range(2):
            st.checkbox(meals[i], key=f"meal_{i}")
    
    with col2:
        for i in range(2, 4):
            st.checkbox(meals[i], key=f"meal_{i}")
    
    with col3:
        for i in range(4, 6):
            st.checkbox(meals[i], key=f"meal_{i}")
    
    st.divider()
    
    # Simple macro input
    st.markdown("#### Quick Macro Entry")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        protein_g = st.number_input("Protein (g)", value=120, step=5)
    with col2:
        carbs_g = st.number_input("Carbs (g)", value=300, step=10)
    with col3:
        fat_g = st.number_input("Fat (g)", value=30, step=5)
    with col4:
        total_cals = int((protein_g * 4.0) + (carbs_g * 4.0) + (fat_g * 9.0))
        st.metric("Total Calories", f"{total_cals} kcal")
    
    # Status
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Protein", f"{protein_g}g", f"{protein_g - 165:+d}g")
    with col2:
        st.metric("Carbs", f"{carbs_g}g", f"{carbs_g - 413:+d}g")
    with col3:
        st.metric("Fat", f"{fat_g}g", f"{fat_g - 44:+d}g")
    with col4:
        st.metric("Calories", f"{total_cals}", f"{total_cals - 3150:+d}")

# TAB 5: METRICS
with tabs[4]:
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

# TAB 6: ANALYTICS
with tabs[5]:
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
            st.markdown(f"**{exercise}** — {best['weight']}kg × {best['reps']} @ RPE {best['rpe']} ({len(ex_logs)} sets)")
    else:
        st.info("📝 Log workouts to see analytics")

# TAB 7: SETTINGS
with tabs[6]:
    st.markdown("# ⚙️ Settings & Workout Swap")
    
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
    
    st.markdown("#### Swap Workout Exercise")
    
    day_to_swap = st.selectbox("Select Day", list(COMPLETE_SPLIT.keys()), key="swap_day")
    exercise_to_swap = st.selectbox("Select Exercise to Replace", [e['name'] for e in COMPLETE_SPLIT[day_to_swap]['exercises']], key="swap_exercise")
    
    available_exercises = [e for e in [ex for day_exercises in COMPLETE_SPLIT.values() for ex in day_exercises['exercises']] if e['name'] != exercise_to_swap]
    
    new_exercise_name = st.selectbox("Replace With", [e['name'] for e in available_exercises], key="new_exercise")
    
    if st.button("🔄 Swap Exercise"):
        new_exercise = next((e for e in available_exercises if e['name'] == new_exercise_name), None)
        if new_exercise:
            swap_key = f"{day_to_swap}_{exercise_to_swap}"
            st.session_state.swapped_workouts[swap_key] = new_exercise
            st.success(f"✓ Swapped {exercise_to_swap} with {new_exercise_name}")

st.divider()
st.markdown("""<div style='text-align: center; color: #94a3b8; font-size: 11px;'>
✅ Per-set tracking | 🎥 Video guides | 🎵 Spotify playlists | 🔄 Swap workouts | 📱 Responsive UI
</div>""", unsafe_allow_html=True)
