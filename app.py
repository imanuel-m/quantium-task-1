import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import glob

# Load and combine all CSV files
files = glob.glob("data/daily_sales_data_*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Clean price column and calculate sales
df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["sales"] = df["price"] * df["quantity"]
df["date"] = pd.to_datetime(df["date"])

regions = ["all"] + sorted(df["region"].unique().tolist())

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={"textAlign": "center"}),
    html.Div([
        html.Label("Region"),
        dcc.RadioItems(
            id="region-filter",
            options=[{"label": r.capitalize(), "value": r} for r in regions],
            value="all",
            inline=True,
        ),
    ], style={"margin": "20px"}),
    dcc.Graph(id="sales-chart"),
], style={"fontFamily": "Arial, sans-serif", "maxWidth": "1100px", "margin": "0 auto"})


@app.callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    # Only pink morsel per task spec
    pink = filtered[filtered["product"] == "pink morsel"]
    daily = pink.groupby("date", as_index=False)["sales"].sum()
    fig = px.line(daily, x="date", y="sales", title=f"Pink Morsel Sales — {region.capitalize()}")
    fig.update_layout(xaxis_title="Date", yaxis_title="Sales ($)")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
