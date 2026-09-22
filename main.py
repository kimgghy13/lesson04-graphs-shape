import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------------------
# 기본 설정
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)

    # 개봉일(8자리 숫자) -> 날짜 타입으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    # 장르 열에 세로막대(|) 기호로 여러 장르가 적혀 있으면 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    return df


def insight_box(key: str):
    """그래프 아래에 '이 그래프로 알 수 있는 것'을 적는 공간"""
    st.text_area(
        "✏️ 이 그래프로 알 수 있는 것을 한 문장으로 써보세요.",
        key=key,
        placeholder="예: ...",
        height=80,
    )


# ----------------------------------------------------------------------------
# 데이터 로드
# ----------------------------------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "최근 1년간 박스오피스 10위권에 든 영화 가운데, 그 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

with st.spinner("데이터를 불러오는 중입니다..."):
    df = load_data(DATA_URL)

with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ----------------------------------------------------------------------------
# 1. 장르별 영화 편수 - 도넛 그래프
# ----------------------------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.45,
    title="장르별 영화 편수",
)
fig_donut.update_traces(
    textinfo="none",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_donut.update_layout(legend_title_text="장르")

st.plotly_chart(fig_donut, use_container_width=True)
insight_box("insight_1_genre_donut")

st.divider()

# ----------------------------------------------------------------------------
# 2. 총 관객 수의 분포 - 히스토그램
# ----------------------------------------------------------------------------
st.header("2. 총 관객 수의 분포")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객 수 분포",
    labels={"total_audi": "총 관객 수(명)"},
)
fig_hist.update_traces(
    hovertemplate="관객 수 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
)
fig_hist.update_layout(yaxis_title="영화 수(편)")

st.plotly_chart(fig_hist, use_container_width=True)
insight_box("insight_2_total_audi_hist")

st.divider()

# ----------------------------------------------------------------------------
# 3. 장르별 총 관객 수 분포 - 박스플롯
# ----------------------------------------------------------------------------
st.header("3. 장르별 총 관객 수 분포")

fig_box = px.box(
    df,
    x="genre",
    y="total_audi",
    title="장르별 총 관객 수 분포",
    labels={"genre": "장르", "total_audi": "총 관객 수(명)"},
    points="all",
)
fig_box.update_layout(xaxis_tickangle=-30)

st.plotly_chart(fig_box, use_container_width=True)
insight_box("insight_3_genre_box")

st.divider()

# ----------------------------------------------------------------------------
# 4. 개봉일 스크린 수와 총 관객 수의 관계 - 산점도
# ----------------------------------------------------------------------------
st.header("4. 개봉일 스크린 수와 총 관객 수의 관계")

fig_scatter1 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수 vs 총 관객 수",
    labels={"first_scrn": "개봉일 스크린 수(개)", "total_audi": "총 관객 수(명)"},
)

st.plotly_chart(fig_scatter1, use_container_width=True)
insight_box("insight_4_screen_vs_audi")

st.divider()

# ----------------------------------------------------------------------------
# 5. 개봉 첫 주 관객 수와 총 관객 수의 관계 - 산점도
# ----------------------------------------------------------------------------
st.header("5. 개봉 첫 주 관객 수와 총 관객 수의 관계")

fig_scatter2 = px.scatter(
    df,
    x="first_week_audi",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉 첫 주 관객 수 vs 총 관객 수",
    labels={"first_week_audi": "개봉 첫 주 관객 수(명)", "total_audi": "총 관객 수(명)"},
)

st.plotly_chart(fig_scatter2, use_container_width=True)
insight_box("insight_5_firstweek_vs_total")

st.divider()

# ----------------------------------------------------------------------------
# 6. 10위권 유지 일수와 총 관객 수의 관계 - 산점도
# ----------------------------------------------------------------------------
st.header("6. 박스오피스 10위권 유지 일수와 총 관객 수의 관계")

fig_scatter3 = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="10위권 유지 일수 vs 총 관객 수",
    labels={"days_in_top10": "10위권 유지 일수(일)", "total_audi": "총 관객 수(명)"},
)

st.plotly_chart(fig_scatter3, use_container_width=True)
insight_box("insight_6_days_vs_total")
