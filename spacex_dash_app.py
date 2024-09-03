# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

df = spacex_df[['Launch Site']]
df1 = {'Launch Site' : 'ALL Sites'}
df = df._append(df1, ignore_index=True)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
            		                        options=[
                                            {'label': site, 'value': site} for site in df['Launch Site'].unique()],
            		                        value='ALL Sites',
            		                        placeholder='Select a Launch Site here',
            		                        style={'width': '80%', 'padding': '3px', 
            		                        'fontSize': '20px', 'textAlignLast': 'center'},
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filt_df = spacex_df
    if entered_site == 'ALL Sites':
        filt_df=filt_df.groupby('Launch Site')['class'].sum().reset_index()
        pie_All = px.pie(filt_df, values='class', 
        names='Launch Site', 
        title='All Sites Success Counts')
        return pie_All
    else:
        # return the outcomes piechart for a selected site
        filt_df = filt_df[filt_df['Launch Site'] == entered_site]
        filt_df = filt_df['class'].value_counts().reset_index()
        pie_Site = px.pie(filt_df, values='count', 
        names='class', 
        title= 'Success Rate ' + entered_site)
        return pie_Site
    # optionally you can return figure after both 
    # if n else statement once using the same variable
    # for both charts, rather than return separate
    # figures for if and else

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_pie_chart(entered_site, payload_mass):
    print(entered_site)
    print(payload_mass)
    filt_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0],payload_mass[1])]
    # thought reusing filtered_df may cause issues, but tried it out of curiosity and it seems to be working fine
    if entered_site == 'ALL Sites':
        scatter_All = px.scatter(filt_df, x= 'Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category', 
        title='Success-Payoad Scatter Chart for All Sites')
        return scatter_All
    else:
        # return the scatterchart for a selected site
        filt_df = filt_df[filt_df['Launch Site'] == entered_site]
        scatter_Site = px.scatter(filt_df, x= 'Payload Mass (kg)', 
                                y='class', 
                                color='Booster Version Category', 
                                title='Success-Payoad Scatter Chart for Site ' + entered_site)
        return scatter_Site

# Run the app
if __name__ == '__main__':
    app.run_server()
