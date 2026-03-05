import streamlit as st
import pandas as pd
from modules.analysis import calculate_expected_draws, calculate_expected_cost
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="매출 기대값 분석", layout="wide")

st.title("💰 매출 기대값 분석")
st.markdown("""
이 페이지에서는 가챠 시스템이 게임 경제(Economy)에 미치는 영향을 분석합니다. 
특정 아이템을 얻기 위해 유저가 지불해야 하는 **평균 비용**을 산출하고, **천장(Pity) 시스템**이 매출과 유저 스트레스에 미치는 효과를 시뮬레이션합니다.
""")
st.markdown("---")

st.markdown("""
### 📊 기대값 분석 모델 (Expected Value Model)
*   **기대 뽑기 횟수 (E):** $1 / p$ (확률의 역수)
*   **기대 비용 (C):** $E \\times \\text{1회당 가격}$
""")

# Sidebar settings
st.sidebar.header("💵 비용 및 확률 설정")
st.sidebar.markdown("게임 내 재화 가치를 설정하여 실제 금액으로 환산합니다.")
draw_price = st.sidebar.number_input("1회 뽑기 가격 (단위: 원/블루잼)", min_value=1, value=50, step=10)

# Main Section
col1, col2 = st.columns(2)

probs_base = get_base_probs()
probs_pickup = get_pickup_probs()

with col1:
    st.header("1. 일반 가챠 기대값")
    st.markdown("상시 판매되는 일반 가챠의 획득 난이도와 예상 매출을 분석합니다.")
    target_grade_base = st.selectbox("일반 가챠 분석 등급 선택", list(probs_base.keys()), index=0)
    p_base = probs_base[target_grade_base]
    
    e_draws = calculate_expected_draws(p_base)
    e_cost = calculate_expected_cost(p_base, draw_price)
    
    st.metric(f"{target_grade_base} 기대 뽑기 횟수", f"{int(e_draws):,}회")
    st.metric(f"{target_grade_base} 평균 획득 비용", f"{int(e_cost):,}원")
    st.caption(f"이론적으로 {target_grade_base}등급 1개를 얻기 위해 약 {int(e_cost):,}원이 소모됩니다.")

with col2:
    st.header("2. 픽업 가챠 기대값")
    st.markdown("이벤트 기간 동안 제공되는 픽업 가챠의 효율성을 분석합니다.")
    target_grade_pickup = st.selectbox("픽업 가챠 분석 등급 선택", list(probs_pickup.keys()), index=0)
    p_pickup = probs_pickup[target_grade_pickup]
    
    e_draws_p = calculate_expected_draws(p_pickup)
    e_cost_p = calculate_expected_cost(p_pickup, draw_price)
    
    st.metric(f"{target_grade_pickup} 기대 뽑기 횟수", f"{int(e_draws_p):,}회")
    st.metric(f"{target_grade_pickup} 평균 획득 비용", f"{int(e_cost_p):,}원")
    st.caption(f"픽업 시 일반 가챠 대비 비용이 약 {e_cost / e_cost_p:.1f}배 절감됩니다.")

st.markdown("---")
st.header("3. 시스템 설계 개선 제안 (천장 시스템 도입)")
st.markdown("""
극악의 확률로 인해 무한정 과금을 해야 하는 상황을 막기 위해 **천장(Pity/Ceiling) 시스템** 도입을 시뮬레이션합니다. 
천장은 유저에게 **'최악의 상황에서도 이만큼 쓰면 얻을 수 있다'**는 확신을 주어 과금 문턱을 낮추는 효과가 있습니다.
""")

pity_count = st.slider("천장(Pity) 횟수 설정 (n회 시 확정 획득)", 100, 2000, 300, step=50)

col_p1, col_p2 = st.columns(2)

with col_p1:
    st.info(f"""
    **천장 도입 시 분석:**
    - **최대 매몰 비용:** {int(pity_count * draw_price):,}원
    - **기존 평균 기대 비용:** {int(e_cost_p):,}원
    """)

with col_p2:
    if (p_pickup > 0):
        prob_before_pity = 1 - (1 - p_pickup)**pity_count
        st.success(f"""
        **기획적 기대 효과:**
        - 유저 중 **{prob_before_pity*100:.1f}%**는 천장 도달 전 운 좋게 획득합니다.
        - 나머지 **{(1-prob_before_pity)*100:.1f}%**의 유저는 천장을 통해 획득하며 구제받게 됩니다.
        """)
        
st.warning("⚠️ **주의:** 천장 횟수가 기대 뽑기 횟수보다 너무 낮으면 매출이 급격히 감소하며, 너무 높으면 유저 스트레스가 해소되지 않습니다. 적절한 밸런싱이 필요합니다.")
