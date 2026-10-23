import pandas as pd
import os
from back.temporal_graphs import load_temporal_data

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
# _df = pd.read_csv(os.path.join(base_path, "dataset_simplify.csv"), dtype=str)
_df = pd.read_csv(
    os.path.join(base_path, "dataset_simplify_v2.csv"),
    dtype=str
)
_df = load_temporal_data(_df)

def get_data():
    return _df.copy()
