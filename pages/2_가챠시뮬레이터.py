import streamlit as st
import pandas as pd
import plotly.express as px
from modules.simulator import run_gacha_simulation, get_simulation_summary
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="가챠 시뮬레이터", layout="wide")

st.title("🎲 Monte Carlo 가챠 시뮬레이터")
st.markdown("""
이 시뮬레이터는 **Monte Carlo(몬테카를로) 방법**을 사용하여 수천 번의 가챠 결과를 미리 시뮬레이션합니다. 
단순한 수치 계산을 넘어, 실제 유저가 겪을 수 있는 **'운의 영역(분산)'**을 시각적으로 확인할 수 있습니다.
""")
st.markdown("---")

# Settings sidebar
st.sidebar.header("🎯 시뮬레이션 설정")
st.sidebar.markdown("시뮬레이션 조건(횟수)을 설정하여 가챠 결과를 예측합니다.")
gacha_type = st.sidebar.selectbox("가챠 종류 선택", ["일반", "픽업"])
n_draws = st.sidebar.slider("1회당 연차 횟수 (n)", 10, 2000, 100)
n_trials = st.sidebar.slider("시뮬레이션 반복 횟수 (Trials)", 100, 10000, 1000)

# Load data based on selection
if gacha_type == "일반":
    probs = get_base_probs()
else:
    probs = get_pickup_probs()

st.markdown(f"### ⚙️ 설정 정보: **{gacha_type}** 가챠 / **{n_draws}**뽑기 / **{n_trials}**번 반복")

# 시뮬레이션 결과 유지를 위해 session_state 사용
if 'df_sim' not in st.session_state:
    st.session_state.df_sim = None
if 'summary' not in st.session_state:
    st.session_state.summary = None

# 시뮬레이션 실행 버튼
if st.button("🚀 시뮬레이션 시작"):
    with st.spinner('Monte Carlo 시뮬레이션 진행 중...'):
        st.session_state.df_sim = run_gacha_simulation(probs, n_draws, n_trials)
        st.session_state.summary = get_simulation_summary(st.session_state.df_sim)

# 결과가 있을 경우 표시
if st.session_state.df_sim is not None:
    df_sim = st.session_state.df_sim
    summary = st.session_state.summary

    # Display main results
    st.header("📈 시뮬레이션 결과 요약")
    st.markdown(f"총 {n_trials}명의 가상 유저가 각각 {n_draws}회씩 뽑기를 진행했을 때의 통계 데이터입니다.")
    st.dataframe(summary)
    
    # Plot distribution for rare grades (SS, S)
    st.header("📊 등급별 획득 분포 분석")
    
    rare_grades = [g for g in df_sim.columns if 'SS' in g or 'S' in g]
    if rare_grades:
        col_a, col_b = st.columns([1, 2])
        with col_a:
            selected_grade = st.selectbox("분포를 확인할 등급 선택", rare_grades)
            avg_hits = df_sim[selected_grade].mean()
            max_hits = int(df_sim[selected_grade].max())
            st.info(f"""
            **{selected_grade} 등급 결과:**
            - 유저 평균 획득: **{avg_hits:.2f}회**
            - 최소 획득: {df_sim[selected_grade].min()}회
            - 최대 획득: {max_hits}회
            
            평균적으로는 {avg_hits:.2f}개를 얻지만, 운이 좋은 유저는 {max_hits}개까지 얻는 것을 확인할 수 있습니다.
            """)
        
        with col_b:
            # 빈도수 계산
            dist_data = df_sim[selected_grade].value_counts().sort_index().reset_index()
            dist_data.columns = [selected_grade, '유저 수']
            
            fig_dist = px.bar(dist_data, x=selected_grade, y='유저 수',
                             title=f"{n_draws}회 뽑기 시 {selected_grade} 획득 빈도 분포 ({n_trials}명 시뮬레이션)",
                             labels={selected_grade: '획득 횟수(Hits)', '유저 수': '유저 수(Users)'},
                             color_discrete_sequence=['#636EFA'])
            
            fig_dist.update_layout(bargap=0.1)
            st.plotly_chart(fig_dist, use_container_width=True)
        
    else:
        st.warning("SS/S 등급 획득 이력이 시뮬레이션에서 발생하지 않았습니다. 뽑기 횟수를 늘려보세요.")

    # Show raw data head
    with st.expander("🔍 시뮬레이션 로우 데이터 확인 (상위 20개 시행 결과)"):
        st.dataframe(df_sim.head(20))
else:
    st.info("사이드바에서 설정을 완료한 후 **시뮬레이션 시작** 버튼을 눌러주세요.")
