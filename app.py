"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Final Production Version V9 - Mobile Optimised, Global Timer, PR Graphs, Smart Swap
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="John's 48-Week Fitness Plan",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- CSS (Mobile-Friendly, Card-Based UI) ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

body {
    background: #020617;
    color: #e5e7eb;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: #0f172a;
    border-radius: 12px;
    padding: 6px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #1f2937;
    border-radius: 10px;
    padding: 10px 14px;
    color: #9ca3af;
    font-weight: 500;
    font-size: 13px;
}

.stTabs [aria-selected="true"] [data-baseweb="tab"] {
    background: linear-gradient(135deg, #facc15, #f97316);
    color: #111827;
}

.stat-card {
    background: #0f172a;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #1f2937;
}

.stat-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #9ca3af;
}

.stat-value {
    font-size: 22px;
    font-weight: 700;
    color: #facc15;
    margin-top: 4px;
}

.exercise-card {
    background: #0b1120;
    border-radius: 12px;
    padding: 10px 10px 8px 10px;
    border: 1px solid #1f2937;
    margin-bottom: 10px;
}

.exercise-title {
    font-size: 13px;
    font-weight: 600;
    color: #e5e7eb;
}

.exercise-sub {
    font-size: 11px;
    color: #9ca3af;
}

.exercise-notes {
    font-size: 11px;
    color: #cbd5e1;
    margin-top: 4px;
}

.best-set {
    background: #22c55e;
    color: #022c22;
    padding: 4px 8px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 600;
    display: inline-block;
    margin-top: 4px;
}

.set-row {
    display: flex;
    gap: 4px;
    align-items: center;
    margin-top: 4px;
}

.set-label {
    font-size: 11px;
    font-weight: 600;
    color: #e5e7eb;
    min-width: 40px;
}

.timer-pill {
    background: #facc15;
    color: #111827;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
}

.global-timer-box {
    background: #0b1120;
    border-radius: 12px;
    padding: 10px;
    border: 1px solid #1f2937;
    margin-top: 8px;
}

.global-timer-label {
    font-size: 11px;
    color: #9ca3af;
}

.global-timer-time {
    font-size: 20px;
    font-weight: 700;
    color: #facc15;
}

.sidebar-info {
    background: #0b1120;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #1f2937;
    font-size: 11px;
    color: #cbd5e1;
    margin-bottom: 8px;
}

.health-badge-good {
    background: #22c55e;
    color: #022c22;
    padding: 3px 8px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 600;
    display: inline-block;
}

.health-badge-warning {
    background: #f97316;
    color: #111827;
    padding: 3px 8px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 600;
    display: inline-block;
}

.health-badge-bad {
    background: #ef4444;
    color: #111827;
    padding: 3px 8px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 600;
    display: inline-block;
}

.footer-text {
    text-align: center;
    color: #6b7280;
    font-size: 11px;
    margin-top: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- SESSION STATE ----------
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
if "global_timer" not in st.session_state:
    st.session_state.global_timer = {
        "running": False,
        "end_time": None,
        "duration": 0,
    }

# ---------- SPLIT (Goal-Oriented, Hypertrophy + Abs) ----------
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
                "w12": 42.0,
                "notes": "Main shoulder builder. Neutral grip. Controlled 2s down, 1s squeeze.",
            },
            {
                "name": "DB Lateral Raise",
                "type": "HYPER",
                "sets": 4,
                "reps": "12-15",
                "rest": 60,
                "w5": 9.0,
                "w12": 12.0,
                "notes": "⭐ Weak point focus. Raise to shoulder height, slow negative.",
            },
            {
                "name": "Cable Lateral Raise",
                "type": "HYPER",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 8.0,
                "w12": 10.0,
                "notes": "Constant tension. No swinging.",
            },
            {
                "name": "Hammer Curl",
                "type": "HYPER",
                "sets": 3,
                "reps": "10-12",
                "rest": 60,
                "w5": 14.0,
                "w12": 16.0,
                "notes": "Neutral grip (elbow-safe). Pause at top.",
            },
            {
                "name": "Triceps Cable Pushdown",
                "type": "HYPER",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 21.6,
                "w12": 25.0,
                "notes": "Rope. Lockout for 1s.",
            },
            {
                "name": "Captain's Chair Leg Raise",
                "type": "ABS",
                "sets": 3,
                "reps": "15-20",
                "rest": 60,
                "w5": 0.0,
                "w12": 0.0,
                "notes": "Lower abs. Controlled, no swinging.",
            },
        ],
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
                "w12": 40.0,
                "notes": "Form priority. Chest up, below parallel.",
            },
            {
                "name": "Leg Press",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest": 180,
                "w5": 85.0,
                "w12": 95.0,
                "notes": "Full range, controlled.",
            },
            {
                "name": "Leg Extension",
                "type": "HYPER",
                "sets": 3,
                "reps": "10-12",
                "rest": 90,
                "w5": 45.0,
                "w12": 50.0,
                "notes": "Quad isolation. Squeeze at top.",
            },
            {
                "name": "RDL",
                "type": "ACC",
                "sets": 3,
                "reps": "10-12",
                "rest": 90,
                "w5": 65.0,
                "w12": 70.0,
                "notes": "Posterior chain. Neutral spine.",
            },
            {
                "name": "Lat Pulldown",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest": 180,
                "w5": 42.0,
                "w12": 48.0,
                "notes": "Full stretch, controlled negative.",
            },
            {
                "name": "Seated Row",
                "type": "MAIN",
                "sets": 4,
                "reps": "8-10",
                "rest": 180,
                "w5": 42.0,
                "w12": 48.0,
                "notes": "Chest up, squeeze shoulder blades.",
            },
            {
                "name": "Pallof Press",
                "type": "ABS",
                "sets": 2,
                "reps": "12 each",
                "rest": 60,
                "w5": 12.0,
                "w12": 15.0,
                "notes": "Anti-rotation. Core stability.",
            },
        ],
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
                "w12": 32.0,
                "notes": "Main chest builder. Controlled 2s down, 1s pause.",
            },
            {
                "name": "DB Bench Press",
                "type": "HYPER",
                "sets": 4,
                "reps": "8-10",
                "rest": 120,
                "w5": 20.0,
                "w12": 23.0,
                "notes": "Full ROM, squeeze at top.",
            },
            {
                "name": "Machine Chest Press",
                "type": "VOL",
                "sets": 3,
                "reps": "12-15",
                "rest": 90,
                "w5": 50.0,
                "w12": 55.0,
                "notes": "High-rep chest volume.",
            },
            {
                "name": "Incline DB Press",
                "type": "VOL",
                "sets": 3,
                "reps": "10-12",
                "rest": 90,
                "w5": 16.0,
                "w12": 18.0,
                "notes": "Upper chest focus.",
            },
            {
                "name": "Machine Dip",
                "type": "ACC",
                "sets": 2,
                "reps": "12-15",
                "rest": 60,
                "w5": 45.0,
                "w12": 50.0,
                "notes": "Assisted, full range.",
            },
            {
                "name": "Cable Crunch",
                "type": "ABS",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 20.0,
                "w12": 25.0,
                "notes": "Loadable abs. Focus on flexion.",
            },
            {
                "name": "Machine Ab Crunch",
                "type": "ABS",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 25.0,
                "w12": 30.0,
                "notes": "Visible abs finisher.",
            },
        ],
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
                "w12": 20.0,
                "notes": "Isolation biceps. Controlled.",
            },
            {
                "name": "Hammer Curl",
                "type": "ARM",
                "sets": 3,
                "reps": "10-12",
                "rest": 60,
                "w5": 14.0,
                "w12": 16.0,
                "notes": "Neutral grip, elbow-safe.",
            },
            {
                "name": "Triceps Pushdown",
                "type": "ARM",
                "sets": 3,
                "reps": "12-15",
                "rest": 60,
                "w5": 21.6,
                "w12": 25.0,
                "notes": "Rope, full lockout.",
            },
            {
                "name": "Leg Press Drop Set",
                "type": "VOL",
                "sets": 2,
                "reps": "Drop to fail",
                "rest": 120,
                "w5": 85.0,
                "w12": 95.0,
                "notes": "85→65→45kg, go to near-failure.",
            },
            {
                "name": "Woodchops",
                "type": "ABS",
                "sets": 3,
                "reps": "20 alt",
                "rest": 60,
                "w5": 0.0,
                "w12": 0.0,
                "notes": "Obliques, controlled rotation.",
            },
            {
                "name": "Reverse Crunch",
                "type": "ABS",
                "sets": 2,
                "reps": "15",
                "rest": 45,
                "w5": 0.0,
                "w12": 0.0,
                "notes": "Lower abs, bodyweight.",
            },
        ],
    },
}

ALL_EXERCISES = sorted({e["name"] for d in COMPLETE_SPLIT.values() for e in d["exercises"]})

DAILY_FACTS = [
    "💡 Train each muscle 2x/week for optimal growth.",
    "💡 RPE 8–9 = 1–2 reps from failure. Perfect for hypertrophy.",
    "💡 Abs grow like any muscle: load + volume + leanness.",
    "💡 Sleep 7–9h is non-negotiable for physique change.",
    "💡 Progressive overload: +0.5–1kg every 1–2 weeks.",
]

# ---------- HELPER: APPLY SMART SWAP ----------
def get_exercise(day_name: str, ex: dict) -> dict:
    key = f"{day_name}_{ex['name']}"
    if key in st.session_state.swapped_workouts:
        return st.session_state.swapped_workouts[key]
    return ex


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### 💪 John's 48-Week Plan")
    selected_week = st.slider(
        "📅 Week",
        min_value=5,
        max_value=48,
        value=st.session_state.current_week,
        step=1,
        key="week_slider",
    )
    st.session_state.current_week = selected_week

    if selected_week <= 12:
        phase_text = "Phase 1 · Foundation"
    elif selected_week <= 24:
        phase_text = "Phase 2 · Hypertrophy"
    else:
        phase_text = "Phase 3 · Definition"

    st.markdown(
        f"<div class='sidebar-info'><strong>{phase_text}</strong><br>Structured for density, strength and visible abs.</div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Weight", "69.6kg", "+2.4")
    with c2:
        st.metric("Target", "75kg", "5.4")

    st.markdown(
        "<div class='sidebar-info'><strong>Key Lifts</strong><br>"
        "Bench: 28 → 32kg (W12)<br>"
        "Lateral Raise: 9 → 12kg (W12)<br>"
        "Leg Press: 85 → 95kg (W12)</div>",
        unsafe_allow_html=True,
    )

    import random

    st.markdown(
        f"<div class='sidebar-info'>{random.choice(DAILY_FACTS)}</div>",
        unsafe_allow_html=True,
    )

    # Global Rest Timer (not per set)
    st.markdown("### ⏱ Global Rest Timer")
    duration = st.selectbox(
        "Duration",
        [60, 90, 120, 180],
        index=2,
        key="global_timer_duration",
    )

    start_global = st.button("Start Global Timer", key="start_global_timer")
    stop_global = st.button("Stop Global Timer", key="stop_global_timer")

    if start_global:
        st.session_state.global_timer["running"] = True
        st.session_state.global_timer["duration"] = duration
        st.session_state.global_timer["end_time"] = datetime.now() + timedelta(
            seconds=duration
        )

    if stop_global:
        st.session_state.global_timer["running"] = False
        st.session_state.global_timer["end_time"] = None

    with st.container():
        st.markdown("<div class='global-timer-box'>", unsafe_allow_html=True)
        st.markdown(
            "<div class='global-timer-label'>Current Rest</div>",
            unsafe_allow_html=True,
        )
        if (
            st.session_state.global_timer["running"]
            and st.session_state.global_timer["end_time"] is not None
        ):
            remaining = (
                st.session_state.global_timer["end_time"] - datetime.now()
            ).total_seconds()
            if remaining <= 0:
                st.session_state.global_timer["running"] = False
                st.session_state.global_timer["end_time"] = None
                st.markdown(
                    "<div class='global-timer-time'>00:00</div>",
                    unsafe_allow_html=True,
                )
                st.success("✅ Global rest complete")
            else:
                mins = int(remaining) // 60
                secs = int(remaining) % 60
                st.markdown(
                    f"<div class='global-timer-time'>{mins:02d}:{secs:02d}</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                "<div class='global-timer-time'>--:--</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- MAIN TABS ----------
tabs = st.tabs(
    [
        "📊 Dashboard",
        "🏋️ Workout Logger",
        "📅 Weekly Split",
        "🍽️ Nutrition",
        "📈 Metrics",
        "📉 Analytics & PRs",
        "⚙️ Settings",
    ]
)

# ---------- TAB 1: DASHBOARD ----------
with tabs[0]:
    st.markdown("### 📊 Overview")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            "<div class='stat-card'><div class='stat-label'>Workouts / Week</div>"
            "<div class='stat-value'>4</div></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            "<div class='stat-card'><div class='stat-label'>Weekly Sets</div>"
            "<div class='stat-value'>~90–110</div></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            "<div class='stat-card'><div class='stat-label'>Target RPE</div>"
            "<div class='stat-value'>8–9</div></div>",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            "<div class='stat-card'><div class='stat-label'>Abs Frequency</div>"
            "<div class='stat-value'>3×/week</div></div>",
            unsafe_allow_html=True,
        )

    st.info(
        f"Week {st.session_state.current_week} · Phase: {phase_text} · Goal: density, strength, visible abs."
    )

# ---------- TAB 2: WORKOUT LOGGER ----------
with tabs[1]:
    st.markdown("### 🏋️ Workout Logger")

    day_selected = st.selectbox(
        "Select Day",
        list(COMPLETE_SPLIT.keys()),
        key="logger_day",
    )
    day_data = COMPLETE_SPLIT[day_selected]

    st.markdown(f"[🎵 Playlist]({day_data['spotify']})")

    for ex_idx, ex in enumerate(day_data["exercises"]):
        ex_effective = get_exercise(day_selected, ex)

        st.markdown("<div class='exercise-card'>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='exercise-title'>{ex_idx + 1}. {ex_effective['name']} ({ex_effective['type']})</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='exercise-sub'>{ex_effective['sets']}×{ex_effective['reps']} · Rest {ex_effective['rest']}s · W5 {ex_effective['w5']}kg → W12 {ex_effective['w12']}kg</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='exercise-notes'>📝 {ex_effective['notes']}</div>",
            unsafe_allow_html=True,
        )

        best_key = f"{day_selected}_{ex_effective['name']}"
        if best_key in st.session_state.best_lifts:
            best = st.session_state.best_lifts[best_key]
            st.markdown(
                f"<div class='best-set'>PR: {best['weight']}kg × {best['reps']} @ RPE {best['rpe']}</div>",
                unsafe_allow_html=True,
            )

        # Smart Swap UI
        swap_col1, swap_col2 = st.columns([2, 1])
        with swap_col1:
            swap_enabled = st.checkbox(
                "🔄 Swap exercise",
                key=f"swap_chk_{day_selected}_{ex_idx}",
            )
        with swap_col2:
            if swap_enabled:
                swap_choice = st.selectbox(
                    "Swap with",
                    [e for e in ALL_EXERCISES if e != ex_effective["name"]],
                    key=f"swap_sel_{day_selected}_{ex_idx}",
                )
                if st.button(
                    "Confirm Swap",
                    key=f"swap_btn_{day_selected}_{ex_idx}",
                ):
                    # Find full exercise definition from any day
                    new_ex = next(
                        (
                            e
                            for d in COMPLETE_SPLIT.values()
                            for e in d["exercises"]
                            if e["name"] == swap_choice
                        ),
                        None,
                    )
                    if new_ex:
                        st.session_state.swapped_workouts[
                            f"{day_selected}_{ex['name']}"
                        ] = new_ex
                        st.success(f"✓ Swapped with {swap_choice}")
        # Per-set logging
        for set_num in range(1, ex_effective["sets"] + 1):
            s1, s2, s3, s4 = st.columns([1, 1, 1, 1.2])
            with s1:
                st.markdown(
                    f"<div class='set-label'>Set {set_num}</div>",
                    unsafe_allow_html=True,
                )
            with s2:
                w_val = st.number_input(
                    f"kg_{day_selected}_{ex_idx}_{set_num}",
                    value=float(ex_effective["w5"]),
                    step=0.5,
                    label_visibility="collapsed",
                    key=f"w_{day_selected}_{ex_idx}_{set_num}",
                )
            with s3:
                r_val = st.number_input(
                    f"reps_{day_selected}_{ex_idx}_{set_num}",
                    value=8,
                    min_value=1,
                    label_visibility="collapsed",
                    key=f"r_{day_selected}_{ex_idx}_{set_num}",
                )
            with s4:
                rpe_val = st.number_input(
                    f"rpe_{day_selected}_{ex_idx}_{set_num}",
                    value=8,
                    min_value=1,
                    max_value=10,
                    label_visibility="collapsed",
                    key=f"rpe_{day_selected}_{ex_idx}_{set_num}",
                )

            log_key = f"log_{day_selected}_{ex_idx}_{set_num}"
            if st.button("Log Set", key=log_key):
                entry = {
                    "date": datetime.now(),
                    "exercise": ex_effective["name"],
                    "set": set_num,
                    "weight": float(w_val),
                    "reps": int(r_val),
                    "rpe": int(rpe_val),
                    "day": day_selected,
                }
                st.session_state.workout_sessions.append(entry)

                if (
                    best_key not in st.session_state.best_lifts
                    or float(w_val)
                    > st.session_state.best_lifts[best_key]["weight"]
                ):
                    st.session_state.best_lifts[best_key] = {
                        "weight": float(w_val),
                        "reps": int(r_val),
                        "rpe": int(rpe_val),
                    }

                st.success(f"✓ {w_val}kg × {r_val} @ RPE {rpe_val}")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------- TAB 3: WEEKLY SPLIT ----------
with tabs[2]:
    st.markdown("### 📅 Weekly Split")

    week_view = st.slider(
        "Week",
        min_value=5,
        max_value=48,
        value=st.session_state.current_week,
        step=1,
        key="week_view_slider",
    )

    for day_name, day_data in COMPLETE_SPLIT.items():
        with st.expander(f"{day_name} · W{week_view}", expanded=False):
            st.markdown(f"[🎵 Playlist]({day_data['spotify']})")
            for ex in day_data["exercises"]:
                st.markdown(
                    f"- **{ex['name']}** ({ex['type']}) · {ex['sets']}×{ex['reps']} · Rest {ex['rest']}s · W5 {ex['w5']}kg → W12 {ex['w12']}kg\n"
                    f"  · 📝 {ex['notes']}"
                )

# ---------- TAB 4: NUTRITION ----------
with tabs[3]:
    st.markdown("### 🍽️ Nutrition Tracker")

    st.info("Daily target: 3,150 kcal · 165g protein · 413g carbs · 44g fat")

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

    st.markdown("#### Quick Macros")

    n1, n2, n3, n4 = st.columns(4)
    with n1:
        protein_g = st.number_input(
            "Protein (g)",
            value=120,
            step=5,
            key="protein_input",
        )
    with n2:
        carbs_g = st.number_input(
            "Carbs (g)",
            value=300,
            step=10,
            key="carbs_input",
        )
    with n3:
        fat_g = st.number_input(
            "Fat (g)",
            value=30,
            step=5,
            key="fat_input",
        )
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

# ---------- TAB 5: METRICS ----------
with tabs[4]:
    st.markdown("### 📈 Metrics & Health")

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown("#### Weekly Log")
        weight_today = st.number_input(
            "Weight (kg)",
            value=69.6,
            step=0.1,
            key="weight_today",
        )
        body_fat = st.number_input(
            "Body Fat (%)",
            value=16.2,
            step=0.1,
            key="body_fat",
        )
        muscle_mass = st.number_input(
            "Muscle Mass (kg)",
            value=55.4,
            step=0.1,
            key="muscle_mass",
        )
        waist_cm = st.number_input(
            "Waist (cm)",
            value=82.0,
            step=0.5,
            key="waist_cm",
        )
        sleep_hours = st.number_input(
            "Sleep (hours)",
            value=5.0,
            step=0.5,
            key="sleep_hours",
        )

        if st.button("Save Metrics", key="save_metrics"):
            st.session_state.metrics_logs.append(
                {
                    "date": datetime.now(),
                    "week": st.session_state.current_week,
                    "weight": weight_today,
                    "body_fat": body_fat,
                    "muscle": muscle_mass,
                    "waist": waist_cm,
                    "sleep": sleep_hours,
                }
            )
            st.success("✓ Metrics saved")

    with mc2:
        st.markdown("#### Health Status")

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

        st.markdown(
            f"**BMI:** {bmi:.1f} · <span class='{bmi_badge}'>{bmi_status}</span>",
            unsafe_allow_html=True,
        )

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

        st.markdown(
            f"**Body Fat:** {body_fat:.1f}% · <span class='{bf_badge}'>{bf_status}</span>",
            unsafe_allow_html=True,
        )

        st.markdown(f"**Muscle Mass:** {muscle_mass:.1f}kg")
        if sleep_hours >= 7:
            sleep_status = "Optimal"
            sleep_badge = "health-badge-good"
        elif sleep_hours >= 5:
            sleep_status = "Adequate"
            sleep_badge = "health-badge-warning"
        else:
            sleep_status = "Low"
            sleep_badge = "health-badge-bad"

        st.markdown(
            f"**Sleep:** {sleep_hours:.1f}h · <span class='{sleep_badge}'>{sleep_status}</span>",
            unsafe_allow_html=True,
        )

# ---------- TAB 6: ANALYTICS & PR GRAPHS ----------
with tabs[5]:
    st.markdown("### 📉 Analytics & PR Graphs")

    if st.session_state.workout_sessions:
        df = pd.DataFrame(st.session_state.workout_sessions)

        a1, a2, a3 = st.columns(3)
        with a1:
            st.metric("Exercises Logged", df["exercise"].nunique())
        with a2:
            st.metric("Total Sets", len(df))
        with a3:
            st.metric("Avg RPE", f"{df['rpe'].mean():.1f}")

        st.markdown("#### Best Performance Per Exercise")
        for exercise in df["exercise"].unique():
            ex_logs = df[df["exercise"] == exercise]
            best = ex_logs.loc[ex_logs["weight"].idxmax()]
            st.markdown(
                f"- **{exercise}** — {best['weight']}kg × {best['reps']} @ RPE {best['rpe']} ({len(ex_logs)} sets)"
            )

        st.markdown("#### PR Graphs")

        ex_choice = st.selectbox(
            "Select exercise for PR graph",
            sorted(df["exercise"].unique()),
            key="pr_ex_choice",
        )

        ex_df = df[df["exercise"] == ex_choice].copy()
        ex_df["date_only"] = ex_df["date"].dt.date
        pr_df = (
            ex_df.groupby("date_only")["weight"]
            .max()
            .reset_index()
            .rename(columns={"weight": "max_weight"})
        )

        st.line_chart(pr_df.set_index("date_only"))
    else:
        st.info("Log workouts to see analytics and PR graphs.")

# ---------- TAB 7: SETTINGS ----------
with tabs[6]:
    st.markdown("### ⚙️ Settings")

    s1, s2 = st.columns(2)
    with s1:
        name = st.text_input("Name", value="John", key="settings_name")
        age = st.number_input("Age", value=33, key="settings_age")
    with s2:
        target_weight = st.number_input(
            "Target Weight (kg)",
            value=75.0,
            step=0.5,
            key="settings_tw",
        )
        target_bf = st.number_input(
            "Target Body Fat (%)",
            value=10.0,
            step=0.5,
            key="settings_tbf",
        )

    if st.button("Save Settings", key="settings_save"):
        st.success("✓ Settings saved")

st.markdown(
    "<div class='footer-text'>✅ Mobile-friendly · ⏱ Global rest timer · 🔄 Smart swap · 📉 PR graphs · Abs built in</div>",
    unsafe_allow_html=True,
)
