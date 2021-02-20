# -*- coding: utf-8 -*-

"""Layout for Plotly Dash webapp to process SWRCGSR Enrollment Reports from Ellucian Banner."""

# Import required libraries
import dash_html_components as html
import dash_bootstrap_components as dbc
from typing import Any, Dict


def generate_layout(graph_dict: Dict[str, Any], term: str) -> Any:
    """Create a dash bootstrap based website layout.

    Args:
        graph_dict (Dict[str, Any]: dictionary of plotly graph objects and dash tables.
        term (str): term to analyze, e.g. "Spring2021"

    Returns:
        html.Div wrapping a website layout.
    """

    nav_text = dbc.NavItem(dbc.NavLink("Designed by", disabled=True, href="#"))

    nav_item = dbc.NavItem(
        dbc.NavLink("Dr. Andrew J. Bonham", href="https://github.com/Paradoxdruid")
    )

    nav_bar = dbc.NavbarSimple(
        children=[nav_text, nav_item],
        brand=f"CHE Enrollment Statistics -- {term}",
        # brand_href="#",
        brand_style={"font-weight": "bold"},
        sticky="top",
        className="mb-2",
        fluid=True,
    )

    bottom_bar = dbc.NavbarSimple(
        children=[
            dbc.NavLink(
                "MSU Denver Covid Tracker",
                href="https://msu-covid-tracker.herokuapp.com",
            ),
            dbc.NavLink("Bonham Code projects", href="https://bonhamcode.com"),
            dbc.NavLink("Dr. Bonham's Research Lab", href="https://www.bonhamlab.com"),
        ],
        brand="Other Projects:",
        sticky="bottom",
        className="mt-2",
        fluid=True,
    )

    all_tabs = dbc.Tabs(
        [
            dbc.Tab(graph_dict["Heatmap"], label="Heatmap"),
            dbc.Tab(graph_dict["Over Time"], label="Over Time"),
            dbc.Tab(graph_dict["Total"], label="Total"),
            dbc.Tab(graph_dict["Percent Max"], label="Percent Max"),
            dbc.Tab(graph_dict["Percent Last Year"], label="Percent Last Year"),
            dbc.Tab(graph_dict["Latest Data"], label="Latest Data"),
        ],
    )

    return html.Div(
        [
            nav_bar,
            dbc.Container(
                fluid=True,
                children=[
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                [all_tabs],
                                className="m-3",
                            ),
                            width=12,
                            style={
                                "min-width": "750px",
                                "max-width": "1400px",
                            },
                        ),
                    ),
                ],
            ),
            bottom_bar,
        ],
    )
