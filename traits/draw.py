import math
from traits.util import traits_stats
import plotly.graph_objects as go

def price_range_graph(df, traits, num_buckets=4, interested_traits = [], traits_colors_dict = None):
    # main function for generating a figure (go.Figure)
    price_tags = ['No Sales'] + [None] + ['&#36;' * i for i in range(1, num_buckets + 1)]
    # &#36; is dollar signs, plain '$' will crash everything (thinking latex)

    testing_stats = traits_stats(df, traits, num_buckets)
    data = []
    for trait in traits:
        if traits_colors_dict is None:
            trait_color = None
        else :
            trait_color = traits_colors_dict.get(trait, None)
        visible = 'legendonly'
        if trait in interested_traits:
            visible = True
        go_scatter = go.Scatter(
            name=trait,
            x=price_tags,
            y=[1 - testing_stats[trait]['sale_prop']]+ [None] + testing_stats[trait]['freqs'],
            visible = visible,
            marker_size=math.sqrt(math.exp(-50 * testing_stats[trait]['rarity']) * 1000) + 10,
            marker_line_width=testing_stats[trait]['rarity'] * 30 + 2,
            marker_symbol=['diamond-open']*len(price_tags),
            marker_color=trait_color, 
            opacity=0.8,
            marker_line_color = trait_color, 
            line_shape='spline',
            customdata=[[trait, testing_stats[trait]['rarity']]] * len(price_tags),
            hovertemplate="<br>".join([
                "Price: %{x}",
                "Proportion: %{y}",
                "Trait: %{customdata[0]}",
                "Rarity: %{customdata[1]}",
                "<extra></extra>"
            ]))
        data.append(go_scatter)
    fig = go.Figure(data=data)

    fig.update_layout(
        barmode='group',
        yaxis_tickformat='0.00%',
        margin=dict(b=20,l=5,r=5,t=40),
    )

    # fig.update_yaxes(rangemode='tozero')
    return fig
