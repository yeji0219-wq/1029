st.title('최예지의 첫번째 앱')
st.subheader('s')
st.write('d')
st.write('https://naver.com')
st.link_button('네이버 바로가기','https://naver.com')

name=st.text_input('이름을 입력해주세요:')
if st.button('환영인사'):
    st.write(name+'님 안녕하세요')
    st.balloons()
st.success('성공')
st.warning('경고')
st.error('오류')
st.info('안내문')
