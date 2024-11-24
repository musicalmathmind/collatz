import numpy as np
import plotly.graph_objects as go
import utils.collatz_construction as cc
from utils.collatz_construction import OrbitOptions

point_size = 5

def draw_3d_scatterplot(points, labels=None, colors=None, width=800, height=600, 
                        x_axis="X Axis", y_axis="Y Axis", z_axis="Z Axis", title="3D Interactive Scatterplot"):
    """
    Draws a 3D interactive scatterplot using Plotly.

    :param points: List of tuples/lists with (x, y, z) coordinates.
    :param labels: List of labels for each point (optional).
    :param colors: List of colors for each point (optional).
    :param width: Width of the plot (default: 800).
    :param height: Height of the plot (default: 600).
    :param x_axis: Title for the X-axis (default: "X Axis").
    :param y_axis: Title for the Y-axis (default: "Y Axis").
    :param z_axis: Title for the Z-axis (default: "Z Axis").
    :param title: Title of the plot (default: "3D Interactive Scatterplot").
    """
    # Extract x, y, z coordinates
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    z = [p[2] for p in points]

    # Create hover text only if labels are provided
    hover_text = labels if labels else [""] * len(points)

    # Create a Plotly scatter plot
    scatter = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=point_size,
            color=colors if colors else 'blue',
            opacity=0.8
        ),
        text=hover_text,
        hoverinfo='text'
    )

    # Define the layout
    layout = go.Layout(
        title=title,
        scene=dict(
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            zaxis_title=z_axis
        ),
        width=width,
        height=height
    )

    # Create the figure and display it
    fig = go.Figure(data=[scatter], layout=layout)
    fig.show()


from typing import Union, List

def graph_options(
    up_to_n: int,
    options: Union[OrbitOptions, List[OrbitOptions]],
    colors: Union[str, List[str]] = 'red',
    title: str = 'Orbit Lengths'
):
    # Ensure options is a list
    if not isinstance(options, list):
        options = [options]
    
    # Ensure colors is a list and matches the length of options
    if isinstance(colors, str):
        colors = [colors] * len(options)
    elif isinstance(colors, list):
        if len(colors) != len(options):
            raise ValueError("The length of colors must match the length of options.")
    else:
        raise TypeError("colors must be a string or a list of strings.")
    
    points, labels, point_colors = process_orbit_info(up_to_n, options, colors)
    draw_3d_scatterplot(points, labels, point_colors, 800, 600, 'n', 'First Orbit Length', 'Total Orbit Length', title)

def process_orbit_info(
    up_to_n: int,
    options: List[OrbitOptions],
    colors: List[str]
):
    points = []
    labels = []
    point_colors = []
    
    for option, color in zip(options, colors):
        batch = cc.generate_orbit_info_batch(up_to_n, option)
        for orbit_info in batch:
            p = (
                orbit_info.n,
                len(orbit_info.first_orbit or []),
                len(orbit_info.total_orbit or [])
            )
            points.append(p)
            labels.append(str(p))
            point_colors.append(color)
    return points, labels, point_colors
