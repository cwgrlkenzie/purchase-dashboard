import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import fitz  # PyMuPDF
import os
import feedparser

# --- CONFIG ---
st.set_page_config(page_title="🕶️ Matrix Data Hub", layout="wide", page_icon="📂")

# --- LOGO AND STYLE ---
st.markdown("""
<style>
body {
    background-color: #000;
}
.stApp {
    background-color: #000000;
    color: #00FF41;
    font-family: 'Courier New', monospace;
}
h1, h2, h3, h4, h5, h6 {
    color: #00FF41;
}
.uploadedFile {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("## 🕶️ Matrix Data Hub")

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6b/Matrix_Digital_rain_animation.gif", width=60)
with col2:
    st.markdown("#### A futuristic landing site for data storage, analysis & construction news")

# --- TIME AND DATE ---
now = datetime.datetime.now()
st.markdown(f"**🕒 {now.strftime('%A, %B %d, %Y — %I:%M:%S %p')}**")

st.markdown("---")

# --- FILE UPLOAD ---
st.markdown("### 📤 Upload Excel or PDF Files")
uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls", "pdf"])

if uploaded_file:
    file_details = {
        "filename": uploaded_file.name,
        "type": uploaded_file.type,
        "size": f"{uploaded_file.size / 1024:.2f} KB"
    }
    st.json(file_details)

    if uploaded_file.type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        df = pd.read_excel(uploaded_file)
        st.markdown("### 📊 Data Preview (Excel)")
        st.dataframe(df, use_container_width=True)

        if len(df.columns) >= 2:
            try:
                chart = px.bar(df, x=df.columns[0], y=df.columns[1], title="Auto Bar Chart")
                st.plotly_chart(chart, use_container_width=True)
            except Exception as e:
                st.warning("Couldn't generate chart automatically.")

    elif uploaded_file.type == "application/pdf":
        st.markdown("### 📄 PDF Content")
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        st.text_area("PDF Text Extracted", text, height=300)

st.markdown("---")

# --- CONSTRUCTION NEWS ---
st.markdown("## 📰 Latest Construction Industry News")

RSS_FEED = "https://www.constructiondive.com/rss/"  # Use a reputable industry RSS feed
feed = feedparser.parse(RSS_FEED)

if feed.entries:
    for entry in feed.entries[:5]:
        st.markdown(f"**[{entry.title}]({entry.link})**")
        st.markdown(f"*{entry.published}*")
        st.markdown(entry.summary[:200] + "...")
        st.markdown("---")
else:
    st.info("Could not fetch news. Please check RSS source.")

# --- FOOTER ---
st.markdown("---")
st.markdown("Made with 🧠 by You • Powered by [Streamlit](https://streamlit.io)")
