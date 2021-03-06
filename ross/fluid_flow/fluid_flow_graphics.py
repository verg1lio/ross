import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "browser"


def plot_eccentricity(fluid_flow_object, z=0, **kwargs):
    """Plot the rotor eccentricity.

    This function assembles pressure graphic along the z-axis.
    The first few plots are of a different color to indicate where theta begins.

    Parameters
    ----------
    fluid_flow_object: a FluidFlow object
    z: int, optional
        The distance in z where to cut and plot.
    kwargs : optional
        Additional key word arguments can be passed to change the plot layout only
        (e.g. width=1000, height=800, ...).
        *See Plotly Python Figure Reference for more information.

    Returns
    -------
    fig : Plotly graph_objects.Figure()
        The figure object with the plot.

    Examples
    --------
    >>> from ross.fluid_flow.fluid_flow import fluid_flow_example
    >>> my_fluid_flow = fluid_flow_example()
    >>> fig = plot_eccentricity(my_fluid_flow, z=int(my_fluid_flow.nz/2))
    >>> # to show the plots you can use:
    >>> # show(fig)
    """
    kwargs_default_values = dict(
        width=600,
        height=600,
        plot_bgcolor="white",
        hoverlabel_align="right",
        legend=dict(
            font=dict(family="sans-serif", size=14),
            bgcolor="white",
            bordercolor="black",
            borderwidth=2,
        ),
    )
    for k, v in kwargs_default_values.items():
        kwargs.setdefault(k, v)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=fluid_flow_object.xre[z],
            y=fluid_flow_object.yre[z],
            mode="markers+lines",
            marker=dict(size=10, color="firebrick"),
            line=dict(width=2.0, color="firebrick"),
            name="Stator",
            legendgroup="Stator",
            hovertemplate=("<b>X: %{x:.3e}</b><br>" + "<b>Y: %{y:.3e}</b>"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=fluid_flow_object.xri[z],
            y=fluid_flow_object.yri[z],
            mode="markers+lines",
            marker=dict(size=10, color="royalblue"),
            line=dict(width=2.0, color="royalblue"),
            name="Rotor",
            legendgroup="Rotor",
            hovertemplate=("<b>X: %{x:.3e}</b><br>" + "<b>Y: %{y:.3e}</b>"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[fluid_flow_object.xi],
            y=[fluid_flow_object.yi],
            marker=dict(size=10, color="firebrick"),
            name="Stator",
            legendgroup="Stator",
            showlegend=False,
            hovertemplate=("<b>X: %{x:.3e}</b><br>" + "<b>Y: %{y:.3e}</b>"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            marker=dict(size=10, color="royalblue"),
            name="Rotor",
            legendgroup="Rotor",
            showlegend=False,
            hovertemplate=("<b>X: %{x:.3e}</b><br>" + "<b>Y: %{y:.3e}</b>"),
        )
    )
    fig.update_xaxes(
        title_text="<b>X axis</b>",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor="lightgray",
        showline=True,
        linewidth=2.5,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        title_text="<b>Y axis</b>",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor="lightgray",
        showline=True,
        linewidth=2.5,
        linecolor="black",
        mirror=True,
    )
    fig.update_layout(
        title=dict(text="<b>Cut in plane Z={}</b>".format(z), font=dict(size=16)),
        **kwargs,
    )

    return fig


def plot_pressure_z(fluid_flow_object, theta=0, **kwargs):
    """Plot the pressure distribution along the z-axis.

    This function assembles pressure graphic along the z-axis for one or both the
    numerically (blue) and analytically (red) calculated pressure matrices, depending
    on if one or both were calculated.

    Parameters
    ----------
    fluid_flow_object: a FluidFlow object
    theta: int, optional
        The theta to be considered.
    kwargs : optional
        Additional key word arguments can be passed to change the plot layout only
        (e.g. width=1000, height=800, ...).
        *See Plotly Python Figure Reference for more information.

    Returns
    -------
    fig : Plotly graph_objects.Figure()
        The figure object with the plot.

    Examples
    --------
    >>> from ross.fluid_flow.fluid_flow import fluid_flow_example
    >>> my_fluid_flow = fluid_flow_example()
    >>> my_fluid_flow.calculate_pressure_matrix_numerical() # doctest: +ELLIPSIS
    array([[...
    >>> fig = plot_pressure_z(my_fluid_flow, theta=int(my_fluid_flow.ntheta/2))
    >>> # to show the plots you can use:
    >>> # fig.show()
    """
    if (
        not fluid_flow_object.numerical_pressure_matrix_available
        and not fluid_flow_object.analytical_pressure_matrix_available
    ):
        raise ValueError(
            "Must calculate the pressure matrix. "
            "Try calling calculate_pressure_matrix_numerical() or calculate_pressure_matrix_analytical() first."
        )
    kwargs_default_values = dict(
        width=800,
        height=600,
        plot_bgcolor="white",
        hoverlabel_align="right",
        legend=dict(
            font=dict(family="sans-serif", size=14),
            bgcolor="white",
            bordercolor="black",
            borderwidth=2,
        ),
    )
    for k, v in kwargs_default_values.items():
        kwargs.setdefault(k, v)

    fig = go.Figure()
    if fluid_flow_object.numerical_pressure_matrix_available:
        fig.add_trace(
            go.Scatter(
                x=fluid_flow_object.z_list,
                y=fluid_flow_object.p_mat_numerical[:, theta],
                mode="lines",
                line=dict(width=3.0, color="royalblue"),
                showlegend=True,
                name="<b>Numerical pressure</b>",
                hovertemplate=(
                    "<b>Axial Length: %{x:.2f}</b><br>"
                    + "<b>Numerical pressure: %{y:.2f}</b>"
                ),
            )
        )
    if fluid_flow_object.analytical_pressure_matrix_available:
        fig.add_trace(
            go.Scatter(
                x=fluid_flow_object.z_list,
                y=fluid_flow_object.p_mat_analytical[:, theta],
                mode="lines",
                line=dict(width=3.0, color="firebrick"),
                showlegend=True,
                name="<b>Analytical pressure</b>",
                hovertemplate=(
                    "<b>Axial Length: %{x:.2f}</b><br>"
                    + "<b>Analytical pressure: %{y:.2f}</b>"
                ),
            )
        )
    fig.update_xaxes(
        title_text="<b>Axial Length</b>",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor="lightgray",
        showline=True,
        linewidth=2.5,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        title_text="<b>Pressure</b>",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor="lightgray",
        showline=True,
        linewidth=2.5,
        linecolor="black",
        mirror=True,
    )
    fig.update_layout(
        title=dict(
            text=(
                "<b>Pressure along the flow (axial direction)<b><br>"
                + "<b>Theta={}</b>".format(theta)
            ),
            font=dict(size=16),
        ),
        **kwargs,
    )

    return fig


def plot_shape(fluid_flow_object, theta=0, **kwargs):
    """Plot the surface geometry of the rotor.

    This function assembles a graphic representing the geometry of the rotor.

    Parameters
    ----------
    fluid_flow_object: a FluidFlow object
    theta: int, optional
        The theta to be considered.

    Returns
    -------
    fig : Plotly graph_objects.Figure()
        The figure object with the plot.
    kwargs : optional
        Additional key word arguments can be passed to change the plot layout only
        (e.g. width=1000, height=800, ...).
        *See Plotly Python Figure Reference for more information.

    Examples
    --------
    >>> from ross.fluid_flow.fluid_flow import fluid_flow_example
    >>> my_fluid_flow = fluid_flow_example()
    >>> fig = plot_shape(my_fluid_flow, theta=int(my_fluid_flow.ntheta/2))
    >>> # to show the plots you can use:
    >>> # fig.show()
    """
    kwargs_default_values = dict(
        width=800,
        height=600,
        plot_bgcolor="white",
        hoverlabel_align="right",
        legend=dict(
            font=dict(family="sans-serif", size=14),
            bgcolor="white",
            bordercolor="black",
            borderwidth=2,
        ),
    )
    for k, v in kwargs_default_values.items():
        kwargs.setdefault(k, v)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=fluid_flow_object.z_list,
            y=fluid_flow_object.re[:, theta],
            mode="lines",
            line=dict(width=3.0, color="firebrick"),
            showlegend=True,
            hoverinfo="none",
            name="<b>Stator</b>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=fluid_flow_object.z_list,
            y=fluid_flow_object.ri[:, theta],
            mode="lines",
            line=dict(width=3.0, color="royalblue"),
            showlegend=True,
            hoverinfo="none",
            name="<b>Rotor</b>",
        )
    )
    fig.update_xaxes(
        title_text="<b>Axial Length</b>",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor="lightgray",
        showline=True,
        linewidth=2.5,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        title_text="<b>Radial direction</b>",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor="lightgray",
        showline=True,
        linewidth=2.5,
        linecolor="black",
        mirror=True,
    )
    fig.update_layout(
        title=dict(
            text=(
                "<b>Shapes of stator and rotor - Axial direction<b><br>"
                + "<b>Theta={}</b>".format(theta)
            ),
            font=dict(size=16),
        ),
        **kwargs,
    )

    return fig


def plot_pressure_theta(fluid_flow_object, z=0, **kwargs):
    """Plot the pressure distribution along theta.

    This function assembles pressure graphic in the theta direction for a given z
    for one or both the numerically (blue) and analytically (red) calculated pressure
    matrices, depending on if one or both were calculated.

    Parameters
    ----------
    fluid_flow_object: a FluidFlow object
    z: int, optional
        The distance along z-axis to be considered.
    kwargs : optional
        Additional key word arguments can be passed to change the plot layout only
        (e.g. width=1000, height=800, ...).
        *See Plotly Python Figure Reference for more information.

    Returns
    -------
    fig : Plotly graph_objects.Figure()
        The figure object with the plot.

    Examples
    --------
    >>> from ross.fluid_flow.fluid_flow import fluid_flow_example
    >>> my_fluid_flow = fluid_flow_example()
    >>> my_fluid_flow.calculate_pressure_matrix_numerical() # doctest: +ELLIPSIS
    array([[...
    >>> fig = plot_pressure_theta(my_fluid_flow, z=int(my_fluid_flow.nz/2))
    >>> # to show the plots you can use:
    >>> # fig.show()
    """
    if (
        not fluid_flow_object.numerical_pressure_matrix_available
        and not fluid_flow_object.analytical_pressure_matrix_available
    ):
        raise ValueError(
            "Must calculate the pressure matrix. "
            "Try calling calculate_pressure_matrix_numerical() or calculate_pressure_matrix_analytical() first."
        )
    kwargs_default_values = dict(
        width=800,
        height=600,
        plot_bgcolor="white",
        hoverlabel_align="right",
        legend=dict(
            font=dict(family="sans-serif", size=14),
            bgcolor="white",
            bordercolor="black",
            borderwidth=2,
        ),
    )
    for k, v in kwargs_default_values.items():
        kwargs.setdefault(k, v)

    fig = go.Figure()
    if fluid_flow_object.numerical_pressure_matrix_available:
        fig.add_trace(
            go.Scatter(
                x=fluid_flow_object.gama[z],
                y=fluid_flow_object.p_mat_numerical[z],
                mode="lines",
                line=dict(width=3.0, color="royalblue"),
                showlegend=True,
                name="<b>Numerical pressure</b>",
                hovertemplate=(
                    "<b>Theta: %{x:.2f}</b><br>" + "<b>Numerical pressure: %{y:.2f}</b>"
                ),
            )
        )
    elif fluid_flow_object.analytical_pressure_matrix_available:
        fig.add_trace(
            go.Scatter(
                x=fluid_flow_object.gama[z],
                y=fluid_flow_object.p_mat_analytical[z],
                mode="lines",
                line=dict(width=3.0, color="firebrick"),
                showlegend=True,
                name="<b>Analytical pressure</b>",
                hovertemplate=(
                    "<b>Theta: %{x:.2f}</b><br>"
                    + "<b>Analytical pressure: %{y:.2f}</b>"
                ),
            )
        )

    fig.update_xaxes(
        title_text="<b>Theta value</b>",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor="lightgray",
        showline=True,
        linewidth=2.5,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        title_text="<b>Pressure</b>",
        title_font=dict(size=16),
        tickfont=dict(size=14),
        gridcolor="lightgray",
        showline=True,
        linewidth=2.5,
        linecolor="black",
        mirror=True,
    )
    fig.update_layout(
        title=dict(
            text=("<b>Pressure along Theta | Z={}<b>".format(z)), font=dict(size=16)
        ),
        **kwargs,
    )

    return fig


def plot_pressure_theta_cylindrical(
    fluid_flow_object, z=0, from_numerical=True, **kwargs
):
    """Plot cylindrical pressure graphic in the theta direction.

    This function assembles cylindrical graphical visualization of the fluid pressure
    in the theta direction for a given axial position (z).

    Parameters
    ----------
    fluid_flow_object: a FluidFlow object
    z: int, optional
        The distance along z-axis to be considered.
    from_numerical: bool, optional
        If True, takes the numerically calculated pressure matrix as entry.
        If False, takes the analytically calculated one instead.
        If condition cannot be satisfied (matrix not calculated), it will take the one
        that is available and raise a warning.
    kwargs : optional
        Additional key word arguments can be passed to change the plot layout only
        (e.g. width=1000, height=800, ...).
        *See Plotly Python Figure Reference for more information.

    Returns
    -------
    fig : Plotly graph_objects.Figure()
        The figure object with the plot.

    Examples
    --------
    >>> from ross.fluid_flow.fluid_flow import fluid_flow_example
    >>> my_fluid_flow = fluid_flow_example()
    >>> my_fluid_flow.calculate_pressure_matrix_numerical() # doctest: +ELLIPSIS
    array([[...
    >>> fig = plot_pressure_theta_cylindrical(my_fluid_flow, z=int(my_fluid_flow.nz/2))
    >>> # to show the plots you can use:
    >>> # fig.show()
    """
    if (
        not fluid_flow_object.numerical_pressure_matrix_available
        and not fluid_flow_object.analytical_pressure_matrix_available
    ):
        raise ValueError(
            "Must calculate the pressure matrix. "
            "Try calling calculate_pressure_matrix_numerical() or calculate_pressure_matrix_analytical() first."
        )
    if from_numerical:
        if fluid_flow_object.numerical_pressure_matrix_available:
            p_mat = fluid_flow_object.p_mat_numerical
        else:
            p_mat = fluid_flow_object.p_mat_analytical
    else:
        if fluid_flow_object.analytical_pressure_matrix_available:
            p_mat = fluid_flow_object.p_mat_analytical
        else:
            p_mat = fluid_flow_object.p_mat_numerical

    r = np.linspace(
        fluid_flow_object.radius_rotor,
        fluid_flow_object.radius_stator,
        fluid_flow_object.nradius,
    )
    theta = np.linspace(
        0.0, 2.0 * np.pi + fluid_flow_object.dtheta / 2, fluid_flow_object.ntheta
    )
    theta *= 180 / np.pi

    pressure_along_theta = p_mat[z, :]
    min_pressure = np.amin(pressure_along_theta)

    r_matrix, theta_matrix = np.meshgrid(r, theta)
    z_matrix = np.zeros((theta.size, r.size))

    for i in range(0, theta.size):
        inner_radius = np.sqrt(
            fluid_flow_object.xri[z][i] * fluid_flow_object.xri[z][i]
            + fluid_flow_object.yri[z][i] * fluid_flow_object.yri[z][i]
        )

        for j in range(r.size):
            if r_matrix[i][j] < inner_radius:
                continue
            z_matrix[i][j] = pressure_along_theta[i] - min_pressure + 0.01

    kwargs_default_values = dict(width=1200, height=900)
    for k, v in kwargs_default_values.items():
        kwargs.setdefault(k, v)

    fig = go.Figure(
        go.Barpolar(
            r=r_matrix.ravel(),
            theta=theta_matrix.ravel(),
            customdata=z_matrix.ravel(),
            marker=dict(
                color=z_matrix.ravel(),
                colorscale="Viridis",
                cmin=np.amin(z_matrix),
                cmax=np.amax(z_matrix),
                colorbar=dict(
                    title=dict(text="<b>Pressure</b>", side="top", font=dict(size=16)),
                    tickfont=dict(size=16),
                ),
            ),
            thetaunit="degrees",
            name="Pressure",
            showlegend=False,
            hovertemplate=(
                "<b>Raddi: %{r:.4e}</b><br>"
                + "<b>θ: %{theta:.2f}</b><br>"
                + "<b>Pressure: %{customdata:.4e}</b>"
            ),
        )
    )
    fig.update_layout(
        polar=dict(
            hole=0.5,
            bgcolor="white",
            bargap=0.0,
            radialaxis=dict(gridcolor="lightgray", nticks=5),
            angularaxis=dict(
                rotation=-90 - fluid_flow_object.attitude_angle * 180 / np.pi,
                gridcolor="lightgray",
                linecolor="black",
                linewidth=2.5,
            ),
        ),
        **kwargs,
    )
    return fig


def plot_pressure_surface(fluid_flow_object, **kwargs):
    """Assembles pressure surface graphic in the bearing, using Plotly.

    Parameters
    ----------
    fluid_flow_object: a FluidFlow object
    kwargs : optional
        Additional key word arguments can be passed to change the plot layout only
        (e.g. width=1000, height=800, ...).
        *See Plotly Python Figure Reference for more information.

    Returns
    -------
    fig : Plotly graph_objects.Figure()
        The figure object with the plot.

    Examples
    --------
    >>> from ross.fluid_flow.fluid_flow import fluid_flow_example
    >>> my_fluid_flow = fluid_flow_example()
    >>> my_fluid_flow.calculate_pressure_matrix_numerical() # doctest: +ELLIPSIS
    array([[...
    >>> fig = plot_pressure_surface(my_fluid_flow)
    >>> # to show the plots you can use:
    >>> # fig.show()
    """
    if (
        not fluid_flow_object.numerical_pressure_matrix_available
        and not fluid_flow_object.analytical_pressure_matrix_available
    ):
        raise ValueError(
            "Must calculate the pressure matrix. "
            "Try calling calculate_pressure_matrix_numerical() or calculate_pressure_matrix_analytical() first."
        )

    kwargs_default_values = dict(width=1200, height=900)
    for k, v in kwargs_default_values.items():
        kwargs.setdefault(k, v)

    fig = go.Figure()
    if fluid_flow_object.numerical_pressure_matrix_available:
        z, theta = np.meshgrid(fluid_flow_object.z_list, fluid_flow_object.gama[0])
        fig.add_trace(
            go.Surface(
                x=z,
                y=theta,
                z=fluid_flow_object.p_mat_numerical.T,
                colorscale="Viridis",
                cmin=np.amin(fluid_flow_object.p_mat_numerical.T),
                cmax=np.amax(fluid_flow_object.p_mat_numerical.T),
                colorbar=dict(
                    title=dict(text="<b>Pressure</b>", side="top", font=dict(size=16)),
                    tickfont=dict(size=16),
                ),
                name="Pressure",
                showlegend=False,
                hovertemplate=(
                    "<b>Length: %{x:.2e}</b><br>"
                    + "<b>Angular Position: %{y:.2f}</b><br>"
                    + "<b>Pressure: %{z:.2f}</b>"
                ),
            )
        )
    if fluid_flow_object.analytical_pressure_matrix_available:
        z, theta = np.meshgrid(fluid_flow_object.z_list, fluid_flow_object.gama[0])
        fig.add_trace(
            go.Surface(
                x=z,
                y=theta,
                z=fluid_flow_object.p_mat_analytical.T,
                colorscale="Viridis",
                cmin=np.amin(fluid_flow_object.p_mat_analytical.T),
                cmax=np.amax(fluid_flow_object.p_mat_analytical.T),
                colorbar=dict(
                    title=dict(text="<b>Pressure</b>", side="top", font=dict(size=16)),
                    tickfont=dict(size=16),
                ),
                name="Pressure",
                showlegend=False,
                hovertemplate=(
                    "<b>Length: %{x:.2e}</b><br>"
                    + "<b>Angular Position: %{y:.2f}</b><br>"
                    + "<b>Pressure: %{z:.2f}</b>"
                ),
            )
        )

    fig.update_layout(
        scene=dict(
            bgcolor="white",
            xaxis=dict(
                title=dict(text="<b>Rotor Length</b>", font=dict(size=14)),
                tickfont=dict(size=16),
                nticks=5,
                backgroundcolor="lightgray",
                gridcolor="white",
                showspikes=False,
            ),
            yaxis=dict(
                title=dict(text="<b>Angular Position</b>", font=dict(size=14),),
                tickfont=dict(size=16),
                nticks=5,
                backgroundcolor="lightgray",
                gridcolor="white",
                showspikes=False,
            ),
            zaxis=dict(
                title=dict(text="<b>Pressure</b>", font=dict(size=14),),
                tickfont=dict(size=16),
                nticks=5,
                backgroundcolor="lightgray",
                gridcolor="white",
                showspikes=False,
            ),
        ),
        title=dict(text=("<b>Bearing Pressure Field</b>"), font=dict(size=20),),
        **kwargs,
    )

    return fig
