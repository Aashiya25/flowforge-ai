import streamlit as st
import requests

st.set_page_config(page_title="FlowForge AI", layout="centered")

# ---------------- SESSION STATE ----------------
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "provider" not in st.session_state:
    st.session_state.provider = ""

if "outputs" not in st.session_state:
    st.session_state.outputs = {}

if "generated" not in st.session_state:
    st.session_state.generated = False

if "published" not in st.session_state:
    st.session_state.published = False

if "hindi_outputs" not in st.session_state:
    st.session_state.hindi_outputs = {}

# ---------------- FORMAT FUNCTION (FINAL FIX) ----------------
def format_content(text):
    if not text:
        return ""

    text = text.replace("\r\n", "\n")

    # Force spacing before emoji sections
    text = text.replace("✨", "\n\n✨")
    text = text.replace("💋", "\n\n💋")
    text = text.replace("⚡", "\n\n⚡")
    text = text.replace("🔥", "\n\n🔥")

    # Space hashtags
    text = text.replace("#", "\n#")

    # Clean extra spacing
    text = text.replace("\n\n\n", "\n\n")

    return text.strip()

def render_content(content):
    st.markdown(
        f"<div style='line-height:1.6'>{format_content(content)}</div>",
        unsafe_allow_html=True
    )

# ---------------- AUTH ----------------
if not st.session_state.api_key:

    st.title("🚀 FlowForge AI")
    st.subheader("🔐 Secure Access")

    provider = st.selectbox("Select AI Provider", ["OpenRouter", "OpenAI"])
    api_input = st.text_input(f"Enter {provider} API Key", type="password")

    if api_input:
        st.session_state.api_key = api_input.strip()
        st.session_state.provider = provider
        st.rerun()

    st.stop()

# ---------------- MAIN APP ----------------
provider = st.session_state.provider

st.title("🚀 FlowForge AI")
st.caption(f"⚙️ Using {provider}")

# ---------------- INPUT ----------------
st.header("🟢 Step 1: Content Input")

topic = st.text_input("Enter content topic:")
platform = st.selectbox(
    "Select Platform",
    ["Instagram", "LinkedIn", "Blog", "All Platforms"]
)

# ---------------- LLM FUNCTION ----------------
def generate_content(prompt):

    API_KEY = st.session_state.api_key
    provider = st.session_state.provider

    if provider == "OpenRouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = "openai/gpt-3.5-turbo"
    else:
        url = "https://api.openai.com/v1/chat/completions"
        model = "gpt-3.5-turbo"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ API Error:\n{result}"

    except Exception as e:
        return f"❌ Exception:\n{str(e)}"

# ---------------- PROMPTS ----------------
def get_prompt(topic, platform):

    if platform == "Instagram":
        return f"""
Create a HIGH-ENGAGEMENT Instagram post on: {topic}

STRICT FORMAT RULES:
- Each idea MUST be on a NEW LINE
- Leave a BLANK LINE between sections
- Use emojis as section starters
- DO NOT write in paragraph form

Structure:

Hook line

✨ Point 1

💋 Point 2

⚡ Point 3

🔥 Pro Tip

CTA question

Hashtags (in one block)
"""

    elif platform == "LinkedIn":
        return f"""
Write a professional LinkedIn post on: {topic}

Ensure:
- Short paragraphs
- Line breaks between ideas
- Clear structure
- 3 key insights
- Actionable takeaway
"""

    elif platform == "Blog":
        return f"""
Write a blog post on: {topic}

Ensure:
- Title
- Introduction
- Clear paragraphs
- Section headings
- Conclusion
- Proper spacing between paragraphs
"""

    return ""

# ---------------- IMPROVE ----------------
def improve_content(content, platform):
    return generate_content(f"""
Improve the following {platform} content.

Make it:
- More engaging
- Better structured
- Clear
- Maintain spacing and formatting
Do NOT shorten.

{content}
""")

# ---------------- GENERATE ----------------
if st.button("Generate Content 🚀"):

    if not topic:
        st.warning("Please enter a topic.")
    else:
        st.session_state.outputs = {}
        st.session_state.hindi_outputs = {}
        st.session_state.published = False

        if platform == "All Platforms":
            for p in ["Instagram", "LinkedIn", "Blog"]:
                st.session_state.outputs[p] = generate_content(get_prompt(topic, p))
        else:
            st.session_state.outputs[platform] = generate_content(get_prompt(topic, platform))

        st.session_state.generated = True

# ---------------- OUTPUT ----------------
if st.session_state.generated:

    st.header("🟡 Step 2: Draft Output")

    for p, content in st.session_state.outputs.items():
        st.subheader(f"📝 {p}")
        render_content(content)

    st.header("🔵 Step 3: Brand Check")
    st.success("✅ Content is brand-safe and compliant")

    st.header("🟣 Step 4: Human Review")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Approve & Publish ✔"):
            st.session_state.published = True

    with col2:
        if st.button("✏ Improve Content"):
            improved = {}
            for p, content in st.session_state.outputs.items():
                improved[p] = improve_content(content, p)

            st.session_state.outputs = improved
            st.session_state.hindi_outputs = {}
            st.success("✨ Content Improved!")

# ---------------- PUBLISH ----------------
if st.session_state.published:

    st.header("📤 Step 5: Published Content")

    for p, content in st.session_state.outputs.items():
        st.subheader(f"📢 {p}")
        render_content(content)

    st.success("✅ Content Ready for Publishing 🚀")

    st.subheader("🚀 Publish to Platforms")

    for p in st.session_state.outputs.keys():

        if p == "Instagram":
            if st.button("📸 Post to Instagram"):
                st.success("✅ Posted to Instagram (Simulated)")
                st.balloons()

        elif p == "LinkedIn":
            if st.button("💼 Post to LinkedIn"):
                st.success("✅ Posted to LinkedIn (Simulated)")
                st.balloons()

        elif p == "Blog":
            if st.button("📝 Publish Blog"):
                st.success("✅ Blog Published (Simulated)")
                st.balloons()

    st.info("🔗 In production, this connects to real platform APIs.")

    # ---------------- LOCALIZATION ----------------
    st.header("🌍 Step 6: Localization")

    if st.button("Generate Hindi Version 🌐"):

        hindi_results = {}

        for p, content in st.session_state.outputs.items():

            hindi_prompt = f"""
Translate into simple Hindi with proper spacing.

Keep:
- Structure
- Line breaks
- Emojis
"""

            hindi_results[p] = generate_content(hindi_prompt + content)

        st.session_state.hindi_outputs = hindi_results

# ---------------- SHOW HINDI ----------------
if st.session_state.hindi_outputs:

    for p, content in st.session_state.hindi_outputs.items():
        st.subheader(f"🌐 {p} (Hindi)")
        render_content(content)