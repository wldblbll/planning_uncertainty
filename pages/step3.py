import pandas as p
import streamlit as st
from monte_carlo_simulation import initialize_MonteCarlo_scenarios, plot_duration_for_a_confidence_level, run_MonteCarlo_simulation


if st.session_state['step'] != 3:
    st.warning("Vous devez valider les étapes précédentes d'abord")
else:
    # Step 3
    st.info("""
            #### Etape 3 : Charger les données de planning
            Souhaitez-vous être sûr à 95% de respecter les délais annoncés, ou bien êtes-vous prêt à prendre plus de risques en acceptant que les deadlines soient respectées dans 70% des cas ?
            
            Dans cette étape, vous pouvez choisir le niveau de confiance souhaité, et l'application vous indiquera la durée totale à considérer pour votre projet.
            """)
    total_simu = 100
    if 'x_simu_durations_sorted' not in st.session_state:
        df = initialize_MonteCarlo_scenarios(st.session_state['df'], total_simu)
        x_simu_durations_sorted, y_frequencies = run_MonteCarlo_simulation(df, total_simu)
        st.session_state['x_simu_durations_sorted'] = x_simu_durations_sorted
        st.session_state['y_frequencies'] = y_frequencies
        st.session_state['step'] = 3

    plot_duration_for_a_confidence_level(st.session_state['x_simu_durations_sorted'], st.session_state['y_frequencies'])

    #reset_button = st.button("Revenir à l'étape 1")
    #if reset_button:
    #    st.session_state['step'] = 1
    #    st.switch_page("step1.py")
