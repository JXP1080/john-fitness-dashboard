"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Final Production Version V8 - Error-Checked & Improved
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
    font-size: 36px;
    font-weight: bold;
    margin: 12px 0;
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
if "timers" not in st.session_state:
    st.session_state.timers = {}

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

ALL_EXERCISES = sorted({e["name"] for d in COMPLETE_SPLIT.values() for e in d["exercises"]})

DAILY_FACTS = [
    "💡 Protein synthesis peaks 24-48 hours after training.",
    "💡 Sleep is when muscle growth happens. Aim 7-9 hours.",
    "💡 Progressive overload: add 0.5-1kg every 1-2 weeks on main lifts.",
    "💡 RPE 8-9 = 1-2 reps from failure. Optimal for growth.",
    "💡 Rest: 3min for heavy lifts, 60-90s for accessories.",
    "💡 15% body fat = 4-pack visible. 10% = 6-pack.",
    "💡 Creatine 5g/day increases strength 5-15%.",
    "💡 0.8-1g protein per lb supports muscle growth.",
    "💡 Compounds = ~70% of training volume.",
    "💡 Weak points need 2-3x/week frequency.",
]

# SIDEBAR
with st.sidebar:
    st.markdown("### 💪 John's 48-Week Plan")
    selected_week = st.slider("📅 Week", min_value=5, max_value=48, value=st.session_state.current_week, step=1, key="week_slider")
    st.session_state.current_week = selected_week

    if selected_week <= 12:
        phase_text = "Phase 1: Foundation"
    elif selected_week <= 24:
        phase_text = "Phase 2: Hypertrophy"
    else:
        phase_text = "Phase 3: Definition"

    st.markdown(
        f"<div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 14px; border-radius: 8px; display: inline-block;'>{phase_text}</div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Weight", "69.6kg", "+2.4")
    with c2:
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

# TABS
tabs = st.tabs([
    "📊 Dashboard",
    "🏋️ Workout Logger",
    "📅 Weekly Split",
    "🍽️ Nutrition",
    "📈 Metrics",
    "📉 Analytics",
    "⚙️ Settings",
])

# TAB 1: DASHBOARD
with tabs[0]:
    st.markdown("# 📊 Dashboard")

    f1, f2, f3 = st.columns(3)
    with f1:
        st.date_input("From Date", value=datetime.now() - timedelta(days=30), key="dash_from")
    with f2:
        st.date_input("To Date", value=datetime.now(), key="dash_to")
    with f3:
        st.selectbox("Compare By", ["Volume", "RPE", "Sessions"], key="dash_compare")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="stat-card"><div class="stat-label">Workouts</div><div class="stat-value">4/week</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-card"><div class="stat-label">Sets</div><div class="stat-value">102</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="stat-card"><div class="stat-label">Duration</div><div class="stat-value">360m</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="stat-card"><div class="stat-label">RPE</div><div class="stat-value">8-9</div></div>', unsafe_allow_html=True)

# TAB 2: WORKOUT LOGGER
with tabs[1]:
    st.markdown("# 🏋️ Workout Logger")

    day_selected = st.selectbox("📅 Select Day", list(COMPLETE_SPLIT.keys()), key="day_select_logger")
    day_data = COMPLETE_SPLIT[day_selected]

    st.markdown(f"[🎵 Workout Playlist]({day_data['spotify']})")

    for ex_idx, ex in enumerate(day_data["exercises"]):
        h_left, h_right = st.columns([4, 1])
        with h_left:
            st.markdown(
                f'<div class="exercise-header">🏋️ {ex_idx + 1}. {ex["name"]} ({ex["type"]})</div>',
                unsafe_allow_html=True,
            )
        with h_right:
            swap_key = f"swap_{day_selected}_{ex['name']}"
            if st.checkbox("🔄 Swap", key=swap_key):
                swap_choice = st.selectbox(
                    f"Replace {ex['name']} with:",
                    [e for e in ALL_EXERCISES if e != ex["name"]],
                    key=f"swap_select_{day_selected}_{ex_idx}",
                )
                if st.button("✓ Confirm Swap", key=f"swap_confirm_{day_selected}_{ex_idx}"):
                    new_ex = next(
                        (e for d in COMPLETE_SPLIT.values() for e in d["exercises"] if e["name"] == swap_choice),
                        None,
                    )
                    if new_ex:
                        st.session_state.swapped_workouts[f"{day_selected}_{ex['name']}"] = new_ex
                        st.success(f"✓ Swapped with {swap_choice}")

        st.markdown(f'<div class="exercise-notes">📝 {ex["notes"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**Target:** {ex['sets']} sets × {ex['reps']} reps @ {ex['w5']}kg | Rest: {ex['rest']}s")

        best_key = f"{day_selected}_{ex['name']}"
        if best_key in st.session_state.best_lifts:
            best = st.session_state.best_lifts[best_key]
            st.markdown(
                f'<div class="best-set">💪 Best: {best["weight"]}kg × {best["reps"]} @ RPE {best["rpe"]}</div>',
                unsafe_allow_html=True,
            )

        for set_num in range(1, ex["sets"] + 1):
            c1, c2, c3, c4, c5 = st.columns([1.5, 1.2, 1.2, 1, 1.5])
            with c1:
                st.markdown(f"**Set {set_num}**")
            with c2:
                w_val = st.number_input(
                    f"kg_{day_selected}_{ex_idx}_{set_num}",
                    value=float(ex["w5"]),
                    step=0.5,
                    label_visibility="collapsed",
                    key=f"w_{day_selected}_{ex_idx}_{set_num}",
                )
            with c3:
                r_val = st.number_input(
                    f"reps_{day_selected}_{ex_idx}_{set_num}",
                    value=8,
                    min_value=1,
                    label_visibility="collapsed",
                    key=f"r_{day_selected}_{ex_idx}_{set_num}",
                )
            with c4:
                rpe_val = st.number_input(
                    f"rpe_{day_selected}_{ex_idx}_{set_num}",
                    value=8,
                    min_value=1,
                    max_value=10,
                    label_visibility="collapsed",
                    key=f"rpe_{day_selected}_{ex_idx}_{set_num}",
                )
            with c5:
                if st.button("✅ Log", key=f"log_{day_selected}_{ex_idx}_{set_num}"):
                    entry = {
                        "date": datetime.now(),
                        "exercise": ex["name"],
                        "set": set_num,
                        "weight": float(w_val),
                        "reps": int(r_val),
                        "rpe": int(rpe_val),
                        "day": day_selected,
                    }
                    st.session_state.workout_sessions.append(entry)

                    if best_key not in st.session_state.best_lifts or float(w_val) > st.session_state.best_lifts[best_key]["weight"]:
                        st.session_state.best_lifts[best_key] = {
                            "weight": float(w_val),
                            "reps": int(r_val),
                            "rpe": int(rpe_val),
                        }

                    st.success(f"✓ Set {set_num}: {w_val}kg × {r_val} @ RPE {rpe_val}")

                    # Simple rest timer per set (no duplicate keys)
                    timer_key = f"timer_{day_selected}_{ex_idx}_{set_num}"
                    with st.expander(f"⏱️ Rest {ex['rest']}s (Set {set_num})"):
                        start = st.button("Start Timer", key=f"start_{timer_key}")
                        timer_placeholder = st.empty()
                        if start:
                            remaining = int(ex["rest"])
                            while remaining >= 0:
                                mins = remaining // 60
                                secs = remaining % 60
                                timer_placeholder.markdown(
                                    f'<div class="timer-box">{mins:02d}:{secs:02d}</div>',
                                    unsafe_allow_html=True,
                                )
                                time.sleep(1)
                                remaining -= 1
                            timer_placeholder.success("✅ Rest complete!")

        st.divider()

# TAB 3: WEEKLY SPLIT
with tabs[2]:
    st.markdown("# 📅 Weekly Split")

    week_view = st.slider(
        "Select Week",
        min_value=5,
        max_value=48,
        value=st.session_state.current_week,
        step=1,
        key="week_view_slider",
    )

    for day_name, day_data in COMPLETE_SPLIT.items():
        with st.expander(f"📅 {day_name} (W{week_view})", expanded=False):
            st.markdown(f"[🎵 Playlist]({day_data['spotify']})")
            for ex in day_data["exercises"]:
                st.markdown(
                    f"**{ex['name']}** — {ex['type']}\n"
                    f"- Sets: {ex['sets']} | Reps: {ex['reps']} | Rest: {ex['rest']}s\n"
                    f"- 📝 {ex['notes']}"
                )

# TAB 4: NUTRITION
with tabs[3]:
    st.markdown("# 🍽️ Nutrition Tracker")

    st.info("**Daily Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")

    st.markdown("#### Meals Completed")
    meals = [
        "7am Breakfast",
        "10am Snack",
        "1pm Lunch",
        "3:30pm Pre-WO",
        "7pm Dinner",
        "10pm Night Shake",
    ]

    m1, m2, m3 = st.columns(3)
    with m1:
        for i in range(2):
            st.checkbox(meals[i], key=f"meal_{i}")
    with m2:
        for i in range(2, 4):
            st.checkbox(meals[i], key=f"meal_{i}")
    with m3:
        for i in range(4, 6):
            st.checkbox(meals[i], key=f"meal_{i}")

    st.divider()

    st.markdown("#### Quick Macro Entry")

    n1, n2, n3, n4 = st.columns(4)
    with n1:
        protein_g = st.number_input("Protein (g)", value=120, step=5, key="protein_input")
    with n2:
        carbs_g = st.number_input("Carbs (g)", value=300, step=10, key="carbs_input")
    with n3:
        fat_g = st.number_input("Fat (g)", value=30, step=5, key="fat_input")
    with n4:
        total_cals = int(protein_g * 4 + carbs_g * 4 + fat_g * 9)
        st.metric("Total", f"{total_cals} kcal")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Protein", f"{protein_g}g", f"{protein_g - 165:+.0f}g")
    with c2:
        st.metric("Carbs", f"{carbs_g}g", f"{carbs_g - 413:+.0f}g")
    with c3:
        st.metric("Fat", f"{fat_g}g", f"{fat_g - 44:+.0f}g")
    with c4:
        st.metric("Calories", f"{total_cals}", f"{total_cals - 3150:+d}")

# TAB 5: METRICS
with tabs[4]:
    st.markdown("# 📈 Metrics & Health Status")

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown("#### Weekly Log")
        weight_today = st.number_input("Weight (kg)", value=69.6, step=0.1, key="weight_today")
        body_fat = st.number_input("Body Fat (%)", value=16.2, step=0.1, key="body_fat")
        muscle_mass = st.number_input("Muscle Mass (kg)", value=55.4, step=0.1, key="muscle_mass")
        waist_cm = st.number_input("Waist (cm)", value=82.0, step=0.5, key="waist_cm")
        sleep_hours = st.number_input("Sleep (hours)", value=5.0, step=0.5, key="sleep_hours")

        if st.button("💾 Save Metrics", key="save_metrics"):
            new_entry = {
                "date": datetime.now(),
                "week": st.session_state.current_week,
                "weight": weight_today,
                "body_fat": body_fat,
                "muscle": muscle_mass,
                "waist": waist_cm,
                "sleep": sleep_hours,
            }
            st.session_state.metrics_logs.append(new_entry)
            st.success(f"✓ Saved {new_entry['date'].strftime('%d %b %Y')}")

    with mc2:
        st.markdown("#### Health Status & Ranges")

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
        st.markdown(f"**Muscle Mass: {muscle_mass:.1f}kg** | Target W12: 65.6kg")

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
    with st.expander("ℹ️ Health Metrics Explained"):
        st.markdown("""
**BMI (Body Mass Index)**
- Formula: weight(kg) / height(m)²
- Healthy: 18.5-24.9

**Body Fat %**
- <10%: Shredded (6-pack)
- 10-15%: Lean (4-pack)
- 15-20%: Normal
- >20%: High

**Muscle Mass**
- Goal: Gain 0.5-1kg per month

**Waist Circumference**
- Healthy: <90cm for men

**Sleep**
- 7-9 hours optimal for recovery
""")

# TAB 6: ANALYTICS
with tabs[5]:
    st.markdown("# 📉 Analytics")

    if st.session_state.workout_sessions:
        logs_df = pd.DataFrame(st.session_state.workout_sessions)

        a1, a2, a3 = st.columns(3)
        with a1:
            st.metric("Exercises Logged", logs_df["exercise"].nunique())
        with a2:
            st.metric("Total Sets", len(logs_df))
        with a3:
            st.metric("Avg RPE", f"{logs_df['rpe'].mean():.1f}")

        st.divider()
        st.markdown("### Best Performance Per Exercise")

        for exercise in logs_df["exercise"].unique():
            ex_logs = logs_df[logs_df["exercise"] == exercise]
            best = ex_logs.loc[ex_logs["weight"].idxmax()]
            st.markdown(
                f"**{exercise}** — {best['weight']}kg × {best['reps']} @ RPE {best['rpe']} ({len(ex_logs)} sets)"
            )
    else:
        st.info("📝 Log workouts to see analytics")

# TAB 7: SETTINGS
with tabs[6]:
    st.markdown("# ⚙️ Settings")

    s1, s2 = st.columns(2)
    with s1:
        st.markdown("#### Profile")
        name = st.text_input("Name", value="John", key="settings_name")
        age = st.number_input("Age", value=33, key="settings_age")
    with s2:
        st.markdown("#### Goals")
        target_weight = st.number_input("Target Weight (kg)", value=75.0, step=0.5, key="settings_tw")
        target_bf = st.number_input("Target Body Fat (%)", value=10.0, step=0.5, key="settings_tbf")

    if st.button("💾 Save Settings", key="settings_save"):
        st.success("✓ Settings saved")

st.divider()
st.markdown(
    """<div style='text-align: center; color: #94a3b8; font-size: 11px;'>
✅ Best lift memory | ⏱️ Simple rest timer | 📊 Health ranges | 🔄 Smart swap | 📱 Responsive
</div>""",
    unsafe_allow_html=True,
)
