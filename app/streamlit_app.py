"""Streamlit entrypoint for the Waveform Teaching App."""

import streamlit as st


def main() -> None:
    """Render a placeholder UI for Lesson 1."""
    st.set_page_config(page_title="Waveform Teaching App", layout="centered")
    st.title("Waveform Teaching App")
    st.subheader("Lesson 1: BPSK + Matched Filter")
    st.write("Hello Lesson 1!")


if __name__ == "__main__":
    main()
