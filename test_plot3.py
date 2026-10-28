# /// script
# dependencies = [
#     "numpy",
#     "matplotlib",
#     "pandas",
#     "seaborn",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    import urllib.request
    import types

    def _load_module(url: str, name: str = "remote_funcs") -> types.ModuleType:
        source = urllib.request.urlopen(url).read().decode("utf-8")
        mod = types.ModuleType(name)
        exec(compile(source, url, "exec"), mod.__dict__)
        return mod

    plot_fn_url = "https://raw.githubusercontent.com/pschwartz26/test_marimo/refs/heads/main/plotting_numpy.py"

    plot_utils = _load_module(plot_fn_url)

    sns.set_theme(context='paper', style='whitegrid', font='serif', font_scale=1.7)
    return mo, pd, plot_utils


@app.cell
def _(pd):
    _BASE = "https://raw.githubusercontent.com/JHU-ACEL/uranus-mpc-data/main/data"

    _datasets = {
        "earth_50":       f"{_BASE}/earth_50.pkl",
        "earth_100":      f"{_BASE}/earth_100.pkl",
        "earth_150":      f"{_BASE}/earth_150.pkl",
        "earth_200":      f"{_BASE}/earth_200.pkl",
        "earth_250":      f"{_BASE}/earth_250.pkl",
        "uranus_50":      f"{_BASE}/uranus_50.pkl",
        "uranus_100":     f"{_BASE}/uranus_100.pkl",
        "uranus_150":     f"{_BASE}/uranus_150.pkl",
        "uranus_200":     f"{_BASE}/uranus_200.pkl",
        "uranus_250":     f"{_BASE}/uranus_250.pkl",
        "torque_df": f"{_BASE}/torque_v_dipole.pkl",
    }

    datasets = {name: pd.read_pickle(url) for name, url in _datasets.items()}
    return (datasets,)


@app.cell(hide_code=True)
def _(mo):
    _DEFAULTS = dict(angle_threshold=15.0, omega_threshold=5.0,
                      angle_tol=10.0, omega_tol=5.0, tail_length=100)

    angle_threshold = mo.ui.slider(0.1, 90,  value=_DEFAULTS["angle_threshold"],  step=0.1, show_value=True, label="Success: angle (deg)")
    omega_threshold = mo.ui.slider(0.1, 30,  value=_DEFAULTS["omega_threshold"],  step=0.1, show_value=True, label="Success: rate (deg/s)")
    angle_tol       = mo.ui.slider(0.1, 30,  value=_DEFAULTS["angle_tol"],        step=0.1, show_value=True, label="Stability: angle tolerance (deg)")
    omega_tol       = mo.ui.slider(0.1, 20,  value=_DEFAULTS["omega_tol"],        step=0.1, show_value=True, label="Stability: rate tolerance (deg/s)")
    tail_length     = mo.ui.slider(5,   500, value=_DEFAULTS["tail_length"],       step=5,   show_value=True, label="Minimum stable samples")
    reset_btn       = mo.ui.run_button(label="↺ Reset to defaults")

    mo.vstack([
        mo.hstack([angle_threshold, omega_threshold]),
        mo.hstack([angle_tol, omega_tol]),
        tail_length,
        reset_btn,
        mo.md(
            "**Success** requires mean angle of stable samples and rate errors below their thresholds. "
            "**Stability** requires the final contiguous segment to stay within both tolerances of the "
            "tail means for at least the requested sample count. Summary statistics always use full "
            "trajectories, independent of the plot time window."
        ),
    ])
    return (
        angle_threshold,
        angle_tol,
        omega_threshold,
        omega_tol,
        reset_btn,
        tail_length,
    )


@app.cell(hide_code=True)
def _(mo, reset_btn):
    # Reset button handler — rebuilds sliders at default values when clicked
    mo.stop(not reset_btn.value, mo.md("_Click **↺ Reset to defaults** above to reset all sliders._"))

    # Display the default values clearly
    mo.md(f"""
    ✅ **Sliders reset.** Reload this cell or re-run to pick up defaults:

    | Slider | Default |
    |---|---|
    | Success angle | {_DEFAULTS['angle_threshold']} deg |
    | Success rate | {_DEFAULTS['omega_threshold']} deg/s |
    | Stability angle tol | {_DEFAULTS['angle_tol']} deg |
    | Stability rate tol | {_DEFAULTS['omega_tol']} deg/s |
    | Min stable samples | {_DEFAULTS['tail_length']} |
    """)
    return


@app.cell
def _(angle_threshold, datasets, mo, omega_threshold, plot_utils):
    _df = datasets["torque_df"]
    _batch_size = int(_df["Time"].value_counts()[0] / _df["Group"].nunique())
    _N = _df["Time"].nunique()
    _time_max=80
    _, fig_list  = plot_utils.plot_costs(df=_df, batch_size=_batch_size, batch_idx=None, N=_N, title=None, legend=None, angle_threshold=angle_threshold.value, omega_threshold=omega_threshold.value, time_max=_time_max, plot_stats=True,compare_groups=False,filename=None)
    mo.hstack(
        [mo.vstack([mo.md("Direct Torque Inputs"), *fig_list[:2]], align="center"), 
         mo.vstack(fig_list[2:])]
    )
    return



if __name__ == "__main__":
    app.run()
