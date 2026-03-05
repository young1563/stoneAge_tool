import streamlit as st
import pandas as pd
import plotly.express as px
from modules.simulator import run_gacha_simulation, get_simulation_summary
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="가챠 시뮬레이터", layout="wide")

st.title("🎲 Monte Carlo 가챠 시뮬레이터")
st.markdown("---")

# Settings sidebar
st.sidebar.header("🎯 시뮬레이션 설정")
gacha_type = st.sidebar.selectbox("가챠 종류 선택", ["일반", "픽업"])
n_draws = st.sidebar.slider("연차 횟수 (n)", 10, 1000, 100)
n_trials = st.sidebar.slider("시뮬레이션 반복 횟수 (Trials)", 100, 5000, 1000)

# Load data based on selection
if gacha_type == "일반":
    probs = get_base_probs()
else:
    probs = get_pickup_probs()

st.markdown(f"### ⚙️ 현재 가챠 종류: **{gacha_type}** 가챠")
st.info(f"선택한 {gacha_type} 가챠 확률 표로 시뮬레이션을 수행합니다.")

# Show progress bar placeholder
if st.button("🚀 시뮬레이션 시작"):
    with st.spinner('Monte Carlo 시뮬레이션 진행 중...'):
        df_sim = run_gacha_simulation(probs, n_draws, n_trials)
        summary = get_simulation_summary(df_sim)
        
        # Display main results
        st.header("📈 시뮬레이션 결과 요약")
        st.dataframe(summary)
        
        # Plot distribution for rare grades (SS, S)
        st.header("📊 등급별 획득 분포")
        
        rare_grades = [g for g in df_sim.columns if 'SS' in g or 'S' in g]
        if rare_grades:
            selected_grade = st.selectbox("분포를 확인할 등급 선택", rare_grades)
            fig_dist = px.histogram(df_sim, x=selected_grade, 
                                   title=f"{n_draws}회 뽑기 당 {selected_grade} 획득 횟수 분포 ({n_trials}회 시행)",
                                   nbins=20,
                                   labels={selected_grade: '획득 횟수'})
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Median/Mode analysis
            avg_hits = df_sim[selected_grade].mean()
            st.metric(f"{selected_grade} 평균 획득 횟수", f"{avg_hits:.2f}회", f"{avg_hits/n_draws*100:.4f}% 실제 기대 확률")
        else:
            st.warning("SS/S 등급 획득 이력이 시뮬레이션에서 발생하지 않았습니다. 뽑기 횟수를 늘려보세요.")

        # Show raw data head
        with st.expander("시뮬레이션 로우 데이터 (상위 10개)"):
            st.dataframe(df_sim.head(10))
else:
    st.write("시작 버튼을 눌러 시뮬레이션을 실행하세요.")
