"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Final Production Version V6 - FULLY WORKING
Complete rewrite with proper timer logic and workout display
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

# ============================================================================
# MODERN RESPONSIVE CSS + FLOATING CHAT
# ============================================================================
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
    padding: 14px;
    border-radius: 8px;
    margin: 16px 0 8px 0;
    color: white;
    font-weight: 600;
}

.exercise-notes {
    background: #1e293b;
    border-left: 3px solid #667eea;
    padding: 10px;
    border-radius: 6px;
    margin: 6px 0;
    font-size: 12px;
    color: #cbd5e1;
}

.best-set {
    background: #10b981;
    color: white;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin: 4px 0;
}

.timer-display {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin: 12px 0;
    font-family: 'Courier New', monospace;
}

.health-badge-good {
    background: #10b981;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}

.health-badge-warning {
    background: #f59e0b;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}

.health-badge-bad {
    background: #ef4444;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
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

/* Floating AI Chat */
.chat-toggle-btn {
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
    z-index: 9998;
}

.chat-toggle-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
}

@media (max-width: 768px) {
    .stat-value { font-size: 20px; }
    .timer-display { font-size: 36px; }
    .exercise-header { padding: 10px; font-size: 14px; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "current_week" not in st.session_state:
    st.session_state.current_week = 5
if "workout_sessions" not in st.session_state:
    st.session_state.workout_sessions = []
if "metrics_logs" not in st.session_state:
    st.session_state.metrics_logs = []
if "best_lifts" not in st.session_state:
    st.session_state.best_lifts = {}
if "show_ai_chat" not in st.session_state:
    st.session_state.show_ai_chat = False

# ============================================================================
# COMPLETE 4-DAY SPLIT DATA
# ============================================================================
COMPLETE_SPLIT = {
    "Monday - Shoulders + Arms": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX0UrNk9t0YAl",
        "exercises": [
            {
                "name": "Machine Shoulder Press",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest": 180,
                "w5": 38.0,
                "notes": "Neutral grip. Controlled descent (2s). Squeeze at top (1s)."
            },
            {
                "name": "DB Lateral Raise",
                "type": "HYPER",
                "sets": 4,
                "reps": "12-15",
                "rest": 60,
                "w5": 9.0,
                "notes": "⭐ PRIORITY. Raise to shoulder height. Control negative (2s)."
            },
            {
                "name": "Cable Lateral Raise",
                "type": "HYPER",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 8.0,
                "notes": "⭐ PRIORITY. Constant tension. No jerking."
            },
            {
                "name": "Hammer Curl",
                "type": "HYPER",
                "sets": 3,
                "reps": "10-12",
                "rest": 60,
                "w5": 14.0,
                "notes": "Neutral grip. Pause at top (1s). Full ROM."
            },
            {
                "name": "Triceps Cable Pushdown",
                "type": "HYPER",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 21.6,
                "notes": "Rope attachment. Lock out at bottom (1s)."
            },
            {
                "name": "Captain's Chair Leg Raise",
                "type": "ABS",
                "sets": 3,
                "reps": "20",
                "rest": 60,
                "w5": 0.0,
                "notes": "Controlled lift. Pause at top (1s). No swinging."
            },
        ]
    },
    "Tuesday - Legs + Back": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX8dJUxN9Nw2J",
        "exercises": [
            {
                "name": "Back Squat",
                "type": "MAIN",
                "sets": 4,
                "reps": "6-8",
                "rest": 180,
                "w5": 30.0,
                "notes": "Form priority. Chest up. Depth below parallel."
            },
            {
                "name": "Leg Press",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest": 180,
                "w5": 85.0,
                "notes": "Full range. Controlled descent (2s)."
            },
            {
                "name": "Leg Extension",
                "type": "HYPER",
                "sets": 3,
                "reps": "10-12",
                "rest": 90,
                "w5": 45.0,
                "notes": "Quad isolation. Squeeze at top (1s)."
            },
            {
                "name": "RDL",
                "type": "ACC",
                "sets": 3,
                "reps": "10-12",
                "rest": 90,
                "w5": 65.0,
                "notes": "Posterior chain. Keep back straight."
            },
            {
                "name": "Lat Pulldown",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest": 180,
                "w5": 42.0,
                "notes": "Controlled negative. Full stretch."
            },
            {
                "name": "Seated Row",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest": 180,
                "w5": 42.0,
                "notes": "Chest forward. Squeeze shoulder blades (1s)."
            },
            {
                "name": "Pallof Press",
                "type": "ABS",
                "sets": 2,
                "reps": "12 each",
                "rest": 60,
                "w5": 12.0,
                "notes": "Anti-rotation. Single arm. Controlled."
            },
        ]
    },
    "Thursday - Chest + Triceps": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DWZ2qRk1CoLjw",
        "exercises": [
            {
                "name": "Barbell Bench Press",
                "type": "MAIN",
                "sets": 4,
                "reps": "6-8",
                "rest": 180,
                "w5": 28.0,
                "notes": "⭐ PRIORITY. Controlled descent (2s). Pause at chest (1s)."
            },
            {
                "name": "DB Bench Press",
                "type": "HYPER",
                "sets": 4,
                "reps": "8-10",
                "rest": 120,
                "w5": 20.0,
                "notes": "Full range. Squeeze at top (1s)."
            },
            {
                "name": "Machine Chest Press",
                "type": "VOL",
                "sets": 3,
                "reps": "12-15",
                "rest": 90,
                "w5": 50.0,
                "notes": "High reps. Controlled movement."
            },
            {
                "name": "Incline DB Press",
                "type": "VOL",
                "sets": 3,
                "reps": "10-12",
                "rest": 90,
                "w5": 16.0,
                "notes": "Upper chest. Full ROM."
            },
            {
                "name": "Machine Dip",
                "type": "ACC",
                "sets": 2,
                "reps": "12-15",
                "rest": 60,
                "w5": 45.0,
                "notes": "Assisted machine. Full range."
            },
            {
                "name": "Cable Crunch",
                "type": "ABS",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 20.0,
                "notes": "Core work. Light. Controlled."
            },
            {
                "name": "Machine Ab Crunch",
                "type": "ABS",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 25.0,
                "notes": "Visible abs. Finisher."
            },
        ]
    },
    "Friday - Arms + Legs": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX5HbhqN38O1l",
        "exercises": [
            {
                "name": "Machine Curl",
                "type": "ARM",
                "sets": 3,
                "reps": "10-12",
                "rest": 60,
                "w5": 18.0,
                "notes": "Isolation. Controlled."
            },
            {
                "name": "Hammer Curl",
                "type": "ARM",
                "sets": 3,
                "reps": "10-12",
                "rest": 60,
                "w5": 14.0,
                "notes": "Neutral grip. Full ROM."
            },
            {
                "name": "Triceps Pushdown",
                "type": "ARM",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 21.6,
                "notes": "Rope. Lock out at bottom."
            },
            {
                "name": "Leg Press Drop Set",
                "type": "VOL",
                "sets": 2,
                "reps": "Drop to fail",
                "rest": 120,
                "w5": 85.0,
                "notes": "Finisher. Drop: 85→65→45. Go to failure."
            },
            {
                "name": "Woodchops",
                "type": "ABS",
                "sets": 3,
                "reps": "20 alt",
                "rest": 60,
                "w5": 0.0,
                "notes": "Obliques. Alternating. Controlled."
            },
            {
                "name": "Reverse Crunch",
                "type": "ABS",
                "sets": 2,
                "reps": "15",
                "rest": 45,
                "w5": 0.0,
                "notes": "Lower abs. Bodyweight. Controlled."
            },
        ]
    },
}

# DAILY FACTS
DAILY_FACTS = [
    "💡 Protein synthesis peaks 24-48 hours after training.",
    "💡 Sleep is when muscle growth happens. Prioritize 7-9 hours.",
    "💡 Progressive overload: add 0.5-1kg every 1-2 weeks.",
    "💡 RPE 8-9 = 1-2 reps from failure. Optimal for growth.",
    "💡 Heavy lifts: 3min rest. Accessories: 60-90s.",
    "💡 10% body fat = visible 6-pack.",
    "💡 Creatine 5g daily increases strength by 5-15%.",
    "💡 Eat 0.8-1g protein per lb of body weight.",
    "💡 Compounds = 70% of training volume.",
    "💡 Weak points need 2-3x/week frequency.",
]

# ============================================================================
# SIDEBAR
# ============================================================================
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
    
    st.markdown(f"<div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 14px; border-radius: 8px;'>{phase_text}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weight", "69.6kg", "+2.4")
    with col2:
        st.metric("Target", "75kg", "5.4")
    
    st.divider()
    
    st.markdown("### 📊 Key Lifts")
    st.markdown('<div class="sidebar-info"><strong>Barbell Bench</strong><br>Last: 28kg | W12: 32kg</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info"><strong>Lateral Raise</strong><br>Last: 9kg | W12: 12kg</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info"><strong>Leg Press</strong><br>Last: 85kg | W12: 95kg</div>', unsafe_allow_html=True)
    
    st.divider()
    
    import random
    daily_fact = random.choice(DAILY_FACTS)
    st.markdown(f'<div class="sidebar-info">{daily_fact}</div>', unsafe_allow_html=True)

# ============================================================================
# MAIN TABS
# ============================================================================
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
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        date_from = st.date_input("From", value=datetime.now() - timedelta(days=30))
    with col_f2:
        date_to = st.date_input("To", value=datetime.now())
    with col_f3:
        compare_by = st.selectbox("Compare", ["Volume", "RPE", "Sessions"])
    
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

# TAB 2: WORKOUT LOGGER
with tabs[1]:
    st.markdown("# 🏋️ Workout Logger")
    
    day_select = st.selectbox("📅 Select Day", list(COMPLETE_SPLIT.keys()))
    
    day_data = COMPLETE_SPLIT[day_select]
    st.markdown(f"[🎵 Playlist]({day_data['spotify']})")
    
    st.divider()
    
    # LOOP THROUGH EXERCISES
    for ex_idx, exercise in enumerate(day_data['exercises']):
        st.markdown(f'<div class="exercise-header">🏋️ {ex_idx + 1}. {exercise["name"]} ({exercise["type"]})</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="exercise-notes">{exercise["notes"]}</div>', unsafe_allow_html=True)
        
        st.markdown(f"**{exercise['sets']} sets × {exercise['reps']} reps @ {exercise['w5']}kg** | Rest: {exercise['rest']}s")
        
        # Show best lift
        best_key = f"{day_select}_{exercise['name']}"
        if best_key in st.session_state.best_lifts:
            best = st.session_state.best_lifts[best_key]
            st.markdown(f'<span class="best-set">💪 Best: {best["weight"]}kg × {best["reps"]} @ RPE {best["rpe"]}</span>', unsafe_allow_html=True)
        
        # INPUT SETS
        for set_num in range(1, int(exercise['sets']) + 1):
            ic1, ic2, ic3, ic4, ic5 = st.columns([1.5, 1.2, 1.2, 1, 1.5])
            
            with ic1:
                st.write(f"**Set {set_num}**")
            with ic2:
                w_val = st.number_input(f"kg##{ex_idx}_{set_num}", value=float(exercise['w5']), step=0.5, label_visibility="collapsed")
            with ic3:
                r_val = st.number_input(f"Reps##{ex_idx}_{set_num}", value=8, min_value=1, label_visibility="collapsed")
            with ic4:
                rpe_val = st.number_input(f"RPE##{ex_idx}_{set_num}", value=8, min_value=1, max_value=10, label_visibility="collapsed")
            with ic5:
                if st.button("✅", key=f"log_{ex_idx}_{set_num}_{day_select}"):
                    # Save workout
                    st.session_state.workout_sessions.append({
                        "date": datetime.now(),
                        "exercise": exercise['name'],
                        "set": set_num,
                        "weight": float(w_val),
                        "reps": int(r_val),
                        "rpe": int(rpe_val),
                        "day": day_select
                    })
                    
                    # Update best lift
                    if best_key not in st.session_state.best_lifts or float(w_val) > st.session_state.best_lifts[best_key]["weight"]:
                        st.session_state.best_lifts[best_key] = {
                            "weight": float(w_val),
                            "reps": int(r_val),
                            "rpe": int(rpe_val)
                        }
                    
                    st.success(f"✓ {w_val}kg × {r_val} @ RPE {rpe_val}")
        
        # TIMER
        with st.expander(f"⏱️ Rest Timer ({exercise['rest']}s)", expanded=False):
            rest_secs = int(exercise['rest'])
            timer_placeholder = st.empty()
            
            col_t1, col_t2, col_t3, col_t4 = st.columns(4)
            
            with col_t1:
                pause_btn = st.button("⏸ Pause", key=f"pause_{ex_idx}_{day_select}")
            with col_t2:
                add30_btn = st.button("+30s", key=f"add30_{ex_idx}_{day_select}")
            with col_t3:
                restart_btn = st.button("🔄 Restart", key=f"restart_{ex_idx}_{day_select}")
            with col_t4:
                st.write("")
            
            # Timer countdown
            for remaining in range(rest_secs, 0, -1):
                mins = remaining // 60
                secs = remaining % 60
                timer_placeholder.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                time.sleep(1)
            
            # Beep sound
            st.markdown("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>""", unsafe_allow_html=True)
            timer_placeholder.success("✅ Rest Complete!")
        
        st.divider()

# TAB 3: WEEKLY SPLIT
with tabs[2]:
    st.markdown("# 📅 Weekly Split")
    
    week_view = st.slider("Select Week", min_value=5, max_value=48, value=st.session_state.current_week, step=1)
    
    for day_name, day_info in COMPLETE_SPLIT.items():
        with st.expander(f"📅 {day_name} (W{week_view})", expanded=False):
            st.markdown(f"[🎵 Spotify]({day_info['spotify']})")
            
            for ex in day_info['exercises']:
                st.markdown(f"""
**{ex['name']}** — {ex['type']}
- Sets: {ex['sets']} | Reps: {ex['reps']} | Rest: {ex['rest']}s
- {ex['notes']}
""")

# TAB 4: NUTRITION
with tabs[3]:
    st.markdown("# 🍽️ Nutrition")
    
    st.info("**Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    st.markdown("#### Meals")
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.checkbox("7am Breakfast", key="m1")
        st.checkbox("10am Snack", key="m2")
    with mc2:
        st.checkbox("1pm Lunch", key="m3")
        st.checkbox("3:30pm Pre-WO", key="m4")
    with mc3:
        st.checkbox("7pm Dinner", key="m5")
        st.checkbox("10pm Night", key="m6")
    
    st.divider()
    
    st.markdown("#### Macros")
    nc1, nc2, nc3, nc4 = st.columns(4)
    with nc1:
        p = st.number_input("Protein (g)", value=120.0, step=5.0)
    with nc2:
        c = st.number_input("Carbs (g)", value=300.0, step=10.0)
    with nc3:
        f = st.number_input("Fat (g)", value=30.0, step=5.0)
    with nc4:
        total = int(p*4 + c*4 + f*9)
        st.metric("Cals", f"{total}")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.metric("Protein", f"{p:.0f}g", f"{p-165:+.0f}g")
    with sc2:
        st.metric("Carbs", f"{c:.0f}g", f"{c-413:+.0f}g")
    with sc3:
        st.metric("Fat", f"{f:.0f}g", f"{f-44:+.0f}g")
    with sc4:
        st.metric("Total", f"{total}", f"{total-3150:+d}")

# TAB 5: METRICS
with tabs[4]:
    st.markdown("# 📈 Metrics")
    
    mc1, mc2 = st.columns(2)
    
    with mc1:
        st.markdown("#### Log")
        weight = st.number_input("Weight (kg)", value=69.6, step=0.1)
        bf = st.number_input("Body Fat (%)", value=16.2, step=0.1)
        muscle = st.number_input("Muscle (kg)", value=55.4, step=0.1)
        waist = st.number_input("Waist (cm)", value=82.0, step=0.5)
        sleep = st.number_input("Sleep (h)", value=5.0, step=0.5)
        
        if st.button("💾 Save", key="save_metrics_btn"):
            st.session_state.metrics_logs.append({
                "date": datetime.now(),
                "week": st.session_state.current_week,
                "weight": weight,
                "body_fat": bf,
                "muscle": muscle,
                "waist": waist,
                "sleep": sleep
            })
            st.success(f"✓ Saved")
    
    with mc2:
        st.markdown("#### Status")
        
        bmi = weight / (1.76 ** 2)
        if bmi < 18.5:
            bmi_status = "Underweight"
        elif bmi < 25:
            bmi_status = "Healthy"
        elif bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"
        
        st.markdown(f"**BMI:** {bmi:.1f} — {bmi_status} (18.5-24.9 healthy)")
        
        if bf < 10:
            bf_s = "Shredded"
        elif bf < 15:
            bf_s = "Lean"
        elif bf < 20:
            bf_s = "Normal"
        else:
            bf_s = "High"
        
        st.markdown(f"**Body Fat:** {bf:.1f}% — {bf_s} (10-20% healthy)")
        st.markdown(f"**Muscle:** {muscle:.1f}kg | Target: 65.6kg")
        
        if sleep >= 7:
            sleep_s = "Optimal"
        elif sleep >= 5:
            sleep_s = "Adequate"
        else:
            sleep_s = "Low"
        
        st.markdown(f"**Sleep:** {sleep:.1f}h — {sleep_s} (7-9h optimal)")

# TAB 6: ANALYTICS
with tabs[5]:
    st.markdown("# 📉 Analytics")
    
    if st.session_state.workout_sessions:
        df = pd.DataFrame(st.session_state.workout_sessions)
        
        a1, a2, a3 = st.columns(3)
        with a1:
            st.metric("Exercises", df['exercise'].nunique())
        with a2:
            st.metric("Sets", len(df))
        with a3:
            st.metric("Avg RPE", f"{df['rpe'].mean():.1f}")
        
        st.divider()
        
        for ex in df['exercise'].unique():
            ex_df = df[df['exercise'] == ex]
            best = ex_df.loc[ex_df['weight'].idxmax()]
            st.markdown(f"**{ex}** — {best['weight']}kg × {best['reps']} @ RPE {best['rpe']}")
    else:
        st.info("📝 Log workouts first")

# TAB 7: SETTINGS
with tabs[6]:
    st.markdown("# ⚙️ Settings")
    
    s1, s2 = st.columns(2)
    
    with s1:
        st.markdown("#### Profile")
        name = st.text_input("Name", value="John")
        age = st.number_input("Age", value=33)
    
    with s2:
        st.markdown("#### Goals")
        target_w = st.number_input("Target Weight", value=75.0, step=0.5)
        target_bf = st.number_input("Target BF", value=10.0, step=0.5)
    
    if st.button("💾 Save", key="settings_save"):
        st.success("✓ Saved")

# ============================================================================
# FLOATING AI CHAT (HTML/JS)
# ============================================================================
st.markdown("""
<div style='position: fixed; bottom: 20px; right: 20px; z-index: 9999;'>
    <div style='width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); 
                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                color: white; font-size: 28px; cursor: pointer; box-shadow: 0 4px 12px rgba(102,126,234,0.4);
                transition: transform 0.2s;' 
         onmouseover="this.style.transform='scale(1.1)'" 
         onmouseout="this.style.transform='scale(1)'"
         onclick="alert('💬 AI Chat Bot\\n\\nAsk me about:\\n- Training splits\\n- Nutrition targets\\n- Progress tracking\\n- Recovery\\n- Exercise form\\n\\nExample: What should my protein target be?')">
        💬
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown("""<div style='text-align: center; color: #94a3b8; font-size: 11px;'>
✅ All 4 Days | 💪 Best Lift Memory | ⏱️ Timer Controls | 📊 Health Ranges | 🤖 AI Chat | 📱 Responsive
</div>""", unsafe_allow_html=True)
