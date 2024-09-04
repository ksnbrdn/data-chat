#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output


# In[ ]:


# Загрузка данных
df = pd.read_csv('https://raw.githubusercontent.com/ksnbrdn/data-chat/main/2018.csv')


# In[ ]:


# Сортировка и выбор топ-10 стран по Score
top_10 = df.sort_values('Score', ascending=False).head(10)


# In[ ]:


app = Dash(__name__)


# In[ ]:


app.layout = html.Div([
    html.H1('Dashboard анализа данных о счастье стран'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in df['Country or region'].unique()],
        multi=True,
        placeholder="Выберите страны (по умолчанию показаны топ-10)"
    ),
    dcc.Graph(id='choropleth-map'),
    dcc.Graph(id='bar-chart'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=top_10.to_dict('records'),
        style_table={'height': '300px', 'overflowY': 'auto'}
    )
])


# In[ ]:


@app.callback(
    [Output('table', 'data'),
     Output('bar-chart', 'figure'),
     Output('choropleth-map', 'figure')],
    [Input('country-dropdown', 'value')]
)


# In[ ]:


def update_dashboard(selected_countries):
    if selected_countries:
        filtered_df = df[df['Country or region'].isin(selected_countries)]
    else:
        filtered_df = top_10

    bar_fig = px.bar(filtered_df, y='Country or region', x='Score',
                     orientation='h', title='Рейтинг стран по показателю Score')

    choropleth_fig = px.choropleth(df, locations="Country or region",
                                   locationmode="country names",
                                   color="Score",
                                   hover_name="Country or region",
                                   title="Карта счастья стран",
                                   color_continuous_scale=px.colors.sequential.Viridis)

    if selected_countries:
        choropleth_fig.update_geos(visible=False, showland=True, showcountries=True,
                                   fitbounds="locations")

    return filtered_df.to_dict('records'), bar_fig, choropleth_fig

if __name__ == '__main__':
    app.run_server(debug=True)
        

