import streamlit as st
import datetime
import google.generativeai as genai

# 한국의 도 리스트
KOREA_PROVINCES = [
    "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",
    "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"
]

def get_travel_recommendations(api_key, start_date, end_date, province, destination):
    # Gemini API 설정
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # 프롬프트 생성
    prompt = f"""
    여행 일정: {start_date}부터 {end_date}까지
    여행지 도: {province}
    상세 여행지: {destination}
    
    위 정보를 바탕으로 다음 내용을 포함한 여행 추천을 제공해주세요:
    1. 여행지 간단 소개
    2. 추천 관광지 3곳
    3. 현지 음식 추천 2가지
    4. 가상의 항공권 정보 (출발지는 서울로 가정)
    5. 가상의 호텔 추천 2곳
    
    각 항목을 구분하여 제공해주세요.
    """
    
    # Gemini API를 사용하여 응답 생성
    response = model.generate_content(prompt)
    
    return response.text

def main():
    st.title("AI 여행 추천 프로그램")

    # 사이드바에 API 키 입력 필드 추가
    api_key = st.sidebar.text_input("Gemini API 키를 입력하세요", type="password")

    # 메인 화면 구성
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("출발일", min_value=datetime.date.today())
    with col2:
        end_date = st.date_input("도착일", min_value=start_date)

    province = st.selectbox("여행할 도를 선택하세요", KOREA_PROVINCES)
    destination = st.text_input("상세 여행지를 입력하세요 (예: 서울 명동, 부산 해운대 등)")

    if st.button("여행 추천 받기"):
        if not api_key:
            st.error("API 키를 입력해주세요.")
        elif start_date > end_date:
            st.error("출발일은 도착일보다 앞서야 합니다.")
        elif not destination:
            st.error("상세 여행지를 입력해주세요.")
        else:
            with st.spinner("여행 추천을 생성 중입니다..."):
                recommendations = get_travel_recommendations(
                    api_key, start_date, end_date, province, destination
                )
                st.subheader("여행 추천 정보:")
                st.write(recommendations)

if __name__ == "__main__":
    main()