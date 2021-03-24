# -*- coding: utf-8 -*-

"""Plotly Dash webapp to process SWRCGSR Enrollment Reports from Ellucian Banner."""

# Import required libraries
import dash
from typing import Any
import dash_bootstrap_components as dbc
import os
import boto3
import pickle

# Module imports
import plotdata
import layout

# import process

# Initalize terms to process
CURRENT_TERM = "Summer2021"
PREVIOUS_TERM = "Summer2020"

# Initialize server
app: dash.Dash = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.FLATLY],
)
server: Any = app.server

app.title = f"Chemistry Enrollment Statistics for {CURRENT_TERM}"

# Load s3 environment variables
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")


# Helper Functions
def get_s3_data(object_name: str = "data.pickle"):
    """Retrieve latest enrollment data from Amazon s3 bucket
       and copy to Heroku local filesystem.

    Returns:
        Dict[datetime.date,pd.DataFrame]
    """

    s3_client = boto3.client("s3")
    s3_client.download_file(AWS_BUCKET_NAME, object_name, object_name)

    with open(object_name, "rb") as in_file:
        process_dict = pickle.load(in_file)
    return process_dict


# Run our data processing
process_dict = get_s3_data()
parse_dict = process_dict["parse_dict"]
tester = process_dict["tester"]
tester3 = process_dict["tester3"]
old_df = process_dict["old_df"]
old1 = process_dict["old1"]
older = process_dict["older"]
max_old = process_dict["max_old"]
test_vs_old = process_dict["test_vs_old"]


# Generate our graphs and tables
fig4, fig2, fig = plotdata.generate_graphs(tester, tester3, older, max_old)
fig_old = plotdata.generate_old_graph(test_vs_old)
fig_map = plotdata.generate_heatmap(tester3)
graph1 = plotdata.data_graph(fig4, "1")
graph2 = plotdata.data_graph(fig2, "2")
graph3 = plotdata.data_graph(fig, "3")
graph4 = plotdata.data_graph(fig_old, "4")
graph5 = plotdata.data_graph(fig_map, "5")

latest_date = max(list(parse_dict.keys()))
data_table = plotdata.create_dash_table(parse_dict[latest_date])

# Package up data for layout
graph_dict = {
    "Heatmap": graph5,
    "Over Time": graph1,
    "Total": graph2,
    "Percent Max": graph3,
    "Percent Last Year": graph4,
    "Latest Data": data_table,
}

# Create layout with graphs
app.layout = layout.generate_layout(graph_dict, CURRENT_TERM)


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
