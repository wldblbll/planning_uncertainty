#import pandas as p
import numpy as np
import streamlit as st
import pandas as p
import plotly.express as px
import math
from planning_data_files import get_example_df, read_user_data_file

__version__ = 1.0

st.title("RobustPlanner")
st.markdown("Votre outil pour rendre votre planning plus robuste")


st.info("""
        #### Etape 1 : Charger les données de planning
        Vous avez deux options ci-dessous :
        """)
col1, col2 = st.columns(2)
with col1:
    st.markdown("##### Option 1 : Charger vos données")
    st.markdown("Cliquez ci-dessous pour charger votre planning au format Excel")
    input_file = st.file_uploader("Input file:", type=["xlsx", "xls"])
    st.markdown("Vous pouvez également télécharger un template Excel et le remplir avec vos données.")
    st.download_button(
        label="📥 Télécharger le template Excel",
        data=open("./data.xlsx", "rb").read(),
        file_name="data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
with col2:
    st.markdown("##### Option 2 : Utiliser des données de tests")
    st.markdown("Cliquez sur le bouton ci-dessous pour charger des données fictives et tester l'outil.")
    load_data_sample = st.button("🧪 Charger un exemple de données")

if input_file:
    st.session_state['df'] = read_user_data_file(input_file)
    st.session_state['step'] = 2
    st.switch_page("pages/step2.py")
if load_data_sample:
    st.session_state['df'] = get_example_df()
    st.session_state['step'] = 2
    st.switch_page("pages/step2.py")



#st.divider()

# Main windows

#tab1, tab2, tab3 = st.tabs(["Charger vos données", "Visualiser le Gantt", "Mesurer le risque"])
#with tab1:
#with tab2:
#    plot_gantt_chart(df)
#with tab3:
#    plot_duration_for_a_confidence_level(x_simu_durations_sorted, y_frequencies)

#proba_average = y[x.searchsorted(average_duration)]
#st.write(f"There is a {int(proba_average*100)}% chance that the project finish before the average duration which is equal to {average_duration} days.")
#st.write(f"The critical path of average durations scenario is: {average_critical_path}")

#fig, ax = plt.subplots()
#p.Series(simu_critical_paths).value_counts().astype(np,int).plot(kind="bar", title="How often each task is on the critical path");
#st.pyplot(fig)



