"""LinguaLab Streamlit application."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from linguolab.services import LinguaLabService


st.set_page_config(page_title="LinguaLab", layout="wide")
service = LinguaLabService()

if "theme" not in st.session_state:
    st.session_state["theme"] = "Default"

with st.sidebar:
    st.title("LinguaLab")
    module = st.selectbox(
        "Choose module",
        [
            "Writing Analytics",
            "Tone and Style Analysis",
            "Literary Analysis",
            "Linguistics Lab",
            "Corpus Analysis",
            "Word Explorer",
            "AI Language Workbench",
            "History",
        ],
    )
    st.session_state["theme"] = st.radio("Theme", ["Default", "Ocean", "Mono"], index=["Default", "Ocean", "Mono"].index(st.session_state["theme"]))

if st.session_state["theme"] == "Ocean":
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #f5fbff 0%, #eef6ff 100%); color: #0b1f33; }
    .stApp [data-testid="stHeader"] { background: transparent; }
    .stApp [data-testid="stSidebar"] { background: #e6f2ff; color: #0b1f33; }
    </style>
    """, unsafe_allow_html=True)
elif st.session_state["theme"] == "Mono":
    st.markdown("""
    <style>
    .stApp { background: #f6f6f6; color: #1f1f1f; }
    .stApp [data-testid="stHeader"] { background: transparent; }
    .stApp [data-testid="stSidebar"] { background: #ebebeb; color: #1f1f1f; }
    </style>
    """, unsafe_allow_html=True)

st.title("LinguaLab: Language Intelligence Platform")
st.caption("Lightweight demo architecture with local analytics and optional OpenAI/Azure OpenAI augmentation.")

if module in {
    "Writing Analytics",
    "Tone and Style Analysis",
    "Literary Analysis",
    "Linguistics Lab",
    "AI Language Workbench",
}:
    text = st.text_area("Input text", height=220, placeholder="Paste text to analyse...")

    if st.button("Run analysis", use_container_width=True):
        if module == "Writing Analytics":
            result = service.writing_analytics(text)
            c1, c2, c3 = st.columns(3)
            c1.metric("Readability", result["readability"])
            c2.metric("Vocabulary richness", result["vocabulary_richness"])
            c3.metric("Passive ratio", result["passive_voice_detection"]["passive_ratio"])

            vocab_df = pd.DataFrame(result["top_vocabulary"], columns=["word", "count"])
            if not vocab_df.empty:
                fig = px.bar(vocab_df, x="word", y="count", title="Top Vocabulary")
                st.plotly_chart(fig, use_container_width=True)
            st.json(result)

        elif module == "Tone and Style Analysis":
            result = service.tone_style(text)
            st.metric("Formality", result["formality_score"])
            sentiment = result["sentiment"]
            sent_df = pd.DataFrame([sentiment]).melt(var_name="metric", value_name="value")
            st.plotly_chart(px.bar(sent_df, x="metric", y="value", title="Sentiment"), use_container_width=True)
            st.json(result)

        elif module == "Literary Analysis":
            result = service.literary_analysis(text)
            st.json(result)
            rel = pd.DataFrame(result["character_relationships"])
            if not rel.empty:
                st.dataframe(rel, use_container_width=True)

        elif module == "Linguistics Lab":
            result = service.linguistics_lab(text)
            st.json(result)
            dep = pd.DataFrame(result["dependency_trees"])
            if not dep.empty:
                st.dataframe(dep, use_container_width=True)

        elif module == "AI Language Workbench":
            result = service.ai_language_workbench(text)
            st.success(f"Provider: {result['provider']}")
            st.json(result)

elif module == "Corpus Analysis":
    docs = st.text_area(
        "Input multiple documents (split with ---)",
        height=260,
        placeholder="Document 1\n---\nDocument 2\n---\nDocument 3",
    )
    ngram_size = st.slider("N-gram size", min_value=2, max_value=4, value=2)

    if st.button("Run corpus analysis", use_container_width=True):
        documents = [d.strip() for d in docs.split("---")]
        result = service.corpus_analysis(documents, ngram_size=ngram_size)
        st.json(result)

        lex_df = service.corpus_lexical_dataframe(documents)
        if not lex_df.empty:
            st.dataframe(lex_df, use_container_width=True)
            st.plotly_chart(
                px.bar(lex_df, x="document", y="lexical_diversity", title="Lexical Diversity"),
                use_container_width=True,
            )

elif module == "Word Explorer":
    word = st.text_input("Word")
    if st.button("Explore word", use_container_width=True):
        result = service.word_explorer(word)
        st.json(result)

else:
    entries = service.history(limit=25)
    if not entries:
        st.info("No analysis history yet.")
    else:
        st.dataframe(pd.DataFrame(entries), use_container_width=True)
