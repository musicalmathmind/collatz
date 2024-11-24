import numpy as np
import plotly.graph_objects as go
import utils.collatz_construction as cc
from utils.collatz_construction import OrbitOptions
from typing import Callable
from typing import Union, List

POINT_SIZE = 5

def draw_3d_scatterplot(points, labels=None, colors=None, width=800, height=600, 
                        x_axis="X Axis", y_axis="Y Axis", z_axis="Z Axis", title="3D Interactive Scatterplot"):
    """
    Draws an interactive 3D scatterplot using Plotly.

    Args:
        points (list[tuple[float, float, float]]): A list of (x, y, z) coordinates for the points to plot.
        labels (list[str], optional): A list of labels corresponding to each point, displayed on hover.
            Defaults to None, resulting in no labels.
        colors (list[str] or list[int], optional): A list of colors for each point. Can be color names, 
            hex codes, or numeric values for a color scale. Defaults to None, using a default color ('blue').
        width (int, optional): The width of the plot in pixels. Defaults to 800.
        height (int, optional): The height of the plot in pixels. Defaults to 600.
        x_axis (str, optional): Label for the X-axis. Defaults to "X Axis".
        y_axis (str, optional): Label for the Y-axis. Defaults to "Y Axis".
        z_axis (str, optional): Label for the Z-axis. Defaults to "Z Axis".
        title (str, optional): Title of the scatterplot. Defaults to "3D Interactive Scatterplot".

    Returns:
        None: Displays the interactive 3D scatterplot using Plotly.

    Notes:
        - Hover text is only enabled if `labels` is provided.
        - Colors can enhance visualization when multiple categories or gradients are represented.
        - Adjust `width` and `height` to fit different display resolutions.

    Example:
        points = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
        labels = ["Point A", "Point B", "Point C"]
        colors = ["red", "green", "blue"]
        draw_3d_scatterplot(points, labels, colors)
    """
    # Extract x, y, z coordinates from the input points
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    z = [p[2] for p in points]

    # Create hover text based on provided labels or use empty strings if no labels
    hover_text = labels if labels else [""] * len(points)

    # Define the 3D scatter plot using Plotly
    scatter = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=POINT_SIZE,  # Default point size
            color=colors if colors else 'blue',  # Use provided colors or default to blue
            opacity=0.8  # Semi-transparent markers
        ),
        text=hover_text,  # Text displayed on hover
        hoverinfo='text'  # Show only hover text in tooltips
    )

    # Define the layout of the plot, including axis labels and dimensions
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

    # Create the figure with the scatter plot and layout, then display it
    fig = go.Figure(data=[scatter], layout=layout)
    fig.show()


def graph_options(
    up_to_n: int,
    options: Union[OrbitOptions, List[OrbitOptions]],
    point_builder: Callable[[cc.OrbitInfo], tuple],
    colors: Union[str, List[str]] = 'red',
    x_axis: str = "X Axis",
    y_axis: str = "Y Axis",
    z_axis: str = "Z Axis",
    title: str = 'Orbit Lengths'
):
    """
    Generates a 3D scatterplot of orbit data for given options.

    Args:
        up_to_n (int): The upper limit for generating orbit data (inclusive).
        options (Union[OrbitOptions, List[OrbitOptions]]): A single `OrbitOptions` instance or 
            a list of `OrbitOptions` instances defining the rules for orbit generation.
        point_builder (Callable[[cc.OrbitInfo], tuple]): A function that processes an orbit's info 
            and returns a tuple of (x, y, z) coordinates for plotting.
        colors (Union[str, List[str]], optional): A single color (str) or a list of colors 
            corresponding to each option. Defaults to 'red'.
        x_axis (str, optional): Label for the X-axis. Defaults to "X Axis".
        y_axis (str, optional): Label for the Y-axis. Defaults to "Y Axis".
        z_axis (str, optional): Label for the Z-axis. Defaults to "Z Axis".
        title (str, optional): Title of the scatterplot. Defaults to 'Orbit Lengths'.

    Raises:
        ValueError: If the length of `colors` does not match the length of `options`.
        TypeError: If `colors` is neither a string nor a list of strings.

    Returns:
        None: Displays the 3D scatterplot.

    Notes:
        - Converts a single `OrbitOptions` object into a list for uniform processing.
        - Ensures the `colors` parameter matches the number of `options` to avoid mismatched data.
        - Calls `process_orbit_info` to generate plotting data for each `OrbitOptions` instance.

    Example:
        options = [
            OrbitOptions("3x_plus_1", 1, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit),
            OrbitOptions("3x_plus_3", 3, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit)
        ]
        graph_options(
            up_to_n=100,
            options=options,
            point_builder=build_point,
            colors=["red", "blue"],
            x_axis="Start",
            y_axis="Length",
            z_axis="Steps",
            title="Orbit Visualization"
        )
    """
    # Ensure `options` is a list for consistent processing
    if not isinstance(options, list):
        options = [options]
    
    # Ensure `colors` is a list and matches the length of `options`
    if isinstance(colors, str):
        colors = [colors] * len(options)
    elif isinstance(colors, list):
        if len(colors) != len(options):
            raise ValueError("The length of colors must match the length of options.")
    else:
        raise TypeError("colors must be a string or a list of strings.")
    
    # Initialize collections for plotting data
    all_points = []
    all_labels = []
    all_colors = []
    
    # Process orbit info for each option and color
    for option, color in zip(options, colors):
        points, labels, point_colors = process_orbit_info(up_to_n, [option], [color], point_builder)
        all_points.extend(points)
        all_labels.extend(labels)
        all_colors.extend(point_colors)
    
    # Generate the 3D scatterplot
    draw_3d_scatterplot(all_points, all_labels, all_colors, 800, 600, x_axis, y_axis, z_axis, title)


def process_orbit_info(
    up_to_n: int,
    options: List[OrbitOptions],
    colors: List[str],
    point_builder: Callable[[cc.OrbitInfo], tuple]
):
    """
    Processes orbit information and prepares data for visualization.

    Args:
        up_to_n (int): The upper limit for generating orbit data (inclusive).
        options (List[OrbitOptions]): A list of `OrbitOptions` instances defining rules for orbit generation.
        colors (List[str]): A list of colors corresponding to each `OrbitOptions` instance. 
            Each color will be assigned to the points generated for the respective option.
        point_builder (Callable[[cc.OrbitInfo], tuple]): A function that processes an `OrbitInfo` object 
            and returns a tuple of (x, y, z) coordinates for plotting.

    Returns:
        tuple: A tuple containing:
            - points (list[tuple]): A list of (x, y, z) coordinates for each processed orbit.
            - labels (list[str]): A list of string labels for each point.
            - point_colors (list[str]): A list of colors corresponding to each point.

    Raises:
        ValueError: If the length of `colors` does not match the length of `options`.

    Notes:
        - Calls `cc.generate_orbit_info_batch` to generate orbit data for each `OrbitOptions` instance.
        - Each generated orbit is processed by the `point_builder` function to extract 3D coordinates.
        - The `colors` list ensures visual distinction between points generated from different options.

    Example:
        options = [
            OrbitOptions("3x_plus_1", 1, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit),
            OrbitOptions("3x_plus_3", 3, should_halt, should_decrease, should_increase, decrease, increase, append_to_orbit)
        ]
        colors = ["red", "blue"]
        points, labels, point_colors = process_orbit_info(100, options, colors, build_point)
    """
    points = []
    labels = []
    point_colors = []
    
    # Iterate through each option and its corresponding color
    for option, color in zip(options, colors):
        # Generate a batch of orbit information up to the specified limit
        batch = cc.generate_orbit_info_batch(up_to_n, option)
        
        # Process each orbit in the batch
        for orbit_info in batch:
            p = point_builder(orbit_info)  # Build the (x, y, z) point
            points.append(p)  # Append the point to the list
            labels.append(str(p))  # Create a string label for the point
            point_colors.append(color)  # Assign the corresponding color to the point

    # Return the processed data
    return points, labels, point_colors

