import streamlit as st
import time
st.title('Hi! I am  Streamlit Dev')
st.subheader('I am a subheader')
st.text('Hello, im a text')
st.markdown('**hello**')
st.write("## H2")
st.metric(label= "WInd Speed", value= '120mph\^-1', delta='1.4ms\^-1')
def changetrkr():
    print(st.session_state.check_box)
st.checkbox('checkbox a', value=False, on_change=changetrkr, key='check_box')
radio_btn=st.radio('any question', options=("us", "mx", "ca"))
print(radio_btn)

def btn_click():
    print('button clicked')

btn=st.button('click me', on_click=btn_click)

select_box=st.selectbox('what is your fav', options=('suv', 'sedan', 'truck'))

image_uploaded=st.file_uploader('upload an image', type=['jpg', 'png'], accept_multiple_files=True)

if image_uploaded is not None:
    for image in image_uploaded:
        st.image(image)

st.slider('slider_str', min_value=0, max_value=45, value=23)

st.text_input('enter text', max_chars=10)
val=st.text_area('text area input')

print(val)

bar=st.progress(0)
for i in range(10):
    bar.progress((i+1)*10)
    time.sleep(1)