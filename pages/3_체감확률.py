import streamlit as st
import pandas as pd
import plotly.express as px
from modules.analysis import calculate_perceived_prob, generate_perceived_prob_table
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="유저 체감 확률 분석", layout="wide")

st.title("📈 유저 체감 확률 분석")
st.markdown("""
많은 유저들이 **'확률이 1%면 100번 뽑으면 무조건 나오는 거 아냐?'**라고 오해하곤 합니다. 
이 페이지에서는 독립 시행의 원리에 따른 **누적 획득 확률**을 계산하여, 유저가 실제로 느끼는 '체감 확률'이 이론적 확률과 어떻게 다른지 분석합니다.
""")
st.markdown("---")

st.markdown("""
### 🧮 누적 확률(Accumulated Probability) 계산식
$n$번 시도했을 때 적어도 한 번 이상 성공할 확률은 다음과 같습니다.
$$P = 1 - (1 - p)^n$$
*   **$p$** : 단일 시도 시 성공 확률 (예: 0.0075%)
*   **$1 - p$** : 단일 시도 시 실패할 확률
*   **$(1 - p)^n$** : $n$번 모두 실패할 확률
""")

# Setup Sidebar
st.sidebar.header("🎯 확률 및 시도 횟수 설정")
target_prob_mode = st.sidebar.radio("목표 확률 선택", ["DB에서 선택", "직접 입력"])

if target_prob_mode == "직접 입력":
    p_input = st.sidebar.number_input("목표 등급 확률 (%)", min_value=0.0001, max_value=10.0, value=0.0075, format="%.5f")
    p = p_input / 100
else:
    options = {
        "SS (일반) - 0.0075%": get_base_probs()['SS'],
        "SS (픽업) - 0.12%": get_pickup_probs()['SS_Pickup'],
        "S 등급 - 0.5%": get_base_probs()['S']
    }
    selected_name = st.sidebar.selectbox("대상 등급 선택", list(options.keys()))
    p = options[selected_name]

# Main Area
st.subheader(f"✅ 분석 대상 확률: :blue[{p*100:.5f}%]")

# Section 1: Perceived Prob Table
st.header("1. 뽑기 횟수에 따른 누적 성공 확률")
st.info(f"💡 이론적으로 {int(1/p):,}번을 뽑아야 1번 나올 확률이지만, 실제로 {int(1/p):,}번 뽑았을 때 획득할 확률은 **약 63.2%**에 불과합니다.")

n_range = [10, 100, 500, 1000, 5000, 10000, 13333, 20000, 50000]
df_perceived = pd.DataFrame(generate_perceived_prob_table(p, n_range))

col1, col2 = st.columns([1, 1.5])

with col1:
    st.write("📋 **누적 확률 데이터 시트**")
    st.table(df_perceived.style.format({"Perceived Prob (%)": "{:.2f}%"}))

with col2:
    fig_line = px.line(df_perceived, x='Draws (n)', y='Perceived Prob (%)', 
                       markers=True, title=f"뽑기 횟수에 따른 누적 성공 확률 곡선",
                       labels={'Perceived Prob (%)': '누적 획득 확률 (%)', 'Draws (n)': '뽑기 횟수 (n)'})
    
    # Calculate 50% and 90% points
    import math
    if p > 0:
         n_50 = math.log(0.5) / math.log(1 - p)
         fig_line.add_vline(x=n_50, line_dash="dash", line_color="green", annotation_text=f"50% 확률 지점 (n={int(n_50)})")
         
         n_90 = math.log(0.1) / math.log(1 - p)
         fig_line.add_vline(x=n_90, line_dash="dash", line_color="red", annotation_text=f"90% 확률 지점 (n={int(n_90)})")
    
    st.plotly_chart(fig_line, use_container_width=True)

# Section 2: Custom n-value calculator
st.header("2. 커스텀 시도 횟수 계산기")
st.markdown("유저가 특정 횟수만큼 뽑았을 때, 아이템을 얻었을 확률을 즉시 계산합니다.")

custom_n = st.number_input("총 뽑기 횟수 입력 (n)", min_value=1, value=1000, step=100)
res_p = calculate_perceived_prob(p, custom_n)

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric(f"{custom_n}회 시도 시 획득 확률", f"{res_p*100:.4f}%")
with col_res2:
    if res_p < 0.3:
        st.error("📉 획득 가능성이 매우 낮습니다. (폭사 주의)")
    elif res_p < 0.7:
        st.warning("🌗 반반의 확률에 가깝습니다. (도전해볼 만함)")
    else:
        st.success("📈 획득 가능성이 높습니다. (안정권)")
