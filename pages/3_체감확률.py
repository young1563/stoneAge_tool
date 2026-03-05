import streamlit as st
import pandas as pd
import plotly.express as px
from modules.analysis import calculate_perceived_prob, generate_perceived_prob_table
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="유저 체감 확률 분석", layout="wide")

st.title("📈 유저 체감 확률 분석")
st.markdown("---")

st.markdown("""
### 🧮 체감 확률 계산식
유저가 특정 횟수(n)만큼 뽑기를 진행했을 때, 최소 1회 이상 목표 등급을 획득할 누적 확률입니다.
$$P = 1 - (1 - p)^n$$
*   $p$ : 단일 시도 시 성공 확률
*   $n$ : 시도 횟수
""")

# Setup Sidebar
st.sidebar.header("🎯 확률 및 시도 횟수 설정")
target_prob_mode = st.sidebar.radio("목표 확률 선택", ["직접 입력", "DB에서 선택"])

if target_prob_mode == "직접 입력":
    p_input = st.sidebar.number_input("목표 등급 확률 (%)", min_value=0.0001, max_value=10.0, value=0.0075, format="%.5f")
    p = p_input / 100
else:
    options = {
        "SS (일반)": get_base_probs()['SS'],
        "SS (픽업)": get_pickup_probs()['SS_Pickup'],
        "S 등급": get_base_probs()['S']
    }
    selected_name = st.sidebar.selectbox("대상 등급", list(options.keys()))
    p = options[selected_name]

# Main Area
st.subheader(f"✅ 현재 설정된 목표 확률: **{p*100:.5f}%**")

# Section 1: Perceived Prob Table
st.header("1. 뽑기 횟수에 따른 누적 획득 확률")
n_range = [10, 50, 100, 300, 500, 1000, 5000, 10000, 15000]
df_perceived = pd.DataFrame(generate_perceived_prob_table(p, n_range))

col1, col2 = st.columns([1, 1.5])

with col1:
    st.table(df_perceived)

with col2:
    fig_line = px.line(df_perceived, x='Draws (n)', y='Perceived Prob (%)', 
                       markers=True, title=f"뽑기 횟수에 따른 누적 획득 확률 (성공 확률 {p*100:.5f}%)",
                       labels={'Perceived Prob (%)': '누적 획득 확률 (%)', 'Draws (n)': '뽑기 횟수 (n)'})
    # Add vertical line for 50% probability
    # Approximate n for 50% prob
    import math
    if p > 0:
        n_50 = math.log(0.5) / math.log(1 - p)
        fig_line.add_vline(x=n_50, line_dash="dash", line_color="green", annotation_text=f"Prob 50% at n={int(n_50)}")
    
    st.plotly_chart(fig_line, use_container_width=True)

# Section 2: Custom n-value calculator
st.header("2. 특정 횟수 시뮬레이션 계산")
custom_n = st.number_input("뽑기 횟수 입력 (n)", min_value=1, value=13333)
res_p = calculate_perceived_prob(p, custom_n)
st.metric(f"{custom_n}회 뽑기 시 누적 획득 확률", f"{res_p*100:.2f}%")
