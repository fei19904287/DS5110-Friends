import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.title(":red[_Friends_: The One with the Analysis]")

df1 = pd.read_csv("friends_episodes_v3.csv")
df2 = pd.read_csv("guest_stars_info.csv")

# concat the df together

# DF_ALL = pd.concat([df1,df2])
# print(DF_ALL.head(2))

# Join the data frames to one

all_episodes_info = pd.merge(df1, df2, on=['Season','Episode_Number'], how='outer')
all_episodes_info['Episode_Index'] = range(1, len(all_episodes_info) + 1)

episodes_celebrities_df = all_episodes_info[all_episodes_info['Guest_Star_Name'].notna()]
episodes_celebrities_cheering_df = episodes_celebrities_df[episodes_celebrities_df['Audience_Cheering'] == 'y']

# Merge episodes_only_with_celebrities with all_episodes_info to add the Episode_Index
print("before merging........")
print(len(episodes_celebrities_df))
#
print(episodes_celebrities_df.head(7))

#Tasks
# for data cleaning, check null value, also , if there is NaN, replace with reasonable values instead
# Check for missing values (NaN) in both DataFrames
print("Missing values in all_episodes_info:")
print(all_episodes_info.isnull().sum())


# For other columns, you can decide based on your domain knowledge if you want to fill them with a specific value
all_episodes_info['Guest_Star_Name'] = all_episodes_info['Guest_Star_Name'].fillna('Non_Exist')
all_episodes_info['Audience_Cheering'] = all_episodes_info['Audience_Cheering'].fillna('n')


# If you want to drop rows with missing values entirely (use cautiously)
# episodes_only_with_celebrities.dropna(inplace=True)

# Verify that missing values were filled
print("Missing values after filling in episodes_only_with_celebrities:")
print(episodes_celebrities_df.isnull().sum())

st.header("Friends All Episodes Info",divider=True)
st.write(all_episodes_info)

chart_data = all_episodes_info[["Votes", "Episode_Index"]].dropna() 

st.header("All Episodes Votes", divider=True)

st.scatter_chart(data=chart_data, x="Episode_Index", y="Votes",color=None)

# based on votes , find the top 8 episodes, display the episode number and season number , and episode title , display using a
# graph

st.header("Top 8 episodes based on Votes", divider=True)
# Sort the episodes based on the number of votes in descending order
top_8_episodes_votes = all_episodes_info.sort_values(by='Votes', ascending=False).head(8)

top_8_episodes_votes_info = top_8_episodes_votes[['Episode_Index', 'Season', 'Episode_Number', 'Episode_Title', 'Votes']]

# Create the plot
plt.figure(figsize=(10, 6))

# Bar plot showing the top 8 episodes by number of votes
sns.barplot(x='Votes', y='Episode_Title', data=top_8_episodes_votes_info)

# Add titles and labels
plt.title("Top 8 Episodes Based on Votes", fontsize=16)
plt.xlabel("Number of Votes", fontsize=14)
plt.ylabel("Episode Title", fontsize=14)

# Add episode number and season number inside the bars
for idx, (i, row) in enumerate(top_8_episodes_votes_info.iterrows()):
    episode_label = f"Ep {row['Episode_Number']} - Season {row['Season']}"
    x_pos = row['Votes'] / 2  # Position the label in the middle of the bar
    plt.text(x_pos, idx, episode_label,
             color='white',
             ha='center',
             va='center',
             fontsize=10, fontweight='bold')

# Adjust the plot limits to accommodate the labels
plt.xlim(0, top_8_episodes_votes_info['Votes'].max() * 1.2)  # Extend x-axis by 20% to fit labels

# Display the plot in Streamlit
st.pyplot(plt)