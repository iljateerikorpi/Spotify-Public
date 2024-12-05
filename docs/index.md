# THIS SITE IS A WORK IN PROGRESS

[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue)](https://creativecommons.org/licenses/by-nc/4.0/)

Welcome

---

## Table of Contents
1. [About the Project](#about-the-Project)
2. [Command-Line Application Features](#command-line-application-features)
3. [Technologies Used](#technologies-used)
4. [Results](#results)
5. [Contact](#contact)

---

## About the Project

This project focuses on tracking, analyzing, and visualizing my Spotify listening habits to showcase my skills in Python, Excel, and Power BI. 
It began as a way to gain deeper insights into my music preferences since Spotify only provides limited data through its annual Wrapped feature. 
To address this limitation, I developed a system for automatically tracking the songs I listen to, enabling me to collect and analyze my own data.

---

## Command-Line Application Features

The core functionality of this command-line application is to fetch recently played songs and store them in a database.

Additionally, the user can leverage the `SpotifyManager` class to run a script that fetches and stores tracks without user interaction. This feature makes the process fully automated.

The command-line application also includes several additional tools designed for flexibility and convenience:

- **View all owned playlists**: Explore all playlists associated with your account.  
- **Download a playlist to a CSV file**: Export playlist data for further analysis or backup.  
- **Create a playlist from a CSV file**: Easily generate new playlists from CSV data.  
- **Delete a playlist**: Remove playlists directly, even when the Spotify app encounters issues.  
- **Save top items to a CSV file**: Export your top tracks or artists for deeper insights.  
- **View last played tracks (up to 50)**: Quickly review your most recently played songs.

These features serve multiple use cases, offering practical tools while laying the groundwork for future enhancements. Whether for troubleshooting or expanding functionality, they make managing Spotify data more efficient and customizable.


---

## Technologies Used

- **Python:** The core application, including command-line functionality and backend processes, is developed in Python, utilizing the Spotify API for data extraction.
- **SQLite:** A lightweight SQLite database is used for data storage, eliminating the need for external hosting.
- **Excel:** Employed for comprehensive data analysis and reporting.
- **Power BI:** Used for creating dynamic and interactive visualizations.

The application code is available on [GitHub](https://github.com/iljateerikorpi/Spotify-Public).

---

## Results

To maintain privacy, the complete dataset will not be shared. Instead, curated insights and analyses from November 2024 will be presented, highlighting select artists to showcase the project's capabilities and potential.

### Excel Analysis: Quick Insights

While Excel primarily served as a source for Power BI, it also proved invaluable for quick insights into my listening data.

A pivot table is a dynamic tool for extracting insights efficiently. In this example, using slicers, I analyzed how many minutes I listened to Drake in November and identified the specific songs that contributed to this total.

![Excel pivot table](assets/Excel_pivot_table.png)

By leveraging Excel functions, I further explored which Drake albums I listened to the most during this period.

![Albums](assets/Excel_albums.png)

Finally, I created a simple table and chart from the collected data to visualize when the majority of my most-played Drake songs were released.

![Table and chart](assets/Excel_table_and_chart.png)

### Power BI Dashboard

Power BI provides deeper insights into my listening habits through an interactive and dynamic dashboard. These screenshots demonstrate its functionality:

![Power BI dashboard](assets/Power_BI_1.png)

When specific artists are selected, their corresponding data is displayed, offering a focused view of listening trends.

![Dashboard with selections](assets/Power_BI_2.png)

*For licensing reasons, the dashboard is not embedded directly on this site. Instead, screenshots are provided for demonstration purposes.*

---

## Contact

For any inquiries or to learn more about this project, feel free to get in touch:

- **GitHub**: [iljateerikorpi](https://github.com/iljateerikorpi)
- **LinkedIn**: [Ilja Teerikorpi](https://www.linkedin.com/in/ilja-teerikorpi-a67377318/)
- **Email**: iljateerikorpi@gmail.com

---

Thank you for visiting this page! Check out the [GitHub repository](https://github.com/iljateerikorpi/Spotify-Public) for more details.
