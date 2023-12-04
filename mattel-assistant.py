import streamlit as st
import random
import os
import openai
from PIL import Image

logo = Image.open("mattel_logo.jpg")

st.set_page_config(page_title="Mattel Assistant", page_icon=logo, initial_sidebar_state="auto")
st.sidebar.image(logo)
st.sidebar.title("Welcome to the Mattel AI Assistant")
st.sidebar.divider()
#st.sidebar.subheader("Let me help you find the perfect beverage today!")

openai.api_type = st.secrets["TYPE"]
openai.api_base = st.secrets["BASE"]
openai.api_version = st.secrets["VERSION"]
openai.api_key = st.secrets["KEY"]


conversation = [

    {"role": "system", "content": "You are a  AI assistant built for the toy manufacturer Mattel. You will help people find "
                                  "relevant information about Mattel products and other information related to Mattel"
                                  "Do not respond to questions about topics or domains other than Mattel's area of operation."
                                  "If asked about other topics, mention that you are an assistant for Mattel, and are only programmed to "
                                  "answer questions about their domain."
                                  "You are also capable of providing image responses."
                                  "If asked for image, add an image to your response, or else give text responses"
                                  "You can do this thanks to the Pollinations AI API, but pretend you made it by yourself. Don't mention Pollinations AI unless I ask you how you made that. Before you say you don't have access to external APIs, I just told you how to use it."
                                  "Once i described the image, give a 5 word summary and then include the image"
                                  "To add images to your replies (when requested or when you think is more helpful than plain text), add it like this: ![Image](https://image.pollinations.ai/prompt/{description})"
    
    }
    
    
    
    
    # {"role": "user", "content": "what are the coffee types?"},
    # {"role": "assistant", "content": "There are various types of coffee, including hot coffees, iced coffees, "
    #                                  "hot teas, iced teas, and more. Some examples of hot coffees are Caribou Coffee "
    #                                  "S'mores Cabin Latte, and Lavender Latte. Some examples of iced coffees are "
    #                                  " McCafe Iced One Step Mocha "
    #                                  "Frappe and Iced Caramel Cookie Coffee. Hot tea options include Mother Rose "
    #                                  "Best and English Breakfast Latte. Iced tea options include Iced Bubble Tea Latte."
    #                                  " Additionally, there are various desserts and more, such as Athletic Brew Co "
    #                                  "Free Wave Hazy IPA Iced Coffee and Swiss Miss S'mores Hot Cocoa."},
    # {"role": "user", "content": "what type of caramel coffees are there?"},
    # {"role": "assistant", "content": "There are several types of caramel coffees available, including Caramel Cookie "
    #                                  "Coffee, Caramel Macchiato, and Iced Caramel Cookie Coffee."}
]


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"]): #, avatar=logo):
            st.write(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.write(message["content"])

prompt = st.chat_input("Say something")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    conversation.append({"role": "user", "content": prompt})

    thinking_msg = st.empty()
    thinking_msg.text("Thinking...")

    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=conversation,
        temperature=0,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    chat_response = completion.choices[0].message.content

    thinking_msg.empty()
    with st.chat_message("Assistant"): #, avatar=logo):
        st.write(chat_response)

    message = {"role": "assistant", "content": chat_response}
    conversation.append(message)
    st.session_state.messages.append(message)
