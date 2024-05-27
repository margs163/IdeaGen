import streamlit as st
import time
from chains import generate_project
from chains import generate_chatbot_response
ai_value = dict

st.markdown("<h1 style='text-align: center;'> &#128526 Project Ideas Generator</h1>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center;'> Find unique ideas for your science investigatory projects</h1>", unsafe_allow_html=True)


st.sidebar.header("**PROJECT INFORMATION**", divider='rainbow')
subject = st.sidebar.text_input("Name a subject of the project:")
field = st.sidebar.text_input("Name a field of the project:")
st.divider()
st.markdown("**To start generating ideas, fill in the textboxes key features of your project and click on :blue[Generate] button.**")
st.caption("This was created by the G.O.A.T :goat: himself - Daniyal :joy:. The purpose of this webapp is to help students with science investigatory projects.")

# typewriting stream function
def stream_data(string: str):
    for word in string.split(" "):
        yield word + " "
        time.sleep(0.04)

if 'generation_counts' not in st.session_state:
    st.session_state.generation_counts = 0


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if 'projects' not in st.session_state:
    st.session_state.projects = [{
        "project_ideas": "none",
        "project_problems": "none",
        "project_objects": "none"
    }]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Generating project info when button is pressed
if st.sidebar.button("Generate"):
    st.session_state.clicked = True
    ai_value = generate_project(subject, field)
    st.session_state.projects.append(ai_value)
    st.session_state.generation_counts += 1

# Showing the UI
if st.session_state.clicked:
    st.divider()
    st.markdown("<h4 style='text-align: center;'> Generated project &#129302:</h4>", unsafe_allow_html=True)

    text_idea = st.text_area("**Your project idea:**", value = st.session_state.projects[st.session_state.generation_counts]['project_ideas'], height=50, disabled=False)
    text_problem = st.text_area("**Researching problems:**", value = st.session_state.projects[st.session_state.generation_counts]['project_problems'], height=300, disabled=False)
    text_object = st.text_area("**Researching objects:**", value = st.session_state.projects[st.session_state.generation_counts]['project_objects'], height=250, disabled=False)
    st.divider()
    is_generated = True
    
    # Chat window
    message_window = st.container(height=200)
    user_message_window = st.container(height=70)
    prompt = user_message_window.chat_input("What's up?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "AI", "content": generate_chatbot_response(prompt, text_idea)['text']})

        for index, message in enumerate(st.session_state.messages):
                if index == len(st.session_state.messages)-1:
                    message_window.chat_message(message["role"]).write_stream(stream_data(message["content"]))
                else:
                    message_window.chat_message(message["role"]).markdown(message["content"])

    else:
        message_window.markdown("<h4 style='text-align: center;'>Do you have any quesitons about the project idea &#129300? </h4>", unsafe_allow_html=True)
        message_window.markdown("<h4 style='text-align: center;'>You can chat with the AI chatbot. </h4>", unsafe_allow_html=True)
