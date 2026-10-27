# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "raddo[cuda13]==0.1.4",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", auto_download=["html"])

with app.setup:
    import marimo as mo

    import os
    os.environ['XLA_PYTHON_CLIENT_PREALLOCATE'] = 'false'

    import pandas as pd

    from raddo.utils import TrajectoryGenerator
    from raddo.dynamics import OrbitDynamics, MagnetorquerDynamics

    sns.set_theme(context='paper', style='whitegrid', font='serif', font_scale=1.7)


@app.cell
def _():
    from fsspec.implementations.github import GithubFileSystem

    _username = os.environ.get("GITHUB_USERNAME")
    _token = os.environ.get("GITHUB_PAT")
    fs = GithubFileSystem(
        org="JHU-ACEL",
        repo="uranus-mpc-private",
        sha="main",
        username=_username,
        token=_token,
    )
    return (fs,)


@app.cell
def _():
    spacecraft_dynamics = MagnetorquerDynamics()
    system = TrajectoryGenerator(dynamics=spacecraft_dynamics, dt=0.1)
    return (system,)


@app.cell
def _(fs):
    with fs.open("data/uranus_200.pkl", "rb") as f:
        uranus_df_200 = pd.read_pickle(f)
    df_list = [uranus_df_200]
    return (df_list,)


@app.cell(hide_code=True)
def _(angle_tolerance, omega_tolerance, tail_samples):
    angle_threshold = mo.ui.slider(0.1, 90, value=15, step=0.1, show_value=True, label="Success: angle (deg)")
    omega_threshold = mo.ui.slider(0.1, 30, value=5, step=0.1, show_value=True, label="Success: rate (deg/s)")
    angle_tol = mo.ui.slider(0.1, 30, value=10, step=0.1, show_value=True, label="Stability: angle tolerance (deg)")
    omega_tol = mo.ui.slider(0.1, 20, value=5, step=0.1, show_value=True, label="Stability: rate tolerance (deg/s)")
    tail_length = mo.ui.slider(5, 500, value=100, step=5, show_value=True, label="Minimum stable samples")
    mo.vstack([mo.hstack([angle_threshold, omega_threshold]), mo.hstack([angle_tolerance, omega_tolerance]), tail_samples,
        mo.md("Success requires mean angle of stable samples and rate errors below their thresholds. Stability requires the final contiguous segment to stay within both tolerances of the tail means for at least the requested sample count. Summary statistics always use full trajectories, independent of the plot time window.")])
    return


@app.cell(hide_code=True)
def _(df_list, system):
    system.plot_violin_and_bar(df_list=df_list)#, angle_threshold=angle_threshold,omega_threshold=omega_threshold,angle_stability_tol=angle_tol, omega_stability_tol=omega_tol, tail_length=tail_length, angle_hist_max=angle_hist_max, omega_hist_max=omega_hist_max, verbose=True, dataset_labels=labels
    return


if __name__ == "__main__":
    app.run()
