import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import platform
import matplotlib.font_manager as fm
import os

# ---------- Streamlit Cloud용 한글 폰트 설정 ---------- #
@st.cache_resource
def install_fonts():
    # 리눅스 서버에 나눔폰트가 설치되는 경로입니다.
    font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
    if os.path.exists(font_path):
        return fm.FontProperties(fname=font_path).get_name()
    return None

font_name = install_fonts()

if font_name:
    plt.rc('font', family=font_name)
else:
    # 로컬(윈도우/맥) 환경용 설정
    import platform
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin':
        plt.rc('font', family='AppleGothic')

plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
# -------------------------------------------------- #

st.title("📊 국세청 근로소득 데이터 분석기")

# 데이터 불러오기

file_path = '국세청_근로소득 백분위(천분위) 자료_20241231.csv'      # ./data/ 폴더에 데이터 파일이 있어야 합니다.
try:
    # 자료 읽기
    df=pd.read_csv(file_path, encoding='cp949')  # 한글 깨짐 방지
    st.success("✅ 데이터가 성공적으로 로드되었습니다!")

    # 데이터 미리보기   
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df.head())       # head뒤에 아무것도 안걸어주면 상단 5줄이 보임

    # 데이터 분석 그래프 그리기
    st.subheader("📈 항목별 분포 그래프")

    # 분석하고 싶은 열 이름을 선택
    # 예를 들어 급여나 인원 같은 숫자 데이터가 있는 칸을 골라야 한다..
    column_names=df.columns.tolist()
    selected_col=st.selectbox("분석할 항목을 선택하세요", column_names)

    # 그래프 그리기(seaborn 활용)
    fig, ax=plt.subplots(figsize=(10,5)) # fig는 전체 그림, ax는 그래프가 그려질 공간
    sns.histplot(df[selected_col], ax=ax, color="#f6ca52", kde=True)      # 16진수 색상 활용
    plt.title(f"[{selected_col} 분포 확인]")    # 그래프 맨 위 제목
    plt.xlabel(selected_col)                    # x축(가로축) 제목 (예시: 급여)
    plt.ylabel("빈도수")                        # y축(세로축) 제목, 얼마나 자주 나오는지

    # 스트림릿 웹 화면에 그래프 표시
    st.pyplot(fig)  # fig를 그려줘

except FileNotFoundError:   # 파일 경로가 잘못되었을 때
    st.error(f"❌ 데이터 파일을 찾을 수 없습니다. '{file_path}' 경로를 확인해주세요.")
except Exception as e:      # SyntaxError, ValueError 등 모든 에러를 잡아냄
    st.error(f"❌ 데이터 처리 중 오류가 발생했습니다: {e}")