import pandas as p
import streamlit as st
from gantt_chart_plot import plot_gantt_chart

st.title("RobustPlanner")
st.markdown("Votre outil pour rendre votre planning plus robuste")

if st.session_state['step'] < 2:
    st.warning("Vous devez valider les étapes précédentes d'abord")
else:
    # Step 2
    st.markdown("""
            #### Etape 2 : Visualiser les données et lancer le calcul
            - En appuyant sur "Lancer le calcul", l'outil examine 100 scénarios.
            - Pour chaque scénario, il calcule le chemin critique et la durée totale du projet.
            """)
    #st.session_state['total_simu']  = total_simu

    run_calculation = st.button("🚀 Lancer le calcul", type="primary")
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
        st.session_state['run_new_calculation'] = True
        st.switch_page("pages/step3.py")
    