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


if 'step' not in st.session_state:
    st.session_state['step'] = 0

#st.info("""
#        #### Etape 1 : Charger les données de planning
#        Vous avez deux options ci-dessous :
#        """)
button_start = st.button("Démarrer", type="primary", use_container_width=True)
if button_start:
    st.session_state['step'] = 0
    st.switch_page("pages/step1.py")





