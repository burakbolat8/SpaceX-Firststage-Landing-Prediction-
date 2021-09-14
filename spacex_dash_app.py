
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options= [
                                                 { "label" : "All sites", "value":  "All sites"},
                                                 { "label" : "CCAFS LC-40", "value": "CCAFS LC-40"} ,
                                                 { "label" : 'VAFB SLC-4E', "value": 'VAFB SLC-4E'},
                                                 { "label" : 'KSC LC-39A', "value": 'KSC LC-39A'},
                                                 { "label" : 'CCAFS SLC-40',"value":'CCAFS SLC-40'},

                                             ],
                                             value = "All sites",
                                             placeholder = "Select a launch site",
                                             searchable = True),

                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),



                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                marks={
                                                    0:"0 ",
                                                    2500:"2500",
                                                    5000:"5000",
                                                    7500:"7500",
                                                    10000:"10000"
                                                }
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_graph(selected_site):
    df = spacex_df.groupby(["Launch Site", "class"]).size().reset_index()
    if selected_site == "All sites":
        fig = px.pie(spacex_df, values='class', names='Launch Site', title="Total success launches by site")
        return fig
    else:
        df_selected = df[(df["Launch Site"] == selected_site)]
        fig = px.pie(df_selected,values=0,names="class",
                     title="Total success launches for site "+selected_site,
                     )
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def scatter(selected_site, slider_range):
    low = slider_range[0]
    high = slider_range[1]
    df = spacex_df[spacex_df['Payload Mass (kg)'].between(low,high)]

    if selected_site == 'All sites':
        scatter_fig = px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                                 title='Payload Success Rate for All Sites')
        return scatter_fig

    else:
        filtered_scatter = df[(df["Launch Site"] == selected_site)]
        scatter_fig = px.scatter(filtered_scatter, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                                 title='Payload Success Rate for ' + selected_site)
        return scatter_fig


# Run the app
if __name__ == '__main__':
    app.run_server()
