# THIS SITE IS A WORK IN PROGRESS

[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-blue)](https://creativecommons.org/licenses/by-nc/4.0/)

Welcome

---

## Table of Contents
1. [About the Project](#about-the-Project)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Results](#results)
5. [Contact](#contact)

---

## About the Project

The point of the project is to track, analyze, and visualize my Spotify listening habits to showcase skills in Python, Excel, and Power BI.
The project started because I wanted to have a deeper insight into my Spotify listening habits, but outside from the annual Spotify wrapped, Spotify does not share any data.
The solution was to implement automatic tracking of songs I listened to and gathering my own data.

---

## Features

The main feature of the simple command-line application is to enable the user to fetch recently played songs and store them in a database.

You can also use the SpotifyManager class to run a script that only fetches and stores the tracks without any interaction. This way you can automate the process.

The command-line application does however offer a couple of additional tools that can be useful:
- View all the users owned playlists.
- Download a playlist to a csv file.
- Create a playlist from a csv file.
- Delete a playlist.
- Save top items to a csv file.
- View last played tracks (up to 50).

I included these features, because they allow for multiple use-cases and sometimes even deleting playlists from the Spotify app won't work. They also act as building blocks for future improvements.

---

## Technologies Used

- **Python:** The core application, including command-line functionality and backend processes, is developed in Python, utilizing the Spotify API for data extraction.
- **SQLite:** A lightweight SQLite database is used for data storage, eliminating the need for external hosting.
- **Excel:** Employed for comprehensive data analysis and reporting.
- **Power BI:** Used for creating dynamic and interactive visualizations.

The application code is available on GitHub: [iljateerikorpi](https://github.com/iljateerikorpi)

---

## Results

For privacy reasons, the entire dataset will not be displayed. However, select insights and analyses from November 2024 will be showcased with select artists to demonstrate the project's capabilities.

### Excel

Excel was primarily used as a source for Power BI, Excel is useful for quick insights.

A pivot table is a quick and dynamic way to get insights from data. In this pivot table, using slicers, I take a look at how many minutes I listened to Drake in November and from what songs the number consists of.

![Excel pivot table](assets/Excel_pivot_table.png)

Now using some Excel functions I can gather information about which Drake albums I listened to the most.

![Albums](assets/Excel_albums.png)

Finally I can create a quick table and chart from the gathered information and gain a good visual on when the bulk of my most listened to Drake songs were released.

![Table and chart](assets/Excel_table_and_chart.png)

### Power BI dashboard

With Power BI, I can have a deeper insight into my listening habits. These screenshots show how the interactive dashboard works.

![Power BI dashboard](assets/Power_BI_1.png)

When you select artists, their corresponding data will be displayed.

![Dashboard with selections](assets/Power_BI_2.png)

*For licensing reasons, I decided to not embed the dashboard, and just include screenshots.*

---

## Contact

For any inquiries or to learn more about this project, feel free to get in touch:

- **GitHub**: [iljateerikorpi](https://github.com/iljateerikorpi)
- **LinkedIn**: [Ilja Teerikorpi](https://www.linkedin.com/in/ilja-teerikorpi-a67377318/)
- **Email**: iljateerikorpi@gmail.com

---

Thank you for visiting this page! Check out the [GitHub repository](https://github.com/iljateerikorpi/Spotify-Public) for more details.
