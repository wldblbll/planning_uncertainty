import pandas as p
import streamlit as st
from gantt_chart_plot import plot_gantt_chart

if st.session_state['step'] != 2:
    st.warning("Vous devez valider les étapes précédentes d'abord")
else:
    # Step 2
    st.info("""
            #### Etape 2 : Visualiser les données et lancer le calcul
            - Vous pouvez ajuster vos données directement dans le tableau ci-dessous si besoin.
            - En appuyant sur "Lancer le calcul", l'outil examine 100 scénarios.
            - Pour chaque scénario, il calcule le chemin critique et la durée totale du projet.
            - Cela aide à comprendre comment les incertitudes influent sur la durée finale du projet.
            """)
    #total_simu = st.number_input("Total number of simulations:", min_value=10, max_value=500, value=100)
    #st.session_state['total_simu']  = total_simu

    run_calculation = st.button("🚀 Lancer le calcul")
    tab1, tab2 = st.tabs(["Visualiser le Gantt", "Tableau de données"])
    with tab2:
        df = st.data_editor(st.session_state['df'], num_rows= "dynamic")
        df.loc[:,f'duration_average'] = (df.duration_min + df.duration_max)/2.
        st.session_state['df']  = df
        df.loc[:,"successor_list"] = df["successor"].apply(lambda x: str(x).split(";") if x else [])
    with tab1:
        plot_gantt_chart(df)

    if run_calculation:
        st.session_state['step'] = 3
        st.switch_page("pages/step3.py")
    