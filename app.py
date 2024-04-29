import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import random

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def roll_dice(dice_type, number_of_dice=1):
    return sum(random.randint(1, dice_type) for _ in range(number_of_dice))

def generate_encounter_with_ai(difficulty):
    prompt = f"Generate a detailed encounter for a D&D game, difficulty {difficulty}. Include the setting, enemy type, and potential rewards."
    response = model.generate_content(prompt)
    return response.text

def ai_response_to_action(encounter, action, success):
    outcome = "successfully" if success else "failed"
    prompt = f"Given the encounter: {encounter}, the player's action is: {action}. The action {outcome}. Narrate the outcome."
    response = model.generate_content(prompt)
    return response.text

# Main Streamlit interface
st.title("Dungeons & Dragons Assistant :crossed_swords:")
st.sidebar.title("Game Tools :wrench:")

# Initialize session state for attributes if not already done
if 'attributes' not in st.session_state:
    st.session_state['attributes'] = {'Strength': 10, 'Intelligence': 10, 'Charisma': 10}

st.sidebar.header("Character Attributes :muscle:")
attribute_keys = ['Strength', 'Intelligence', 'Charisma']

total_attributes = sum(st.session_state['attributes'].values())
if total_attributes > 30:
    st.sidebar.error("Total attribute value cannot exceed 30. Please adjust your attributes.")

for attribute in attribute_keys:
    st.session_state['attributes'][attribute] = st.sidebar.slider(
        attribute, min_value=1, max_value=20, value=st.session_state['attributes'][attribute], key=attribute)

# Initialize other parts of session state
if 'encounter' not in st.session_state:
    st.session_state['encounter'] = "Press 'Generate AI Encounter' to start an event."
if 'latest_response' not in st.session_state:
    st.session_state['latest_response'] = None

st.header("AI-Powered Random Encounter Generator :dragon:")
difficulty = st.selectbox("Select difficulty:", ["Easy", "Medium", "Hard"])
if st.button("Generate AI Encounter"):
    st.session_state['encounter'] = generate_encounter_with_ai(difficulty)
    st.session_state['latest_response'] = None

st.write(st.session_state['encounter'])

action_type = st.selectbox("Choose your action type:", ["Physical", "Intellectual", "Social"])
st.header("Respond to the Encounter :speech_balloon:")
user_response = st.text_input("Your action:", key="action")
if st.button("Submit Response"):
    if user_response:
        modifier_dict = {'Physical': 'Strength', 'Intellectual': 'Intelligence', 'Social': 'Charisma'}
        modifier = st.session_state['attributes'][modifier_dict[action_type]] // 2
        dc = {'Physical': 12, 'Intellectual': 18, 'Social': 15}[action_type]
        
        success_roll = roll_dice(20) + modifier
        success = success_roll >= dc
        response = ai_response_to_action(st.session_state['encounter'], user_response, success)
        st.session_state['latest_response'] = {"player": user_response, "ai": response, "success": success}
        st.text_input("Your action:", value="", key="response")  # Reset input box

if st.session_state['latest_response']:
    response = st.session_state['latest_response']
    st.header("Latest Response :scroll:")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("**Player:**")
        st.write(response["player"])
    with col2:
        outcome = "successfully" if response["success"] else "failed"
        st.markdown(f"**Outcome:** *{outcome}*")
        st.markdown("**AI Response:**")
        st.write(response["ai"])
