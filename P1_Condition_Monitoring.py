import streamlit as st
import os, sys, pandas as pd, numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly_resampler import FigureResampler
import streamlit.components.v1 as components
from multiprocessing import Process
import warnings
warnings.filterwarnings('ignore')
# load custom functions
sys.path.append(os.path.abspath('..'))
from src.helpers import *
from src.all_plots import *
from src.plot_descriptions import *


# Page config
st.set_page_config(page_title="HPP Digital Twins", page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: Condition Monitoring App")

st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

st.sidebar.image('media/srp_logo.jpg')
st.logo('media/asu_logo.png')

# Load Data
df = None
# File uploader for a single .pkl file
# uploaded_file = st.file_uploader("Upload a .pkl file. Else download data by clicking [here](https://drive.google.com/file/d/14kFHUjzUk4uSXidZ6xM_g78gqiE_bvqk/view?usp=drive_link) 📥", type='pkl', accept_multiple_files=False)

st.markdown(
    '''
    ------------------------------------------------------------------------------------
    ### Upload Data
    '''
)


uploaded_file = st.file_uploader("Upload a .pkl file 📥. In case you don't have data, request it by emailing to me (mgupta70@asu.edu) or Russell Genet (Russell.Genet@srpnet.com) of SRP.", type='pkl', accept_multiple_files=False)

anomaly_file = st.file_uploader("Upload .pkl file 📥 for the results file of anomaly detection.", type='pkl', accept_multiple_files=False)

if uploaded_file is not None:
    # Read the uploaded file into a DataFrame
    try:
        # Load the DataFrame from the uploaded file
        df = pd.read_pickle(uploaded_file)

    except Exception as e:
        st.error(f"Error loading the file: {e}")

if df is not None:
    # Get list of names of all sensors
    sensors_list = [o for o in list(df.columns) if 'HYDRO' in o]

    # sidebar selections
    sensor = st.sidebar.multiselect("Select Sensor(s)", sensors_list)
    month_name = st.sidebar.selectbox("Month", list(month_num2name.values()), index=0, key=21)  # default - January 
    year_num = st.sidebar.selectbox("Select Year", [int(yr) for yr in list(df.year.unique())], index=3, key=31)
    n_months = st.sidebar.selectbox("Past n Months", list(range(1, 12)), index=1, key=32)

    if sensor:
        in_family, out_family = get_same_family_sensors(sensors_list, sensor=sensor[0])


    #####################
    # Advanced Analytics
    #####################

    modify = st.checkbox("Add filters")
    if not modify:
        filtered_df = df.copy()
    else:
        col1, col2 = st.columns((2))  
        startDate = df.index.min() 
        endDate = df.index.max()  
        with col1:
            date1 = pd.to_datetime(st.date_input("Start Date", startDate))
        with col2:
            date2 = pd.to_datetime(st.date_input("End Date", endDate))
        if date1 and date2:
            df = df[(df.index >= date1) & (df.index<= date2)].copy()
        filtered_df = filter_dataframe(df)


        
    ##########
    # Plot-1
    ##########
    col11, col12 = st.columns([1 , 0.01])
    with col11: 
        st.subheader('1. Data Streaming')
        with st.expander('Select a sensor to analyse. For more information - Click here'):
            st.markdown(f"{data_streaming_plot_description}")
        if sensor:
            df1 = df[sensor].copy()
            ## Top plot and Bottom plot
            fig1 = plot_sensor_data(df1, sensor, is_app=True)
            st.plotly_chart(fig1,use_container_width=True)
        

    ###########
    # Plot-2
    ###########
    col21, col22 = st.columns([1 , 1])
    with col21:
        st.subheader('2. Year-on-Year Trend')
        with st.expander('This plot helps us see the current state of the selected sensor w.r.t. past years. For more information - Click here'):
            st.markdown(f"{yoy_plot_description}")
        if sensor and month_name:        
            ## Plotly
            fig2, avg_data = plotly_YOY_trend(df, sensor, month_name) # avg_data is df with daily average data of every year for given month
            st.plotly_chart(fig2,use_container_width=True)
            
            monthly_averages = {}
            for yr in avg_data.year.unique():
                monthly_averages[yr] = avg_data[avg_data['year'] == yr][sensor[0]].mean()
                #monthly_averages[yr] = avg_data.loc[yr][sensor[0]].mean()
                
            m1_value = get_m1(monthly_averages, year_num)
            m2_value = get_m2(monthly_averages, year_num)
            m3_value = get_m3(avg_data, year_num, sensor)
                
            col_left, col_right = st.columns(2)
        
            with col_left:
                st.metric(label='Monthly average', value=f'{m1_value} {sensors_units[sensor[0]]}', delta=f'{m2_value} % w.r.t. past yrs')

            with col_right:
                st.metric(label='Number of days with Peak daily Average', value=f'{m3_value} Days', delta=None)
    
        
    ##########
    # Plot-3
    ##########
    with col22:
        st.subheader('3. Month-on-Month Trend')
        with st.expander('This plot helps us see the current state of the selected sensor w.r.t. past months. For more information - Click here'):
            st.markdown(f"{mom_plot_description}")
        if sensor and year_num:        
            ## Plotly
            fig3, df3 = plotly_MOM_trend(df, sensor, month_name, year_num, n_months)
            st.plotly_chart(fig3,use_container_width=True)
            
            avg_data2 = df3.groupby(['month', 'day'])[['day', 'month', 'year', sensor[0]]].mean()
            m4_value, m5_value = get_m4_m5(df3, month_name, sensor) 
            m6_value = get_m6(avg_data2, month_name, sensor)
            
            col_left, col_right = st.columns(2)
        
            with col_left:
                st.metric(label='Monthly average', value=f'{m4_value} {sensors_units[sensor[0]]}', delta=f'{m5_value} %')

            with col_right:
                st.metric(label='Daily average exceeds', value=f'{m6_value} Days', delta=None)


        
    ###########
    # Plot-4
    ##########
    col4, col5 = st.columns([1, 1])
    with col4:
        st.subheader('4. Psuedo-Sensor Analysis')
        with st.expander('Plot shows the true value on x-axis and corresponding predicted value on y-axis. For more information - Click here'):
            st.markdown(f"{psuedo_sensor_plot_description}")
        if sensor:
            if anomaly_file is not None:
                df_reconstructed = pd.read_pickle(anomaly_file)
                
                original_values = df[sensor[0]]
                reconstructed_values = df_reconstructed[sensor[0]]
                
                # Create a scatter plot
                fig4 = px.scatter(
                    df,
                    x=original_values,
                    y=reconstructed_values,
                    labels={"x": "Original Values", "y": "Reconstructed Values"},
                    title=f"Original vs Predicted Values for {sensor[0]}",
                    opacity=0.1,
                )
                
                # Add custom data (year, month, day, hour) for the hover tooltip
                fig4.update_traces(
                    customdata=df[['year', 'month', 'day', 'hour']],
                
                    hovertemplate=(
                        "Year: %{customdata[0]}<br>" +
                        "Month: %{customdata[1]}<br>" +
                        "Day: %{customdata[2]}<br>" +
                        "Hour: %{customdata[3]}<br>" +
                        "<extra></extra>"  # Remove default x and y values
                    )
                )
                
                # Update layout for better visualization
                fig4.update_layout(
                    xaxis_title="Original Values",
                    yaxis_title="Predicted Values",
                    title_x=0.5  # Center the title
                )
                
                # Add a line y = x for ideal behavior
                fig4.add_trace(
                    go.Scatter(
                        x=original_values,
                        y=original_values,
                        mode='lines',
                        name='Ideal Behavior (y=x)',
                        line=dict(color='red', dash='dash', width=2),
                        opacity=1.0
                        
                    )
                )
                st.plotly_chart(fig4,use_container_width=True)
                                

            else:               
                st.image("media/lock.png")


    ##########
    # Plot-5
    ##########
    with col5:
        st.subheader('5. Correlation Analysis')
        with st.expander('Plotting monthly correlation of selected sensor with same-family sensors. For more information - Click here'):
            st.write(f"{correlation_plot_description}")

        if sensor:
            
            df5 = df.copy()
            time_scale = 'monthly' 
            correlations_dict = {}   
            for s in in_family:
                if s not in correlations_dict:
                    correlations_dict[s] = []

            if time_scale == 'monthly':
                for yr in df5.index.year.unique():
                    data = df5[df5.index.year==yr]
                    for m in list(range(1,13)):
                        sub_df = data[data.index.month==m]
                        for s in in_family:
                            if len(sub_df)>0:
                                corr = sub_df[s].corr(sub_df[sensor[0]])
                                correlations_dict[s].append(corr)
                            else:
                                correlations_dict[s].append(None)

            xticks = []
            for yr in df.index.year.unique():
                for m in list(range(1,13)):
                    xticks.append(f"{yr}-{month_num2name[m]}")

            rotation = 90
            fig = go.Figure()
            for s, v in correlations_dict.items():
                v = v[9:-3]
                x_vals = xticks[9:-3]
                y_vals = v

                # Add scatter plot for each sensor
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines+markers', name=s))

                # Highlight None values with red "x"
                for i, value in enumerate(y_vals):
                    if value is None:
                        fig.add_trace(go.Scatter(
                            x=[x_vals[i]],
                            y=[0.0],
                            mode='markers',
                            marker=dict(color='red', symbol='x'),
                            showlegend=False
                        ))

            # Update layout
            fig.update_layout(
                title='Correlation Analysis',
                xaxis_title='Yr-Month',
                yaxis_title='Correlation',
                xaxis=dict(tickmode='array', tickvals=xticks[9:-3], tickangle=rotation),
                yaxis=dict(showgrid=True),
                legend=dict(x=0.4, y=0.2, bgcolor = 'rgba(255,255,255,0.5)'),
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

    ##########
    # Plot-6
    ##########
    st.subheader('6. Heatmap of Sensor Data')
    with st.expander("This plot gives a snapshot of sensor's behavior in its lifetime. For more information - Click here"):
        st.markdown(''' 
            ''')
    if sensor:
        df_gg = get_pivot_table(filtered_df, sensor)
        fig6 = plot_daily_heatmap(df_gg, sensor)
        st.plotly_chart(fig6,use_container_width=True)

st.markdown(
    '''
    ------------------------------------------------------------------------------------
    🛠️ Created by [Mohit Gupta](https://mgupta70.github.io), Ph.D., Arizona State University || Email :email:: mgupta70@asu.edu
    '''
)

