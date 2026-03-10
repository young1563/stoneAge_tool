import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="타 게임 벤치마크 비교", layout="wide")

# ----- 프리미엄 시각화 스타일링 -----
st.markdown("""
<style>
    /* 비교 카드 스타일 */
    .compare-card {
        background: #fdfdfd;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #eee;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
    }
    .compare-card:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        transform: translateY(-5px);
    }
    .vs-tag {
        color: #ff4b4b;
        font-weight: 900;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        opacity: 0.5;
    }
    .highlight-red { color: #ff4b4b; font-weight: bold; }
    .highlight-blue { color: #636EFA; font-weight: bold; }
    
    /* 하단 요약 배경 */
    .summary-box {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        color: white;
        padding: 35px;
        border-radius: 20px;
        border-left: 6px solid #ff4b4b;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ 가챠 벤치마크 분석")
st.markdown("""
장르별(수집형 RPG vs 방치형 RPG) 확률 설계의 본질적인 차이점을 데이터를 통해 비교합니다. 
기획자로서 **'확률의 높고 낮음'**이 아닌 **'경험의 차이'**에 집중하여 분석합니다.
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

# Section 1: Comparison Visualization
st.header("1. 장르별 최고 등급 확률 분포 (로그 스케일)")
fig_bar = px.bar(df_bench, x='게임명', y='SSR 확률 (%)', color='장르', 
                 text='SSR 확률 (%)', title='게임별 SSR/SS 기본 확률 (Log Scale)',
                 height=500, log_y=True, color_discrete_sequence=px.colors.qualitative.Set1)
fig_bar.update_traces(texttemplate='%{text:.4f}%', textposition='outside')
fig_bar.update_layout(xaxis_title="", yaxis_title="기본 확률 (%)", showlegend=True)
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Section 2: 핵심 설계 로직 요약 (VS 카드)
st.header("2. 시스템 설계 철학 비교 (Core Logic)")

c_lo, c_vs, c_hi = st.columns([1, 0.2, 1])

with c_lo:
    st.markdown("""
    <div class="compare-card">
        <h2 style="color:#e63946; margin-top:0;">🧱 수집형 모델 (High-Value)</h2>
        <p style="color:#666; font-size:1.1rem; border-bottom:1px solid #eee; padding-bottom:10px;"><b>"하나를 얻어도 확실한 가치"</b></p>
        <ul style="line-height:2.2; font-size:1rem; padding-left:20px;">
            <li><b>확률 체감:</b> <span class="highlight-red">1% ~ 4%</span> (당첨 기대감 높음)</li>
            <li><b>재화 공급:</b> 무료 뽑기가 한정적이며 개별 가치가 매우 높음</li>
            <li><b>천장 시스템:</b> 70~200회 사이의 강력한 확정 획득 보정</li>
            <li><b>기획 초점:</b> 신규 캐릭터 출시 시 <b>단기 매출 폭발력</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c_vs:
    st.markdown('<div class="vs-tag">VS</div>', unsafe_allow_html=True)

with c_hi:
    st.markdown("""
    <div class="compare-card">
        <h2 style="color:#636EFA; margin-top:0;">🌾 방치형 모델 (High-Volume)</h2>
        <p style="color:#666; font-size:1.1rem; border-bottom:1px solid #eee; padding-bottom:10px;"><b>"끊임없는 획득과 성장의 쾌감"</b></p>
        <ul style="line-height:2.2; font-size:1rem; padding-left:20px;">
            <li><b>확률 체감:</b> <span class="highlight-blue">0.007% ~ 0.1%</span> (당첨 확률 매우 낮음)</li>
            <li><b>재화 공급:</b> <b>매일 수백 회</b>의 압도적 무료 뽑기 공급</li>
            <li><b>천장 시스템:</b> 300~500회 이상의 높은 천장 (마일리지 개념)</li>
            <li><b>기획 초점:</b> 대량 배포를 통한 <b>장기 리텐션과 성장 유도</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Section 3: Strategic Conclusion
st.markdown("""
<div class="summary-box">
    <h2 style="margin-top:0; color:white;">🏁 전략적 분석 결론: '박리다매' 시스템의 핵심</h2>
    <p style="font-size:1.1rem; line-height:1.7; opacity:0.9;">
        방치형 게임인 스톤에이지 시스템의 본질은 "오늘 대박이 날까?" 하는 단발성 운이 아니라, 
        <b>"한 달간의 꾸준한 뽑기로 손에 쥐는 총 결과물이 몇 개인가?"</b> 하는 장기적 기대값에 있습니다.
    </p>
    <div style="background:rgba(255,255,255,0.1); padding:20px; border-radius:10px; margin-top:15px;">
        <b>기획자의 역할:</b> 단순히 낮은 확률을 방치하는 것이 아니라, 대량 배포 과정에서 발생하는 
        <b>'재화 가치 하락(인플레이션)'</b>을 방어하면서도, 유저가 끊임없이 <b>'성장의 즐거움'</b>을 
        느끼게 하는 황금 밸런스를 유지하는 나침반이 되어야 합니다.
    </div>
</div>
""", unsafe_allow_html=True)

# 데이터 백업 (작게 표시)
with st.expander("📊 로우 데이터 테이블 확인"):
    st.dataframe(df_bench, use_container_width=True)
