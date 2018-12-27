# -*- coding: utf-8 -*-

"""Top-level package for chartify-pandas."""

__author__ = """Lars Yencken"""
__email__ = 'lars@yencken.org'
__version__ = '0.1.0'

import pandas as pd
import chartify


class NotebookChart(chartify.Chart):
    def _ipython_display_(self) -> None:
        self.show()


def _detect_axis_type(s: pd.Series) -> str:
    name = s.dtype.name

    if name in ('int64', 'float64'):
        return 'linear'

    if name in ('object',):
        return 'categorical'

    raise Exception(f'unknown axis type: {name}')


def df_plot(df: pd.DataFrame, x_column: str, y_column: str, c: str = None,
            kind: str = None) -> NotebookChart:
    "Generate a Chartify plot using 2 or 3 dimensions of the available data."
    x_axis_type = _detect_axis_type(df[x_column])
    ch = NotebookChart(x_axis_type=x_axis_type, blank_labels=True)

    if not kind:
        if x_axis_type == 'categorical':
            kind = 'bar'
        else:
            kind = 'line'

    getattr(ch.plot, kind)(
        df,
        x_column=x_column,
        y_column=y_column,
        color_column=c,
    )
    ch.axes.set_xaxis_label(x_column)
    ch.axes.set_yaxis_label(y_column)
    return ch


def s_plot(s: pd.Series) -> NotebookChart:
    "Generate a Chartify plot of this series, auto-detecting the plot type."
    x_axis_type = _detect_axis_type(s.index)
    ch = NotebookChart(x_axis_type=x_axis_type, blank_labels=True)

    df = s.to_frame().reset_index()
    df.columns = ['index', 'value']

    if x_axis_type == 'categorical':
        ch.plot.bar(
            df,
            categorical_columns='index',
            numeric_column='value',
        )
    else:
        ch.plot.line(
            df,
            x_column='index',
            y_column='value',
        )

    if s.name:
        ch.axes.set_yaxis_label(s.name)

    if s.index.name:
        ch.axes.set_xaxis_label(s.index.name)

    return ch


def s_kde(s: pd.Series) -> NotebookChart:
    "Generate a density plot for this series."
    ch = NotebookChart(y_axis_type='density', blank_labels=True)
    ch.plot.kde(s.to_frame(),
                values_column=s.name)
    return ch


def s_hist(s: pd.Series) -> NotebookChart:
    "Generate a histogram for this series."
    ch = NotebookChart(y_axis_type='density', blank_labels=True)
    ch.plot.histogram(s.to_frame(),
                      values_column=s.name)
    return ch


pd.DataFrame.ch_plot = df_plot
pd.Series.ch_plot = s_plot
pd.Series.ch_hist = s_hist
pd.Series.ch_kde = s_kde
