import pandas as pd
import os as os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px

#read data

data = "X_train_labeled_kmeans_mini_done.csv"

X_train_labeled_kmeans_mini_done = pd.read_csv(data,index_col=0)

name = ['VEHOWNMO_label',
 'HHFAMINC_label',
 'HBRESDN_label',
 'HBPPOPDN_label',
 'EDUC_label',
 'PRICE_label',
 'CAR_label',
 'PLACE_label']

app = dash.Dash(__name__)
server = app.server
app.title = "Results from Clustering"


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="", className="header-emoji"),
                html.H1(
                    children="Results from Clustering", className="header-title"
                ),
                html.P(
                    children="The plots here show the results based on clustering for the National Household Travel Survey data",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
        
            children=[
                html.Div(
                    children=[
                        html.Div(children="cluster", className="menu-title"),
                        dcc.Dropdown(
                            id="cluster-filter",
                            options=[
                                {"label": cluster, "value": cluster}
                                for cluster in X_train_labeled_kmeans_mini_done.type.unique()
                            ],
                            value="Kmeans",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),    
                html.Div(
                    children=[
                        html.Div(children="Variable", className="menu-title"),
                        dcc.Dropdown(
                            id="variable-filter",
                            options=[{"label": van, "value": van}
                            for van in name
                            ],
                            value="EDUC",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="y_train", className="menu-title"),
                        dcc.Dropdown(
                            id="ytrain-filter",
                            options=[
                                {"label": avocado_type, "value": avocado_type}
                                for avocado_type in X_train_labeled_kmeans_mini_done.predict.unique()
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                

            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),

            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    [
        Input("cluster-filter", "value"),
        Input("variable-filter", "value"),
        Input("ytrain-filter", "value"),
    ],
)
def update_charts(cluster, van, avocado_type):
    
    print(van)
    
    print(avocado_type)
    
    dat1 = X_train_labeled_kmeans_mini_done[X_train_labeled_kmeans_mini_done['type']==cluster]
    
    dat2 = dat1.groupby([van, "y_train"])["predict"].value_counts().reset_index(name='count')
    mask = ((dat2.y_train == avocado_type)
    )
    filtered_data = dat2.loc[mask, [van,"predict","count"]]
    
    fig = px.bar(filtered_data, x=van, y="count", 
                 color="predict", barmode="group")
    return fig



if __name__ == "__main__":
    app.run_server(debug=True,use_reloader=False)