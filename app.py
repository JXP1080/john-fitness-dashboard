"""
JOHN'S FITNESS DASHBOARD - Week 5 Tracker
12-Month Physique Transformation
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

def init_session_state():
    if 'meals' not in st.session_state:
        st.session_state.meals = []
    if 'exercises' not in st.session_state:
        st.session_state.exercises = []
    if 'metrics' not in st.session_state:
        st.session_state.metrics = [
            {'date': '2026-09-19', 'weight': 69.6, 'fat': 16.2, 'muscle': 55.4, 'waist': 82, 'sleep': 5.0}
        ]

init_session_state()

# ============================================================================
# CONSTANTS
# ============================================================================

PROFILE = {
    'name': 'John',
    'age': 33,
    'height': 176,
    'location': 'UK',
    'weight_current': 69.6,
    'fat_current': 16.2,
    'muscle_current': 55.4,
    'weight_target': 75.0,
    'fat_target': 10.0,
    'muscle_target': 62.0,
}

# ============================================================================
# HEADER
# ============================================================================

col1, col2 = st.columns([2, 1])
with col1:
    st.title("💪 John's Fitness Dashboard")
    st.subheader("Week 5 - Phase 1: Foundation + Density")
with col2:
    st.info(f"**Week 5** | Phase 1\n69.6kg → 75kg\n16.2% → 10% fat")

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
            'Main Lift': ['Bench 78kg', 'Squat 82kg', 'Hammer 16kg',
