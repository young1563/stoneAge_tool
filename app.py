import streamlit as st

st.set_page_config(
    page_title="StoneAge Gacha Analysis Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗿 StoneAge Idle Gacha System Analysis Tool")
st.markdown("---")

st.markdown("""
# 데이터 기반 게임 시스템 분석
본 도구는 모바일 게임 "스톤에이지 키우기"의 가챠 시스템을 데이터 기반으로 분석하고 시뮬레이션하기 위해 제작되었습니다.

### 📋 주요 기능
1.  **📊 확률 구조 분석**: 전체 등급별 등장 확률 파악 및 레벨별 성장 확률 시각화
2.  **🎲 가챠 시뮬레이터**: Monte Carlo 기법을 활용한 대규모 뽑기 시뮬레이션
3.  **📈 유저 체감 확률**: 뽑기 횟수에 따른 실제 획득 확률 계산
4.  **💰 매출 기대값 분석**: 확률 기반 예상 과금액 및 기대값 도출

---
### 🛠️ 기술 스택
-   **Frontend**: Streamlit
-   **Data Processing**: Pandas, NumPy
-   **Visualization**: Plotly
-   **Analysis**: Monte Carlo Simulation

---
**분석을 시작하려면 사이드바 메뉴에서 분석 항목을 선택하세요.**
""")

# Sidebar info
st.sidebar.info("StoneAge Idle Gacha System Analysis Tool v1.0")
st.sidebar.markdown("Produced by Developer/Game Designer")
