import streamlit as st
import pandas as pd
import mysql.connector as sql
import plotly.express as px
st.title(":violet[PhonePe Pulse]")
st.markdown(":violet[Welcome to the PhonePe Pulse Dashboard ,This PhonePe Pulse Data Visualization and Exploration dashboard is a user-friendly tool designed to provide insights and information about the data in the PhonePe Pulse GitHub repository. This dashboard offers a visually appealing and interactive interface for users to explore various metrics and statistics.]")
mydb = sql.connect(host="localhost",
                   user="root",
                   password= "Nila123@#",
                   database= "phonepe"
                  )
mycursor = mydb.cursor(buffered=True)

# Creating the side bars
with st.sidebar:
      selected = st.selectbox("Select a page", ["Top Performers", "Explore Data"])
if selected == "Top Performers":
    st.markdown("## :violet[Top 10 performers]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    if Type == "Transactions":
        Data_segmentation = st.sidebar.selectbox("**Data segmentation**", ("State", "District", "Pincode"), key="Data segmentation_selectbox")
        colum1,colum2= st.columns([1,1.5],gap="large")
        with colum1:
                Year = st.slider("**Select the Year**", min_value=2018, max_value=2022)
                Quarter = st.selectbox('**Select the Quarter**',('1','2','3','4'),key='qgwe2')

        if Data_segmentation == "State":
                mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total_amount from agg_transaction where year = {Year} and quarter = {Quarter} group by state order by Total_amount desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                title = "Top 10 Phonepe Transaction according to States"

                fig = px.pie(df, values='Transactions_Count',
                        names='State',
                        title=title,
                        color_discrete_sequence=px.colors.sequential.Magenta,
                        hover_data=['Total_Amount'],
                        labels={'Total_Amount':'Total Amount'})
                col1 = st.columns([1])[0]
                with col1:
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)
        if Data_segmentation == "District":
                mycursor.execute(f"SELECT district, state, sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total_amount FROM map_transaction WHERE year = {Year} AND quarter = {Quarter} GROUP BY district, state ORDER BY Total_amount DESC LIMIT 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'State', 'Transactions_Count', 'Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                        names='District',
                        title='Top 10 Phonepe Transactions according to Districts',
                        color_discrete_sequence=px.colors.sequential.Magenta,
                        hover_data=['State', 'Transactions_Count'],
                        labels={'Transactions_Count': 'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        if Data_segmentation == "Pincode":
                mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total_amount from top_transaction where year = {Year} and quarter = {Quarter} group by pincode order by Total_amount desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                        names='Pincode',
                        title='Top 10 Phonepe Transactions according to Pincode',
                        color_discrete_sequence=px.colors.sequential.Magenta,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count':'Transactions_Count'})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
    if Type == "Users":
        Data_segmentation = st.sidebar.selectbox("**Data segmentation**", ("Brands", "Registered_User", "Appopeners"), key="Data segmentation_selectbox")
        colum1,colum2= st.columns([1,1.5],gap="large")
        with colum1:
            Year = st.slider("**Select the Year**", min_value=2018, max_value=2022)
            Quarter = st.selectbox('**Select the Quarter**',('1234'),key='quat')
        if Data_segmentation == "Brands":
                mycursor.execute(f"select Brand, sum(Brand_count) as Total_Count, avg(Brand_percentage)*100 as Avg_Percentage from agg_user where Year = {Year} and Quarter = {Quarter} group by Brand order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                st.write(df)
                fig = px.pie(df,
                        values='Total_Users',
                        names='Brand',
                        title='Top 10 Phonepe users according to Brands',
                        hole=0.5,
                        color='Avg_Percentage')
                st.plotly_chart(fig, use_container_width=True)

        if Data_segmentation == "Registered_User":
                mycursor.execute(f"select district, sum(Registered_User) as Total_Registered_Users from map_user where Year = {Year} and quarter = {Quarter} group by District order by Total_Registered_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Registered_Users'])
                st.write(df)
                fig = px.pie(df,
                        title='Top 10 Phonepe users according to Districts',
                        values="Total_Registered_Users",
                        names="District",
                        hole = 0.5,
                        color='Total_Registered_Users')
                st.plotly_chart(fig, use_container_width=True)
        if Data_segmentation == "Appopeners":
                mycursor.execute(f"SELECT state, SUM(App_opening) AS Total_Appopeners FROM map_user WHERE year = {Year} AND quarter = {Quarter} AND App_opening > 0 GROUP BY state ORDER BY Total_Appopeners DESC limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State','Total_Appopeners'])
                st.write(df)
                fig = px.pie(df, 
                        values='Total_Appopeners',
                        names='State',
                        title='Top 10 Phonepe users according to Appopeners',
                        hole=0.5,
                        color='Total_Appopeners')
                st.plotly_chart(fig, use_container_width=True)
# Exploring the data
if selected == "Explore Data":
    st.markdown("## :violet[Exploring the data]")
    Type = st.sidebar.selectbox("**Type**", ("Analysis of Transactions", "Users"))
    if Type == "Analysis of Transactions":
        colum1,colum2= st.columns([1,1.5],gap="large")
        with colum1:
                        Year = st.slider("**Select the Year**", min_value=2018, max_value=2022)
                        Quarter = st.selectbox('**Select the Quarter**',('1','2','3','4'),key='qgwe2')
        st.markdown("## :violet[**Transaction Count According To District**]")
        selected_state = st.selectbox("**please select any State to visualize**",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=22,key="state_to_selectbox")
         
        mycursor.execute(f"select State, District,year,quarter, sum(Transaction_count) as Total_Transactions_count from map_transaction where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions_count'])
        fig = px.bar(df1,
                     title='Transaction Count According To District' ,
                     x="District",
                     y="Total_Transactions_count",
                     orientation='v',
                     color='Total_Transactions_count',
                     color_continuous_scale=px.colors.sequential.Magenta)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("## :violet[payment type]")
        selected_state = st.selectbox("**please select any State to visualize**",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),key="state_selectbox")
        Type = st.selectbox('**Please select the values to visualize**', ('Transaction_count', 'Transaction_amount'))
        if Type == "Transaction_count":
                        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions_count from agg_transaction where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
                        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions_count'])
                        fig = px.bar(df,
                                title='Transaction Types vs Total_Transactions_count',
                                x="Transaction_type",
                                y="Total_Transactions_count",
                                orientation='v',
                                color='Transaction_type',
                                color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=False)
        if Type == "Transaction_amount":
                        mycursor.execute(f"select Transaction_type, sum(Transaction_amount) as Total_Transaction_amount from agg_transaction where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
                        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions_amount'])
                        fig = px.bar(df,
                                title='Transaction Types vs Total_Transactions_amount',
                                x="Transaction_type",
                                y="Total_Transactions_amount",
                                orientation='v',
                                color='Transaction_type',
                                color_continuous_scale=px.colors.sequential.Magenta)
                        st.plotly_chart(fig,use_container_width=False)
       #geomap
        select1 = st.selectbox("Select a any one", ["Transaction count","Transaction amount"])
        st.markdown(":violet[This Geomap used to show the State based data according to Transaction count andTransaction amount ]")
        mycursor.execute(f"select State, sum(Transaction_count) as Total_Transaction_count, sum(Transaction_amount) as Total_Transaction_amount from map_transaction where year = {Year} and quarter = {Quarter} group by State order by State ")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transaction_count', 'Total_Transaction_amount'])
        State_name = "C:\\Users\\91994\\Desktop\\la,lo\\states.csv"
        data= pd.read_csv(State_name)
        df1.State = data
        if select1 == "Transaction amount":
                    fig1= px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Transaction_amount',
                        color_continuous_scale='Aggrnyl')

                    fig1.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig1,use_container_width=True)
        if select1 == "Transaction count":
                    fig2= px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Transaction_count',
                        color_continuous_scale='Aggrnyl')

                    fig2.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig2,use_container_width=True)
             
    if Type == "Users":
        Data_segmentation = st.sidebar.selectbox("**Data segmentation**", ( "Registered Users","Analysis of country"), key="Data_selectbox")
        colum1,colum2= st.columns([1,1.5],gap="large")
        with colum1:
            Year = st.slider("**Select the Year**", min_value=2018, max_value=2022)
            Quarter = st.selectbox('**Select the Quarter**',('1234'),key='quart')
        if Data_segmentation == "Registered Users": 
                st.markdown("## :violet[Total Numbers Of Registered Users  According to Districts]")
                selected_state = st.selectbox("**Select any state to fetch the data**",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=1)
        
                mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Registered_Users from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District','Total_Registered_Users'])
                fig = px.bar(df,
                     x="District",
                     y="Total_Registered_Users",
                     orientation='v',
                     color="Total_Registered_Users",
                     color_continuous_scale=px.colors.sequential.Magenta)
                st.plotly_chart(fig,use_container_width=True)

        if Data_segmentation == "Analysis of country":
                st.markdown(":violet[This Geomap used to show the State based data according to Registered users and App_Openers ]")
                mycursor.execute(f"select State, sum(Registered_user) as Registered_Users, sum(app_opening) as App_Opens from map_user where year={Year} and quarter={Quarter} group by state")
                df1 = pd.DataFrame(mycursor.fetchall(), columns=["State", "Registered_Users", "App_Opens"])
                State_name = "C:\\Users\\91994\\Desktop\\la,lo\\states.csv"
                data= pd.read_csv(State_name)
                df1.State = data
                fig = px.choropleth(df1,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey="properties.ST_NM",
                        locations="State",
                        color="Registered_Users",
                        hover_data=["State", "Registered_Users", "App_Opens"],
                        color_continuous_scale={
                      
                    })
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(height=600, width=800)
                st.plotly_chart(fig, use_container_width=False, key='choropleth_chart')
 