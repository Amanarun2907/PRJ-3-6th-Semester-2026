import streamlit as st

# Import existing phase apps as modules
import main as phase1_app
import main_phase2 as phase2_app
import main_phase3 as phase3_app


def main():
    # Global router sidebar (kept very simple so text stays clear)
    with st.sidebar:
        st.title("Global Phase Navigation")
        phase = st.radio(
            "Select Phase",
            [
                "Phase 1 – Foundation",
                "Phase 2 – Core Analytics",
                "Phase 3 – IPO Intelligence",
            ],
        )

    # Delegate rendering to the selected phase app
    if phase == "Phase 1 – Foundation":
        phase1_app.main()
    elif phase == "Phase 2 – Core Analytics":
        phase2_app.main()
    elif phase == "Phase 3 – IPO Intelligence":
        phase3_app.main()


if __name__ == "__main__":
    main()

