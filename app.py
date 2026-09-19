"""
JOHN'S FITNESS DASHBOARD
Week 5 - Phase 1 Tracker
12-Month Transformation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="John's Fitness Dashboard",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if 'meals' not in st.session_state:
    st.session_state.meals = []
if 'exercises' not in st.session_state:
    st.session_state.exercises = []
if 'metrics' not in st.session_state:
    st.session_state.metrics = [
        {'date': '2026-09-19', 'weight': 69.6, 'fat': 16.2, 'muscle': 55.4, 'waist': 82, 'sleep': 5.0}
    ]

# ============================================================================
# HEADER
# ============================================================================

col1, col2 = st.columns([2, 1])
with col1:
    st.title("💪 John's Fitness Dashboard")
    st.subheader("Week 5 - Phase 1: Foundation + Density")
with col2:
    st.info("Week 5 | Phase 1\n69.6kg → 75kg\n16.2% → 10% fat")

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Section:", [
    "📊 Dashboard",
    "🍽️ Nutrition",
    "🏋️ Training",
    "📈 Metrics",
    "📉 Analytics",
    "🎯 12-Month Plan"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
st.sidebar.metric("Weight", "69.6 kg", "+0.3 kg")
st.sidebar.metric("Body Fat", "16.2%", "Stable")
st.sidebar.metric("Workouts", "3/4", "75%")
st.sidebar.metric("Nutrition", "92%", "Good")

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================

if page == "📊 Dashboard":
    st.markdown("## Weekly Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Weight", "69.6 kg", "+0.3 kg")
    with col2:
        st.metric("Body Fat", "16.2%", "Stable")
    with col3:
        st.metric("Muscle Mass", "55.4 kg", "+0.2 kg")
    with col4:
        st.metric("Sleep Avg", "5.2h", "⚠️ Low")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 This Week's Workouts")
        workouts = pd.DataFrame({
            'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
            'Focus': ['Upper A', 'Lower A', 'Upper B', 'Lower B'],
            'Main Lift': ['Bench 78kg', 'Squat 82kg', 'Hammer 16kg', 'RDL 85kg'],
            'Status': ['✓ Done', '✓ Done', '○ Pending', '○ Pending']
        })
        st.dataframe(workouts, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 This Week Summary")
        summary = pd.DataFrame({
            'Metric': ['Workouts', 'Volume', 'Calories', 'Sleep'],
            'Current': ['3/4', '65k kg', '3,280', '5.2h'],
            'Target': ['4/4', '88k kg', '3,300', '7h']
        })
        st.dataframe(summary, use_container_width=True)
    
    st.markdown("---")
    st.info("⚠️ Missing Thursday workout. Sleep critically low (5.2h). Keep pushing!")

# ============================================================================
# PAGE 2: NUTRITION
# ============================================================================

elif page == "🍽️ Nutrition":
    st.markdown("## Nutrition Tracker")
    
    st.markdown("### 📝 Log Meal")
    col1, col2 = st.columns(2)
    
    with col1:
        meal_type = st.selectbox("Meal", ["7am Breakfast", "10am Snack", "1pm Lunch", "3:30pm Pre-workout", "7pm Dinner", "10pm Night shake"])
    with col2:
        meal_date = st.date_input("Date", datetime.now())
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cal = st.number_input("Calories", 0, 1000, 500)
    with col2:
        prot = st.number_input("Protein (g)", 0, 100, 25)
    with col3:
        carbs = st.number_input("Carbs (g)", 0, 200, 75)
    with col4:
        fats = st.number_input("Fats (g)", 0, 50, 8)
    
    if st.button("✅ Log Meal"):
        st.session_state.meals.append({
            'date': meal_date,
            'meal': meal_type,
            'cal': cal,
            'prot': prot,
            'carbs': carbs,
            'fats': fats
        })
        st.success(f"✅ {meal_type} logged!")
    
    st.markdown("---")
    st.markdown("### 📊 Today's Totals")
    
    today = datetime.now().date()
    today_meals = [m for m in st.session_state.meals if m['date'] == today]
    
    total_cal = sum([m['cal'] for m in today_meals])
    total_prot = sum([m['prot'] for m in today_meals])
    total_carbs = sum([m['carbs'] for m in today_meals])
    total_fats = sum([m['fats'] for m in today_meals])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Calories", f"{total_cal}", "/ 3300")
    with col2:
        st.metric("Protein", f"{total_prot}g", "/ 174g")
    with col3:
        st.metric("Carbs", f"{total_carbs}g", "/ 420g")
    with col4:
        st.metric("Fats", f"{total_fats}g", "/ 44g")
    
    if st.session_state.meals:
        st.markdown("---")
        st.markdown("### 📋 Recent Meals")
        meals_df = pd.DataFrame(st.session_state.meals[-10:])
        st.dataframe(meals_df[['date', 'meal', 'cal', 'prot', 'carbs', 'fats']], use_container_width=True)

# ============================================================================
# PAGE 3: TRAINING
# ============================================================================

elif page == "🏋️ Training":
    st.markdown("## Training Tracker")
    
    st.markdown("### 🏋️ Log Exercise")
    col1, col2 = st.columns(2)
    
    with col1:
        ex_name = st.text_input("Exercise", "Barbell Bench Press")
    with col2:
        muscle = st.selectbox("Muscle", ["Chest", "Back", "Biceps", "Triceps", "Shoulders", "Legs", "Core"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Weight (kg)", 10, 200, 78, step=0.5)
    with col2:
        reps = st.number_input("Reps", 1, 50, 8)
    with col3:
        sets = st.number_input("Sets", 1, 10, 4)
    
    col1, col2 = st.columns(2)
    with col1:
        rpe = st.slider("RPE", 1, 10, 8)
    with col2:
        ex_date = st.date_input("Date", datetime.now())
    
    if st.button("✅ Log Exercise"):
        volume = weight * reps * sets
        st.session_state.exercises.append({
            'date': ex_date,
            'exercise': ex_name,
            'muscle': muscle,
            'weight': weight,
            'reps': reps,
            'sets': sets,
            'rpe': rpe,
            'volume': volume
        })
        st.success(f"✅ {ex_name} logged! {volume:,.0f}kg volume")
    
    st.markdown("---")
    st.markdown("### 📊 Today's Training")
    
    today = datetime.now().date()
    today_ex = [e for e in st.session_state.exercises if e['date'] == today]
    
    if today_ex:
        total_vol = sum([e['volume'] for e in today_ex])
        avg_rpe = np.mean([e['rpe'] for e in today_ex])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Sets", sum([e['sets'] for e in today_ex]))
        with col2:
            st.metric("Volume", f"{total_vol:,.0f}kg")
        with col3:
            st.metric("Avg RPE", f"{avg_rpe:.1f}")
        with col4:
            st.metric("Exercises", len(today_ex))
    else:
        st.info("No exercises logged yet today.")
    
    if st.session_state.exercises:
        st.markdown("---")
        st.markdown("### 📋 Recent Exercises")
        exercises_df = pd.DataFrame(st.session_state.exercises[-15:])
        st.dataframe(
            exercises_df[['date', 'exercise', 'weight', 'reps', 'sets', 'rpe', 'volume']].sort_values('date', ascending=False),
            use_container_width=True
        )

# ============================================================================
# PAGE 4: METRICS
# ============================================================================

elif page == "📈 Metrics":
    st.markdown("## Body Metrics")
    
    st.markdown("### 📏 Log Body Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        met_date = st.date_input("Date", datetime.now(), key="metric_date")
    with col2:
        weight = st.number_input("Weight (kg)", 60.0, 100.0, 69.6, step=0.1)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        fat = st.number_input("Body Fat %", 5.0, 40.0, 16.2, step=0.1)
    with col2:
        muscle = st.number_input("Muscle Mass (kg)", 40.0, 80.0, 55.4, step=0.1)
    with col3:
        sleep = st.number_input("Sleep (hours)", 0, 12, 5, step=0.5)
    
    waist = st.number_input("Waist (cm)", 50, 120, 82, step=0.5)
    
    if st.button("✅ Save Metrics"):
        st.session_state.metrics.append({
            'date': met_date,
            'weight': weight,
            'fat': fat,
            'muscle': muscle,
            'waist': waist,
            'sleep': sleep
        })
        st.success("✅ Metrics saved!")
    
    st.markdown("---")
    st.markdown("### 📊 Current Body Stats")
    
    latest_metric = st.session_state.metrics[-1]
    prev_metric = st.session_state.metrics[-2] if len(st.session_state.metrics) > 1 else latest_metric
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        weight_change = latest_metric['weight'] - prev_metric['weight']
        st.metric(
            "Weight",
            f"{latest_metric['weight']:.1f} kg",
            f"{weight_change:+.1f} kg"
        )
    
    with col2:
        fat_change = latest_metric['fat'] - prev_metric['fat']
        st.metric(
            "Body Fat",
            f"{latest_metric['fat']:.1f}%",
            f"{fat_change:+.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        muscle_change = latest_metric['muscle'] - prev_metric['muscle']
        st.metric(
            "Muscle Mass",
            f"{latest_metric['muscle']:.1f} kg",
            f"{muscle_change:+.1f} kg"
        )
    
    with col4:
        st.metric("Sleep (Last)", f"{latest_metric['sleep']:.1f}h", "⚠️ Low" if latest_metric['sleep'] < 7 else "✓ Good")
    
    st.markdown("---")
    
    if len(st.session_state.metrics) > 1:
        st.markdown("### 📈 Progress Chart")
        
        metrics_df = pd.DataFrame(st.session_state.metrics)
        metrics_df['date'] = pd.to_datetime(metrics_df['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=metrics_df['date'], y=metrics_df['weight'], name='Weight (kg)', line=dict(color='#667eea')))
        fig.add_trace(go.Scatter(x=metrics_df['date'], y=metrics_df['muscle'], name='Muscle (kg)', line=dict(color='#764ba2')))
        fig.add_trace(go.Scatter(x=metrics_df['date'], y=metrics_df['fat'], name='Fat %', line=dict(color='#ff6b6b')))
        
        fig.update_layout(
            title="Body Composition Over Time",
            xaxis_title="Date",
            yaxis_title="Value",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 5: ANALYTICS
# ============================================================================

elif page == "📉 Analytics":
    st.markdown("## Weekly Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Workouts", "3/4", "75%")
    with col2:
        st.metric("Nutrition", "92%", "Good")
    with col3:
        st.metric("Volume", "65k kg", "on track")
    with col4:
        st.metric("Sleep", "5.2h", "⚠️ Low")
    
    st.markdown("---")
    st.success("✅ Nutrition adherence excellent. Keep it up!")
    st.warning("⚠️ Sleep is CRITICAL. Only 5.2h avg. Prioritize recovery.")
    st.info("💡 Complete Thursday workout for full weekly volume.")
    
    st.markdown("---")
    st.markdown("### 📋 Week-by-Week Comparison")
    
    comparison = pd.DataFrame({
        'Week': ['Week 2', 'Week 3', 'Week 4', 'Week 5'],
        'Weight': [70.1, 70.35, 69.3, 69.6],
        'Fat %': [16.7, 16.6, 16.6, 16.2],
        'Volume (k kg)': [58, 61, 59, 65],
        'Workouts': ['3/4', '3/4', '3/4', '3/4'],
        'Score': [76, 78, 79, 82]
    })
    
    st.dataframe(comparison, use_container_width=True)

# ============================================================================
# PAGE 6: 12-MONTH PLAN
# ============================================================================

elif page == "🎯 12-Month Plan":
    st.markdown("## 12-Month Transformation Roadmap")
    
    st.markdown("### 📌 6-Phase Periodization")
    
    phases_df = pd.DataFrame({
        'Phase': [
            'Phase 1: Foundation',
            'Phase 2: Hypertrophy',
            'Phase 3: Volume Spec',
            'Phase 4: Strength+Cut',
            'Phase 5: Aggressive Recomp',
            'Phase 6: Shred+Polish'
        ],
        'Weeks': ['5-8', '9-12', '13-20', '21-24', '25-36', '37-48'],
        'Dates': [
            'Oct 21 - Nov 18',
            'Nov 19 - Dec 16',
            'Dec 17 - Feb 11',
            'Feb 12 - Mar 11',
            'Mar 12 - Jun 2',
            'Jun 3 - Sep 2027'
        ],
        'Cal/Day': [3300, 3400, 3500, 3200, 3300, 3100],
        'Est. Gain': ['+1.2kg', '+1.6kg', '+2kg', '+0.5kg', '+1kg', '-0.9kg']
    })
    
    st.dataframe(phases_df, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Milestones")
    
    milestones = pd.DataFrame({
        'Timeline': ['Oct (Wk8)', 'Nov (Wk12)', 'Dec (Wk16)', 'Jan (Wk24)', 'Feb (Wk32)', 'Sep (Wk48)'],
        'Weight': ['70.8kg', '72.4kg', '74.4kg', '74.9kg', '75.6kg', '75.0kg'],
        'Fat %': ['16.1%', '15.9%', '15.7%', '14.8%', '13.4%', '10.0%'],
        'Visual': ['Arm outline', 'Clear peaks', 'Full def', 'Abs show', '5-pack', 'Reference ✓']
    })
    
    st.dataframe(milestones, use_container_width=True)
    
    st.success("✅ Target: September 2027 (52 weeks)")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("Week 5 of 48 | Phase 1: Foundation + Density | Target: September 2027")
