import streamlit as st
import requests

st.set_page_config(page_title="🎬 Movie Explorer")
st.title("🎬 Movie Explorer")

backend_url = "http://127.0.0.1:8000"

if "movie" not in st.session_state:
    st.session_state.movie = None
if "summary" not in st.session_state:
    st.session_state.summary = None

if st.button("🎲 Show Random Movie"):
    try:
        resp = requests.get(f"{backend_url}/movies/random/")
        resp.raise_for_status()
        st.session_state.movie = resp.json()
        st.session_state.summary = None
    except:
        st.error("Could not fetch a random movie.")

movie = st.session_state.movie
if movie:
    st.header(f"{movie['title']} ({movie['year']})")
    st.subheader(f"🎬 Director: {movie['director']}")
    st.markdown("**Actors:**")
    for actor in movie['actors']:
        st.write(f"🎭 {actor['actor_name']}")

    if st.button("🧠 Get Summary"):
        try:
            resp = requests.post(f"{backend_url}/generate_summary/", json={"movie_id": movie["id"]})
            resp.raise_for_status()
            st.session_state.summary = resp.json()["summary_text"]
        except:
            st.error("Could not generate summary.")

if st.session_state.summary:
    st.subheader("📖 Movie Summary")
    st.info(st.session_state.summary)