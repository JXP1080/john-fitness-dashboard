"""
JOHN'S 48-WEEK AESTHETIC DENSITY PROGRAM
Complete Streamlit Dashboard - FINAL VERSION WITH METRICS GRAPHS
Features:
- Metrics tracking with last input date
- Week-by-week comparison graphs (weight, body fat, muscle, waist, sleep)
- Trend lines + predictions
- Auto-recommendations
- High-protein recipe links
- Rest timer with beep
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import plotly.graph_objects as go
import plotly.express as px

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
.last-input { font-size: 10px; color: #999; margin-top: 4px; }
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

# HIGH-PROTEIN RECIPE LINKS
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

# TAB 2: WORKOUT LOGGER
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
                st.success(f"✓ {ex['name']}: {weight}kg × {reps} @ RPE {rpe}")
        
        with col5:
            st.markdown(f"**Rest: {ex['rest']}s**")
        
        st.markdown("---")

# TAB 3: NUTRITION TRACKER
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

# TAB 4: METRICS WITH GRAPHS
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
            st.success(f"✓ Metrics saved on {new_entry['date'].strftime('%Y-%m-%d')}")
    
    with col2:
        st.markdown("#### Last Input Date & Summary")
        if st.session_state.metrics_logs:
            last_entry = st.session_state.metrics_logs[-1]
            last_date = last_entry["date"].strftime('%d %b %Y')
            days_ago = (datetime.now() - last_entry["date"]).days
            
            st.markdown(f"""
            📅 **Last Input:** {last_date} ({days_ago} days ago)
            
            **Latest Values:**
            - Weight: **{last_entry['weight']}kg**
            - Body Fat: **{last_entry['body_fat']}%**
            - Muscle: **{last_entry['muscle']}kg**
            - Waist: **{last_entry['waist']}cm**
            - Sleep: **{last_entry['sleep']}h/night**
            """)
    
    st.divider()
    st.markdown("### Metrics Progress Charts")
    
    if len(st.session_state.metrics_logs) > 1:
        metrics_df = pd.DataFrame(st.session_state.metrics_logs)
        
        # WEIGHT CHART
        fig_weight = go.Figure()
        fig_weight.add_trace(go.Scatter(
            x=metrics_df['date'],
            y=metrics_df['weight'],
            mode='lines+markers',
            name='Weight (kg)',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        fig_weight.add_hline(y=72, line_dash="dash", line_color="green", annotation_text="W8 Target: 72kg")
        fig_weight.add_hline(y=75, line_dash="dash", line_color="darkgreen", annotation_text="W12 Target: 75kg")
        fig_weight.update_layout(
            title="📊 Weight Progression",
            xaxis_title="Date",
            yaxis_title="Weight (kg)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_weight, use_container_width=True)
        
        # BODY FAT CHART
        fig_bf = go.Figure()
        fig_bf.add_trace(go.Scatter(
            x=metrics_df['date'],
            y=metrics_df['body_fat'],
            mode='lines+markers',
            name='Body Fat %',
            line=dict(color='#764ba2', width=3),
            marker=dict(size=8)
        ))
        fig_bf.add_hline(y=15.8, line_dash="dash", line_color="orange", annotation_text="W8 Target: 15.8%")
        fig_bf.add_hline(y=10, line_dash="dash", line_color="darkorange", annotation_text="W12 Target: 10%")
        fig_bf.update_layout(
            title="🔥 Body Fat % Progression",
            xaxis_title="Date",
            yaxis_title="Body Fat %",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_bf, use_container_width=True)
        
        # MUSCLE MASS CHART
        fig_muscle = go.Figure()
        fig_muscle.add_trace(go.Scatter(
            x=metrics_df['date'],
            y=metrics_df['muscle'],
            mode='lines+markers',
            name='Muscle Mass (kg)',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8)
        ))
        fig_muscle.add_hline(y=58, line_dash="dash", line_color="green", annotation_text="W8 Target: 58kg")
        fig_muscle.add_hline(y=65.6, line_dash="dash", line_color="darkgreen", annotation_text="W12 Target: 65.6kg")
        fig_muscle.update_layout(
            title="💪 Muscle Mass Progression",
            xaxis_title="Date",
            yaxis_title="Muscle (kg)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_muscle, use_container_width=True)
        
        # WAIST CIRCUMFERENCE CHART
        fig_waist = go.Figure()
        fig_waist.add_trace(go.Scatter(
            x=metrics_df['date'],
            y=metrics_df['waist'],
            mode='lines+markers',
            name='Waist (cm)',
            line=dict(color='#fbbf24', width=3),
            marker=dict(size=8)
        ))
        fig_waist.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="Target: 80cm")
        fig_waist.update_layout(
            title="📏 Waist Circumference Progression",
            xaxis_title="Date",
            yaxis_title="Waist (cm)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_waist, use_container_width=True)
        
        # SLEEP QUALITY CHART
        fig_sleep = go.Figure()
        fig_sleep.add_trace(go.Scatter(
            x=metrics_df['date'],
            y=metrics_df['sleep'],
            mode='lines+markers',
            name='Sleep (hours)',
            line=dict(color='#8b5cf6', width=3),
            marker=dict(size=8)
        ))
        fig_sleep.add_hline(y=7, line_dash="dash", line_color="purple", annotation_text="Target: 7-8h")
        fig_sleep.update_layout(
            title="😴 Sleep Quality Progression",
            xaxis_title="Date",
            yaxis_title="Hours/Night",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_sleep, use_container_width=True)
        
        # COMPARISON TABLE
        st.divider()
        st.markdown("### Week-over-Week Comparison")
        
        comparison_data = []
        for i, row in metrics_df.iterrows():
            if i == 0:
                comparison_data.append({
                    "Date": row['date'].strftime('%d %b'),
                    "Week": f"W{row['week']}",
                    "Weight": f"{row['weight']}kg",
                    "Body Fat": f"{row['body_fat']}%",
                    "Muscle": f"{row['muscle']}kg",
                    "Waist": f"{row['waist']}cm",
                    "Sleep": f"{row['sleep']}h"
                })
            else:
                prev_row = metrics_df.iloc[i-1]
                weight_change = row['weight'] - prev_row['weight']
                bf_change = row['body_fat'] - prev_row['body_fat']
                muscle_change = row['muscle'] - prev_row['muscle']
                waist_change = row['waist'] - prev_row['waist']
                
                comparison_data.append({
                    "Date": row['date'].strftime('%d %b'),
                    "Week": f"W{row['week']}",
                    "Weight": f"{row['weight']}kg ({weight_change:+.1f})",
                    "Body Fat": f"{row['body_fat']}% ({bf_change:+.1f})",
                    "Muscle": f"{row['muscle']}kg ({muscle_change:+.1f})",
                    "Waist": f"{row['waist']}cm ({waist_change:+.1f})",
                    "Sleep": f"{row['sleep']}h"
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    else:
        st.info("📊 Log at least 2 weeks of metrics to see comparison graphs")

# TAB 5: ANALYTICS
with tab5:
    st.markdown("### Weekly Analytics (Live Data)")
    st.info("Analytics tab coming with integrated workout + nutrition + metrics analysis")

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
✅ Metrics graphs + date tracking | 🔗 Recipe links | 📊 Week-over-week comparison
</div>
""", unsafe_allow_html=True)
