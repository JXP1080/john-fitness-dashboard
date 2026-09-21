"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Final Production Version V7.2 - Mobile Optimized Workout Logger
Sets displayed horizontally in compact single-screen view
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="John's 48-Week Fitness Plan",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# RESPONSIVE CSS - MOBILE OPTIMIZED
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
body { background: #0f172a; color: #e2e8f0; }

.stat-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-left: 4px solid #667eea;
    padding: 16px;
    border-radius: 12px;
    margin: 8px 0;
}

.stat-value { font-size: 28px; font-weight: 700; color: #667eea; }
.stat-label { font-size: 12px; color: #94a3b8; }

.exercise-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 12px; border-radius: 8px; color: white; font-weight: 600;
    font-size: 14px; margin: 14px 0 6px 0;
}

.exercise-notes {
    background: #1e293b; border-left: 3px solid #667eea;
    padding: 8px; border-radius: 6px; font-size: 11px; color: #cbd5e1;
    margin: 4px 0 8px 0;
}

.best-set {
    background: #10b981; color: white; padding: 4px 8px;
    border-radius: 6px; font-size: 10px; font-weight: 600; display: inline-block;
    margin: 4px 0;
}

.timer-display {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white; padding: 16px; border-radius: 12px; text-align: center;
    font-size: 42px; font-weight: bold; font-family: 'Courier New', monospace;
}

.sidebar-info {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155; border-left: 3px solid #10b981;
    padding: 12px; border-radius: 8px; margin: 8px 0; font-size: 12px;
}

/* COMPACT SET ROW - HORIZONTAL LAYOUT */
.set-row {
    background: #1e293b;
    border: 1px solid #334155;
    border-left: 3px solid #10b981;
    padding: 8px;
    border-radius: 6px;
    margin: 4px 0;
    display: flex;
    gap: 6px;
    align-items: center;
    font-size: 12px;
    flex-wrap: wrap;
}

.set-number {
    background: #667eea;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: 600;
    min-width: 35px;
    text-align: center;
}

.set-input {
    flex: 1;
    min-width: 60px;
}

.set-input input {
    width: 100%;
    background: #0f172a;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 4px;
    font-size: 11px;
}

.set-button {
    background: #10b981;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
    cursor: pointer;
    font-size: 11px;
    font-weight: 600;
}

.set-button:hover {
    background: #059669;
}

/* MOBILE RESPONSIVE */
@media (max-width: 768px) {
    .stat-value { font-size: 20px; }
    .timer-display { font-size: 36px; padding: 12px; }
    .exercise-header { font-size: 13px; padding: 10px; }
    
    .set-row {
        padding: 6px;
        gap: 4px;
    }
    
    .set-input input {
        font-size: 10px;
        padding: 3px;
    }
    
    .set-button {
        padding: 3px 6px;
        font-size: 10px;
    }
    
    .set-number {
        min-width: 30px;
        padding: 3px 6px;
        font-size: 10px;
    }
}

@media (max-width: 480px) {
    body { font-size: 12px; }
    .exercise-header { font-size: 12px; padding: 8px; }
    .exercise-notes { font-size: 10px; padding: 6px; }
    
    .set-row {
        padding: 4px;
        gap: 2px;
    }
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
if "best_lifts" not in st.session_state:
    st.session_state.best_lifts = {}

# SPLIT DATA
COMPLETE_SPLIT = {
    "Monday - Shoulders + Arms": {
        "playlist": "RapidFire Workout Mix",
        "exercises": [
            {"name": "Machine Shoulder Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 38.0, "notes": "Neutral grip. Controlled (2s). Squeeze (1s)."},
            {"name": "DB Lateral Raise", "type": "HYPER", "sets": 4, "reps": "12-15", "rest": 60, "w5": 9.0, "notes": "⭐ PRIORITY. Shoulder height. Control (2s)."},
            {"name": "Cable Lateral Raise", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 8.0, "notes": "⭐ PRIORITY. Constant tension."},
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "notes": "Neutral grip. Pause (1s). Full ROM."},
            {"name": "Triceps Cable Pushdown", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "notes": "Rope. Lock out (1s)."},
            {"name": "Captain's Chair Leg Raise", "type": "ABS", "sets": 3, "reps": "20", "rest": 60, "w5": 0.0, "notes": "Controlled. Pause (1s)."},
        ]
    },
    "Tuesday - Legs + Back": {
        "playlist": "Pump Iron - Gym Motivation",
        "exercises": [
            {"name": "Back Squat", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 30.0, "notes": "Form priority. Chest up. Below parallel."},
            {"name": "Leg Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 85.0, "notes": "Full range. Controlled (2s)."},
            {"name": "Leg Extension", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 90, "w5": 45.0, "notes": "Isolation. Squeeze (1s)."},
            {"name": "RDL", "type": "ACC", "sets": 3, "reps": "10-12", "rest": 90, "w5": 65.0, "notes": "Posterior chain. Straight back."},
            {"name": "Lat Pulldown", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0, "notes": "Controlled negative. Full stretch."},
            {"name": "Seated Row", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0, "notes": "Chest forward. Squeeze (1s)."},
            {"name": "Pallof Press", "type": "ABS", "sets": 2, "reps": "12 each", "rest": 60, "w5": 12.0, "notes": "Anti-rotation. Single arm."},
        ]
    },
    "Thursday - Chest + Triceps": {
        "playlist": "Beast Mode - Chest Day",
        "exercises": [
            {"name": "Barbell Bench Press", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 28.0, "notes": "⭐ PRIORITY. Controlled (2s). Pause (1s)."},
            {"name": "DB Bench Press", "type": "HYPER", "sets": 4, "reps": "8-10", "rest": 120, "w5": 20.0, "notes": "Full range. Squeeze (1s)."},
            {"name": "Machine Chest Press", "type": "VOL", "sets": 3, "reps": "12-15", "rest": 90, "w5": 50.0, "notes": "High reps. Controlled."},
            {"name": "Incline DB Press", "type": "VOL", "sets": 3, "reps": "10-12", "rest": 90, "w5": 16.0, "notes": "Upper chest. Full ROM."},
            {"name": "Machine Dip", "type": "ACC", "sets": 2, "reps": "12-15", "rest": 60, "w5": 45.0, "notes": "Assisted. Full range."},
            {"name": "Cable Crunch", "type": "ABS", "sets": 3, "reps": "12-15", "rest": 60, "w5": 20.0, "notes": "Core work. Light."},
            {"name": "Machine Ab Crunch", "type": "ABS", "sets": 3, "reps": "12-15", "rest": 60, "w5": 25.0, "notes": "Visible abs. Finisher."},
        ]
    },
    "Friday - Arms + Legs": {
        "playlist": "Pump It Up - Training Hits",
        "exercises": [
            {"name": "Machine Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 18.0, "notes": "Isolation. Controlled."},
            {"name": "Hammer Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0, "notes": "Neutral grip. Full ROM."},
            {"name": "Triceps Pushdown", "type": "ARM", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6, "notes": "Rope. Lock out."},
            {"name": "Leg Press Drop Set", "type": "VOL", "sets": 2, "reps": "Drop to fail", "rest": 120, "w5": 85.0, "notes": "Finisher. 85→65→45."},
            {"name": "Woodchops", "type": "ABS", "sets": 3, "reps": "20 alt", "rest": 60, "w5": 0.0, "notes": "Obliques. Alternating."},
            {"name": "Reverse Crunch", "type": "ABS", "sets": 2, "reps": "15", "rest": 45, "w5": 0.0, "notes": "Lower abs. Bodyweight."},
        ]
    },
}

ALL_EXERCISES = []
for day_data in COMPLETE_SPLIT.values():
    ALL_EXERCISES.extend([e['name'] for e in day_data['exercises']])
ALL_EXERCISES = sorted(list(set(ALL_EXERCISES)))

DAILY_FACTS = [
    "💡 Protein synthesis peaks 24-48 hours after training.",
    "💡 Sleep is muscle growth time. Aim 7-9 hours.",
    "💡 Progressive overload: +0.5-1kg every 1-2 weeks.",
    "💡 RPE 8-9 = 1-2 reps from failure. Optimal.",
    "💡 Heavy lifts: 3min rest. Accessories: 60-90s.",
    "💡 10% body fat = visible 6-pack.",
    "💡 Creatine 5g/day boosts strength 5-15%.",
    "💡 Eat 0.8-1g protein per lb bodyweight.",
    "💡 Compounds = 70% of training volume.",
    "💡 Weak points need 2-3x/week frequency.",
]

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
    
    st.markdown(f"<div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 14px; border-radius: 8px;'>{phase_text}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weight", "69.6kg", "+2.4")
    with col2:
        st.metric("Target", "75kg", "5.4")
    
    st.divider()
    
    st.markdown("### 📊 Key Lifts")
    st.markdown('<div class="sidebar-info"><strong>Bench</strong><br>28kg → 32kg</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info"><strong>Lateral Raise</strong><br>9kg → 12kg</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-info"><strong>Leg Press</strong><br>85kg → 95kg</div>', unsafe_allow_html=True)
    
    st.divider()
    
    import random
    daily_fact = random.choice(DAILY_FACTS)
    st.markdown(f'<div class="sidebar-info">{daily_fact}</div>', unsafe_allow_html=True)

# MAIN TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dashboard",
    "🏋️ Workout Logger",
    "📅 Weekly Split",
    "🍽️ Nutrition",
    "📈 Metrics",
    "📉 Analytics",
    "⚙️ Settings"
])

# TAB 1: DASHBOARD
with tab1:
    st.markdown("# 📊 Dashboard")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.date_input("From", value=datetime.now() - timedelta(days=30), key="dash_from")
    with col_f2:
        st.date_input("To", value=datetime.now(), key="dash_to")
    with col_f3:
        st.selectbox("Compare", ["Volume", "RPE", "Sessions"], key="dash_compare")
    
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
    
    st.info(f"📈 Week {st.session_state.current_week} tracking active")

# TAB 2: WORKOUT LOGGER - MOBILE OPTIMIZED
with tab2:
    st.markdown("# 🏋️ Workout Logger")
    
    day_select = st.selectbox("📅 Select Day", list(COMPLETE_SPLIT.keys()), key="day_logger")
    day_info = COMPLETE_SPLIT[day_select]
    
    st.markdown(f"🎵 **Playlist:** {day_info['playlist']}")
    st.divider()
    
    for ex_idx, exercise in enumerate(day_info['exercises']):
        st.markdown(f'<div class="exercise-header">🏋️ {ex_idx + 1}. {exercise["name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exercise-notes">{exercise["notes"]}</div>', unsafe_allow_html=True)
        st.markdown(f"**{exercise['sets']}×{exercise['reps']} @ {exercise['w5']}kg** | Rest: {exercise['rest']}s")
        
        best_key = f"{day_select}_{exercise['name']}"
        if best_key in st.session_state.best_lifts:
            best = st.session_state.best_lifts[best_key]
            st.markdown(f'<div class="best-set">💪 Best: {best["weight"]}kg × {best["reps"]} @ RPE {best["rpe"]}</div>', unsafe_allow_html=True)
        
        # COMPACT SET ROWS - HORIZONTAL LAYOUT
        for set_num in range(1, int(exercise['sets']) + 1):
            col1, col2, col3, col4, col5 = st.columns([0.8, 1, 1, 1, 1])
            
            with col1:
                st.markdown(f"<div style='font-weight:600; color:#667eea;'>S{set_num}</div>", unsafe_allow_html=True)
            with col2:
                w = st.number_input(f"kg#{ex_idx}_{set_num}", value=float(exercise['w5']), step=0.5, label_visibility="collapsed", key=f"w_{ex_idx}_{set_num}")
            with col3:
                r = st.number_input(f"R#{ex_idx}_{set_num}", value=8, min_value=1, label_visibility="collapsed", key=f"r_{ex_idx}_{set_num}")
            with col4:
                rpe = st.number_input(f"RPE#{ex_idx}_{set_num}", value=8, min_value=1, max_value=10, label_visibility="collapsed", key=f"rpe_{ex_idx}_{set_num}")
            with col5:
                if st.button("✅", key=f"log_{ex_idx}_{set_num}_{day_select}"):
                    st.session_state.workout_sessions.append({
                        "date": datetime.now(),
                        "exercise": exercise['name'],
                        "set": set_num,
                        "weight": float(w),
                        "reps": int(r),
                        "rpe": int(rpe),
                        "day": day_select
                    })
                    
                    if best_key not in st.session_state.best_lifts or float(w) > st.session_state.best_lifts[best_key]["weight"]:
                        st.session_state.best_lifts[best_key] = {
                            "weight": float(w),
                            "reps": int(r),
                            "rpe": int(rpe)
                        }
                    
                    st.success(f"✓ {w}kg × {r} @ RPE {rpe}")
        
        # COMPACT TIMER
        with st.expander(f"⏱️ {exercise['rest']}s rest"):
            rest_secs = int(exercise['rest'])
            timer_ph = st.empty()
            
            for remaining in range(rest_secs, 0, -1):
                mins = remaining // 60
                secs = remaining % 60
                timer_ph.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                time.sleep(1)
            
            st.markdown("""<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>""", unsafe_allow_html=True)
            timer_ph.success("✅ Done!")
        
        st.divider()

# TAB 3: WEEKLY SPLIT
with tab3:
    st.markdown("# 📅 Weekly Split")
    
    week_view = st.slider("Week", min_value=5, max_value=48, value=st.session_state.current_week, step=1, key="w_slider")
    
    for day_name, day_data in COMPLETE_SPLIT.items():
        with st.expander(f"📅 {day_name} (W{week_view})"):
            st.markdown(f"🎵 **{day_data['playlist']}**")
            
            for ex in day_data['exercises']:
                st.markdown(f"**{ex['name']}**\n{ex['sets']}×{ex['reps']} | Rest: {ex['rest']}s\n{ex['notes']}\n")

# TAB 4: NUTRITION
with tab4:
    st.markdown("# 🍽️ Nutrition")
    
    st.info("**Daily Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    st.markdown("#### Meals")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.checkbox("7am Breakfast", key="m1")
        st.checkbox("10am Snack", key="m2")
    with m2:
        st.checkbox("1pm Lunch", key="m3")
        st.checkbox("3:30pm Pre-WO", key="m4")
    with m3:
        st.checkbox("7pm Dinner", key="m5")
        st.checkbox("10pm Night", key="m6")
    
    st.divider()
    
    st.markdown("#### Macros")
    nc1, nc2, nc3, nc4 = st.columns(4)
    with nc1:
        p = st.number_input("Protein (g)", value=120.0, step=5.0, key="n_p")
    with nc2:
        c = st.number_input("Carbs (g)", value=300.0, step=10.0, key="n_c")
    with nc3:
        f = st.number_input("Fat (g)", value=30.0, step=5.0, key="n_f")
    with nc4:
        total = int(p * 4 + c * 4 + f * 9)
        st.metric("Cals", f"{total}")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.metric("P", f"{p:.0f}g", f"{p - 165:+.0f}g")
    with sc2:
        st.metric("C", f"{c:.0f}g", f"{c - 413:+.0f}g")
    with sc3:
        st.metric("F", f"{f:.0f}g", f"{f - 44:+.0f}g")
    with sc4:
        st.metric("Total", f"{total}", f"{total - 3150:+d}")

# TAB 5: METRICS
with tab5:
    st.markdown("# 📈 Metrics & Health")
    
    mc1, mc2 = st.columns(2)
    
    with mc1:
        st.markdown("#### Log")
        weight = st.number_input("Weight (kg)", value=69.6, step=0.1, key="m_weight")
        bf = st.number_input("Body Fat (%)", value=16.2, step=0.1, key="m_bf")
        muscle = st.number_input("Muscle (kg)", value=55.4, step=0.1, key="m_muscle")
        waist = st.number_input("Waist (cm)", value=82.0, step=0.5, key="m_waist")
        sleep = st.number_input("Sleep (h)", value=5.0, step=0.5, key="m_sleep")
        
        if st.button("💾 Save", key="m_save"):
            st.session_state.metrics_logs.append({
                "date": datetime.now(),
                "week": st.session_state.current_week,
                "weight": weight,
                "body_fat": bf,
                "muscle": muscle,
                "waist": waist,
                "sleep": sleep
            })
            st.success("✓ Saved")
    
    with mc2:
        st.markdown("#### Status")
        
        bmi = weight / (1.76 ** 2)
        bmi_s = "Healthy" if 18.5 <= bmi < 25 else ("Underweight" if bmi < 18.5 else ("Overweight" if bmi < 30 else "Obese"))
        st.markdown(f"**BMI:** {bmi:.1f} | {bmi_s}")
        
        bf_s = "Shredded" if bf < 10 else ("Lean" if bf < 15 else ("Normal" if bf < 20 else "High"))
        st.markdown(f"**BF:** {bf:.1f}% | {bf_s}")
        
        st.markdown(f"**Muscle:** {muscle:.1f}kg")
        
        sleep_s = "Optimal" if sleep >= 7 else ("Adequate" if sleep >= 5 else "Low")
        st.markdown(f"**Sleep:** {sleep:.1f}h | {sleep_s}")

# TAB 6: ANALYTICS
with tab6:
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
with tab7:
    st.markdown("# ⚙️ Settings")
    
    s1, s2 = st.columns(2)
    
    with s1:
        st.markdown("#### Profile")
        st.text_input("Name", value="John", key="s_name")
        st.number_input("Age", value=33, key="s_age")
    
    with s2:
        st.markdown("#### Goals")
        st.number_input("Target Weight", value=75.0, step=0.5, key="s_tw")
        st.number_input("Target BF", value=10.0, step=0.5, key="s_tbf")
    
    if st.button("💾 Save", key="s_save"):
        st.success("✓ Settings saved")

# FOOTER
st.divider()
st.markdown("""<div style='text-align: center; color: #94a3b8; font-size: 11px;'>
✅ Compact mobile view | 🏋️ Per-set tracking | 💪 Best lift memory | ⏱️ Rest timer | 📊 Health ranges | 📱 Responsive
</div>""", unsafe_allow_html=True)
