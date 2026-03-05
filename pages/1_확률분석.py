import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_loader import get_base_probs, get_pickup_probs, get_level_progression

st.set_page_config(page_title="확률 구조 분석", layout="wide")

st.title("📊 확률 구조 분석")
st.markdown("---")

# Section 1: Base Probabilities
st.header("1. 등급별 등장 확률 분포")
probs = get_base_probs()
df_probs = pd.DataFrame(list(probs.items()), columns=['Grade', 'Probability'])
df_probs['Probability (%)'] = df_probs['Probability'] * 100

col1, col2 = st.columns([1, 1])

with col1:
    st.write("📊 기본 확률 데이터")
    st.table(df_probs)

with col2:
    st.write("📈 등급별 확률 비중 (Pie Chart)")
    # Filter out C grade for better view of rare grades if desired, or just show all
    fig1 = px.pie(df_probs, values='Probability', names='Grade', title='등급별 확률 분포', hole=0.3)
    st.plotly_chart(fig1, use_container_width=True)

# Section 2: Pickup Comparison
st.header("2. 일반 vs 픽업 확률 비교")
p_probs = get_pickup_probs()
df_p_probs = pd.DataFrame(list(p_probs.items()), columns=['Grade', 'Probability'])
df_p_probs['Type'] = 'Pickup'

# For comparison, add normal probs
df_base = pd.DataFrame(list(probs.items()), columns=['Grade', 'Probability'])
df_base['Type'] = 'General'

# Highlight SS specifically
ss_diff = p_probs.get('SS_Pickup', 0) / probs.get('SS', 1)
st.metric("픽업 SS 확률 증가율", f"{ss_diff:.1f}배", "기존 0.0075% -> 0.12%")

# Section 3: Level Progression
st.header("3. 레벨 기반 확률 변화")
df_level = get_level_progression()
df_level['SS_Prob (%)'] = df_level['SS_Prob'] * 100

fig3 = px.line(df_level, x='Level', y='SS_Prob (%)', markers=True, 
               title='성장 레벨에 따른 SS 획득 확률 변화 곡선',
               labels={'SS_Prob (%)': 'SS 획득 확률 (%)', 'Level': '플레이어 레벨'})
st.plotly_chart(fig3, use_container_width=True)
