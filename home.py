import streamlit as st
import config as cfg

st.markdown(
    """<style>.block-container{max-width: 86rem !important;}</style>""",
    unsafe_allow_html=True,
)


def run_interface():
    st.title("Precificação de Títulos de Renda Fixa")
    st.write("---")

    with open("texts/home_intro.md", "r") as file:
        intro = file.read()

    st.markdown(intro)

    st.write("---")

    with open("texts/referencias.md", "r") as file:
        referencias = file.read()

    st.markdown(referencias)


def main():
    run_interface()


if __name__ == "__main__":
    main()
