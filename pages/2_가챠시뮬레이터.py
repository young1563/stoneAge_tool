import streamlit as st
import pandas as pd
import plotly.express as px
import os
import streamlit.components.v1 as components
from modules.simulator import run_gacha_simulation, get_simulation_summary
from modules.data_loader import get_base_probs, get_pickup_probs

st.set_page_config(page_title="가챠 시뮬레이터", layout="wide")

# ----- 최적화된 고급 스타일링 (높이 정렬 및 프리미엄 디자인) -----
st.markdown("""
<style>
    /* 메인 컨테이너 패딩 */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* 이미지 스타일링: 카드 느낌 극대화 */
    .stImage > img {
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease;
        object-fit: cover;
        height: 400px !important; /* 높이 고정으로 우측과 정렬 */
    }
    .stImage > img:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(255, 75, 75, 0.2);
    }
    
    /* 프리미엄 픽업 카드 (높이 고정) */
    .pickup-container {
        background: linear-gradient(145deg, #1e1e2f 0%, #252538 100%);
        padding: 35px;
        border-radius: 20px 20px 0 0;
        color: white;
        height: 330px; /* 버튼(70px) + 카드(330px) = 총 400px (이미지와 일치) */
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.05);
        border-right: 5px solid #ff4b4b;
        position: relative;
        overflow: hidden;
    }
    /* 카드 배경 장식 */
    .pickup-container::after {
        content: "";
        position: absolute;
        top: -50px;
        right: -50px;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(255,75,75,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }

    .pickup-header {
        font-size: 0.85rem;
        color: #ff4b4b;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    .pet-title {
        font-size: 2.2rem;
        font-weight: 900;
        margin-bottom: 15px;
        letter-spacing: -1px;
    }
    .prob-badge {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #ddd;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 15px;
        display: inline-block;
    }
    .pickup-badge {
        background: rgba(255, 75, 75, 0.15);
        border: 1px solid rgba(255, 75, 75, 0.4);
        color: #ff4b4b;
    }
    .desc-text {
        font-size: 1rem;
        color: #aaa;
        line-height: 1.6;
        margin-top: 10px;
    }
    
    /* 실행 버튼 (카드 하단 일체형) */
    div.stButton > button {
        height: 70px !important;
        width: 100% !important;
        background: linear-gradient(90deg, #ff4b4b 0%, #e63946 100%) !important;
        color: white !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        border-radius: 0 0 20px 20px !important;
        border: none !important;
        margin-top: -2px !important;
        box-shadow: 0 10px 20px rgba(255, 75, 75, 0.25) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #ff6b6b 0%, #ff4b4b 100%) !important;
        box-shadow: 0 15px 30px rgba(255, 75, 75, 0.4) !important;
        transform: translateY(2px); /* 살짝 눌리는 느낌 */
    }

    /* 대시보드 메트릭 카드 */
    .metric-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        text-align: center;
        border-bottom: 4px solid #636EFA;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        box-shadow: 0 8px 15px rgba(0,0,0,0.05);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

st.title("🦖 가챠 시뮬레이터")
st.caption("실제 게임 확률 데이터를 기반으로 한 Monte Carlo 시뮬레이션 분석")

# Settings sidebar
st.sidebar.header("⚙️ 시뮬레이션 설정")
gacha_type = st.sidebar.selectbox("가챠 종류", ["픽업", "일반"])
n_draws = st.sidebar.slider("1인 장착 뽑기 횟수 (n)", 100, 5000, 1000, step=100)
n_trials = st.sidebar.slider("시뮬레이션 인원 (Trials)", 100, 5000, 2000, step=100)

# Load data
if gacha_type == "일반":
    probs = get_base_probs()
else:
    probs = get_pickup_probs()

# ----------------- 헤드 영역: 이미지 & 정보 카드 (높이 정렬) -----------------
if 'df_sim' not in st.session_state:
    st.session_state.df_sim = None

# 컬럼 비율 조정 (가독성 최적화)
col_img, col_main = st.columns([1.2, 2.3])

with col_img:
    img_path = "img/모가로스.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.error("⚠️ 이미지를 찾을 수 없습니다.")

with col_main:
    # 정보 카드 렌더링
    if gacha_type == "픽업":
        st.markdown(f"""
        <div class="pickup-container">
            <div class="pickup-header">Legendary Pickup Event</div>
            <div class="pet-title">🔥 [전설] 모가로스</div>
            <div>
                <span class="prob-badge">기본 확률: 0.0075%</span>
                <span class="prob-badge pickup-badge">픽업 확률: 0.12% (16배 ↑)</span>
            </div>
            <div class="desc-text">
                이 시뮬레이터는 <b>{n_trials}명</b>의 가상 유저 데이터 샘플링을 통해<br>
                <b>{n_draws}회</b> 시행 시의 획득 편차를 정밀하게 분석합니다.<br><br>
                <i>"과연 상위 1%의 유저는 몇 마리를 획득할까요? 지금 확인해 보세요."</i>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="pickup-container" style="border-right-color: #636EFA;">
            <div class="pickup-header" style="color: #636EFA;">General Probability Analysis</div>
            <div class="pet-title">💎 일반 가챠 통합 분석</div>
            <div class="desc-text">
                특정 이벤트가 배제된 표준 확률 그룹의 데이터를 분석합니다.<br>
                등급별 펫 획득 빈도와 전체적인 시뮬레이션 분포를 시각화합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 하단 일체형 실행 버튼
    btn_start = st.button("🚀 분석 데이터 생성 시작", use_container_width=True)

# 시뮬레이션 실행 로직
if btn_start:
    with st.spinner('대규모 데이터 샘플링 진행 중...'):
        st.session_state.df_sim = run_gacha_simulation(probs, n_draws, n_trials)
        from modules.simulator import get_simulation_summary
        st.session_state.summary = get_simulation_summary(st.session_state.df_sim)
        
        # --- 알림 시스템 추가 ---
        st.toast(f"✅ {n_trials}명의 시뮬레이션이 성공적으로 완료되었습니다!", icon="🦖")
        st.balloons() # 시각적 피드백

# 결과 표시 영역
if st.session_state.df_sim is not None:
    # --- 자동 스크롤 스크립트 ---
    components.html(
        """
        <script>
            window.parent.document.querySelector('section.main').scrollTo({
                top: 600, 
                behavior: 'smooth'
            });
        </script>
        """,
        height=0
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success(f"🎊 분석 리포트 생성이 완료되었습니다! (대상: {n_trials}명 / 시도: {n_draws}회)", icon="✅")
    
    df_sim = st.session_state.df_sim
    summary = st.session_state.summary

    # 주요 지표 (커스텀 디자인)
    st.subheader("📊 시뮬레이션 핵심 보고서")
    
    available_cols = df_sim.columns.tolist()
    default_select = "SS_Pickup" if "SS_Pickup" in available_cols else (available_cols[0] if available_cols else None)
    rare_grades = [g for g in df_sim.columns if 'SS' in g or 'S' in g]
    
    selected_grade = st.selectbox("집중 분석 대상 등급 선택", rare_grades, index=rare_grades.index(default_select) if default_select in rare_grades else 0)
    
    avg_hits = df_sim[selected_grade].mean()
    max_hits = int(df_sim[selected_grade].max())
    success_rate = (df_sim[selected_grade] > 0).mean() * 100
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f'<div class="metric-card"><div style="color:#666; font-size:0.9rem;">1인 평균 획득</div><div style="font-size:1.8rem; font-weight:900;">{avg_hits:.2f}개</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="metric-card" style="border-bottom-color:#ff4b4b;"><div style="color:#666; font-size:0.9rem;">1개 이상 획득 유저</div><div style="font-size:1.8rem; font-weight:900; color:#ff4b4b;">{success_rate:.1f}%</div></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'<div class="metric-card" style="border-bottom-color:#ffd700;"><div style="color:#666; font-size:0.9rem;">최대 획득 기록</div><div style="font-size:1.8rem; font-weight:900; color:#ffd700;">{max_hits}개</div></div>', unsafe_allow_html=True)
    
    # 하단 탭
    tab1, tab2, tab3 = st.tabs(["📉 획득 분포 차트", "📋 데이터 써머리", "🔍 로우 데이터 데이터셋"])
    
    with tab1:
        dist_data = df_sim[selected_grade].value_counts().sort_index().reset_index()
        dist_data.columns = ['획득 횟수', '유저 수']
        
        fig_dist = px.bar(dist_data, x='획득 횟수', y='유저 수',
                         height=450,
                         color='유저 수', color_continuous_scale='Reds' if 'SS' in selected_grade else 'Blues',
                         title=f"{selected_grade} 등급 획득 분포 (전체 {n_trials}명 중)")
        fig_dist.update_layout(plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=50, b=20))
        st.plotly_chart(fig_dist, use_container_width=True)
        
    with tab2:
        st.table(summary)
        
    with tab3:
        st.dataframe(df_sim.head(100), use_container_width=True)
else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("💡 설정을 마치셨다면 우측 상단의 '분석 데이터 생성 시작' 버튼을 눌러주세요.")
