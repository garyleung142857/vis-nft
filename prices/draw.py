from turtle import fillcolor
import plotly.graph_objects as go
import plotly.express as px
import copy
import numpy as np

def make_price_strip_fig(df_dc):
    point_data = df_dc.sort_values('num_sales', ascending = False)
    point_data.reset_index()

    # print(df_dc.columns)
    # point_data = df_dc

    point_color = list(['blue'] * len(point_data))
    price_strip_fig = px.strip(point_data, y='last_sale_total_price', x='num_sales', color=point_color, stripmode='overlay', custom_data=['name'])
    price_strip_fig.update_layout(
        showlegend=False,
        margin=dict(b=20,l=5,r=5,t=40)
    )
    price_strip_fig.update_traces(hovertemplate="<extra></extra>")

    return price_strip_fig, point_color

def linkTreeChartToStripChart(hoverData, point_color, price_strip_fig, token_df_filtered):
    # updateColor = copy.deepcopy(point_color)

    if hoverData is not None and 'label' in hoverData['points'][0]:
        hover_label = hoverData['points'][0]['label']
        point_data = token_df_filtered.sort_values('num_sales', ascending = False)
        point_data.reset_index()
        tokens_contain_owner = (point_data['owner_address'] == hover_label).tolist()
        updateColor = ['red' if owner else 'blue' for owner in tokens_contain_owner]
        updateStrip = px.strip(
            point_data,
            y='last_sale_total_price',
            x='num_sales',
            color=updateColor,
            stripmode='overlay',
            color_discrete_map={'red': 'red', 'blue': '#636EFA'},
            custom_data=['name']
        )
        updateStrip.update_layout(
            showlegend=False,
            margin=dict(b=20,l=5,r=5,t=40)
        )
        updateStrip.update_traces(hovertemplate="<extra></extra>")
    else:
        updateStrip = copy.deepcopy(price_strip_fig)
        updateStrip = go.Figure(updateStrip)
    return updateStrip

def linkAttrChartToStripChart(hoverData, point_color, price_strip_fig, strip_data):
    # print(updateColor, len(updateColor), type(updateColor))
    if hoverData is not None and 'customdata' in hoverData['points'][0]:
        # updateColor = copy.deepcopy(point_color)
        hover_label = hoverData['points'][0]['customdata'][0]
        # print(hover_label)
        tokens_contain_trait = strip_data['traits_list_aslist'].apply(lambda tr : hover_label in tr).tolist()
        # print(tokens_contain_trait )
        updateColor = np.array(['red' if contain_trait else 'blue' for i,contain_trait in enumerate(tokens_contain_trait)])
        # print(updateColor)
        updateStrip = px.strip(
            strip_data,
            y='last_sale_total_price',
            x='num_sales',
            color=updateColor,
            color_discrete_map={'red': 'red', 'blue': '#636EFA'},
            stripmode='overlay',
            custom_data=['name']
        )
        updateStrip.update_layout(
            showlegend=False,
            margin=dict(b=20,l=5,r=5,t=40)
        )
        updateStrip.update_traces(hovertemplate="<extra></extra>")
    else:
        updateStrip = copy.deepcopy(price_strip_fig)
        updateStrip = go.Figure(updateStrip)
    return updateStrip
