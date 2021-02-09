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

[assets/log-data.png]

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

There are several constraints applied to the database that may be worth highlighting:

dim_artists table
- artist_id: This field has been defined as the primary key for this table. Whilst Redshift does not enforce referential integrity, this will still allow the query optimiser/planner to give us better performance. It has also been specified that this field cannot be NULL, as it's the primary key.
- artist_name: This field has the NOT NULL constraint on it. Incoming songs metadata should provide us with this as a minimum and so constraining the data in this way will highlight potential issues with our source data before they get to the database.
- The distribution style for this table has been set to ALL as the million songs dataset has approximately only 50,000 artists in. It is my view that this is small enough to copy across all nodes for improved query performance (I also expect that a high proportion of queries will join on this table).
- As Redshift doesn't support a typical MERGE/UPSERT command, loads into this table are performed within a transaction with a deletion of already existing records followed by a full insert of the staged songs/artists data.

dim_songs table
- song_id: This field has been defined as the primary key for this table, along with a NOT NULL constraint. The same comment as artist_id above stands here too. This has also been defined as the distkey for this table (and therefore the table has been set to a KEY distribution style). This is because an EVEN distribution could be more likely to result in a skewed distribution and so this meaningless integer value has been used instead.
- title: This field has the NOT NULL constraint on it. Incoming songs metadata should provide us with this as a minimum and so constraining the data in this way will highlight potential issues with our source data before they get to the database.
- artist_id: This field has the NOT NULL constraint on it. Incoming songs metadata should provide us with this as a minimum and so constraining the data in this way will highlight potential issues with our source data before they get to the database. It could be worth investgating removing this field from the songplays fact table in the future and creating a snowflake schema with the artists table mentioned already referenced by this table instead of the songplays table.
- As Redshift doesn't support a typical MERGE/UPSERT command, loads into this table are performed within a transaction with a deletion of already existing records followed by a full insert of the staged songs/artists data.

dim_users table
- user_id: This field has been defined as the primary key for this table, the same comment as artist_id above stands here too. We do not want to end up with duplicate users in this table. This has also been defined as the distkey for this table (and therefore the table has been set to a KEY distribution style). This is because an EVEN distribution could be more likely to result in a skewed distribution and so this meaningless integer value has been used instead.
- As Redshift doesn't support a typical MERGE/UPSERT command, loads into this table are performed within a transaction with a deletion of already existing records followed by a full insert of the NextSong event users.

dim_time table
- start_time: This field has been defined as the primary key for this table. We do not want to end up with duplicate times in this table.
- All other fields have the NOT NULL constraint. These fields are generated by the ETL process based on the start_time field and therefore highlighting where NULLs occur could identify issues with our ETL process.
- start_time: This has been defined as the distkey and sortkey for this table (and therefore the table has been set to a KEY distribution style). This is to align with the fact table distribution style and keys.
- As Redshift doesn't support a typical MERGE/UPSERT command, loads into this table are performed within a transaction with a deletion of already existing records followed by a full insert of the NextSong event start times.

fact_songplays table
- songplay_id: This field has been defined with the IDENTITY(0,1) property which is Redshift's equivalent of the SERIAL keyword - this means that we can allow the insertion process to auto-generate an auto-incrementing integer key value to input here. This is useful as we don't have anything immediately available to use within the logs data.
- start_time: This has been defined as the distkey and sortkey for this table (and therefore the table has been set to a KEY distribution style). This is because many queries run against this table will involve a date/time filter, and/or will be joined to the dim_time table.


Instructions
- Clone repo into a directory on your computer.
- Create a virtual environment and activate
- Install requirements (use requirements-dev if you will be developing against this repo or requirements-prod if just running the ETL pipeline)
- Make sure you have created a Cluster subnet group and launched a Redshift cluster attached to this subnet group. 
- You will need an IAM role with Read access to S3 permission assigned.
- Create a config file called dwh.cfg and save in the root of this repo. 
- Within dwh.cfg input the config variables needed by this project.
- Using Python, run src/create_tables.py
- Using Python, run src/etl.py