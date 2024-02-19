import pandas as p
import streamlit as st
from monte_carlo_simulation import initialize_MonteCarlo_scenarios, plot_duration_for_a_confidence_level, run_MonteCarlo_simulation, get_average_scenario

st.title("RobustPlanner")
st.markdown("Votre outil pour rendre votre planning plus robuste")


if st.session_state['step'] < 3:
    st.warning("Vous devez valider les étapes précédentes d'abord")
else:
    # Step 3
    st.markdown("""
            #### Etape 3 : Charger les données de planning            
            Dans cette étape, vous pouvez choisir le niveau de confiance souhaité, et l'application vous indiquera la durée totale à considérer pour votre projet.
            """)
    total_simu = 200
    #total_simu = st.number_input("Total number of simulations:", min_value=10, max_value=500, value=100)

    if ('x_simu_durations_sorted' not in st.session_state) or (('run_new_calculation' in st.session_state)):
        df = initialize_MonteCarlo_scenarios(st.session_state['df'], total_simu)
        x_simu_durations_sorted, y_frequencies = run_MonteCarlo_simulation(df, total_simu)
        st.session_state['x_simu_durations_sorted'] = x_simu_durations_sorted
        st.session_state['y_frequencies'] = y_frequencies
        st.session_state['step'] = 3

    _, average_total_duration = get_average_scenario(df)
    plot_duration_for_a_confidence_level(st.session_state['x_simu_durations_sorted'], st.session_state['y_frequencies'], average_total_duration)

    #reset_button = st.button("Revenir à l'étape 1")
    #if reset_button:
    #    st.session_state['step'] = 1
    #    st.switch_page("step1.py")
