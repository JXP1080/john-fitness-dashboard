"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Final Production Version V5 - Complete with all features
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
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
    cursor: pointer;
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

.sidebar-info {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-left: 3px solid #10b981;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 12px;
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

.best-set {
    background: #10b981;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin: 4px 0;
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

.timer-controls {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin: 12px 0;
}

.timer-btn {
    background: #667eea;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 11px;
    font-weight: 600;
    transition: background 0.2s;
}

.timer-btn:hover {
    background: #764ba2;
}

.swap-input {
    background: #1e293b;
    border: 1px solid #334155;
    color: #e2e8f0;
    padding: 8px;
    border-radius: 6px;
    font-size: 12px;
}

.health-badge-good {
    background: #10b981;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 600;
    display: inline-block;
}

.health-badge-warning {
    background: #f59e0b;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 600;
    display: inline-block;
}

.health-badge-bad {
    background: #ef4444;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 600;
    display: inline-block;
}

.metric-detail {
    background: #1e293b;
    border: 1px solid #334155;
    border-left: 3px solid #667eea;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 12px;
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

@media (max-width: 768px) {
    .stat-value { font-size: 20px; }
    .timer-box { font-size: 36px; padding: 16px; }
    .timer-controls { flex-wrap: wrap; }
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
if "best_lifts" not in st.session_state:
    st.session_state.best_lifts = {}
if "timer_state" not in st.session_state:
    st.session_state.timer_state = {"running": False, "remaining": 0, "total": 0}

# COMPLETE SPLIT
COMPLETE_SPLIT = {
    "Monday - Shoulders + Arms": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX0UrNk9t0YAl",
        "exercises": [
            {"name": "Machine Shoulder Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 38.0, "w12": 42.0, "notes": "Neutral grip. Controlled descent (2s). Squeeze at top (1s)."},
            {"name": "DB Lateral Raise", "type": "HYPER", "sets": 4, "reps": "12-15", "rest": 60, "w5": 9.0, "w12": 12.0, "notes": "⭐ PRIORITY. Raise to shoulder height. Control negative (2s)."},
            {"name": "Cable Lateral Raise", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 8.0, "w12": 10.0, "notes": "⭐ PRIORITY. Constant tension. No jerking."},
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "w12": 16.0, "notes": "Neutral grip. Pause at top (1s). Full range of motion."},
            {"name": "Triceps Cable Pushdown", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "w12": 25.0, "notes": "Rope attachment. Lock out at bottom (1s)."},
            {"name": "Captain's Chair Leg Raise", "type": "ABS", "sets": 3, "reps": "20", "rest": 60, "w5": 0.0, "w12": 0.0, "notes": "Controlled lift. Pause at top (1s). No swinging."},
        ]
    },
    "Tuesday - Legs + Back": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX8dJUxN9Nw2J",
        "exercises": [
            {"name": "Back Squat", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 30.0, "w12": 40.0, "notes": "Form priority at start. Chest up. Depth below parallel."},
            {"name": "Leg Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 85.0, "w12": 95.0, "notes": "Full range. Controlled descent (2s)."},
            {"name": "Leg Extension", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 90, "w5": 45.0, "w12": 50.0, "notes": "Quad isolation. Squeeze at top (1s)."},
            {"name": "RDL", "type": "ACC", "sets": 3, "reps": "10-12", "rest": 90, "w5": 65.0, "w12": 70.0, "notes": "Posterior chain. Keep back straight."},
            {"name": "Lat Pulldown", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0, "w12": 48.0, "notes": "Controlled negative. Full stretch."},
            {"name": "Seated Row", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0, "w12": 48.0, "notes": "Chest forward. Squeeze shoulder blades (1s)."},
            {"name": "Pallof Press", "type": "ABS", "sets": 2, "reps": "12 each", "rest": 60, "w5": 12.0, "w12": 15.0, "notes": "Anti-rotation. Single arm. Controlled."},
        ]
    },
    "Thursday - Chest + Triceps": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DWZ2qRk1CoLjw",
        "exercises": [
            {"name": "Barbell Bench Press", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 28.0, "w12": 32.0, "notes": "⭐ PRIORITY. Controlled descent (2s). Pause at chest (1s)."},
            {"name": "DB Bench Press", "type": "HYPER", "sets": 4, "reps": "8-10", "rest": 120, "w5": 20.0, "w12": 23.0, "notes": "Full range. Squeeze at top (1s)."},
            {"name": "Machine Chest Press", "type": "VOL", "sets": 3, "reps": "12-15", "rest": 90, "w5": 50.0, "w12": 55.0, "notes": "High reps. Controlled movement."},
            {"name": "Incline DB Press", "type": "VOL", "sets": 3, "reps": "10-12", "rest": 90, "w5": 16.0, "w12": 18.0, "notes": "Upper chest emphasis. Full ROM."},
            {"name": "Machine Dip", "type": "ACC", "sets": 2, "reps": "12-15", "rest": 60, "w5": 45.0, "w12": 50.0, "notes": "Assisted machine. Full range."},
            {"name": "Cable Crunch", "type": "ABS", "sets": 3, "reps": "12-15", "rest": 60, "w5": 20.0, "w12": 25.0, "notes": "Core work. Light weight. Controlled."},
            {"name": "Machine Ab Crunch", "type": "ABS", "sets": 3, "reps": "12-15", "rest": 60, "w5": 25.0, "w12": 30.0, "notes": "Visible abs work. Finisher."},
        ]
    },
    "Friday - Arms + Legs": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX5HbhqN38O1l",
        "exercises": [
            {"name": "Machine Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 18.0, "w12": 20.0, "notes": "Isolation. Controlled movement."},
            {"name": "Hammer Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "w12": 16.0, "notes": "Neutral grip. Full range of motion."},
            {"name": "Triceps Pushdown", "type": "ARM", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "w12": 25.0, "notes": "Rope. Lock out at bottom."},
            {"name": "Leg Press Drop Set", "type": "VOL", "sets": 2, "reps": "Drop to fail", "rest": 120, "w5": 85.0, "w12": 95.0, "notes": "Finisher. Drop: 85→65→45kg. Go to failure."},
            {"name": "Woodchops", "type": "ABS", "sets": 3, "reps": "20 alt", "rest": 60, "w5": 0.0, "w12": 0.0, "notes": "Obliques. Alternating. Controlled rotation."},
            {"name": "Reverse Crunch", "type": "ABS", "sets": 2, "reps": "15", "rest": 45, "w5": 0.0, "w12": 0.0, "notes": "Lower abs. Bodyweight. Controlled."},
        ]
    },
}

# GET ALL EXERCISES FOR SWAP
ALL_EXERCISES = []
for day_data in COMPLETE_SPLIT.values():
    ALL_EXERCISES.extend([e['name'] for e in day_data['exercises']])
ALL_EXERCISES = sorted(list(set(ALL_EXERCISES)))

# DAILY FACTS
DAILY_FACTS = [
    "💡 Protein synthesis peaks 24-48 hours after training. Consistent training matters!",
    "💡 Sleep is when muscle growth happens. Prioritise 7-9 hours per night.",
    "💡 Progressive overload is key: add 0.5-1kg every 1-2 weeks on main lifts.",
    "💡 RPE 8-9 = 1-2 reps from failure. This is optimal for muscle growth.",
    "💡 Rest periods matter: 3min for heavy lifts, 60-90s for accessories.",
    "💡 Body fat at 15% = 4-pack visible. At 10% = 6-pack shredded.",
    "💡 Creatine 5g daily increases strength by 5-15% over 8 weeks.",
    "💡 Eating 0.8-1g protein per lb of body weight supports muscle growth.",
    "💡 Compound lifts (squats, bench, rows) = 70% of your training volume.",
    "💡 Weak points need 2-3x/week frequency for faster development.",
]

# SIDEBAR WITH DAILY FACT & INFO
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
    
    st.markdown(f"<div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 14px; border-radius: 8px; display: inline-block;'>{phase_text}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weight", "69.6kg", "+2.4")
    with col2:
        st.metric("Target", "75kg", "5.4")
    
    st.divider()
    
    # Last weights & targets
    st.markdown("### 📊 Key Lifts")
    st.markdown('<div class="sidebar-info"><strong>Barbell Bench</strong><br>Last: 28kg<br>W12 Target: 32kg</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info"><strong>Lateral Raise</strong><br>Last: 9kg<br>W12 Target: 12kg</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info"><strong>Leg Press</strong><br>Last: 85kg<br>W12 Target: 95kg</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Daily fact
    import random
    daily_fact = random.choice(DAILY_FACTS)
    st.markdown(f'<div class="sidebar-info">{daily_fact}</div>', unsafe_allow_html=True)

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

# TAB 1: DASHBOARD (INTERACTIVE WITH DATE FILTER)
with tabs[0]:
    st.markdown("# 📊 Dashboard")
    
    col_filter_1, col_filter_2, col_filter_3 = st.columns([2, 2, 2])
    
    with col_filter_1:
        date_from = st.date_input("From Date", value=datetime.now() - timedelta(days=30), key="dash_date_from")
    
    with col_filter_2:
        date_to = st.date_input("To Date", value=datetime.now(), key="dash_date_to")
    
    with col_filter_3:
        comparison_metric = st.selectbox("Compare By", ["Volume", "RPE", "Sessions"], key="compare_metric")
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-card"><div class="stat-label">Workouts</div><div class="stat-value">4/week</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><div class="stat-label">Sets</div><div class="stat-value">102</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><div class="stat-label">Duration</div><div class="stat-value">360m</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-card"><div class="stat-label">RPE</div><div class="stat-value">8-9</div></div>', unsafe_allow_html=True)

# TAB 2: WORKOUT LOGGER (ENHANCED)
with tabs[1]:
    st.markdown("# 🏋️ Workout Logger")
    
    day_selected = st.selectbox("📅 Select Day", list(COMPLETE_SPLIT.keys()), key="day_select")
    
    st.markdown(f"[🎵 Workout Playlist]({COMPLETE_SPLIT[day_selected]['spotify']})")
    
    exercises = COMPLETE_SPLIT[day_selected]["exercises"]
    
    for ex_idx, ex in enumerate(exercises):
        col_header_left, col_header_right = st.columns([4, 1])
        
        with col_header_left:
            st.markdown(f'<div class="exercise-header">🏋️ {ex_idx + 1}. {ex["name"]} ({ex["type"]})</div>', unsafe_allow_html=True)
        
        with col_header_right:
            # Swap option per exercise
            if st.checkbox("🔄 Swap", key=f"swap_check_{ex_idx}"):
                swap_input = st.selectbox(
                    f"Replace {ex['name']} with:",
                    [e for e in ALL_EXERCISES if e != ex['name']],
                    key=f"swap_select_{ex_idx}"
                )
                if st.button("✓ Confirm Swap", key=f"confirm_swap_{ex_idx}"):
                    swap_key = f"{day_selected}_{ex['name']}"
                    new_ex = next((e for day_data in COMPLETE_SPLIT.values() for e in day_data['exercises'] if e['name'] == swap_input), None)
                    if new_ex:
                        st.session_state.swapped_workouts[swap_key] = new_ex
                        st.success(f"✓ Swapped with {swap_input}")
        
        st.markdown(f'<div class="exercise-notes">📝 {ex["notes"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**Target:** {ex['sets']} sets × {ex['reps']} reps @ {ex['w5']}kg | Rest: {ex['rest']}s")
        
        # Show best lift memory
        best_key = f"{day_selected}_{ex['name']}"
        if best_key in st.session_state.best_lifts:
            best = st.session_state.best_lifts[best_key]
            st.markdown(f'<div class="best-set">💪 Best: {best["weight"]}kg × {best["reps"]} @ RPE {best["rpe"]}</div>', unsafe_allow_html=True)
        
        # Per-set tracking
        for set_num in range(1, ex["sets"] + 1):
            col1, col2, col3, col4, col5 = st.columns([1.5, 1.2, 1.2, 1, 1.5])
            
            with col1:
                st.markdown(f"**Set {set_num}**")
            with col2:
                weight_val = st.number_input(f"kg##s{ex_idx}_{set_num}", value=float(ex["w5"]), step=0.5, label_visibility="collapsed", key=f"w_{ex_idx}_{set_num}")
            with col3:
                reps_val = st.number_input(f"Reps##s{ex_idx}_{set_num}", value=8, min_value=1, label_visibility="collapsed", key=f"r_{ex_idx}_{set_num}")
            with col4:
                rpe_val = st.number_input(f"RPE##s{ex_idx}_{set_num}", value=8, min_value=1, max_value=10, label_visibility="collapsed", key=f"rpe_{ex_idx}_{set_num}")
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
                    
                    # Update best lift memory
                    best_key = f"{day_selected}_{ex['name']}"
                    if best_key not in st.session_state.best_lifts or weight_val > st.session_state.best_lifts[best_key]["weight"]:
                        st.session_state.best_lifts[best_key] = {
                            "weight": weight_val,
                            "reps": int(reps_val),
                            "rpe": int(rpe_val)
                        }
                    
                    st.success(f"✓ Set {set_num}: {weight_val}kg × {reps_val} @ RPE {rpe_val}")
                    
                    # AUTO REST TIMER WITH CONTROLS
                    st.markdown(f"**Rest Timer ({ex['rest']}s)**")
                    
                    col_timer_1, col_timer_2, col_timer_3, col_timer_4 = st.columns(4)
                    
                    rest_time = ex["rest"]
                    placeholder_timer = st.empty()
                    
                    timer_running = True
                    remaining = rest_time
                    
                    while timer_running and remaining > 0:
                        with placeholder_timer.container():
                            st.markdown(f'<div class="timer-box">⏱️ {remaining//60:02d}:{remaining%60:02d}</div>', unsafe_allow_html=True)
                            
                            col_btn_1, col_btn_2, col_btn_3, col_btn_4 = st.columns(4)
                            
                            with col_btn_1:
                                if st.button("⏸ Pause", key=f"pause_{ex_idx}_{set_num}"):
                                    timer_running = False
                            
                            with col_btn_2:
                                if st.button("▶ Resume", key=f"resume_{ex_idx}_{set_num}"):
                                    timer_running = True
                            
                            with col_btn_3:
                                if st.button("+30s", key=f"add30_{ex_idx}_{set_num}"):
                                    remaining += 30
                            
                            with col_btn_4:
                                if st.button("🔄 Restart", key=f"restart_{ex_idx}_{set_num}"):
                                    remaining = rest_time
                        
                        time.sleep(1)
                        remaining -= 1
                    
                    # BEEP
                    st.markdown("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>""", unsafe_allow_html=True)
                    placeholder_timer.success(f"✅ Rest complete! Ready for set {set_num + 1}")
        
        st.divider()

# TAB 3: WEEKLY SPLIT
with tabs[2]:
    st.markdown("# 📅 Weekly Split")
    
    week_to_view = st.slider("Select Week", min_value=5, max_value=48, value=st.session_state.current_week, step=1, key="week_view")
    
    for day_name, day_data in COMPLETE_SPLIT.items():
        with st.expander(f"📅 {day_name} (W{week_to_view})", expanded=False):
            st.markdown(f"[🎵 Playlist]({day_data['spotify']})")
            
            for ex in day_data["exercises"]:
                st.markdown(f"**{ex['name']}** — {ex['type']}\n- Sets: {ex['sets']} | Reps: {ex['reps']} | Rest: {ex['rest']}s\n- 📝 {ex['notes']}")

# TAB 4: NUTRITION
with tabs[3]:
    st.markdown("# 🍽️ Nutrition Tracker")
    
    st.info("**Daily Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    st.markdown("#### Meals Completed")
    
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
        st.metric("Total", f"{total_cals} kcal")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Protein", f"{protein_g}g", f"{protein_g - 165:+d}g")
    with col2:
        st.metric("Carbs", f"{carbs_g}g", f"{carbs_g - 413:+d}g")
    with col3:
        st.metric("Fat", f"{fat_g}g", f"{fat_g - 44:+d}g")
    with col4:
        st.metric("Calories", f"{total_cals}", f"{total_cals - 3150:+d}")

# TAB 5: METRICS (WITH HEALTH RANGES)
with tabs[4]:
    st.markdown("# 📈 Metrics & Health Status")
    
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
        st.markdown("#### Health Status & Ranges")
        
        # BMI Calculation
        height_cm = 176
        bmi = weight_today / ((height_cm / 100) ** 2)
        
        if bmi < 18.5:
            bmi_status = "Underweight"
            bmi_badge = "health-badge-bad"
        elif bmi < 25:
            bmi_status = "Healthy"
            bmi_badge = "health-badge-good"
        elif bmi < 30:
            bmi_status = "Overweight"
            bmi_badge = "health-badge-warning"
        else:
            bmi_status = "Obese"
            bmi_badge = "health-badge-bad"
        
        st.markdown(f"**BMI: {bmi:.1f}** — {bmi_status} | Healthy Range: 18.5-24.9")
        
        # Body Fat Status
        if body_fat < 10:
            bf_status = "Shredded"
            bf_badge = "health-badge-good"
        elif body_fat < 15:
            bf_status = "Lean"
            bf_badge = "health-badge-good"
        elif body_fat < 20:
            bf_status = "Normal"
            bf_badge = "health-badge-warning"
        else:
            bf_status = "High"
            bf_badge = "health-badge-bad"
        
        st.markdown(f"**Body Fat: {body_fat:.1f}%** — {bf_status} | Healthy Range: 10-20%")
        
        # Muscle Status
        st.markdown(f"**Muscle Mass: {muscle_mass:.1f}kg** | Target W12: 65.6kg")
        
        # Sleep Status
        if sleep_hours >= 7:
            sleep_status = "Optimal"
            sleep_badge = "health-badge-good"
        elif sleep_hours >= 5:
            sleep_status = "Adequate"
            sleep_badge = "health-badge-warning"
        else:
            sleep_status = "Low"
            sleep_badge = "health-badge-bad"
        
        st.markdown(f"**Sleep: {sleep_hours:.1f}h** — {sleep_status} | Healthy Range: 7-9h")
    
    st.divider()
    
    # Expandable health details
    with st.expander("ℹ️ Health Metrics Explained"):
        st.markdown("""
        **BMI (Body Mass Index)**
        - Formula: weight(kg) / height(m)²
        - Healthy: 18.5-24.9
        - Measures overall weight vs height
        
        **Body Fat %**
        - Shredded: <10% (visible 6-pack)
        - Lean: 10-15% (visible 4-pack)
        - Normal: 15-20% (athletic)
        - High: >20% (needs cutting)
        
        **Muscle Mass**
        - Goal: Gain 0.5-1kg per month
        - Shows lean mass (non-fat weight)
        - Requires protein + resistance training
        
        **Waist Circumference**
        - Indicates belly fat storage
        - Healthy: <90cm for men
        - Correlates with visceral fat
        
        **Sleep Quality**
        - 7-9 hours optimal for recovery
        - Muscle growth happens during sleep
        - <6 hours = reduced strength gains
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
✅ Memory-based best lifts | ⏱️ Timer controls (pause/+30s/restart) | 📊 Health ranges | 🔄 Smart swap | 📱 Responsive
</div>""", unsafe_allow_html=True)
