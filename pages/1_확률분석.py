import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_loader import get_base_probs, get_pickup_probs, get_level_progression

st.set_page_config(page_title="확률 구조 분석", layout="wide")

st.title("📊 확률 구조 분석")
st.markdown("""
이 페이지에서는 **등급별 기본 확률**과 **레벨에 따른 확률 변화**를 분석합니다. 
가챠 시스템의 가장 기초가 되는 데이터 구조를 시각화하여 설계 의도를 파악할 수 있습니다.
""")
st.markdown("---")

# Section 1: Base Probabilities
st.header("1. 등급별 등장 확률 분포")
st.info("💡 **시스템 기획 포인트:** 하위 등급(C, B)의 비중을 높여 획득감을 조절하고, 상위 등급(SS)의 희소성을 극대화한 구조입니다.")

probs = get_base_probs()
df_probs = pd.DataFrame(list(probs.items()), columns=['Grade', 'Probability'])
df_probs['Probability (%)'] = df_probs['Probability'] * 100

col1, col2 = st.columns([1, 1])

with col1:
    st.write("📋 **등급별 확률 표**")
    st.table(df_probs)

with col2:
    st.write("🍩 **등급별 비중 (Donut Chart)**")
    fig1 = px.pie(df_probs, values='Probability', names='Grade', title='전체 등급 분포', hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)

# Section 2: Pickup Comparison
st.header("2. 일반 vs 픽업 확률 비교")
st.markdown("""
특정 캐릭터의 획득 확률을 일시적으로 상승시키는 **픽업(Pick-up) 시스템**의 효과를 분석합니다. 
유저는 픽업 기간 동안 더 높은 기대값을 가지고 유료 재화를 소모하게 됩니다.
""")

p_probs = get_pickup_probs()
ss_diff = p_probs.get('SS_Pickup', 0) / probs.get('SS', 1)
st.metric("🔥 픽업 SS 등급 획득 확률 증가율", f"{ss_diff:.1f}배", "기본 0.0075% -> 0.12%")

# Section 3: Level Progression
st.header("3. 레벨 기반 확률 변화")
st.markdown("""
본 게임의 시스템 중 하나인 **레벨에 따른 확률 보정** 분석입니다. 
초반 유저에게는 낮은 확률을 제공하다가, 게임 진행도(레벨)가 높아짐에 따라 SS 등급 획득 확률을 점진적으로 상향하여 **장기 리텐션을 유도**하는 설계입니다.
""")

df_level = get_level_progression()
df_level['SS_Prob (%)'] = df_level['SS_Prob'] * 100

fig3 = px.line(df_level, x='Level', y='SS_Prob (%)', markers=True, 
               title='성장 레벨에 따른 SS 획득 확률 변화 곡선',
               labels={'SS_Prob (%)': 'SS 획득 확률 (%)', 'Level': '플레이어 레벨'})
st.plotly_chart(fig3, use_container_width=True)
