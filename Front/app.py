import streamlit as st
import requests


st.set_page_config(page_title="애니메이션 추천기", page_icon="📺", layout="centered")

st.title("📺 맞춤형 애니메이션 추천기")
st.markdown("당신의 취향을 분석하여 최적의 애니메이션을 찾아드립니다!")
st.divider()


st.subheader("1. 선호 장르 (제한 없음)")
genre_options = [
    "다크", "마법소녀", "판타지", "이능력", "배틀", "일상", "러브코미디", "순정", 
    "이세계전생", "힐링", "고어", "스릴러", "추리", "괴이", "스포츠", "토벌", 
    "시대물", "히어로", "개그", "학원물", "회귀물", "먹방", "음악"
]
selected_genres = st.multiselect("장르 선택", genre_options)

st.subheader("2. 나의 시청 스타일 (최대 3개)")
style_options = ["몰입형", "밥친구", "뇌빼고보기", "정주행", "옴니버스"]
selected_styles = st.multiselect("스타일 선택", style_options, max_selections=3)

st.subheader("3. 시청 목적 (최대 2개)")
purpose_options = ["작품감상", "씹덕력충전", "여가활동", "사운드채우기"]
selected_purposes = st.multiselect("목적 선택", purpose_options, max_selections=2)

st.subheader("4. 애니메이션 강도")
selected_ota = st.select_slider(
    "1.누구나 한 번쯤 들어본 애니 / 2.평범하게 재밌게 볼 수 있는 애니 / 3.애니 좀 본 사람들의 애니 / 4.숨어서 봐야 하는 애니 / 5.'진짜'들의 애니", 
    options=["1", "2", "3", "4", "5"], 
    value="3"
)

st.subheader("5. 특별히 원하는 태그가 있나요?")
tag_options = ["선택 안 함", "고전명작", "씹덕교양", "장르정석", "매니악"]
selected_tag = st.selectbox("태그 선택 (선택사항)", tag_options)

st.divider()


if st.button("🚀 추천 받기!", type="primary"):
    if not selected_genres or not selected_styles or not selected_purposes:
        st.warning("장르, 스타일, 목적을 최소 1개 이상 선택해 주세요!")
    else:
        payload = {
            "genres": selected_genres,
            "styles": selected_styles,
            "purposes": selected_purposes,
            "otaRate": selected_ota,
            "tag": selected_tag if selected_tag != "선택 안 함" else None
        }

        with st.spinner("데이터베이스를 뒤지는 중... 🔍"):
            try:
                
                response = requests.post("http://back:8000/recommend", json=payload)
                response_data = response.json()

                if response_data.get("recommendations"):
                    st.success("🎉 취향 저격 애니메이션을 찾았습니다!")
                    for i, anime in enumerate(response_data["recommendations"]):
                        with st.container():
                            st.markdown(f"### {i+1}위: **{anime['title']}**")
                            st.write(f"🏷️ **장르:** {', '.join(anime['genre'])}")
                            if anime.get('tag'):
                                st.write(f"🔖 **태그:** {', '.join(anime['tag']) if isinstance(anime['tag'], list) else anime['tag']}")
                            st.write("---")
                else:
                    st.info("조건에 딱 맞는 애니메이션이 없습니다. 조건을 조금 완화해 보세요! 🥲")

            except requests.exceptions.ConnectionError:
                st.error("🚨 백엔드 서버(FastAPI)와 연결할 수 없습니다. 서버가 켜져 있는지 확인해 주세요!")
