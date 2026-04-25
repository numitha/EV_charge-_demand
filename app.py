import streamlit as st
import requests
import streamlit.components.v1 as components
from ev_logic import best_station, nearest_low_queue, peak_hour, low_demand_hour
from ev_logic import lowest_queue_station
from ev_logic import station_feedback

# -------------------------
# 🔑 API KEY
# -------------------------
API_KEY = "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"   # 🔥 replace with your key

# -------------------------
# 🤖 LLM FUNCTION
# -------------------------
def ask_ai(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {"role": "system", "content": "You are a smart EV assistant. Be friendly and explain clearly."},
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    if 'choices' in data:
        return data['choices'][0]['message']['content']
    else:
        return f"⚠️ API Error: {data}"

# -------------------------
# 🧠 QUERY HANDLER
# -------------------------
def handle_query(query):
    query_lower = query.lower()

    if "best station" in query_lower:
        result = best_station()
        explanation = ask_ai(f"Explain this EV charging result clearly: {result}")
        return result + "\n\n🤖 " + explanation

    elif "nearest" in query_lower:
        result = nearest_low_queue()
        explanation = ask_ai(f"Explain this result: {result}")
        return result + "\n\n🤖 " + explanation

    elif "peak" in query_lower:
        result = peak_hour()
        explanation = ask_ai(f"Explain why this is peak time: {result}")
        return result + "\n\n🤖 " + explanation

    elif "best time" in query_lower or "when to charge" in query_lower:
        result = low_demand_hour()
        explanation = ask_ai(f"Explain why this is the best time to charge: {result}")
        return result + "\n\n🤖 " + explanation
    
    elif "low queue" in query_lower:
       result = lowest_queue_station()
       explanation = ask_ai(f"Explain why this station has low queue: {result}")
       return result + "\n\n🤖 " + explanation
    
    elif "feedback" in query_lower:
    # Extract station name
      station_name = query_lower.replace("tell me the feedback of", "").strip()

      result = station_feedback(station_name)

      explanation = ask_ai(f"Give a user-friendly review for this EV station: {result}")

      return result + "\n\n🤖 " + explanation
    

    else:
        return ask_ai(query)

# -------------------------
# 💬 CHAT UI
# -------------------------
st.title("⚡ AI EV Smart Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------------
# ⚡ QUICK BUTTONS
# -------------------------
st.write("### ⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

if col1.button("Suggest me a Best Station"):
    st.session_state.messages.append({"role": "user", "content": "best station"})

if col2.button("which is the Nearest Station?"):
    st.session_state.messages.append({"role": "user", "content": "nearest station"})

if col3.button("Which is the Best Time to Charge my EV"):
    st.session_state.messages.append({"role": "user", "content": "best time to charge"})

# -------------------------
# 💬 USER INPUT
# -------------------------
user_input = st.chat_input("Ask anything about EV charging...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# -------------------------
# 🤖 GENERATE RESPONSE
# -------------------------
if st.session_state.messages:
    last_message = st.session_state.messages[-1]

    if last_message["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("⚡ Thinking..."):
                answer = handle_query(last_message["content"])
                st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

# -------------------------
# 🗺️ MAP DISPLAY
# -------------------------
st.subheader("🗺️ Charging Stations Map")
components.html(open("ev_map.html", "r").read(), height=500)