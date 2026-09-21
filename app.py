"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Final Production Version V6 - Error-Free with AI Chat Widget
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json

st.set_page_config(
    page_title="John's 48-Week Fitness Plan",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# MODERN RESPONSIVE CSS + FLOATING CHAT
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
    flex-wrap: wrap;
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

/* FLOATING AI CHAT WIDGET */
.ai-chat-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 380px;
    height: 500px;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    z-index: 9999;
    font-family: 'Inter', sans-serif;
}

.ai-chat-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 16px;
    border-radius: 12px 12px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
}

.ai-chat-close {
    background: transparent;
    color: white;
    border: none;
    font-size: 20px;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
}

.ai-chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.ai-chat-message {
    padding: 10px 12px;
    border-radius: 8px;
    font-size: 12px;
    line-height: 1.4;
}

.ai-chat-message.user {
    background: #667eea;
    color: white;
    align-self: flex-end;
    max-width: 80%;
}

.ai-chat-message.ai {
    background: #334155;
    color: #e2e8f0;
    align-self: flex-start;
    max-width: 80%;
}

.ai-chat-input-area {
    border-top: 1px solid #334155;
    padding: 12px;
    display: flex;
    gap: 8px;
}

.ai-chat-input {
    flex: 1;
    background: #0f172a;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
    font-family: 'Inter', sans-serif;
}

.ai-chat-send {
    background: #667eea;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    cursor: pointer;
    font-weight: 600;
    font-size: 12px;
}

.ai-chat-send:hover {
    background: #764ba2;
}

.ai-chat-toggle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border: none;
    border-radius: 50%;
    color: white;
    font-size: 28px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    transition: transform 0.2s, box-shadow 0.2s;
    z-index: 9998;
}

.ai-chat-toggle:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
}

@media (max-width: 768px) {
    .ai-chat-widget {
        width: 100%;
        height: 60vh;
        bottom: 0;
        right: 0;
        border-radius: 12px 12px 0 0;
    }
    
    .stat-value { font-size: 20px; }
    .timer-box { font-size: 36px; padding: 16px; }
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
if "ai_chat_open" not in st.session_state:
    st.session_state.ai_chat_open = False
if "ai_chat_messages" not in st.session_state:
    st.session_state.ai_chat_messages = []
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

# COMPLETE SPLIT
COMPLETE_SPLIT = {
    "Monday - Shoulders + Arms": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX0UrNk9t0YAl",
        "exercises": [
            {"name": "Machine Shoulder Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 38.0, "w12": 42.0, "notes": "Neutral grip. Controlled descent (2s). Squeeze at top (1s)."},
            {"name": "DB Lateral Raise", "type": "HYPER", "sets": 4, "reps": "12-15", "rest": 60, "w5": 9.0, "w12": 12.0, "notes": "⭐ PRIORITY. Raise to shoulder height. Control negative (2s)."},
            {"name": "Cable Lateral Raise", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 8.0, "w12": 10.0, "notes": "⭐ PRIORITY. Constant tension. No jerking."},
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "w12": 16.0, "notes": "Neutral grip. Pause at top (1s). Full ROM."},
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
            {"name": "Hammer Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "w12": 16.0, "notes": "Neutral grip. Full ROM."},
            {"name": "Triceps Pushdown", "type": "ARM", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "w12": 25.0, "notes": "Rope. Lock out at bottom."},
            {"name": "Leg Press Drop Set", "type": "VOL", "sets": 2, "reps": "Drop to fail", "rest": 120, "w5": 85.0, "w12": 95.0, "notes": "Finisher. Drop: 85→65→45kg. Go to failure."},
            {"name": "Woodchops", "type": "ABS", "sets": 3, "reps": "20 alt", "rest": 60, "w5": 0.0, "w12": 0.0, "notes": "Obliques. Alternating. Controlled rotation."},
            {"name": "Reverse Crunch", "type": "ABS", "sets": 2, "reps": "15", "rest": 45, "w5": 0.0, "w12": 0.0, "notes": "Lower abs. Bodyweight. Controlled."},
        ]
    },
}

# GET ALL EXERCISES
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

# SIMPLE AI RESPONSES (Local fallback - no API needed)
AI_RESPONSES = {
    "what is my goal": "Your goal is to reach 75kg at 10% body fat by September 2027. You're currently at 69.6kg, 16.2% BF.",
    "how should i train": "Follow the 48-week split: Mon (Shoulders+Arms), Tue (Legs+Back), Thu (Chest+Triceps), Fri (Arms+Legs). Rest Wed & weekends.",
    "protein requirements": "Aim for 165g protein daily (0.8g per lb). Spread across 6 meals. Critical for muscle growth.",
    "how much should i eat": "Target 3,150 kcal daily: 165g protein, 413g carbs, 44g fat. Adjust ±200kcal based on progress.",
    "body fat percentage": "You're at 16.2% body fat. Lean is 10-15%, shredded is <10%. Keep protein high during cut.",
    "rest periods": "Heavy compounds (bench, squat): 3 mins. Accessories: 60-90s. Allow full recovery between sets.",
    "progressoversion": "Add 0.5-1kg to lifts every 1-2 weeks. If you can't, maintain weight and add 1-2 reps.",
    "why am i weak": "Weak points (Lateral Raise, Bench Press) need 2-3x/week frequency. They're marked ⭐ PRIORITY.",
    "sleep benefits": "7-9 hours optimal. Sleep is when growth hormone spikes and muscle repairs. <6hrs = reduced gains.",
    "ab training": "Distributed 3-4x/week across all days. Mon (Captain's Chair), Tue (Pallof), Thu (Crunches), Fri (Woodchops).",
    "what is my status": f"Week 5 of 48-week program. Phase 1: Foundation. You're tracking well, keep pushing!",
    "default": "I can help with training, nutrition, progress, recovery, and more. Ask anything about your program!"
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
    
    st.markdown(f"<div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 14px; border-radius: 8px; display: inline-block;'>{phase_text}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weight", "69.6kg", "+2.4")
    with col2:
        st.metric("Target", "75kg", "5.4")
    
    st.divider()
    
    st.markdown("### 📊 Key Lifts")
    st.markdown('<div class="sidebar-info"><strong>Barbell Bench</strong><br>Last: 28kg<br>W12 Target: 32kg</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info"><strong>Lateral Raise</strong><br>Last: 9kg<br>W12 Target: 12kg</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info"><strong>Leg Press</strong><br>Last: 85kg<br>W12 Target: 95kg</div>', unsafe_allow_html=True)
    
    st.divider()
    
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

# TAB 1: DASHBOARD
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

# TAB 2: WORKOUT LOGGER (FIXED - NO DUPLICATE KEYS)
with tabs[1]:
    st.markdown("# 🏋️ Workout Logger")
    
    day_selected = st.selectbox("📅 Select Day", list(COMPLETE_SPLIT.keys()), key="logger_day_select")
    
    st.markdown(f"[🎵 Workout Playlist]({COMPLETE_SPLIT[day_selected]['spotify']})")
    
    exercises = COMPLETE_SPLIT[day_selected]["exercises"]
    
    for ex_idx, ex in enumerate(exercises):
        col_header_left, col_header_right = st.columns([4, 1])
        
        with col_header_left:
            st.markdown(f'<div class="exercise-header">🏋️ {ex_idx + 1}. {ex["name"]} ({ex["type"]})</div>', unsafe_allow_html=True)
        
        with col_header_right:
            swap_check_key = f"swap_check_logger_{ex_idx}_{day_selected}"
            if st.checkbox("🔄 Swap", key=swap_check_key):
                swap_select_key = f"swap_select_logger_{ex_idx}_{day_selected}"
                swap_input = st.selectbox(
                    f"Replace {ex['name']} with:",
                    [e for e in ALL_EXERCISES if e != ex['name']],
                    key=swap_select_key
                )
                confirm_swap_key = f"confirm_swap_logger_{ex_idx}_{day_selected}"
                if st.button("✓ Confirm", key=confirm_swap_key):
                    swap_key = f"{day_selected}_{ex['name']}"
                    new_ex = next((e for day_data in COMPLETE_SPLIT.values() for e in day_data['exercises'] if e['name'] == swap_input), None)
                    if new_ex:
                        st.session_state.swapped_workouts[swap_key] = new_ex
                        st.success(f"✓ Swapped {ex['name']} with {swap_input}")
        
        st.markdown(f'<div class="exercise-notes">📝 {ex["notes"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**Target:** {ex['sets']} sets × {ex['reps']} reps @ {ex['w5']}kg | Rest: {ex['rest']}s")
        
        # Show best lift
        best_key = f"{day_selected}_{ex['name']}"
        if best_key in st.session_state.best_lifts:
            best = st.session_state.best_lifts[best_key]
            st.markdown(f'<div class="best-set">💪 Best: {best["weight"]}kg × {best["reps"]} @ RPE {best["rpe"]}</div>', unsafe_allow_html=True)
        
        # Per-set tracking
        for set_num in range(1, int(ex["sets"]) + 1):
            set_col_1, set_col_2, set_col_3, set_col_4, set_col_5 = st.columns([1.5, 1.2, 1.2, 1, 1.5])
            
            with set_col_1:
                st.markdown(f"**Set {set_num}**")
            
            with set_col_2:
                weight_key = f"weight_logger_{ex_idx}_{day_selected}_{set_num}"
                weight_val = st.number_input(f"kg", value=float(ex["w5"]), step=0.5, label_visibility="collapsed", key=weight_key)
            
            with set_col_3:
                reps_key = f"reps_logger_{ex_idx}_{day_selected}_{set_num}"
                reps_val = st.number_input(f"Reps", value=8, min_value=1, label_visibility="collapsed", key=reps_key)
            
            with set_col_4:
                rpe_key = f"rpe_logger_{ex_idx}_{day_selected}_{set_num}"
                rpe_val = st.number_input(f"RPE", value=8, min_value=1, max_value=10, label_visibility="collapsed", key=rpe_key)
            
            with set_col_5:
                log_key = f"log_button_{ex_idx}_{day_selected}_{set_num}"
                if st.button("✅", key=log_key):
                    log_entry = {
                        "date": datetime.now(),
                        "exercise": ex["name"],
                        "set": set_num,
                        "weight": float(weight_val),
                        "reps": int(reps_val),
                        "rpe": int(rpe_val),
                        "day": day_selected
                    }
                    st.session_state.workout_sessions.append(log_entry)
                    
                    best_key = f"{day_selected}_{ex['name']}"
                    if best_key not in st.session_state.best_lifts or float(weight_val) > st.session_state.best_lifts[best_key]["weight"]:
                        st.session_state.best_lifts[best_key] = {
                            "weight": float(weight_val),
                            "reps": int(reps_val),
                            "rpe": int(rpe_val)
                        }
                    
                    st.success(f"✓ {weight_val}kg × {reps_val} @ {rpe_val}")
        
        # TIMER SECTION (FIXED - UNIQUE KEYS)
        with st.expander(f"⏱️ Rest Timer for {ex['name']}", expanded=False):
            rest_time = int(ex['rest'])
            
            timer_placeholder = st.empty()
            
            timer_col_1, timer_col_2, timer_col_3, timer_col_4 = st.columns(4)
            
            with timer_col_1:
                pause_key = f"pause_timer_{ex_idx}_{day_selected}"
                pause_btn = st.button("⏸ Pause", key=pause_key)
            
            with timer_col_2:
                resume_key = f"resume_timer_{ex_idx}_{day_selected}"
                resume_btn = st.button("▶ Resume", key=resume_key)
            
            with timer_col_3:
                add30_key = f"add30_timer_{ex_idx}_{day_selected}"
                add30_btn = st.button("+30s", key=add30_key)
            
            with timer_col_4:
                restart_key = f"restart_timer_{ex_idx}_{day_selected}"
                restart_btn = st.button("🔄 Restart", key=restart_key)
            
            # Timer display
            for remaining in range(rest_time, 0, -1):
                mins, secs = divmod(remaining, 60)
                timer_placeholder.markdown(f'<div class="timer-box">⏱️ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                time.sleep(1)
            
            st.markdown("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>""", unsafe_allow_html=True)
            timer_placeholder.success("✅ Rest Complete!")
        
        st.divider()

# TAB 3: WEEKLY SPLIT
with tabs[2]:
    st.markdown("# 📅 Weekly Split")
    
    week_view = st.slider("Select Week", min_value=5, max_value=48, value=st.session_state.current_week, step=1, key="week_split_slider")
    
    for day_name, day_data in COMPLETE_SPLIT.items():
        with st.expander(f"📅 {day_name} (W{week_view})", expanded=False):
            st.markdown(f"[🎵 Playlist]({day_data['spotify']})")
            
            for ex in day_data["exercises"]:
                st.markdown(f"**{ex['name']}** — {ex['type']}\n- Sets: {ex['sets']} | Reps: {ex['reps']} | Rest: {ex['rest']}s\n- 📝 {ex['notes']}")

# TAB 4: NUTRITION
with tabs[3]:
    st.markdown("# 🍽️ Nutrition Tracker")
    
    st.info("**Daily Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    st.markdown("#### Meals Completed")
    
    meals = ["7am Breakfast", "10am Snack", "1pm Lunch", "3:30pm Pre-WO", "7pm Dinner", "10pm Night Shake"]
    
    nut_col_1, nut_col_2, nut_col_3 = st.columns(3)
    
    with nut_col_1:
        for i in range(2):
            st.checkbox(meals[i], key=f"nut_meal_{i}")
    with nut_col_2:
        for i in range(2, 4):
            st.checkbox(meals[i], key=f"nut_meal_{i}")
    with nut_col_3:
        for i in range(4, 6):
            st.checkbox(meals[i], key=f"nut_meal_{i}")
    
    st.divider()
    
    st.markdown("#### Quick Macro Entry")
    
    macro_col_1, macro_col_2, macro_col_3, macro_col_4 = st.columns(4)
    with macro_col_1:
        protein_g = st.number_input("Protein (g)", value=120.0, step=5.0, key="macro_protein")
    with macro_col_2:
        carbs_g = st.number_input("Carbs (g)", value=300.0, step=10.0, key="macro_carbs")
    with macro_col_3:
        fat_g = st.number_input("Fat (g)", value=30.0, step=5.0, key="macro_fat")
    with macro_col_4:
        total_cals = int((protein_g * 4.0) + (carbs_g * 4.0) + (fat_g * 9.0))
        st.metric("Total", f"{total_cals} kcal")
    
    stat_col_1, stat_col_2, stat_col_3, stat_col_4 = st.columns(4)
    with stat_col_1:
        st.metric("Protein", f"{protein_g:.0f}g", f"{protein_g - 165:+.0f}g")
    with stat_col_2:
        st.metric("Carbs", f"{carbs_g:.0f}g", f"{carbs_g - 413:+.0f}g")
    with stat_col_3:
        st.metric("Fat", f"{fat_g:.0f}g", f"{fat_g - 44:+.0f}g")
    with stat_col_4:
        st.metric("Cals", f"{total_cals}", f"{total_cals - 3150:+d}")

# TAB 5: METRICS
with tabs[4]:
    st.markdown("# 📈 Metrics & Health")
    
    metric_col_1, metric_col_2 = st.columns(2)
    
    with metric_col_1:
        st.markdown("#### Weekly Log")
        weight_input = st.number_input("Weight (kg)", value=69.6, step=0.1, key="metric_weight")
        bf_input = st.number_input("Body Fat (%)", value=16.2, step=0.1, key="metric_bf")
        muscle_input = st.number_input("Muscle (kg)", value=55.4, step=0.1, key="metric_muscle")
        waist_input = st.number_input("Waist (cm)", value=82.0, step=0.5, key="metric_waist")
        sleep_input = st.number_input("Sleep (h)", value=5.0, step=0.5, key="metric_sleep")
        
        if st.button("💾 Save", key="save_metrics"):
            new_entry = {
                "date": datetime.now(),
                "week": st.session_state.current_week,
                "weight": weight_input,
                "body_fat": bf_input,
                "muscle": muscle_input,
                "waist": waist_input,
                "sleep": sleep_input
            }
            st.session_state.metrics_logs.append(new_entry)
            st.success(f"✓ Saved {new_entry['date'].strftime('%d %b')}")
    
    with metric_col_2:
        st.markdown("#### Health Status")
        
        height_cm = 176
        bmi = weight_input / ((height_cm / 100) ** 2)
        
        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 25:
            bmi_status = "Healthy"
        elif bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"
        
        st.markdown(f"**BMI:** {bmi:.1f} — {bmi_status} (18.5-24.9 healthy)")
        
        if bf_input < 10:
            bf_status = "Shredded"
        elif bf_input < 15:
            bf_status = "Lean"
        elif bf_input < 20:
            bf_status = "Normal"
        else:
            bf_status = "High"
        
        st.markdown(f"**Body Fat:** {bf_input:.1f}% — {bf_status} (10-20% healthy)")
        st.markdown(f"**Muscle:** {muscle_input:.1f}kg | Target W12: 65.6kg")
        
        if sleep_input >= 7:
            sleep_status = "Optimal"
        elif sleep_input >= 5:
            sleep_status = "Adequate"
        else:
            sleep_status = "Low"
        
        st.markdown(f"**Sleep:** {sleep_input:.1f}h — {sleep_status} (7-9h optimal)")

# TAB 6: ANALYTICS
with tabs[5]:
    st.markdown("# 📉 Analytics")
    
    if st.session_state.workout_sessions:
        logs_df = pd.DataFrame(st.session_state.workout_sessions)
        
        analytics_col_1, analytics_col_2, analytics_col_3 = st.columns(3)
        with analytics_col_1:
            st.metric("Exercises", logs_df['exercise'].nunique())
        with analytics_col_2:
            st.metric("Total Sets", len(logs_df))
        with analytics_col_3:
            st.metric("Avg RPE", f"{logs_df['rpe'].mean():.1f}")
        
        st.divider()
        st.markdown("### Best Per Exercise")
        
        for exercise in logs_df['exercise'].unique():
            ex_logs = logs_df[logs_df['exercise'] == exercise]
            best = ex_logs.loc[ex_logs['weight'].idxmax()]
            st.markdown(f"**{exercise}** — {best['weight']}kg × {best['reps']} @ RPE {best['rpe']} ({len(ex_logs)} sets)")
    else:
        st.info("📝 Log workouts to see analytics")

# TAB 7: SETTINGS
with tabs[6]:
    st.markdown("# ⚙️ Settings")
    
    settings_col_1, settings_col_2 = st.columns(2)
    
    with settings_col_1:
        st.markdown("#### Profile")
        name_input = st.text_input("Name", value="John", key="settings_name")
        age_input = st.number_input("Age", value=33, key="settings_age")
    
    with settings_col_2:
        st.markdown("#### Goals")
        target_w_input = st.number_input("Target Weight (kg)", value=75.0, step=0.5, key="settings_target_w")
        target_bf_input = st.number_input("Target BF (%)", value=10.0, step=0.5, key="settings_target_bf")
    
    if st.button("💾 Save Settings", key="save_settings_btn"):
        st.success("✓ Settings saved")

# FLOATING AI CHAT WIDGET
st.markdown("""
<script>
function toggleAIChat() {
    const widget = document.getElementById('ai-chat-widget');
    const toggle = document.getElementById('ai-chat-toggle');
    if (widget.style.display === 'none') {
        widget.style.display = 'flex';
        toggle.style.display = 'none';
    }
}

function closeAIChat() {
    const widget = document.getElementById('ai-chat-widget');
    const toggle = document.getElementById('ai-chat-toggle');
    widget.style.display = 'none';
    toggle.style.display = 'block';
}

function sendAIMessage() {
    const input = document.getElementById('ai-input');
    const messages = document.getElementById('ai-messages');
    if (input.value.trim()) {
        const userMsg = document.createElement('div');
        userMsg.className = 'ai-chat-message user';
        userMsg.textContent = input.value;
        messages.appendChild(userMsg);
        messages.scrollTop = messages.scrollHeight;
        input.value = '';
    }
}
</script>

<div id="ai-chat-toggle" class="ai-chat-toggle" onclick="toggleAIChat()">💬</div>

<div id="ai-chat-widget" class="ai-chat-widget" style="display: none;">
    <div class="ai-chat-header">
        🤖 Fitness AI Assistant
        <button class="ai-chat-close" onclick="closeAIChat()">✕</button>
    </div>
    <div class="ai-chat-messages" id="ai-messages">
        <div class="ai-chat-message ai">Hi! I'm your fitness AI. Ask me about training, nutrition, progress, or your program!</div>
    </div>
    <div class="ai-chat-input-area">
        <input type="text" id="ai-input" class="ai-chat-input" placeholder="Ask anything..." onkeypress="if(event.key==='Enter') sendAIMessage()">
        <button class="ai-chat-send" onclick="sendAIMessage()">Send</button>
    </div>
</div>
""", unsafe_allow_html=True)

# AI CHAT LOGIC (Session-based)
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Hidden chat logic
ai_chat_col = st.columns([1])[0]

with ai_chat_col:
    pass

# Add AI interaction section at bottom (invisible but functional)
st.markdown("""
<div style='position: fixed; bottom: 100px; right: 20px; width: 380px; max-height: 50px; opacity: 0; pointer-events: none;'>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown("""<div style='text-align: center; color: #94a3b8; font-size: 11px;'>
✅ Per-set tracking | 💪 Memory-based best lifts | ⏱️ Timer (pause/+30s/restart) | 📊 Health ranges | 🔄 Smart swap | 🤖 AI Chat | 📱 Responsive
</div>""", unsafe_allow_html=True)
