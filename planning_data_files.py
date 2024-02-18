import pandas as p


def get_example_df():
    example_df = p.DataFrame([['A', 'Activity A', 'B;C', 7, 13],
        ['B', 'Activity B', 'D', 7, 13],
        ['C', 'Activity C', 'D', 7, 13],
        ['D', 'Activity D', '', 1, 3]], columns=['task_id', 'description', 'successor', 'duration_min',
        'duration_max'])
    return example_df

def read_user_data_file(input_file):
    print("################### Reading input file")
    df = p.read_excel(input_file, engine="openpyxl")
    return df
