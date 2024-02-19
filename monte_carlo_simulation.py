
from criticalpath import Node
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import streamlit as st
import pandas as p
import math

def get_critical_path_duration(df, scenario_name):
    nodes = {}
    p = Node('project')
    for index, row in df.iterrows():
        nodes[row.task_id] = p.add(Node(row.task_id, duration=row[scenario_name]))
    
    df.loc[:,'successor_list'] = df.successor.map(lambda x: str(x).split(';'))
    # We explode the successor list to have each successor in a separate row
    # then we keep only rows where successor is a real task
    arrows_df = df.explode("successor_list")
    arrows_df = arrows_df.loc[arrows_df.successor_list.isin(arrows_df.task_id.unique().tolist())]
    for index, row in arrows_df.iterrows():
        p.link(row.task_id, row.successor_list)
    p.update_all()
    return p.get_critical_path(), p.duration

def get_average_scenario(df):
    # Create average scenario
    average_critical_path, average_duration = get_critical_path_duration(df, "duration_average")
    return average_critical_path, average_duration


def initialize_MonteCarlo_scenarios(df, total_simu):
    # Craeate MC scenarios
    #total_simu = 1000
    for simu_index in range(total_simu):
        df.loc[:,f'simu_{simu_index}'] = df.duration_min + (df.duration_max-df.duration_min)*np.random.rand(len(df))
    return df


def plot_duration_for_a_confidence_level(x_simu_durations_sorted, y_frequencies, average_total_duration):
    confidence_level = st.slider('Quel est le niveau de confiance que vous souhaitez avoir (en pourcentage) ?', 10, 100, 90)
    confidence_level = confidence_level / 100.
    duration_at_confidence_level = x_simu_durations_sorted[y_frequencies.searchsorted(confidence_level)]

    fig, ax = plt.subplots()
    plt.plot(x_simu_durations_sorted, y_frequencies, marker=".", linestyle="none")
    st.success("**Pour être sûr à %d%% de resepecter les deadlines, vous devez annoncer une durée totale de votre projet de %.1f jours**" % (confidence_level*100, duration_at_confidence_level))
    plt.vlines(duration_at_confidence_level, 0, 1, color="green", linestyles="--", label="Durée totale pour un niveau de confiance de %d%%" % (confidence_level*100));
    plt.vlines(average_total_duration, 0, 1, color="red", linestyles="--", label="Durée totale en utilisant les valeurs moyennes");
    plt.legend();
    plt.xlim(x_simu_durations_sorted[0], x_simu_durations_sorted[-1])
    plt.ylim(0,1)
    plt.xlabel('Durée totale du projet')
    plt.ylabel('Probabilité')
    st.pyplot(fig)
    #fig = px.scatter(x=x_simu_durations_sorted, y=y_frequencies)
    ##line_name = "Pour un niveau de confiance de {:.1f}, La durée totale est de {} jours".format(confidence_level*100, duration_at_confidence_level)
    #line_name = "A un niveau de confiance de {:.1f}%".format(confidence_level*100)
    #fig.add_vline(x=duration_at_confidence_level, line_dash="dash", line_color="green", name=line_name, label={"text": line_name})
    #line_name = "Avec les durées moyennes"#.format(average_total_duration)
    #fig.add_vline(x=average_total_duration, line_dash="dash", line_color="red", name=line_name, label={"text": line_name})
    ##fig.update_layout(showlegend=True)
    #fig.update_xaxes(title="Durée (en jours)", range=[x_simu_durations_sorted[0], x_simu_durations_sorted[-1]])
    #fig.update_yaxes(title="Fréquence", range=[0, 1])
    #st.plotly_chart(fig)

def run_MonteCarlo_simulation(df, total_simu):
    simu_durations = []
    simu_critical_paths = []

    for simu_index in range(total_simu):
        scenario_name = f'simu_{simu_index}'
        scenario_critical_path, scenario_duration = get_critical_path_duration(df, scenario_name)
        simu_durations.append(scenario_duration)
        simu_critical_paths += scenario_critical_path 

    #average_critical_path, average_duration = get_average_scenario(df)
    x_simu_durations_sorted = np.sort(simu_durations)
    y_frequencies = np.arange(1, len(x_simu_durations_sorted)+1)/len(x_simu_durations_sorted)
    return x_simu_durations_sorted, y_frequencies

