# SI507_FInal_Project
SI 507 Final Project

## Data Sorces
Data used in this project was obtained from imbd.com. Two levels of webpages were crawled and scraped. First, information in https://www.imdb.com/chart/top?ref_=nv_mv_250 about movie names and rankings, together with the link to the movie's own webpage, was collected. Afterwards, in each movie's own webpage, information about the movie's content rating, average rating, genre, actors, and directors, was collected. 

## Running the Program
Please use the command pip install -r requirements.txt to ensure all the required packages are installed before running the python file. 

Type python cjyang_finalproject.py in the command line to run the program.

First, it takes some time for the program to initialize itself. Please be patient. Reading the cache file and generating tables in the database could take some time. 

After the program is initialized, the user will be asked to write command in the interactive prompt. While running the program for the first time, please type "help" to see the available plotting command options. There are four plotting commands. The instructions are available in the *help.txt* file, and the program also use *help.txt* to display the help information. So please also download the *help.txt* file into your repo.

## Code Structure

1. Scrape the webpage https://www.imdb.com/chart/top?ref_=nv_mv_250. Obtain each movie's ranking, full link, and name.
2. Use the full links obtained in step 1. Go into each link to get information about each movie's actors, directors, year published, average rating and content rating. 
3. Write SQL code and generate plots using plotly

Important functions: Beautifulsoup, requests, sqlite3, dictionary and list operations.

## User Guide
Most instrucitons were already mentioned in Running the Program section. Below are the four available commands for data visualizaiton:

directoraverage:

        Provides you a bar chart of directors and the average rating of their films. Note that only the directors who have directed more than one film will be included in this graph.

yeartrend:

        Provides you a line chart of the number of top 250 movies released each year.

actor:

        Provides you a bar chart of actors and the total number of their top 250 films. Note that only the actors who have starred in more than one film will be included.

contentrating:

        Provides you a bar chart of the total number of top 250 films in each content rating. 
