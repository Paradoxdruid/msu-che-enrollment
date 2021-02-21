# -*- coding: utf-8 -*-

"""Graphs and tables for Plotly Dash webapp to process SWRCGSR Enrollment Reports."""

# Import required libraries
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from typing import Any, Tuple
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import dash_table

# Include pretty graph formatting
pio.templates.default = "ggplot2"


def generate_graphs(
    tester: pd.DataFrame,
    tester3: pd.DataFrame,
    old: pd.DataFrame,
    max_old: pd.DataFrame,
) -> Tuple[Any, Any, Any]:
    """Create plotly objects for our graphs.

    Args:
        tester (pd.DataFrame): Course Data by total enrollment
        tester3 (pd.DataFrame): Course data by percentage enrollment
        old (pd.DataFrame): Course data by total enrollment, previous term
        max_old (pd.DataFrame): Course data by max enrollment, previous term

    Returns:
        Tuple[Any, Any, Any]: Plotly graph objects for:
                            enrollment over time (fig4), total enrollment (fig2),
                            and percentage enrollment (fig)
    """

    # Graph 1
    all_true = [True] * 34

    core_lecture = [
        True,  # 1010
        True,  # 1100
        False,  # 1150
        True,  # 1800
        False,  # 1801
        True,  # 1810
        False,  # 1811
        True,  # 2100
        False,  # 2150
        False,  # 2710
        False,  # 2711
        True,  # 3000
        False,  # 3010
        True,  # 3100
        True,  # 3110
        False,  # 3120
        False,  # 3130
        False,  # 3190
        False,  # 3200
        False,  # 3610
        False,  # 3980
        False,  # 4100
        False,  # 4110
        False,  # 4300
        True,  # 4310
        False,  # 4320
        False,  # 4350
        False,  # 4370
        False,  # 4460
        False,  # 4490
        False,  # 4700
        False,  # 4710
        False,  # 4950
        False,  # 4960
    ]

    core_lab = [
        False,  # 1010
        False,  # 1100
        True,  # 1150
        False,  # 1800
        True,  # 1801
        False,  # 1810
        True,  # 1811
        False,  # 2100
        True,  # 2150
        False,  # 2710
        False,  # 2711
        False,  # 3000
        True,  # 3010
        False,  # 3100
        False,  # 3110
        True,  # 3120
        True,  # 3130
        False,  # 3190
        False,  # 3200
        False,  # 3610
        False,  # 3980
        False,  # 4100
        False,  # 4110
        False,  # 4300
        False,  # 4310
        False,  # 4320
        True,  # 4350
        False,  # 4370
        False,  # 4460
        False,  # 4490
        False,  # 4700
        False,  # 4710
        False,  # 4950
        False,  # 4960
    ]

    upper_courses = [
        False,  # 1010
        False,  # 1100
        False,  # 1150
        False,  # 1800
        False,  # 1801
        False,  # 1810
        False,  # 1811
        False,  # 2100
        False,  # 2150
        False,  # 2710
        False,  # 2711
        False,  # 3000
        False,  # 3010
        False,  # 3100
        False,  # 3110
        False,  # 3120
        False,  # 3130
        True,  # 3190
        True,  # 3200
        False,  # 3610
        False,  # 3980
        True,  # 4100
        True,  # 4110
        True,  # 4300
        False,  # 4310
        True,  # 4320
        False,  # 4350
        False,  # 4370
        True,  # 4460
        True,  # 4490
        False,  # 4700
        False,  # 4710
        True,  # 4950
        True,  # 4960
    ]

    crim_courses = [
        False,  # 1010
        False,  # 1100
        False,  # 1150
        False,  # 1800
        False,  # 1801
        False,  # 1810
        False,  # 1811
        False,  # 2100
        False,  # 2150
        True,  # 2710
        True,  # 2711
        False,  # 3000
        False,  # 3010
        False,  # 3100
        False,  # 3110
        False,  # 3120
        False,  # 3130
        False,  # 3190
        False,  # 3200
        True,  # 3610
        False,  # 3980
        False,  # 4100
        False,  # 4110
        False,  # 4300
        False,  # 4310
        False,  # 4320
        False,  # 4350
        False,  # 4370
        False,  # 4460
        False,  # 4490
        True,  # 4700
        True,  # 4710
        False,  # 4950
        False,  # 4960
    ]

    fig4 = go.Figure()

    our_df = tester.T

    for column in our_df:
        fig4.add_trace(go.Scatter(x=our_df.index, y=our_df[column], name=column,))

    fig4.update_yaxes(title="Enrolled")
    fig4.update_layout(
        legend_title_text="Course",
        title="Core Lecture Course Enrollment Over Time",
        template="ggplot2",
        #     colorscale=px.colors.sequential.Rainbow,
    )

    fig4.update_layout(
        updatemenus=[
            go.layout.Updatemenu(
                active=0,
                buttons=list(
                    [
                        dict(
                            label="All",
                            method="update",
                            args=[
                                {"visible": all_true},
                                {"title": "All Courses", "showlegend": True},
                            ],
                        ),
                        dict(
                            label="Core Lectures",
                            method="update",
                            args=[
                                {"visible": core_lecture},
                                {"title": "Core Lectures", "showlegend": True},
                            ],
                        ),
                        dict(
                            label="Core Labs",
                            method="update",
                            args=[
                                {"visible": core_lab},
                                {"title": "Core Labs", "showlegend": True},
                            ],
                        ),
                        dict(
                            label="Upper Div",
                            method="update",
                            args=[
                                {"visible": upper_courses},
                                {"title": "Upper Div Courses", "showlegend": True},
                            ],
                        ),
                        dict(
                            label="Crim Courses",
                            method="update",
                            args=[
                                {"visible": crim_courses},
                                {"title": "Criminalistics Courses", "showlegend": True},
                            ],
                        ),
                    ]
                ),
            )
        ]
    )

    # # graph 2
    # fig2 = px.bar(
    #     tester.iloc[:, :15],
    #     color_discrete_sequence=px.colors.sequential.Turbo_r,
    #     template="ggplot2",
    #     barmode="overlay",
    #     title="Student total enrollment over time",
    # )

    # fig2.update_layout(yaxis_title="Student Count",)

    # Graph 2
    fig2 = go.Figure()
    for i in range(15):
        fig2.add_trace(
            go.Bar(
                x=tester.index,
                y=tester.iloc[:, i],
                name=tester.columns[i].strftime("%Y-%m-%d"),
                marker_color=px.colors.sequential.Turbo_r[i],
            )
        )

    for i in range(len(old.index)):
        if old.index[i] in tester.index:
            ind = list(tester.index).index(old.index[i])
            fig2.add_shape(
                type="line",
                x0=ind - 0.4,
                y0=old.iloc[i, 0],
                x1=ind + 0.4,
                y1=old.iloc[i, 0],
                opacity=1,
                line=dict(color="Magenta", width=3),
            )

    fig2.update_layout(
        barmode="overlay",
        colorscale={"sequential": px.colors.sequential.Turbo_r},
        template="ggplot2",
        title="Student total enrollment over time",
        yaxis_title="Student Count",
    )

    # Graph 3
    # fig = px.bar(
    #     tester3.iloc[:, :15],
    #     template="ggplot2",
    #     barmode="overlay",
    #     color_discrete_sequence=px.colors.sequential.Turbo_r,
    #     title="Percent max enrollment over time",
    # )

    # fig.update_layout(yaxis_title="Fraction",)

    # Graph 3
    fig = go.Figure()
    for i in range(15):
        fig.add_trace(
            go.Bar(
                x=tester3.index,
                y=tester3.iloc[:, i],
                name=tester3.columns[i].strftime("%Y-%m-%d"),
                marker_color=px.colors.sequential.Turbo_r[i],
            )
        )

    for i in range(len(max_old.index)):
        if max_old.index[i] in tester.index:
            ind = list(tester.index).index(max_old.index[i])
            fig.add_shape(
                type="line",
                x0=ind - 0.4,
                y0=max_old.iloc[i, 0],
                x1=ind + 0.4,
                y1=max_old.iloc[i, 0],
                opacity=1,
                line=dict(color="Magenta", width=3),
            )

    fig.update_layout(
        barmode="overlay",
        colorscale={"sequential": px.colors.sequential.Turbo_r},
        template="ggplot2",
        title="Student total enrollment over time",
        yaxis_title="Student Count",
    )

    return fig4, fig2, fig


def generate_old_graph(test_vs_old: pd.DataFrame) -> Any:
    """Take in comparison vs previous year data and create a graph object.

    Args:
        test_vs_old (pd.DataFrame):

    Returns:
        Any: plotly graph object
    """

    # Graph 4
    fig_old = px.bar(
        test_vs_old.iloc[:, :15],
        template="ggplot2",
        barmode="overlay",
        color_discrete_sequence=px.colors.sequential.Turbo_r,
        title="Percent enrollment vs previous year, over time",
    )

    fig_old.add_shape(
        type="line",
        x0=0,
        x1=1,
        xref="paper",
        y0=1,
        y1=1,
        line=dict(color="black", width=2, dash="dot"),
    )

    fig_old.update_layout(yaxis_title="Fraction",)

    return fig_old


def generate_heatmap(tester3: pd.DataFrame) -> Any:
    """Take in enrollment over time data and create a heatmap graph object.

    Args:
        tester (pd.DataFrame):

    Returns:
        Any: plotly graph object
    """

    test = tester3
    test = test.drop(["CHE3980", "CHE4370", "CHE4700", "CHE4710"])
    test = test.iloc[::-1]
    fig_map = go.Figure()

    fig_map.add_trace(
        go.Heatmap(y=test.index, x=test.columns, z=test, colorscale="viridis", ygap=1,)
    )

    fig_map.update_layout(
        template="ggplot2",
        xaxis=dict(tickformat="%b %d"),
        yaxis=dict(dtick="D1"),
        title="Percent Max Enrollment over time",
    )

    return fig_map


def data_bars(column_data, column_apply):
    """Apply styling to dash table columns.

    Args:
        column_data: data from column.
        column_apply: id of column to apply styles to.

    Returns:
        styles: a list of styles for the dash table
    """

    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [100 * i for i in bounds]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append(
            {
                "if": {
                    "filter_query": (
                        "{{{column}}} >= {min_bound}"
                        + (
                            " && {{{column}}} < {max_bound}"
                            if (i < len(bounds) - 1)
                            else ""
                        )
                    ).format(
                        column=column_data, min_bound=min_bound, max_bound=max_bound
                    ),
                    "column_id": column_apply,
                },
                "background": (
                    """
                    linear-gradient(90deg,
                    #CACACA 0%,
                    #CACACA {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(
                        max_bound_percentage=max_bound_percentage
                    )
                ),
                "paddingBottom": 2,
                "paddingTop": 2,
            }
        )

    return styles


def create_dash_table(df):
    """Create a nicely formatted dash table

    Args:
        df (pd.DataFrame): Course dataframe to use

    Returns:
        dash_table: dash_table html element
    """

    nice_table = dash_table.DataTable(
        id="datatable-filtering",
        data=df.to_dict("records"),
        columns=[
            {"name": n, "id": i}
            for n, i in zip(
                [
                    "Subj",
                    "Nmbr",
                    "CRN",
                    "Sec",
                    "S",
                    "Cam",
                    "Title",
                    "Credit",
                    "Max",
                    "Enrl",
                    "WCap",
                    "WLst",
                    "Days",
                    "Time",
                    "Loc",
                    "Rcap",
                    "%Ful",
                    "Begin/End",
                    "Instructor",
                ],
                [*df.columns[:6], *df.columns[7:-3]],
            )
        ],
        style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold",},
        style_cell={"font-family": "lato", "font-size": "0.6rem"},
        style_cell_conditional=[
            {
                "if": {"column_id": i},
                "textAlign": "left",
                "minWidth": w,
                "width": w,
                "maxWidth": w,
                "whiteSpace": "normal",
                "lineHeight": "0.5rem",
            }
            for i, w in zip(
                [*df.columns[:6], *df.columns[7:-3]],
                [
                    "3.5%",
                    "5%",
                    "4%",
                    "4%",
                    "2%",
                    "4%",
                    "10%",
                    "5%",
                    "4%",
                    "4%",
                    "5%",
                    "5%",
                    "5%",
                    "7.5%",
                    "6%",
                    "4.5%",
                    "4.5%",
                    "7.5%",
                    "9.5%",
                ],
            )
        ],
        # sort_action="native",
        # filter_action="native",
        fixed_rows={"headers": True, "data": 0},
        # page_size=5000,
        # page_action="native",
        style_table={"height": "62vh", "overflowY": "auto"},
        style_data_conditional=[
            *data_bars("Ratio", "Max"),
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)",},
            {
                "if": {"filter_query": "{WList} > 0", "column_id": "WList"},
                "backgroundColor": "#FFEB9C",
                "color": "#9C6500",
            },
            {
                "if": {
                    "filter_query": "({Enrolled} < 10 && {Max} >= 20 && {S} contains A) || ({Enrolled} < 6 && {S} contains A)",  # noqa
                    "column_id": "Enrolled",
                },
                "backgroundColor": "#FFC7CE",
                "color": "#9C0006",
            },
            {
                "if": {"filter_query": "{Ratio} > 80", "column_id": "Enrolled"},
                "backgroundColor": "#C6EFCE",
                "color": "#006100",
            },
            {
                "if": {"filter_query": "{Ratio} > 94", "column_id": "Enrolled"},
                "backgroundColor": "#008000",
                "color": "white",
            },
            {"if": {"filter_query": "{S} contains C",}, "backgroundColor": "#FF4136",},
        ],
    )

    return dbc.Container(
        [nice_table], className="ml-2 mr-2 mt-5", style={"height": "65vh"}
    )


def data_graph(fig_obj: Any, id_name: str) -> Any:
    """Creates dash graph from plotly graph object.

    Args:
        fig_obj (Any): a dash graph object
        id_name (str): a unique id name for the component

    Returns:
        Any: a dash graph
    """

    return (
        dcc.Graph(
            figure=fig_obj, id=id_name, style={"height": "65vh", "min-height": "750px"},
        ),
    )
