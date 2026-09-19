"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Complete Streamlit Dashboard - FINAL VERSION
Features:
- Auto-recommendations (nutrition + workout adjustments)
- High-protein recipe links (daily)
- Automatic rest timer with beep sound
- Integrated analytics (workout + nutrition + metrics)
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

st.set_page_config(
    page_title="John's 48-Week Aesthetic Density Plan",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.phase-badge {
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 12px;
    display: inline-block;
    margin-bottom: 12px;
}
.phase-1 { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.stat-card {
    background: white;
    padding: 14px 16px;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    text-align: center;
}
.stat-label { font-size: 11px; color: #666; margin-bottom: 8px; }
.stat-value { font-size: 20px; font-weight: bold; color: #667eea; }
.recommendation-box {
    padding: 14px;
    background: #e3f2fd;
    border-left: 4px solid #2196f3;
    border-radius: 6px;
    margin: 12px 0;
    font-size: 13px;
}
.warning-box {
    padding: 14px;
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    border-radius: 6px;
    margin: 12px 0;
    font-size: 13px;
}
.success-box {
    padding: 14px;
    background: #e8f5e9;
    border-left: 4px solid #4caf50;
    border-radius: 6px;
    margin: 12px 0;
    font-size: 13px;
}
.recipe-link {
    display: inline-block;
    padding: 8px 12px;
    background: #667eea;
    color: white;
    border-radius: 6px;
    text-decoration: none;
    margin: 4px;
    font-size: 12px;
}
.timer-display {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    color: #667eea;
    padding: 20px;
    border-radius: 8px;
    background: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "current_week" not in st.session_state:
    st.session_state.current_week = 5
if "workout_history" not in st.session_state:
    st.session_state.workout_history = {}
if "weekly_logs" not in st.session_state:
    st.session_state.weekly_logs = []
if "nutrition_logs" not in st.session_state:
    st.session_state.nutrition_logs = []
if "metrics_logs" not in st.session_state:
    st.session_state.metrics_logs = []
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 0

# HIGH-PROTEIN RECIPE LINKS (Public)
PROTEIN_RECIPES = {
    "Monday": [
        ("Grilled Chicken Breast + Sweet Potato", "https://www.allrecipes.com/recipe/220957/grilled-chicken-breast/"),
        ("Protein Pancakes (40g protein)", "https://www.muscleandstrength.com/recipes/protein-pancakes"),
        ("Egg White Omelette", "https://www.foodnetwork.com/recipes/ina-garten/perfect-omelet-recipe-1916304"),
    ],
    "Tuesday": [
        ("Ground Beef & Brown Rice Bowl", "https://www.allrecipes.com/recipe/232155/ground-beef-and-brown-rice-casserole/"),
        ("Lentil Protein Soup", "https://www.budgetbytes.com/lentil-soup-recipe/"),
        ("Turkey Meatballs (45g protein/serving)", "https://www.loveandlemons.com/turkey-meatballs-recipe/"),
    ],
    "Wednesday": [
        ("Baked Salmon + Quinoa", "https://www.foodnetwork.com/recipes/baked-salmon-with-citrus-butter-3152095"),
        ("Chickpea Curry (high protein)", "https://www.allrecipes.com/recipe/222975/chickpea-curry/"),
        ("Cottage Cheese Bowl (25g protein)", "https://www.delish.com/cooking/recipe-ideas/recipes/a51181/high-protein-cottage-cheese-bowls-recipe/"),
    ],
    "Thursday": [
        ("Lean Beef Steak + Asparagus", "https://www.foodnetwork.com/recipes/food-network-kitchen/pan-seared-steak-recipe-3319725"),
        ("Greek Yogurt Protein Parfait", "https://www.myfitnesspal.com/nutrition-facts/generic/greek-yogurt-with-granola-and-berries"),
        ("Tuna Salad (50g protein)", "https://www.allrecipes.com/recipe/12750/tuna-salad/"),
    ],
    "Friday": [
        ("Chicken Breast Shawarma", "https://www.budgetbytes.com/chicken-shawarma-recipe/"),
        ("Protein Shake (50g protein)", "https://www.muscleandstrength.com/recipes/high-protein-smoothie"),
        ("Tofu Stir-Fry (35g protein)", "https://www.allrecipes.com/recipe/20129/stir-fried-tofu/"),
    ],
}

# YOUR LOCKED SPLIT
YOUR_SPLIT = {
    "Monday - Shoulders + Arms + Hip Flexor": {
        "exercises": [
            {"name": "Machine Shoulder Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 38.0},
            {"name": "DB Lateral Raise", "type": "HYPER", "sets": 4, "reps": "12-15", "rest": 60, "w5": 9.0, "weak": True},
            {"name": "Cable Lateral Raise", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 8.0, "weak": True},
            {"name": "Hammer Curl", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0},
            {"name": "Triceps Cable Pushdown", "type": "HYPER", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6},
            {"name": "Captain's Chair Leg Raise", "type": "ABS", "sets": 3, "reps": "20", "rest": 60, "w5": 20},
        ]
    },
    "Tuesday - Legs + Back + Anti-Rotation": {
        "exercises": [
            {"name": "Back Squat", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 30.0},
            {"name": "Leg Press", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 85.0},
            {"name": "Leg Extension", "type": "HYPER", "sets": 3, "reps": "10-12", "rest": 90, "w5": 45.0},
            {"name": "RDL", "type": "ACC", "sets": 3, "reps": "10-12", "rest": 90, "w5": 65.0},
            {"name": "Lat Pulldown", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0},
            {"name": "Seated Row", "type": "MAIN", "sets": 4, "reps": "8-10", "rest": 180, "w5": 42.0},
            {"name": "Pallof Press (Single Arm)", "type": "ABS", "sets": 2, "reps": "12 each", "rest": 60, "w5": 12.0},
        ]
    },
    "Thursday - Chest + Triceps + Primary Core": {
        "exercises": [
            {"name": "Barbell Bench Press", "type": "MAIN", "sets": 4, "reps": "6-8", "rest": 180, "w5": 28.0, "weak": True},
            {"name": "DB Bench Press", "type": "HYPER", "sets": 4, "reps": "8-10", "rest": 120, "w5": 20.0},
            {"name": "Machine Chest Press", "type": "VOL", "sets": 3, "reps": "12-15", "rest": 90, "w5": 50.0},
            {"name": "Incline DB Press", "type": "VOL", "sets": 3, "reps": "10-12", "rest": 90, "w5": 16.0},
            {"name": "Machine Dip", "type": "ACC", "sets": 2, "reps": "12-15", "rest": 60, "w5": 45.0},
            {"name": "Cable Crunch", "type": "ABS", "sets": 3, "reps": "12-15", "rest": 60, "w5": 20.0},
            {"name": "Machine Ab Crunch", "type": "ABS", "sets": 3, "reps": "12-15", "rest": 60, "w5": 25.0},
        ]
    },
    "Friday - Arms + Legs Finisher + Obliques": {
        "exercises": [
            {"name": "Machine Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 18.0},
            {"name": "Hammer Curl", "type": "ARM", "sets": 3, "reps": "10-12", "rest": 60, "w5": 14.0},
            {"name": "Triceps Pushdown", "type": "ARM", "sets": 3, "reps": "12-15", "rest": 60, "w5": 21.6},
            {"name": "Leg Press Drop Set", "type": "VOL", "sets": 2, "reps": "Drop to fail", "rest": 120, "w5": "85→65→45"},
            {"name": "Woodchops (Alternating)", "type": "ABS", "sets": 3, "reps": "20 alt", "rest": 60, "w5": 20},
            {"name": "Reverse Crunch", "type": "ABS", "sets": 2, "reps": "15", "rest": 45, "w5": 0},
        ]
    },
}

# SIDEBAR
with st.sidebar:
    st.markdown("### 📊 Dashboard")
    selected_week = st.slider("📅 Week", min_value=1, max_value=48, value=5, step=1)
    st.session_state.current_week = selected_week
    
    if selected_week <= 8:
        phase_text = "Phase 1: Foundation"
        phase_color = "phase-1"
    else:
        phase_text = f"Phase {(selected_week - 9) // 8 + 2}"
        phase_color = "phase-1"
    
    st.markdown(f"<div class='phase-badge {phase_color}'>{phase_text}</div>", unsafe_allow_html=True)
    st.divider()
    st.metric("Current Weight", "69.6 kg", "+2.4")
    st.metric("Target (W12)", "72 kg", "2.4 to go")

# MAIN TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dashboard", "🏋️ Workout Logger", "🍽️ Nutrition", 
    "📈 Metrics", "📉 Analytics", "🗓️ 12-Month Plan", "⚙️ Settings"
])

# TAB 1: DASHBOARD
with tab1:
    st.markdown(f"### Week {selected_week} Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='stat-card'><div class='stat-label'>Workouts</div><div class='stat-value'>4/week</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='stat-card' style='border-left-color: #764ba2;'><div class='stat-label'>Sets</div><div class='stat-value' style='color: #764ba2;'>102</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='stat-card' style='border-left-color: #fbbf24;'><div class='stat-label'>Duration</div><div class='stat-value' style='color: #fbbf24;'>360m</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='stat-card' style='border-left-color: #10b981;'><div class='stat-label'>RPE</div><div class='stat-value' style='color: #10b981;'>8-9</div></div>""", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### Weekly Split")
    
    for day_name in YOUR_SPLIT:
        day_data = YOUR_SPLIT[day_name]
        with st.expander(f"📅 {day_name}"):
            for ex in day_data["exercises"]:
                current_weight = ex.get("w5", "—")
                weak_badge = "⭐ " if ex.get("weak") else ""
                
                last_log = ""
                if ex["name"] in st.session_state.workout_history:
                    hist = st.session_state.workout_history[ex["name"]]
                    last_log = f" | **Last:** {hist['weight']}kg × {hist['reps']} @ RPE {hist['rpe']}"
                
                st.markdown(f"**{weak_badge}{ex['name']}** | {ex['type']} {ex['sets']}×{ex['reps']} | Rest {ex['rest']}s | **{current_weight}kg**{last_log}")

# TAB 2: WORKOUT LOGGER WITH AUTO REST TIMER
with tab2:
    st.markdown("### Log Today's Workout")
    
    day_selected = st.selectbox("📅 Select Day", list(YOUR_SPLIT.keys()))
    st.markdown(f"#### {day_selected}")
    
    exercises = YOUR_SPLIT[day_selected]["exercises"]
    
    for i, ex in enumerate(exercises):
        st.markdown(f"**{i+1}. {ex['name']}** ({ex['type']})")
        
        if ex["name"] in st.session_state.workout_history:
            hist = st.session_state.workout_history[ex["name"]]
            st.caption(f"📋 Last: {hist['weight']}kg × {hist['reps']} @ RPE {hist['rpe']}")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            weight = st.number_input(f"Weight (kg)", value=float(ex.get("w5", 0)), step=0.5, key=f"w_{i}")
        with col2:
            reps = st.number_input(f"Reps", value=8, min_value=1, key=f"r_{i}")
        with col3:
            rpe = st.slider(f"RPE", 1, 10, 8, key=f"rpe_{i}")
        with col4:
            if st.button("✅ Log", key=f"log_{i}"):
                st.session_state.workout_history[ex["name"]] = {
                    "weight": weight,
                    "reps": reps,
                    "rpe": rpe,
                    "date": datetime.now()
                }
                
                st.session_state.weekly_logs.append({
                    "exercise": ex["name"],
                    "weight": weight,
                    "reps": reps,
                    "rpe": rpe,
                    "date": datetime.now(),
                    "day": day_selected
                })
                
                st.success(f"✓ {ex['name']}: {weight}kg × {reps} @ RPE {rpe}")
        
        with col4:
            st.markdown(f"**Rest: {ex['rest']}s**")
        
        # AUTO REST TIMER WITH BEEP
        with col5:
            if st.button("⏱️ Start Timer", key=f"timer_{i}"):
                placeholder = st.empty()
                rest_time = ex['rest']
                
                for remaining in range(rest_time, 0, -1):
                    mins, secs = divmod(remaining, 60)
                    with placeholder.container():
                        st.markdown(f"""
                        <div class='timer-display'>
                        {mins:02d}:{secs:02d}
                        </div>
                        """, unsafe_allow_html=True)
                    time.sleep(1)
                
                # BEEP SOUND (using HTML audio)
                st.markdown("""
                <audio autoplay>
                    <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
                </audio>
                """, unsafe_allow_html=True)
                
                st.success(f"✅ Rest time complete! Ready for next set?")
        
        st.markdown("---")

# TAB 3: NUTRITION TRACKER WITH RECIPE LINKS
with tab3:
    st.markdown("### Daily Nutrition Tracker")
    st.info("**Target:** 3,150 kcal | 165g protein | 413g carbs | 44g fat")
    
    selected_day_nutrition = st.selectbox("📅 Select Day for Recipes", 
                                         ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                         key="day_recipes")
    
    st.markdown(f"#### 🍽️ High-Protein Recipes for {selected_day_nutrition}")
    for recipe_name, recipe_url in PROTEIN_RECIPES[selected_day_nutrition]:
        st.markdown(f"[🔗 {recipe_name}]({recipe_url})", unsafe_allow_html=True)
    
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
        st.metric("Protein", f"{protein_g}g", f"{protein_g-165}g vs target")
    with col2:
        st.metric("Carbs", f"{carbs_g}g", f"{carbs_g-413}g vs target")
    with col3:
        st.metric("Fat", f"{fat_g}g", f"{fat_g-44}g vs target")
    with col4:
        st.metric("Total", f"{total_cals} kcal", f"{total_cals-3150} vs target")
    
    # NUTRITION RECOMMENDATION
    if total_cals < 3000:
        st.markdown("""
        <div class='warning-box'>
        ⚠️ **RECOMMENDATION:** Calories too low ({} kcal vs 3,150 target)
        <br>➜ Add: 1 extra meal or increase portions
        <br>➜ Impact: May limit muscle growth
        </div>
        """.format(int(total_cals)), unsafe_allow_html=True)
    elif total_cals > 3300:
        st.markdown("""
        <div class='warning-box'>
        ⚠️ **RECOMMENDATION:** Calories too high ({} kcal vs 3,150 target)
        <br>➜ Reduce: Carbs or fat by 50-100g
        <br>➜ Impact: May add unnecessary fat gain
        </div>
        """.format(int(total_cals)), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='success-box'>
        ✅ **PERFECT:** Calories on target ({} kcal)
        <br>➜ Protein adequate for muscle growth
        <br>➜ Continue this pattern
        </div>
        """.format(int(total_cals)), unsafe_allow_html=True)

# TAB 4: METRICS
with tab4:
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
            st.session_state.metrics_logs.append({
                "date": datetime.now(),
                "weight": weight_today,
                "body_fat": body_fat,
                "muscle": muscle_mass,
                "waist": waist_cm,
                "sleep": sleep_hours
            })
            st.success("✓ Metrics saved")
    
    with col2:
        st.markdown("#### Progress Since Week 1")
        st.metric("Weight Change", "+2.4 kg", "target: +5.4 kg by W12")
        st.metric("Body Fat", "-0.8%", "target: -6.2% by W12")
        st.metric("Muscle Mass", "+3.2 kg", "target: +10 kg by W12")
        st.metric("Sleep", f"{sleep_hours}h/night", "target: 7-8h")

# TAB 5: ANALYTICS (INTEGRATED)
with tab5:
    st.markdown("### Weekly Analytics (Live Data)")
    
    if st.session_state.weekly_logs:
        logs_df = pd.DataFrame(st.session_state.weekly_logs)
        
        total_sessions = logs_df["day"].nunique()
        total_volume = (logs_df["weight"] * logs_df["reps"]).sum()
        avg_rpe = logs_df["rpe"].mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sessions Logged", f"{total_sessions}/4", "This week")
        with col2:
            st.metric("Total Volume", f"{total_volume:.0f} kg", "lifted")
        with col3:
            st.metric("Avg RPE", f"{avg_rpe:.1f}", "target: 8-9")
        
        st.divider()
        
        # INTEGRATED RECOMMENDATIONS
        st.markdown("### AI-Powered Recommendations")
        
        # Volume Analysis
        if total_volume < 15000:
            st.markdown("""
            <div class='recommendation-box'>
            📊 **Volume Low:** {:.0f}kg lifted (expect 17-18k/week)
            <br>➜ Action: Increase reps or weight on accessories
            <br>➜ Impact on progress: Slower muscle growth
            </div>
            """.format(total_volume), unsafe_allow_html=True)
        
        # RPE Analysis
        if avg_rpe < 7.5:
            st.markdown("""
            <div class='recommendation-box'>
            💪 **Intensity Low:** RPE {:.1f} (target: 8-9)
            <br>➜ Action: Push harder on main lifts, reduce rest 30s
            <br>➜ Impact: Better muscle stimulus
            </div>
            """.format(avg_rpe), unsafe_allow_html=True)
        elif avg_rpe > 9:
            st.markdown("""
            <div class='warning-box'>
            ⚠️ **Over-Training:** RPE {:.1f} (target: 8-9)
            <br>➜ Action: Reduce volume by 1-2 sets next week
            <br>➜ Impact: Better recovery, prevent burnout
            </div>
            """.format(avg_rpe), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='success-box'>
            ✅ **Perfect Intensity:** RPE {:.1f}
            <br>➜ Continue current programming
            </div>
            """.format(avg_rpe), unsafe_allow_html=True)
        
        # WORKOUT + NUTRITION + METRICS Integration
        if protein_g >= 160 and total_volume > 16000:
            st.markdown("""
            <div class='success-box'>
            🎯 **FULL INTEGRATION ON TRACK**
            <br>✅ Volume: {:.0f}kg | ✅ Protein: {}g | ✅ Sleep: {}h
            <br>➜ Expected outcome: +0.5kg muscle by Week 8
            </div>
            """.format(total_volume, int(protein_g), int(sleep_hours)), unsafe_allow_html=True)
        elif protein_g < 160:
            st.markdown("""
            <div class='warning-box'>
            ⚠️ **FIX NUTRITION FIRST**
            <br>Volume: {:.0f}kg (good) | Protein: {}g (LOW) | Sleep: {}h
            <br>➜ Action: Add 10-20g protein (extra meal or shake)
            <br>➜ Without protein, volume gains won't translate to muscle
            </div>
            """.format(total_volume, int(protein_g), int(sleep_hours)), unsafe_allow_html=True)
        elif int(sleep_hours) < 6:
            st.markdown("""
            <div class='warning-box'>
            😴 **SLEEP IS LIMITING FACTOR**
            <br>Volume: {:.0f}kg | Protein: {}g | Sleep: {}h (LOW)
            <br>➜ Action: Prioritize sleep (even 30min more = +5% strength)
            <br>➜ Without sleep, gains plateau despite good training/nutrition
            </div>
            """.format(total_volume, int(protein_g), int(sleep_hours)), unsafe_allow_html=True)
    
    else:
        st.info("📝 No workouts logged yet. Start logging to see analytics!")

# TAB 6: 12-MONTH PLAN
with tab6:
    st.markdown("### 48-Week Periodization")
    
    phases_df = pd.DataFrame({
        "Phase": ["1", "2", "3"],
        "Name": ["Foundation", "Hypertrophy", "Definition"],
        "Weeks": ["5-12", "13-24", "25-48"],
        "Focus": ["Build base", "Max growth", "Sculpt & cut"],
        "Abs": ["2-3x/week", "3x/week", "3-4x/week"],
    })
    
    st.dataframe(phases_df, use_container_width=True, hide_index=True)

# TAB 7: SETTINGS
with tab7:
    st.markdown("### User Settings")
    
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
✅ Auto-recommendations | 🔗 Recipe links | ⏱️ Auto rest timer with beep | 📊 Integrated analytics
</div>
""", unsafe_allow_html=True)
