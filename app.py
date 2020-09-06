import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import re




app = dash.Dash(__name__,title='Customer Gambling Analytics',update_title='Processing...'   )


# Set up the app

server = app.server

global product_df
global dict_products

def create_dict_list_of_account_no():
    dictlist = []
    unique_list = product_df.Account_No.unique()
    for Account_No in unique_list:
        dictlist.append({'value': Account_No, 'label': Account_No})
    return dictlist

def dict_Account_No(dict_list):
    Account_No = []
    for dict in dict_list:
        Account_No.append(dict.get('value'))
    return Account_No
    
product_df = pd.read_excel("testfile_vindy.xlsx")
#product_df = dbm.read()
dict_products = create_dict_list_of_account_no()

output_card = dbc.Card(
    [
        dbc.CardHeader("Real-time Prediction"),
        dbc.CardBody(html.H2(id="predicted-grade", style={"text-align": "center"})),
    ]
)


app.layout = html.Div([
    html.Div([
        html.H1('TEAM: DATA IS NEW OIL'),
        html.Hr(),
        html.H2('Customer gambling addiction analysis'),
        html.H2('Choose a Account Number'),

        dcc.Dropdown(
            id='product-dropdown',
            options=dict_products,
            multi=True,
            value = ["Ben & Jerry's Wake and No Bake Cookie Dough Core Ice Cream","Brewdog Punk IPA"]
        ),
        dcc.Graph(
            id='product-like-bar'
        )
    ], style={'width': '30%', 'float': 'left','display': 'inline-block','padding': '25px'}),

    html.Div([
        html.H1('ACCOUNT INFORMATION'),
        html.Hr(),
        #html.H2('ACCOUNT INFORMATION'),
        html.Table(id='my-table'),
        html.P(''),
       
    ], style={'width': '65%', 'float': 'right', 'display': 'inline-block', 'padding': '25px'}
    ),
    html.Div([
        html.H2('Spending graph'),
        dcc.Graph(id='product-trend-graph'),
        html.P('')
    ], style={'width': '100%',  'display': 'inline-block'}),
    #html.Div(id='hidden-email-alert', style={'display':'none'})
])



@app.callback(Output('product-like-bar', 'figure'), [Input('product-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    product_df_filter = product_df[(product_df['Account_No'].isin(selected_dropdown_value))]

    # Take the one with max datetime and remove duplicates for this bar chart
    #product_df_filter = product_df_filter.sort_values('datetime', ascending=False)
    product_df_filter = product_df_filter.drop_duplicates(['index'])


    #Rating count check
    """def format_rating(rating):
        return re.sub('\((\d+)\)', r'\1', rating)

    product_df_filter['BAD_CATEGORY_TRANSACTION'] = product_df_filter['BAD_CATEGORY_TRANSACTION'].apply(format_rating)"""

    figure = {
        'data': [go.Bar(
            y=product_df_filter.WITHDRAWAL_AMT,
            x=product_df_filter.SHOP_TYPE,
            orientation='v'
            
        )],
        'layout':go.Layout(
            title= 'Spending Analysis',
            plot_bgcolor = '#FFFFFF', # Graph background
            paper_bgcolor = '#774AE5', #Last layout backgournd
             



            yaxis = dict(
                # autorange=True,
                automargin=True
            )
        )
    }
  
    return figure

# For the top topics graph
@app.callback(Output('product-trend-graph', 'figure'), [Input('product-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    product_df_filter = product_df[(product_df['Account_No'].isin(selected_dropdown_value))]

    data = timeline_top_product_filtered(product_df_filter,selected_dropdown_value)
    # Edit the layout
    layout = dict(title='Spending Trend',
                  xaxis=dict(title='datetime'),
                  yaxis=dict(title='Amount'),
                  )
    figure = dict(data=data,layout=layout)
    return figure

def timeline_top_product_filtered(top_product_filtered_df, selected_dropdown_value):
    # Make a timeline
    trace_list = []
    for value in selected_dropdown_value:
        top_product_value_df = top_product_filtered_df[top_product_filtered_df['Account_No']==value]
        trace = go.Scatter(
            y=top_product_value_df.BALANCE_AMT,
            x=top_product_value_df.datetime,
            name = value
        )
        trace_list.append(trace)
    return trace_list


# for the table
@app.callback(Output('my-table', 'children'), [Input('product-dropdown', 'value')])
def generate_table(selected_dropdown_value, max_rows=15):
    product_df_filter = product_df[(product_df['Account_No'].isin(selected_dropdown_value))]
    product_df_filter = product_df_filter.sort_values(['index','datetime'], ascending=True)

    return [html.Tr([html.Th(col) for col in product_df_filter.iloc[:, 1:8]])] + [html.Tr([

        html.Td(product_df_filter.iloc[i][col]) for col in product_df_filter.iloc[:, 1:8]

    ]) for i in range(min(len(product_df_filter  ), max_rows))]




if __name__ == '__main__':
    app.run_server(debug=True)



# For the product price graph individual
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    product_df_filter = product_df[(product_df['Account_No'].isin(selected_dropdown_value))]
    return {
         'data': [{
             'x': product_df_filter.datetime,
             'y': product_df_filter.BALANCE_AMT
         }]
     }