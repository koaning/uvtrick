# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "altair",
#   "polars",
#   "vl-convert-python"
# ]
# ///

import polars as pl
import altair as alt


df = pl.read_csv("results.csv")
p = alt.Chart(df).mark_point().encode(x='version:N', y='time').save("plot.png")