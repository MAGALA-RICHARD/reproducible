import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os, subprocess


def open_file(file_name):
    try:
        if hasattr(os, 'startfile'):  # windows platform
            os.startfile(file_name)
        else:
            subprocess.call(['open', file_name])
    except FileNotFoundError:
        pass
    except OSError:
        pass


def plot_reg_fit(
        X, y,
        data: pd.DataFrame | None = None,
        fig_name: str = None,
        xname: str | None = None,
        yname: str | None = None,
        color_by: str | None = None,  # e.g., 'year' to color groups
        n_points: int = 200,
        xlabel: str = "Observed soil organic carbon",
        ylabel: str = "APSIM model predicted soil organic carbon",
        show_eq: bool = True
):
    """
    Plot a simple linear regression fit for a single predictor X vs. y.

    - Supports X as 1D array/Series OR (data, xname) with y=(data, yname).
    - Raises if X has more than 1 column.
    - Sorts X for a clean fitted line.
    """
    fig_name = fig_name or f'{xname}corn_grain_yield_Mg{yname}.png'
    # Resolve X, y from DataFrame if names are given
    if data is not None and xname and yname:
        Xv = data[xname].to_numpy().reshape(-1, 1)
        yv = data[yname].to_numpy().ravel()
    else:
        X = np.asarray(X)
        y = np.asarray(y)
        # Accept Series/list/1D array; also allow shape (n, 1)
        if X.ndim == 1:
            Xv = X.reshape(-1, 1)
        elif X.ndim == 2 and X.shape[1] == 1:
            Xv = X
        else:
            raise ValueError("X must be 1D (n,) or (n,1) to plot a fitted line.")
        yv = y.ravel()

    # Fit
    model = LinearRegression()
    model.fit(Xv, yv)

    # Make a sorted grid for the line
    x_min = np.nanmin(Xv)
    x_max = np.nanmax(Xv)
    x_grid = np.linspace(x_min, x_max, n_points).reshape(-1, 1)
    y_grid = model.predict(x_grid)

    # Coeffs / metrics
    slope = float(model.coef_[0])
    intercept = float(model.intercept_)
    r2 = model.score(Xv, yv)

    # Plot
    plt.figure(figsize=(8, 5))

    # Scatter points
    if data is not None and xname and yname and color_by and color_by in data.columns:
        for key, dsub in data.groupby(color_by):
            plt.scatter(dsub[xname], dsub[yname], label=f"{color_by}={key}", alpha=0.8)
    else:
        # single color scatter
        if data is not None and xname and yname:
            plt.scatter(data[xname], data[yname], alpha=0.8, label="Data")
        else:
            plt.scatter(Xv.ravel(), yv, alpha=0.8, label="Data")

    # Fitted line
    plt.plot(x_grid.ravel(), y_grid, 'r--', lw=2, label='fitted line')

    # Labels
    plt.xlabel(xlabel if xlabel else (xname or "X"))
    plt.ylabel(ylabel if ylabel else (yname or "y"))

    # Equation / R²
    if show_eq:
        eq = f"y = {slope:.3g} x + {intercept:.3g}"
        r2_text = f"R² = {r2:.3f}"
        ax = plt.gca()
        ax.text(0.02, 0.98, eq, transform=ax.transAxes, va="top")
        ax.text(0.02, 0.90, r2_text, transform=ax.transAxes, va="top")

    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig(fig_name, dpi=600)
    plt.close()
    open_file(fig_name)
