# -*- coding: utf-8 -*-

"""Plotly Dash webapp to process SWRCGSR Enrollment Reports from Ellucian Banner."""

# Import required libraries
import dash
from typing import Any
import dash_bootstrap_components as dbc

# Module imports
import plotdata
import layout
import process

# Initalize terms to process
CURRENT_TERM = "Spring2021"
PREVIOUS_TERM = "Spring2020"

# Initialize server
app: dash.Dash = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.FLATLY],
)
server: Any = app.server

app.title = f"Chemistry Enrollment Statistics for {CURRENT_TERM}"


# Run our data processing
parse_dict = process.parse_files(CURRENT_TERM)
tester, tester3 = process.process_data(parse_dict)
old_df = process.parse_old(PREVIOUS_TERM)
old1 = process.parse_files(PREVIOUS_TERM)
older = process.process_df_to_counts(old1)
max_old = process.process_max_old(old1)
test_vs_old = process.process_vs_old(parse_dict, old_df)

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
