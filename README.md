# Data Engineering Nanodegree - Project 3
## Cloud Data Warehousing
### Introduction
This is the third project issued as part of Udacity's Data Engineering Nanodegree program.

Sparkify is a startup that provides a music streaming app. They want to analyse the data that they have so far been collecting. By analysing their data they will be able to identify simple things such as most commonly played songs and most active users. With extensions to their data collection and storage ability they could use data analytics to model retention, recurring revenue and even forecast things such as whether, and when, a free user is likely to convert to paid.

### Data Sources
Sparkify have already began collected event logs from their app and have been outputting two forms of logs to an S3 bucket. 

The first set of logs is metadata on songs that have been added to the app. This metadata is stored in individual JSON files for each song. They are organised in the bucket into three levels of keys by the first three letters of the song's ID. Here is an example song file:

{
    "num_songs": 1, 
    "artist_id": "ARJIE2Y1187B994AB7", 
    "artist_latitude": null, 
    "artist_longitude": null, 
    "artist_location": "", 
    "artist_name": "Line Renaud", 
    "song_id": "SOUPIRU12A6D4FA1E1", 
    "title": "Der Kleine Dompfaff", 
    "duration": 152.92036, 
    "year": 0
}

Each of these metadata records can be used to extract song and artist information for loading into an analytical data warehouse.

The second set of logs is also a collection of JSON files, but these are user interaction event logs grouped by date, aggregating a days-worth of user activity within the app into each file. Here is an example log file (from 12/11/2018) formatted as a table:

[assets/logfileexample.png]

### Schema Design

To optimise this data for analytical queries we are modelling as a star schema. The following tables were created:

Fact table:

- fact_songplays

Dimension tables:

- dim_songs
- dim_artists
- dim_users
- dim_time

Structuring the data in this way allows easy, fast aggregation queries over the songplays table to analyse activity but also allows simple and fast joins to the dimensions where necessary. De-normalising the artists and songs into dimenison tables allows easier and faster updates if they become necessary at some point in the future.