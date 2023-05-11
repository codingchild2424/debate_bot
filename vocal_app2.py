import streamlit as st
#import SessionState

# Page Configuration
st.set_page_config(page_title="Streamlit App")

if "page" not in st.session_state:
    st.session_state.page = "Page 1"

# Save function (placeholder)
def save_info(user_id, openAI_token, debate_theme):
    # You can add the code to save the submitted info (e.g., to a database)
    st.session_state.user_id = user_id, 
    st.session_state.openAI_token = openAI_token, 
    st.session_state.debate_theme = debate_theme

# Session state
#session_state = SessionState.get(user_id="", openAI_token="", debate_theme="")

# for callback when button is clicked
def page_controller():
    st.session_state.page = "Page 2"


# Page 1
def page1():
    st.header('Page 1')
    st.session_state.user_id = st.text_input("Enter user ID")
    st.session_state.openAI_token = st.text_input("Enter OpenAI token")
    debate_themes = ['Education','Sports','Religion','Justice','Pandemic','Politics','Minority','etc']
    st.session_state.debate_theme = st.selectbox("Select a debate theme", debate_themes)

    if st.button('Submit debate theme'):
        if st.session_state.debate_theme == 'Education':
            topic_list = ['Topic 1', 'Topic 2', 'Topic 3']
        elif st.session_state.debate_theme == 'Sports':
            topic_list = ['Topic 4', 'Topic 5', 'Topic 6']
        # Add more conditions for other debate themes
        st.write('Topics:', ', '.join(topic_list))

    if st.button(
        label='Submit all information',
        on_click=page_controller
        ):
        # You can add a function here to save the submitted info
        save_info(
            st.session_state.user_id, 
            st.session_state.openAI_token, 
            st.session_state.debate_theme
            )
        st.write('Information submitted successfully.')


# Page 2
def page2():
    st.header('Page 2')
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    
    with tab1:
        st.header("Tab 1")

    with tab2:
        st.header("Tab 2")

    with tab3:
        st.header("Tab 3")

    #st.write(f"You have selected {selected_tab}. Please input sound.")
    # Insert the code to input sound using mike and convert to text


# Page Routing
pages = {
    "Page 1": page1,
    "Page 2": page2
}

st.sidebar.title('Navigation')
#selection = st.sidebar.radio("Go to", list(pages.keys()))

selection = st.session_state.page

print("selection:", selection)

page = pages[selection]

# Execute selected page function
page()


