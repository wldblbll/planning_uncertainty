#import pandas as p
from criticalpath import Node
import matplotlib.pyplot as plt
import numpy as np
import streamlit
import pandas as p

__version__ = 1.0

#try:
#    streamlit.set_option('deprecation.showfileUploaderEncoding', False)
#except:
#    pass

def create_MonteCarlo_scenarios(df, total_simu):
    # Craeate MC scenarios
    total_simu = 1000
    for simu_index in range(total_simu):
        df.loc[:,f'simu_{simu_index}'] = df.duration_min + (df.duration_max-df.duration_min)*np.random.rand(len(df))
    return df

def get_critical_path_duration(df, scenario_name):
    p = Node('project')
    for index, row in df.iterrows():
        nodes[row.task_id] = p.add(Node(row.task_id, duration=row[scenario_name]))
    
    df.loc[:,'successor_list'] = df.successor.map(lambda x: str(x).split(';'))
    arrows_df = df.explode("successor_list")
    for index, row in arrows_df.loc[~arrows_df.successor.isnull()].iterrows():
        p.link(row.task_id, row.successor_list)
    p.update_all()
    return p.get_critical_path(), p.duration

def get_average_scenario(df):
    # Create average scenario
    df.loc[:,f'simu_average'] = (df.duration_min + df.duration_max)/2.
    average_critical_path, average_duration = scenario_duration = get_critical_path_duration(df, "simu_average")
    return average_critical_path, average_duration

streamlit.title("Quantify uncertainty in your plans")
status = streamlit.empty()

input_file = streamlit.file_uploader("Input file:", type=["xlsx", "xls"])
example_df = p.DataFrame([['A', 'B;C;D', 10, 15],
       ['B', 'E', 10, 15],
       ['C', 'E', 10, 15],
       ['D', 'E', 10, 15],
       ['E', "", 10, 15]], columns=['task_id', 'successor', 'duration_min',
       'duration_max'])
streamlit.write("You need to load an excel file with following columns:")
streamlit.write(example_df)

total_simu = streamlit.number_input("Total number of simulations:", min_value=100, max_value=1000, value=100)


if input_file:
    df = p.read_excel(input_file, engine="openpyxl")
    df = create_MonteCarlo_scenarios(df, total_simu)

    nodes = {}
    simu_durations = []
    simu_critical_paths = []

    for simu_index in range(total_simu):
        scenario_name = f'simu_{simu_index}'
        scenario_critical_path, scenario_duration = get_critical_path_duration(df, scenario_name)
        simu_durations.append(scenario_duration)
        simu_critical_paths += scenario_critical_path 

    average_critical_path, average_duration = get_average_scenario(df)
    x = np.sort(simu_durations+[average_duration])
    y = np.arange(1, len(x)+1)/len(x)
    fig, ax = plt.subplots()
    plt.plot(x, y, marker=".", linestyle="none")
    plt.vlines(average_duration, 0, 1, color="green", linestyles="--", label="Average duration");
    plt.legend();
    streamlit.pyplot(fig)


    proba_average = y[x.searchsorted(average_duration)]
    streamlit.write(f"There is a {int(proba_average*100)}% chance that the project finish before the average duration which is equal to {average_duration} days.")
    streamlit.write(f"The critical path of average durations scenario is: {average_critical_path}")

    fig, ax = plt.subplots()
    p.Series(simu_critical_paths).value_counts().plot(kind="bar", title="How often each task is on the critical path");
    streamlit.pyplot(fig)



