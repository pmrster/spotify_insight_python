import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime




def get_total_track_by_day_chart(data):
    ##data
    
    ##format date
    # for i in data:
    #     added_date = datetime.strptime(i["added_at"],"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        
    df = pd.DataFrame(data)
    df["added_date"] = pd.to_datetime(df['added_at']).dt.strftime('%Y-%m-%d')
    
    count_by_day_df = df.groupby("added_date",as_index=False).track_id.agg("count")
    
    ## full date range
    date_range = pd.date_range(start=df["added_date"].min(), end=df["added_date"].max(), freq="D")
    full_df = pd.DataFrame(date_range, columns=["added_date"])
    full_df["added_date"] = pd.to_datetime(full_df["added_date"], errors='coerce')
    count_by_day_df["added_date"] = pd.to_datetime(count_by_day_df["added_date"], errors='coerce')
    merged_df = full_df.merge(count_by_day_df, on="added_date", how="left").fillna(0)
    
    ##chart
    fig = px.line(merged_df, x="added_date", y="track_id", title="Added tracks by day",markers=True)
    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Date", 
        yaxis_title="Count of song added"  
    )
    fig.update_traces(line=dict(color="#1DB954", width=2),
                    #   line_shape='spline'
                    )


    fig.update_xaxes(
        showline=True,
        linecolor='lightgrey'
    )
    fig.update_yaxes(
        showline=True,
        linecolor='lightgrey'
    )
    # fig.show()

    # แปลงกราฟเป็น HTML ที่สามารถแสดงในเว็บ
    graph_html = pio.to_html(fig, full_html=False)
    
    return graph_html