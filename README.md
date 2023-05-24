# League of Legends Tournament Code Scraper

A Python based project which uses Playwrighter and Beautiful Soup to scrape Tournament Codes

The codes are scraped from https://www.toornament.com/en_GB/

## Setup

* Setup a Organiser Account: https://organizer.toornament.com/en_GB/login/
* Once setup, create a tournament, noting down the name given.
* Create a League of Legends Tournament with a player size of 32.
* Create a new stage, select **Duel**, then choose **League** format.
* Set the size to 32, and the number divisions to 3.
* Once created, add the fake players to the league using the *participants* tab.
* Then use the **Fill All** button, to add the fake players.
* Return to the Overview section, click the three dots icon under *Structure*, select configure.
* Head to the *advanced* tab, and select 'yes' for *place participants automatically*.
* Return back to the Overview section, then select *Enter Match Results*.
* Select the *Settings* tab, and enable **Tournament Codes**.
* The configure the Match Settings, to *Single Game* & *Result Based*.

## Running the Script

To run use: python scrape.py [username] [password] [tournament name] [number of match pages] [headerless]

* Username: Toornament Username
* Password: Toornament Password
* Tournament Name: Name of Tournament
* Number of Match Pages: Number of pages on the enter results page. Can be found at the bottom.
* Headerless: True or False, you can see the bot do it in real-time!







