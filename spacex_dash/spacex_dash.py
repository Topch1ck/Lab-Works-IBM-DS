# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as poi

poi.renderers.default = "browser"
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"dashbords\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

options= [{'label':'All', 'value':'All'},
            {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
            {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
            {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
            {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}]

# Create an app layout
app.layout = html.Div([
                        html.H1('SpaceX Launch Records Dashboard',
                                style={'textAlign': 'center', 
                                    'color': '#503D36',
                                    'font-size': 40}
                                ),
                        
                        dcc.Dropdown(
                                        id='site-dropdown',
                                        options=options,
                                        value='All',
                                        multi=False,
                                        searchable=True,
                                        placeholder="Select a Launch Site..."
                                    ),
                        html.Br(),

                        dcc.Graph(id='success-pie-chart'),
                        html.Br(),

                        html.P("Payload range (Kg):"),
                        
                        dcc.RangeSlider(
                                        id='payload-slider',
                                        min = min_payload,
                                        max = max_payload,
                                        value=[0, 9600],
                                        marks={0:'0', 
                                            2500:'2500',
                                            5000:"5000", 
                                            7500:"7500", 
                                            9600:'9600'},
                                        step = 1),
                        
                        dcc.Graph(id='success-payload-scatter-chart')
                        ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
                Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value')
            )
def get_pie_chart(entered_site):
    if entered_site == 'All':
        fig = px.pie(
                    spacex_df, 
                    values = 'class', 
                    names = 'Launch Site', 
                    title = 'All Launch Sites'
                    )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='count')

        fig = px.pie(
                    filtered_df, 
                    values ='count', 
                    names = 'class', 
                    title = entered_site
                    )
        return fig

        # return the outcomes piechart for a selected site



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
                Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                (Input(component_id='payload-slider', component_property='value'))
                ]
            )
def get_scatter_plot(entered_site,payload):
    df_filter = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & 
                        (spacex_df['Payload Mass (kg)'] <= payload[1] )]
    if entered_site == "All":
        fig = px.scatter(df_filter, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        df_filter = df_filter[df_filter['Launch Site'] == entered_site]
        fig = px.scatter(df_filter, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()