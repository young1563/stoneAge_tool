import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="타 게임 벤치마크 비교", layout="wide")

st.title("⚖️ 타 게임 벤치마크 비교")
st.markdown("""
본 페이지에서는 시장 내 메이저 가챠 게임들의 확률 설계와 **스톤에이지 분석 모델**을 비교합니다. 
장르별(수집형 RPG vs 방치형 RPG) 확률 설계의 차이점을 파악하고 기획적 시사점을 도출합니다.
""")
st.markdown("---")

# 1. Benchmark Data Definition
benchmark_data = [
    {"게임명": "원신 / 스타레일", "장르": "수집형 RPG", "SSR 확률 (%)": 0.6, "픽업 확률 (%)": 0.3, "천장 (회)": 90, "이월": "YES"},
    {"게임명": "블루 아카이브", "장르": "수집형 RPG", "SSR 확률 (%)": 3.0, "픽업 확률 (%)": 0.7, "천장 (회)": 200, "이월": "NO"},
    {"게임명": "승부의 여신: 니케", "장르": "건슈팅/수집형", "SSR 확률 (%)": 4.0, "픽업 확률 (%)": 2.0, "천장 (회)": 200, "이월": "YES"},
    {"게임명": "Fate/Grand Order", "장르": "수집형 RPG", "SSR 확률 (%)": 1.0, "픽업 확률 (%)": 0.8, "천장 (회)": 330, "이월": "NO"},
    {"게임명": "명일방주", "장르": "디펜스 RPG", "SSR 확률 (%)": 2.0, "픽업 확률 (%)": 1.0, "천장 (회)": 99, "이월": "YES"},
    {"게임명": "메이플스토리 키우기", "장르": "방치형 RPG", "SSR 확률 (%)": 0.005, "픽업 확률 (%)": 0.1, "천장 (회)": 500, "이월": "NO"},
]

# Our Data
our_base_ss = get_base_probs()['SS'] * 100
our_pickup_ss = get_pickup_probs()['SS_Pickup'] * 100
benchmark_data.append({"게임명": "스톤에이지 (분석 모델)", "장르": "방치형 RPG", "SSR 확률 (%)": our_base_ss, "픽업 확률 (%)": our_pickup_ss, "천장 (회)": 300, "이월": "TBD"})

df_bench = pd.DataFrame(benchmark_data)

# Section 1: Comparison Table
st.header("1. 주요 가챠 게임 확률 설계 비교")
st.dataframe(df_bench.style.highlight_max(axis=0, subset=['SSR 확률 (%)', '픽업 확률 (%)'], color='#D4EFDF')
                          .highlight_min(axis=0, subset=['SSR 확률 (%)', '픽업 확률 (%)'], color='#FADBD8'))

st.info("💡 **데이터 해석:** 수집형 RPG(RPG)는 뽑기 시도 횟수가 적은 대신 개별 확률이 높고, 방치형(Idle)은 시도 횟수가 압도적으로 많은 대신 개별 확률을 낮게 설정합니다.")

# Section 2: Visual Comparison (Log Scale)
st.header("2. 최고 등급 획득 확률 시각화 (Log Scale)")
st.markdown("스톤에이지와 같은 방치형 게임은 일반 RPG 대비 확률이 수백 배 낮기 때문에, 로그 스케일로 시각화하여 비교합니다.")

fig_bar = px.bar(df_bench, x='게임명', y='SSR 확률 (%)', color='장르', 
                 text='SSR 확률 (%)', title='게임별 최고 등급(SSR/SS) 기본 확률 비교',
                 log_y=True) # Use log scale because 0.0075 is too small compared to 4.0
fig_bar.update_traces(texttemplate='%{text:.4f}%', textposition='outside')
st.plotly_chart(fig_bar, use_container_width=True)

# Section 3: Analysis Commentary
st.header("3. 시스템 기획적 분석 (Insight)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🧱 수집형 RPG 모델 (High-Value)
    - **특징:** 캐릭터 하나하나의 가치가 매우 높음.
    - **설계:** 낮은 뽑기 횟수 + 높은 확률 (1~4%).
    - **천장:** 70~200회 사이에서 강력한 보정(Soft Pity) 발동.
    - **매출 구조:** 소수의 고액 과금러와 다수의 소액 과금러가 공존.
    """)

with col2:
    st.markdown("""
    ### 🌾 방치형 RPG 모델 (High-Volume)
    - **특징:** 캐릭터 성장 단계(초월 등)가 많아 대량의 베이스가 필요함.
    - **설계:** **압도적인 뽑기 횟수** + 낮은 확률 (0.007x%).
    - **천장:** 천장 횟수 자체가 높거나(예: 300~500회), 마일리지를 쌓아 선택권을 구매하는 방식.
    - **매출 구조:** 광고 시청 및 '뽑기권 패키지'를 통한 박리다매형 매출.
    """)

st.markdown("---")
st.subheader("🏁 결론: 우리 프로젝트의 방향성")
st.success("""
본 분석 도구에서 다루는 스톤에이지 시스템은 **'낮은 확률'**이 단점이 아니라, **'매일 주어지는 수백 번의 무료 뽑기'**라는 장르적 특성과 결합된 설계입니다. 
따라서 분석 시에는 '단발 확률'보다는 **'일일 기대 획득량'** 혹은 **'주간 누적 확률'** 지표를 중점적으로 관리하는 것이 유효합니다.
""")
