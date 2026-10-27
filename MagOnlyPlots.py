# /// script
# requires-python = ">=3.13"
# dependencies = [
#    "numpy>=2.5.3",
#    "matplotlib>=3.11.2",
#    "pandas>=3.0.6",
#    "seaborn>=0.13.2",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt

    sns.set_theme(context='paper', style='whitegrid', font='serif', font_scale=1.7)
    return mo, pd, plt, sns


@app.cell
def _(pd):
    import subprocess
    from pathlib import Path
    
    # subprocess.run(
    #     ["git", "clone", "https://github.com/pschwartz26/test_marimo.git"],
    #     check=True,
    # )
    
    repo = Path("test_marimo")
    pkl = (repo / "uranus_200.pkl")
    df = pd.read_pickle(pkl)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    angle_threshold = mo.ui.slider(0.1, 90, value=15, step=0.1, show_value=True, label="Success: angle (deg)")
    omega_threshold = mo.ui.slider(0.1, 30, value=5, step=0.1, show_value=True, label="Success: rate (deg/s)")
    angle_tol = mo.ui.slider(0.1, 30, value=10, step=0.1, show_value=True, label="Stability: angle tolerance (deg)")
    omega_tol = mo.ui.slider(0.1, 20, value=5, step=0.1, show_value=True, label="Stability: rate tolerance (deg/s)")
    tail_length = mo.ui.slider(5, 500, value=100, step=5, show_value=True, label="Minimum stable samples")
    mo.vstack([mo.hstack([angle_threshold, omega_threshold]), mo.hstack([angle_tol, omega_tol]), tail_length,
        mo.md("Success requires mean angle of stable samples and rate errors below their thresholds. Stability requires the final contiguous segment to stay within both tolerances of the tail means for at least the requested sample count. Summary statistics always use full trajectories, independent of the plot time window.")])
    return


@app.cell(hide_code=True)
def _(df, plt, sns):
    _fig, _axes = plt.subplots(1, 3, figsize=(16, 6))

    _metrics = ["Quaternion Errors", "Angle Errors", "Omega Errors"]
    _group_order = ["True", "Fixed", "Adapt"]
    _palette = {"True": "#4f46e5", "Fixed": "#0891b2", "Adapt": "#b45309"}

    for _ax, _metric in zip(_axes, _metrics):
        sns.violinplot(
            data=df,
            x="Group",
            y=_metric,
            order=_group_order,
            palette=_palette,
            inner="quartile",
            ax=_ax,
        )
        _ax.set_title(_metric)
        _ax.set_xlabel("Group")

    _fig.suptitle("Trajectory Error Comparison by Group", fontsize=18, fontweight="bold")
    _fig.tight_layout()
    plt.gca()

    return


if __name__ == "__main__":
    app.run()
