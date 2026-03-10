import streamlit as st

st.set_page_config(
    page_title="StoneAge Gacha Analysis Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗿 StoneAge Idle Gacha System Analysis Tool")
st.caption("데이터 기반 게임 시스템 분석 및 가챠 시뮬레이션 포트폴리오")
st.markdown("---")

# Section 1: 프로젝트 배경 & 목적 (Main Content)
col_bg, col_pur = st.columns(2)

with col_bg:
    st.subheader("🚀 1. 개발 배경 (Background)")
    st.markdown("""
    현대 게임의 가챠 구조는 천장, 픽업, 스택형 보정 등 다양한 기획 요소들이 복합적으로 설계되어 있어, 
    단순히 '운'에 맡기는 시스템이 아닌 기획자의 치밀한 계산이 요구됩니다. 
    
    기획자의 **직관만으로는 완벽한 밸런싱을 담보하기 어려운** 확률적 변수들을 
    사전에 검증하고, 모든 유저에게 일관된 재미와 공정한 경험을 제공하기 위한 
    **데이터 기반의 설계 접근법**을 고민하게 되었습니다.
    """)

with col_pur:
    st.subheader("🎯 2. 활용 목적 (Purpose)")
    st.markdown("""
    단순한 확률 계산을 넘어 **'데이터(Data)'로 증명하는 설계**를 지향합니다. 
    
    - **취약점 검증:** 몬테카를로 시뮬레이션을 통해 확률 구조의 예외 상황을 미리 파악합니다.
    - **경험 설계 유지:** 유저의 획득 경험이 설계자의 의도(Intended Experience) 내에 안착하는지 분석합니다.
    - **합리적 근거 마련:** 시스템 설계 시 '직관'이 아닌 '객관적 수치'를 바탕으로 한 의사결정 프레임워크를 구축합니다.
    """)

st.markdown("---")

# Section 2: 주요 분석 페이지 안내
st.subheader("🔍 주요 분석 기능 안내")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.info("**📊 확률 구조**\n\n등급별 분포 및 레벨별 보정 곡선")
with c2:
    st.info("**🎲 시뮬레이션**\n\nMonte Carlo 기반 대량 추출 분석")
with c3:
    st.info("**📈 체감 확률**\n\n누적 확률 및 획득 성공률 계산")
with c4:
    st.info("**💰 매출/기대값**\n\n평균 획득 비용 및 천장 효과")
with c5:
    st.info("**⚖️ 벤치마크**\n\n타사 메이저 게임과의 비교 분석")

st.markdown("---")
st.success("왼쪽 사이드바 메뉴를 통해 상세 분석 내용을 확인할 수 있습니다.")

# Sidebar info
st.sidebar.title("System Overview")
st.sidebar.info("StoneAge Idle Gacha System Analysis Tool v1.0")
st.sidebar.markdown("""
**Author:** Game System Designer  
**Tech:** Python | Streamlit | Plotly  
""")
