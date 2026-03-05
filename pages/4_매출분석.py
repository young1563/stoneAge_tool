import streamlit as st
import pandas as pd
from modules.analysis import calculate_expected_draws, calculate_expected_cost
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="매출 기대값 분석", layout="wide")

st.title("💰 매출 기대값 분석")
st.markdown("---")

st.markdown("""
### 📊 기대값 분석 모델
가챠 시스템의 매출 구조를 분석하기 위해 특정 등급을 획득하기 위한 **평균 뽑기 횟수**와 **평균 소모 비용**을 산출합니다.
- **기대 뽑기 횟수 (E):** $1 / p$
- **기대 비용 (C):** $E \\times \\text{1회당 가격}$
""")

# Sidebar settings
st.sidebar.header("💵 비용 및 확률 설정")
draw_price = st.sidebar.number_input("1회 뽑기 가격 (원/크리스탈)", min_value=1, value=300)

# Main Section
col1, col2 = st.columns(2)

probs_base = get_base_probs()
probs_pickup = get_pickup_probs()

with col1:
    st.header("1. 일반 가챠 기대값")
    target_grade_base = st.selectbox("일반 가챠 분석 등급", list(probs_base.keys()), index=0)
    p_base = probs_base[target_grade_base]
    
    e_draws = calculate_expected_draws(p_base)
    e_cost = calculate_expected_cost(p_base, draw_price)
    
    st.metric(f"{target_grade_base} 기대 뽑기 횟수", f"{int(e_draws):,}회")
    st.metric(f"{target_grade_base} 평균 획득 비용", f"{int(e_cost):,}원")

with col2:
    st.header("2. 픽업 가챠 기대값")
    target_grade_pickup = st.selectbox("픽업 가챠 분석 등급", list(probs_pickup.keys()), index=0)
    p_pickup = probs_pickup[target_grade_pickup]
    
    e_draws_p = calculate_expected_draws(p_pickup)
    e_cost_p = calculate_expected_cost(p_pickup, draw_price)
    
    st.metric(f"{target_grade_pickup} 기대 뽑기 횟수", f"{int(e_draws_p):,}회")
    st.metric(f"{target_grade_pickup} 평균 획득 비용", f"{int(e_cost_p):,}원")

st.markdown("---")
st.header("3. 시스템 설계 개선 제안 시뮬레이션 (천장 도입)")
pity_count = st.slider("천장(Pity) 횟수 설정", 100, 1000, 300)

st.markdown(f"""
- **천장 시스템 도입 시 변화:** {pity_count}회 뽑기 시 무조건 {target_grade_pickup} 획득 보장
- **효과:** 유저의 과금 상한선(Ceiling)이 명확해지며, 확률적 리스크(Stress)가 완화됩니다.
- **기존 기대 비용:** {int(e_cost_p):,}원 → **천장 도입 시 최대 비용:** {int(pity_count * draw_price):,}원
""")

if (p_pickup > 0):
    prob_before_pity = 1 - (1 - p_pickup)**pity_count
    st.success(f"천장 도달 전 획득 확률: **{prob_before_pity*100:.2f}%** (유저 중 {(1-prob_before_pity)*100:.1f}%가 천장으로 획득)")
