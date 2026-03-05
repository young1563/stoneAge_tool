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
    모바일 게임 시장에서 **확률형 시스템(Gacha)**은 핵심 콘텐츠이지만, 단순한 수치 표만으로는 다음과 같은 한계가 존재합니다.
    *   **직관성 부족:** 복잡한 확률 구조를 한눈에 이해하기 어려움
    *   **체감 확률의 괴리:** 유저가 실제로 느끼는 획득 확률 분석의 부재
    *   **경제적 영향성:** 가챠 시스템이 게임 경제 및 과금 구조에 미치는 영향 파악 난해
    
    특히 최근의 **픽업, 진행도 기반 확률 변화, 천장 시스템** 등이 결합된 구조는 데이터 분석과 시뮬레이션을 통한 정밀한 분석이 필수적입니다.
    """)

with col_pur:
    st.subheader("🎯 2. 활용 목적 (Purpose)")
    st.markdown("""
    **스톤에이지 키우기**의 실제 확률 데이터를 기반으로 차별화된 인사이트를 제공합니다.
    *   **구조 분석:** 가챠 시스템의 설계 의도 및 확률 구조 파악
    *   **시뮬레이션:** 특정 캐릭터 획득까지의 평균 횟수 및 비용 산출
    *   **경험 분석:** 유저 체감 확률 및 픽업 시스템의 데이터적 효과 검증
    *   **인사이트:** 데이터 기반의 시스템 밸런싱 및 개선안 도출
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
