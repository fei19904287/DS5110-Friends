import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.sidebar.success("Select a demo below:")

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


all_episodes_info = pd.merge(df1, df2, on=['Season','Episode_Number'], how='outer')
all_episodes_info['Episode_Index'] = range(1, len(all_episodes_info) + 1)

episodes_celebrities_df = all_episodes_info[all_episodes_info['Guest_Star_Name'].notna()]
episodes_celebrities_cheering_df = episodes_celebrities_df[episodes_celebrities_df['Audience_Cheering'] == 'y']

all_episodes_info['Guest_Star_Name'] = all_episodes_info['Guest_Star_Name'].fillna('Non_Exist')
all_episodes_info['Audience_Cheering'] = all_episodes_info['Audience_Cheering'].fillna('n')


if st.sidebar.button(":red[Friends All Episodes Info]"):
    #st.header(":red[Friends All Episodes Info]",divider=True)
    st.write(all_episodes_info)

    

if st.sidebar.button(":blue[All Episodes Votes]"):
    chart_data = all_episodes_info[["Votes", "Episode_Index"]].dropna() 
   # st.header(":blue[All Episodes Votes]", divider=True)

    st.scatter_chart(data=chart_data, x="Episode_Index", y="Votes",color=None)

# based on votes , find the top 8 episodes, display the episode number and season number , and episode title 
if st.sidebar.button(":green[Top 8 episodes based on Votes]"):
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

    # Button to display the "Stars Trend" scatter plot
if st.sidebar.button(":red[Stars Trend Scatter Plot]"):

    fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size
    sns.scatterplot(data=all_episodes_info, x='Episode_Index', y='Stars', color='red', ax=ax)
    
    # Add titles and labels
    ax.set_title("Stars Trend", fontsize=16)
    ax.set_xlabel("Episode_Index", fontsize=14)
    ax.set_ylabel("Stars", fontsize=14)

    # Display the plot in Streamlit
    st.pyplot(fig)
# Button to display the Top 8 Episodes by Stars plot
if st.sidebar.button(":blue[Top 8 Episodes by Stars]"):

    top_8_episodes_Stars = all_episodes_info.sort_values(by='Stars', ascending=False).head(8)

    top_8_episodes_info_Stars = top_8_episodes_Stars[['Episode_Index', 'Season', 'Episode_Number', 'Episode_Title', 'Stars']]

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



# Button to display the "Average Stars by Season" bar plot
if st.sidebar.button(":orange[Show Average Stars by Season]"):

    season_totals = all_episodes_info.groupby('Season')['Stars'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size
    sns.barplot(data=season_totals, x='Season', y='Stars', hue='Season', dodge=False, ax=ax, palette='viridis')

    # Add values to the top of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", label_type="edge")  # Show 2 decimal points

    # Add titles and labels
    ax.set_title("Average Stars by Season", fontsize=16)
    ax.set_xlabel("Season", fontsize=14)
    ax.set_ylabel("Average Stars", fontsize=14)

    ax.legend_.remove()
    st.pyplot(fig)

# Top 8 episodes by votes
top_8_episodes_votes = all_episodes_info.sort_values(by='Votes', ascending=False).head(8)
votes_episodes = set(top_8_episodes_votes['Episode_Title'])

# Top 8 episodes by stars
top_8_episodes_stars = all_episodes_info.sort_values(by='Stars', ascending=False).head(8)
stars_episodes = set(top_8_episodes_stars['Episode_Title'])

if st.sidebar.button(":red[Common episodes of stars and votes]"):
    # Find common episodes
    common_episodes = votes_episodes.intersection(stars_episodes)

    # Filter the common episodes from the DataFrame
    common_episodes_info = all_episodes_info[all_episodes_info['Episode_Title'].isin(common_episodes)]

    # Display in Streamlit
    st.write("Common Episodes in Top 8 by Votes and Stars:")
    st.write(common_episodes_info[['Episode_Title', 'Votes', 'Stars', 'Season', 'Episode_Number']])

# Filter episodes with guest stars
episodes_celebrities_df = all_episodes_info[all_episodes_info['Guest_Star_Name'] != 'Non_Exist']
if st.sidebar.button(":red[Episodes With Guest Star Info]"):
    st.write(episodes_celebrities_df)

if st.sidebar.button(":blue[Episodes With Guest Star Votes Trend]"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=episodes_celebrities_df, x='Episode_Index', y='Votes', color='blue', ax=ax)
    ax.set_title("Episodes With Guest Star Votes Trend", fontsize=16)
    ax.set_xlabel("Episode_Index", fontsize=14)
    ax.set_ylabel("Votes", fontsize=14)

    st.pyplot(fig)

    # Sort the DataFrame by Votes in descending order
    sorted_df = episodes_celebrities_df.sort_values(by='Votes', ascending=False)

    # Display the top 2 rows with Guest Star Name, Season, Episode Number, and Votes
    st.write("### Top Episodes With Guest Stars by Votes")
    st.dataframe(sorted_df[['Guest_Star_Name', 'Season', 'Episode_Number', 'Votes']].head(2))

    st.video("https://www.youtube.com/watch?v=AqzJ_jbVUJw&ab_channel=JoeyFriendsClips")
    st.video("https://www.youtube.com/watch?v=xHLaISBRmdI&t=6s&ab_channel=FriendsOriginals")


# Scatter plot for Votes with Guest Star and Audience Cheering
if st.sidebar.button(":green[Audience Cheering Votes Trend]"):

    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=episodes_celebrities_cheering_df, x='Episode_Index', y='Votes', color='blue', ax=ax)
    ax.set_title("Episodes With Guest Star (with Audience Cheering) Votes Trend", fontsize=16)
    ax.set_xlabel("Episode_Index", fontsize=14)
    ax.set_ylabel("Votes", fontsize=14)

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Sort the DataFrame by Votes in descending order
    sorted_df = episodes_celebrities_cheering_df.sort_values(by='Votes', ascending=False)

    # Display the top episode
    st.write("### Top Episode With Guest Stars and Audience Cheering by Votes")
    st.dataframe(sorted_df[['Guest_Star_Name', 'Season', 'Episode_Number', 'Votes']].head(1))

    st.image(
        "https://i0.wp.com/bamfstyle.com/wp-content/uploads/2021/11/Friends809BP-MAIN1.jpg?ssl=1", 
        use_column_width=True
    )



if st.sidebar.button(":blue[Scripts Analysis]"):

    # Provide the image path 
    image_path = "output.png" 
    image_path2 = "output2.png" 
    image_path3 = "output3.png" 
    image_path4 = "output4.png" 
    image_path5= "output5.png" 
    image_path6 = "output6.png" 
    image_path7 = "output7.png" 

    # Write the image to the canvas
    st.image(image_path, caption="Number of lines for the entire show", use_column_width=True)
    st.image(image_path2, caption="Number of lines by Season", use_column_width=True)
    st.image(image_path3, caption="Number of mentions in the Script", use_column_width=True)
    st.image(image_path4, caption="Largest Vacablury", use_column_width=True)
    st.image(image_path5, caption="Ross Sentiment per episode season 1 to 3", use_column_width=True)
    st.image(image_path6, caption="Ross Sentiment per episode season 4 to 6", use_column_width=True)
    st.image(image_path7, caption="Ross Sentiment per episode season 7 to 10", use_column_width=True)










