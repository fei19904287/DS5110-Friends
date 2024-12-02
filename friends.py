import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


image_url = "https://miro.medium.com/v2/resize:fit:1400/0*MHCh12pKc4A1aif-"
# Set up the background image using custom CSS
def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({image_url});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with the image URL
set_background(image_url)

st.title(":green[_The One with the Analysis_]")

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

# # Merge episodes_only_with_celebrities with all_episodes_info to add the Episode_Index
# print("before merging........")
# print(len(episodes_celebrities_df))
# #
# print(episodes_celebrities_df.head(7))

# #Tasks
# # for data cleaning, check null value, also , if there is NaN, replace with reasonable values instead
# # Check for missing values (NaN) in both DataFrames
# print("Missing values in all_episodes_info:")
# print(all_episodes_info.isnull().sum())


# For other columns, you can decide based on your domain knowledge if you want to fill them with a specific value
all_episodes_info['Guest_Star_Name'] = all_episodes_info['Guest_Star_Name'].fillna('Non_Exist')
all_episodes_info['Audience_Cheering'] = all_episodes_info['Audience_Cheering'].fillna('n')


# If you want to drop rows with missing values entirely (use cautiously)
# episodes_only_with_celebrities.dropna(inplace=True)

# Verify that missing values were filled
# print("Missing values after filling in episodes_only_with_celebrities:")
# print(episodes_celebrities_df.isnull().sum())

if st.button(":red[Friends All Episodes Info]"):
    st.header(":red[Friends All Episodes Info]",divider=True)
    st.write(all_episodes_info)

    chart_data = all_episodes_info[["Votes", "Episode_Index"]].dropna() 

    st.header(":blue[All Episodes Votes]", divider=True)

    st.scatter_chart(data=chart_data, x="Episode_Index", y="Votes",color=None)

# based on votes , find the top 8 episodes, display the episode number and season number , and episode title , display using a
# graph
if st.button(":green[Top 8 episodes based on Votes]"):
    st.header(":green[Top 8 episodes based on Votes]", divider=True)
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


# Button to display the Top 8 Episodes by Stars plot
if st.button("Show Top 8 Episodes by Stars"):
    st.header("Top 8 episodes based on Stars", divider=True)
    # Step 1: Sort the episodes based on the star ratings in descending order
    top_8_episodes_Stars = all_episodes_info.sort_values(by='Stars', ascending=False).head(8)

    # Step 2: Create a new DataFrame with the relevant columns
    top_8_episodes_info_Stars = top_8_episodes_Stars[['Episode_Index', 'Season', 'Episode_Number', 'Episode_Title', 'Stars']]

    # Step 3: Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))  # Increase the figure size for better visualization

    # Apply a color palette based on the 'Stars' rating
    sns.barplot(x='Stars', y='Episode_Title', data=top_8_episodes_info_Stars, palette='coolwarm', ax=ax)

    # Add titles and labels
    ax.set_title("Top 8 Episodes Based on Stars", fontsize=16)
    ax.set_xlabel("Star Ratings", fontsize=14)
    ax.set_ylabel("Episode Title", fontsize=14)

    # Add episode number and season number inside the bars
    for idx, (i, row) in enumerate(top_8_episodes_info_Stars.iterrows()):
        episode_label = f"Ep {row['Episode_Number']} - Season {row['Season']}"
        x_pos = row['Stars'] / 2  # Position the label in the middle of the bar
        ax.text(x_pos, idx, episode_label,
                color='white', ha='center', va='center', fontsize=12, fontweight='bold')

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Button to display the "Stars Trend" scatter plot
if st.button("Show Stars Trend Scatter Plot"):
    st.header("Stars Trend Scatter Plot", divider=True)
    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size
    sns.scatterplot(data=all_episodes_info, x='Episode_Index', y='Stars', color='red', ax=ax)
    
    # Add titles and labels
    ax.set_title("Stars Trend", fontsize=16)
    ax.set_xlabel("Episode_Index", fontsize=14)
    ax.set_ylabel("Stars", fontsize=14)

    # Display the plot in Streamlit
    st.pyplot(fig)

# Button to display the "Average Stars by Season" bar plot
if st.button("Show Average Stars by Season"):
    st.header("Average Stars by Season", divider=True)
    # Calculate the total Stars by Season
    season_totals = all_episodes_info.groupby('Season')['Stars'].mean().reset_index()

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size
    sns.barplot(data=season_totals, x='Season', y='Stars', hue='Season', dodge=False, ax=ax, palette='viridis')

    # Add values to the top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", label_type="edge")  # Show 2 decimal points

    # Add titles and labels
    ax.set_title("Average Stars by Season", fontsize=16)
    ax.set_xlabel("Season", fontsize=14)
    ax.set_ylabel("Average Stars", fontsize=14)

    # Remove legend (optional, since the hue is the same as the x-axis)
    ax.legend_.remove()

    # Display the plot in Streamlit
    st.pyplot(fig)

# Top 8 episodes by votes
top_8_episodes_votes = all_episodes_info.sort_values(by='Votes', ascending=False).head(8)
votes_episodes = set(top_8_episodes_votes['Episode_Title'])

# Top 8 episodes by stars
top_8_episodes_stars = all_episodes_info.sort_values(by='Stars', ascending=False).head(8)
stars_episodes = set(top_8_episodes_stars['Episode_Title'])

if st.button("Show common episodes of stars and votes"):
    # Find common episodes
    common_episodes = votes_episodes.intersection(stars_episodes)

    # Filter the common episodes from the DataFrame
    common_episodes_info = all_episodes_info[all_episodes_info['Episode_Title'].isin(common_episodes)]

    # Display in Streamlit
    st.write("Common Episodes in Top 8 by Votes and Stars:")
    st.write(common_episodes_info[['Episode_Title', 'Votes', 'Stars', 'Season', 'Episode_Number']])

# Filter episodes with guest stars
episodes_celebrities_df = all_episodes_info[all_episodes_info['Guest_Star_Name'] != 'Non_Exist']

if st.button("Episodes With Guest Stars"):
    # Display dataset
    st.dataframe(episodes_celebrities_df)
    st.scatter_chart(data=episodes_celebrities_df, x="Episode_Index", y="Votes",color=None)













