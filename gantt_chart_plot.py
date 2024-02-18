import numpy as np
import streamlit as st
import pandas as p
import plotly.figure_factory as ff


def draw_arrow_between_jobs(fig, first_job_dict, second_job_dict):
    ## retrieve tick text and tick vals
    job_yaxis_mapping = dict(zip(fig.layout.yaxis.ticktext,fig.layout.yaxis.tickvals))
    jobs_delta = second_job_dict['Start'] - first_job_dict['Finish']
    ## horizontal line segment
    fig.add_shape(
        x0=first_job_dict['Finish'], y0=job_yaxis_mapping[first_job_dict['Task']], 
        x1=first_job_dict['Finish'] + jobs_delta/2, y1=job_yaxis_mapping[first_job_dict['Task']],
        line=dict(color="black", width=1)
    )
    ## vertical line segment
    fig.add_shape(
        x0=first_job_dict['Finish'] + jobs_delta/2, y0=job_yaxis_mapping[first_job_dict['Task']], 
        x1=first_job_dict['Finish'] + jobs_delta/2, y1=job_yaxis_mapping[second_job_dict['Task']],
        line=dict(color="black", width=1)
    )
    ## horizontal line segment
    fig.add_shape(
        x0=first_job_dict['Finish'] + jobs_delta/2, y0=job_yaxis_mapping[second_job_dict['Task']], 
        x1=second_job_dict['Start'], y1=job_yaxis_mapping[second_job_dict['Task']],
        line=dict(color="black", width=1)
    )
    ## draw an arrow
    fig.add_annotation(
        x=second_job_dict['Start'], y=job_yaxis_mapping[second_job_dict['Task']],
        xref="x",yref="y",
        showarrow=True,
        ax=-10,
        ay=0,
        arrowwidth=1,
        arrowcolor="black",
        arrowhead=2,
    )
    return fig

def plot_gantt_chart(df):
    # Date de début des premières actions
    start_date = "2024-01-01"
    start_date = p.to_datetime(start_date)

    df.loc[:,"start_date"] = start_date
    df.loc[:,"end_date"] = df["start_date"] + p.to_timedelta(df["duration_average"], unit='D')
    for index, row in df.iterrows():
        row = df.loc[index]
        #if row.task_id=="B":
        #    import pdb; pdb.set_trace()
        if len(row.successor_list)>0:
            current_activity_end_date_plus_one = row.end_date + p.to_timedelta(1, unit='D')
            successors_index = df.task_id.isin(row.successor_list)
            df.loc[successors_index, "start_date"] = df.loc[successors_index, "start_date"].map(lambda x: max(x, current_activity_end_date_plus_one))
            df.loc[successors_index, "end_date"] = df.loc[successors_index, "start_date"] + p.to_timedelta(df.loc[successors_index, "duration_average"], unit='D') #df.loc[successors_index, "duration_average"].map(lambda x: p.to_timedelta(math.ceil(x), unit='D'))


    df.loc[:, "late_end_date"] = df.start_date + p.to_timedelta(df.duration_max, unit='D') #+ df.loc[:, "duration_max"].map(lambda x: p.to_timedelta(math.ceil(x), unit='D'))

    tasks = []
    tasks_dict = {}

    for index, row in df.iterrows():
        task = dict(Task=f"Task {row['task_id']}", Start=row['start_date'], Finish=row['end_date'], Description=f"Durées moyennes")
        tasks_dict[row['task_id']] = task
        tasks.append(task)

    for index, row in df.iterrows():
        task = dict(Task=f"Task {row['task_id']}", Start=row['end_date'], Finish=row['late_end_date'], Description=f"Exposition")
        tasks.append(task)

    # Créer le diagramme de Gantt
    fig = ff.create_gantt(tasks, index_col='Description', show_colorbar=True, group_tasks=True)

    arrows_df = df.explode("successor_list")
    arrows_df = arrows_df.loc[arrows_df.successor_list.isin(arrows_df.task_id.unique().tolist())]
    for index, row in arrows_df.iterrows():
        fig = draw_arrow_between_jobs(fig, tasks_dict[row.task_id], tasks_dict[row.successor_list])

    #for index, row in df.iterrows():
    #    if len(row.successor_list)>0:
    #        for successor_id in row.successor_list:
    #            fig = draw_arrow_between_jobs(fig, tasks_dict[row.task_id], tasks_dict[successor_id])

    st.plotly_chart(fig)
    return fig