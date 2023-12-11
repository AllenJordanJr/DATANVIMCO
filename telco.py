from dash import Dash, dcc, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
#from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc

app = dash.Dash(__name__)

strDataset = "https://raw.githubusercontent.com/AllenJordanJr/DATANVIMCO/main/telecom_customer_churn.csv"

dfDataset = pd.read_csv(strDataset, encoding = "ISO-8859-1")
dfDataset.head() 

dfDataset1 = churned_data = dfDataset[dfDataset['Customer Status'] == 'Churned']
dfDataset1

dfDataset2 = dfDataset1[['Gender', 'Married', 'Offer', 'Phone Service', 'Multiple Lines', 'Internet Service', 'Internet Type', 'Contract', 'Paperless Billing', 'Payment Method']]
dfDataset2

dfDataset3 = dfDataset[['Gender', 'Married', 'Offer', 'Phone Service', 'Multiple Lines', 'Internet Service', 'Internet Type', 'Contract', 'Paperless Billing', 'Payment Method']]

dfDataset4 = dfDataset[dfDataset['Internet Service'] == 'Yes']
dfDataset4

cmpntTitle = html.H1(children = "Telecom Customer Churn", id = "Title")

cmpntGraphTitle1 = html.H3(children = "Churned Customer Metrics", className = "graph-title")
cmpntGraphTitle2 = html.H3(children = "Scatter Plot of Monthly Charge vs Total Charges of Churned Customers by Category", className = "graph-title")
cmpntGraphTitle3 = html.H3(children = "Total Number of Churned vs Retained Customers", className = "graph-title")
cmpntGraphTitle4 = html.H3(children = "Box Plot of the tenure of Churned and Retained Customers", className = "graph-title")
cmpntGraphTitle5 = html.H3(children = "Treemap of Churn Categories and Churn Reasons", className = "graph-title")

graphData2 = px.scatter(dfDataset1, x='Monthly Charge', y='Total Charges',
                         hover_data=['Customer ID', 'Payment Method'],
                         color='Total Charges',
                         color_continuous_scale=px.colors.sequential.Blues)

graphData2.update_layout(
    paper_bgcolor='rgba(17,17,17,1)',
    plot_bgcolor='rgba(17,17,17,1)',
    font=dict(color='white'),
    xaxis=dict(gridcolor='grey'),
    yaxis=dict(gridcolor='grey'),
    title=dict(x=0.5, xanchor='center', font=dict(size=20))
)
cmpntGraph2 = dcc.Graph(figure=graphData2, id='scatter-plot')


@callback(
    [Output('pie-chart', 'figure'), Output('bar-chart', 'figure')],
    [Input('shared-dropdown', 'value')]
)
def update_charts(selected_attribute):
    pie_fig = px.pie(dfDataset2, names=selected_attribute, color_discrete_sequence=px.colors.sequential.Blues)
    pie_fig.update_layout(
        paper_bgcolor='rgba(17,17,17,1)',
        plot_bgcolor='rgba(17,17,17,1)',
        font=dict(color='white'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    selected_category = selected_attribute
    churned_counts = dfDataset[dfDataset['Customer Status'] == 'Churned'][selected_category].value_counts().rename('Churned')
    retained_counts = dfDataset[dfDataset['Customer Status'] == 'Stayed'][selected_category].value_counts().rename(
        'Stayed')
    combined_counts = pd.concat([churned_counts, retained_counts], axis=1).reset_index()
    combined_counts.columns = ['Category', 'Churned', 'Stayed']
    melted_combined_counts = combined_counts.melt(id_vars='Category', var_name='Status', value_name='Count')

    bar_fig = px.bar(
        melted_combined_counts,
        y='Count',
        color='Status',
        barmode='group',
        color_discrete_map={'Churned': 'rgba(79, 129, 189, 0.8)', 'Stayed': 'rgba(204, 204, 204, 0.8)'}
    )

    bar_fig.update_traces(
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5,
        opacity=0.6
    )
    bar_fig.update_layout(
        paper_bgcolor='rgba(17,17,17,1)',
        plot_bgcolor='rgba(17,17,17,1)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='grey', tickangle=-45),
        xaxis_title=selected_category,
        yaxis=dict(gridcolor='grey'),
        yaxis_title='Count',
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )

    return pie_fig, bar_fig


@callback(
    Output('tenure-distribution-plot', 'figure'),
    [Input('churn-status-dropdown', 'value')]
)
def update_boxplot(churn_status):
    filtered_df = dfDataset[dfDataset['Customer Status'] == churn_status]

    fig = px.box(
        filtered_df,
        x='Tenure in Months',
        color='Customer Status',
        notched=True
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        transition_duration=500
    )

    return fig

graphData5 = px.treemap(
    dfDataset1,
    path=['Churn Category', 'Churn Reason'],
    color_discrete_sequence=px.colors.sequential.Blues
)

graphData5.update_layout(
    paper_bgcolor='rgba(17,17,17,1)',
    plot_bgcolor='rgba(17,17,17,1)',
    font=dict(color='white'),
)

cmpntGraph5 = dcc.Graph(figure=graphData5, id='churn-treemap')

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
server.route("/static/styles/styles.css") 

app.layout = dbc.Container(fluid=True, children=[
    html.Div(cmpntTitle),
    html.Hr(),
    dbc.Row([
        dbc.Col([
          html.Div(cmpntGraphTitle5),
          cmpntGraph5
        ], width = 12)

    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Div(cmpntGraphTitle1),
            dcc.Dropdown(
                id='shared-dropdown',
                options=[{'label': col, 'value': col} for col in dfDataset2.columns if dfDataset2[col].dtype == 'object'],
                value='Payment Method'
            ),
            dcc.Graph(id='pie-chart')
        ], width=12),

        dbc.Col([
            html.Div(cmpntGraphTitle3),
            dcc.Graph(id='bar-chart')
        ], width=12),
    ]),

    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Div(cmpntGraphTitle2),
            cmpntGraph2
        ], width=12)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
          html.Div(cmpntGraphTitle4),
          dcc.Dropdown(
            id='churn-status-dropdown',
            options=[
            {'label': 'Churned', 'value': 'Churned'},
            {'label': 'Stayed', 'value': 'Stayed'},
        ],
        value='Churned',
        clearable=False
    ),
      dcc.Graph(id='tenure-distribution-plot')
        ], width = 12)
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)