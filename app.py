import streamlit as st
import colorsys

# Streamlit 앱의 제목 설정
st.title('🎨 박광재의 빤스색 맞추기')
st.write('아래 색상 선택기를 사용하여 비밀 색상을 맞춰보세요!')

st.markdown('---')

# --- 비밀 색상 설정 ---
# 비밀 색상: 여기서는 Streamlit의 상징색 중 하나와 비슷한 연한 청록색 계열로 설정했습니다.
SECRET_HEX = '#00CED1'  # 16진수 코드 (Deep Sky Blue)

# 16진수 코드를 R, G, B 값으로 변환하는 함수 (비교를 위해)
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# 비밀 색상의 RGB 값
SECRET_RGB = hex_to_rgb(SECRET_HEX)

### 1. 사용자 입력 받기
# 색상 선택기 위젯
user_color = st.color_picker('당신의 추측 색상을 선택하세요:', '#ffffff') # 기본값은 흰색

### 2. 결과 확인 버튼
if st.button('색상 유추 결과 확인'):
    # 사용자가 선택한 색상의 RGB 값
    USER_RGB = hex_to_rgb(user_color)

    # --- 유추 로직: 색상 차이 계산 ---
    # 각 R, G, B 채널별 차이의 제곱을 합하여 색상 간의 거리를 계산 (유클리드 거리)
    r_diff = (SECRET_RGB[0] - USER_RGB[0]) ** 2
    g_diff = (SECRET_RGB[1] - USER_RGB[1]) ** 2
    b_diff = (SECRET_RGB[2] - USER_RGB[2]) ** 2
    
    # 총 색상 차이 (Distance)
    color_distance = (r_diff + g_diff + b_diff) ** 0.5
    
    # 0에 가까울수록 정답입니다. (최대값은 약 441.67)

    st.subheader('당신의 유추 결과')
    
    # 비밀 색상과 사용자의 선택을 나란히 보여줍니다.
    col1, col2 = st.columns(2)
    with col1:
        st.write('**당신의 선택**')
        st.markdown(f'<div style="width:100px; height:50px; background-color:{user_color}; border:1px solid #ccc;"></div>', unsafe_allow_html=True)
        st.write(f'HEX: `{user_color}`')
    with col2:
        st.write('**비밀 색상**')
        # SECRET_HEX를 직접 보여주지 않고 비밀로 유지합니다.
        st.markdown(f'<div style="width:100px; height:50px; background-color:black; border:1px solid #ccc;"></div>', unsafe_allow_html=True) 
        st.write(f'HEX: `비밀`')
        

    st.markdown(f'**색상 차이 (거리):** **{color_distance:.2f}** (0에 가까울수록 정답!)')

    # --- 피드백 메시지 ---
    if color_distance == 0:
        st.success('🎉 **완벽합니다!** 비밀 색상을 정확히 맞추셨어요!')
        st.balloons()
        st.markdown(f'비밀 색상은 **`{SECRET_HEX}`**였습니다.')
    elif color_distance < 50:
        st.warning('👍 **아주 가깝습니다!** 거의 정답에 도달했어요.')
    elif color_distance < 150:
        st.info('🤏 **조금 더!** 아직 차이가 있지만, 방향은 맞습니다.')
    else:
        st.error('😔 **아직 멀어요.** 다른 색상 계열을 시도해 보세요.')
