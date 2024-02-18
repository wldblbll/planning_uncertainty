
from criticalpath import Node
import matplotlib.pyplot as plt
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


def plot_duration_for_a_confidence_level(x_simu_durations_sorted, y_frequencies):
    confidence_level = st.slider('Quel est le niveau de confiance que vous souhaitez avoir (entre 30% et 100%) ?', 30, 100, 90)
    confidence_level = confidence_level / 100.
    duration_at_confidence_level = x_simu_durations_sorted[y_frequencies.searchsorted(confidence_level)]

    fig, ax = plt.subplots()
    plt.xlim(x_simu_durations_sorted[0], x_simu_durations_sorted[-1])
    plt.plot(x_simu_durations_sorted, y_frequencies, marker=".", linestyle="none")
    #plt.vlines(average_duration, 0, 1, color="green", linestyles="--", label="Average duration");
    st.success("**Pour être sûr à %d%% de resepecter les deadlines, vous devez annoncer une durée totale de votre projet de %d jours**" % (confidence_level*100, duration_at_confidence_level))
    plt.vlines(duration_at_confidence_level, 0, 1, color="green", linestyles="--", label="Duration at choosen confidence level is %0.1f" % duration_at_confidence_level);
    plt.legend();
    st.pyplot(fig)

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

