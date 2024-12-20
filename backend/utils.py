import pandas as pd

def get_random_sample(filtered_behaviour_data, num_rows=30):
    if num_rows > len(filtered_behaviour_data):
        raise ValueError("The number of rows to sample exceeds the size of the DataFrame.")
    sampled_data = filtered_behaviour_data.sample(n=num_rows, random_state=42)
    return sampled_data
