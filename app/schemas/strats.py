"""Schemas for strategies applied to frontend"""

import pandas as pd
from matplotlib.figure import Figure
from pydantic import BaseModel, ConfigDict


class BackTestComponents(BaseModel):
    """
    Represents a backtesting computation result with visualization components.
    Attributes:
        fig (plt.Figure): Matplotlib figure object for plotting
        back_test_df (pd.DataFrame): DataFrame containing backtesting results
    """

    fig: Figure
    result_df: pd.DataFrame
    model_config = ConfigDict(arbitrary_types_allowed=True)
