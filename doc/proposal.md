# Proposal
#### Group 12
members：Shiyi Chen, Ruomeng Tian,Zerui Zhang,Hanwen Zhang

## Section 1: Motivation and Purpose
##### Our role: Digital Content Analytics Team
##### Target audience: Content creators, digital marketers, and media strategy teams in North America
In the digital era, where YouTube stands as a colossal platform for content dissemination and audience engagement, understanding what content trends and why is crucial for anyone in the content creation and digital marketing sphere. The landscape of YouTube is dynamic, with viewer preferences and content trends evolving rapidly. This presents a challenge for content creators and marketers to stay ahead of the curve, necessitating a tool that can provide insights into trending content across different regions. Our dashboard aims to address this need by offering an in-depth analysis of YouTube trending videos, specifically focusing on the USA, Canada, and Mexico. This regional focus allows for a comparative analysis of viewer preferences and content strategies that are effective in North America. By identifying the characteristics of trending videos and understanding regional content preferences, our dashboard solves the problem of navigating the complex content landscape on YouTube, enabling users to tailor their content and marketing strategies to capitalize on current trends and maximize viewer engagement.

## Section 2: Description of the Data
For our project, we have refined our focus within the YouTube Trending Video Dataset, originally encompassing a broad selection of countries, to specifically analyze data from the USA, Canada, and Mexico. This targeted approach allows us to closely examine trends and viewer preferences within these North American countries. Furthermore, we have concentrated our analysis on the most recent three months of data. This temporal limitation ensures our insights remain timely and relevant, providing a snapshot of current trends and audience behaviors on YouTube.
The dataset encompasses a variety of variables that describe both the content of the videos and the audience's reaction to them. Key variables include:
- video_id, title, channelTitle: Identifiers for each video, including the video's title and the channel name.
- publishedAt: The timestamp indicating when the video was uploaded.
- categoryId: The genre or category of the video as specified by the uploader.
- trending_date: The date(s) on which the video appeared on the trending list.
- tags: Keywords associated with the video.
- view_count, likes, dislikes, comment_count: Metrics representing viewer engagement.
- thumbnail_link: The URL of the video's thumbnail image.
- comments_disabled, ratings_disabled: Indicators of whether comments or ratings are disabled for the video.
- description: A brief description of the video content.
- country: The country in which the video trended.

## Section 3: Research Questions and Usage Scenarios
Research Questions:
- What types of content are most likely to trend in each of the three countries? This question seeks to identify the categories or themes of videos that capture the largest audience interest in each region.
- Are there identifiable patterns in the timing of when videos trend in these countries? Understanding whether the timing of posting affects a video's likelihood to trend could inform optimal content release strategies.
- How long does it typically take for a video to become trending after it is published? Analyzing the time interval between the publishedAt and trending_date for videos can provide insights into how quickly content can capture audience attention.
- Which channels have the most videos that trend? Identifying channels that consistently produce trending content could reveal successful content strategies and themes that resonate with a broad audience.
- What are the most common words in the titles of trending YouTube videos? Analyzing how these keywords vary by category and country uncover insights into viewer interests and content optimization strategies.

Usage Scenarios:

Mia, a YouTube content creator focused on expanding her channel's reach across North America, seeks to understand regional preferences to tailor her video topics effectively.
She uses the YouTube Trending Video Analytics Dashboard to filter videos by country and category, observing which genres trend in the USA, Canada, and Mexico. She notes the popularity of gaming content in the USA, culinary videos in Mexico, and fitness tutorials in Canada.
Armed with these insights, Mia plans her content calendar to include gaming walkthroughs tailored to her US audience, Mexican cuisine recipes for viewers in Mexico, and workout routines for her Canadian followers, optimizing her channel's appeal across regions.

#### Sketch of the application
![sketch](551projectdashboard.jpg)
