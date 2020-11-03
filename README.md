<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg" width="200" style="margin-right: 50px">


</div>

<h2 align="center">Spotify User Data Analyzer</h2>

<p align="center">
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href="https://github.com/chronoB/SpotifyDataAnalyzer/issues"><img alt="Open Issues" src="https://img.shields.io/github/issues/chronoB/SpotifyDataAnalyzer"></a>
  <a href="https://github.com/chronoB/SpotifyDataAnalyzer/releases"><img alt="Release" src="https://img.shields.io/github/release/chronoB/SpotifyDataAnalyzer.svg"></a>
  <a href="https://dev.azure.com/chronoB/SpotifyDataAnalyzer/_build/latest?definitionId=1&branchName=master"><img alt="Azure Pipelines status" src="https://dev.azure.com/finnobayer/SpotifyDataAnalyzer/_apis/build/status/chronoB.SpotifyDataAnalyzer?branchName=master"></a>
  <a href="https://results.pre-commit.ci/latest/github/chronoB/SpotifyDataAnalyzer/master"><img alt="pre-commit-ci status" src="https://results.pre-commit.ci/badge/github/chronoB/SpotifyDataAnalyzer/master.svg"></a>

</p>

<p><br /></p>

## About

This repository is build to analyze the user data spotify is collecting. The downloadable personal user data can be examined regarding different features. Right now it only analyses the streaming history of one or multiple users. Other analyses aren't planned at the moment.

## Dependencies

PYTHON >=3.7

## How to get the spotify user data

Disclaimer: Only checked for german spotify account. I don't know if it works for every account or is a country-specific features due to specific GDPR laws.

Go to : https://www.spotify.com/account/privacy/
Follow the instructions under "Deine Daten herunterladen". The process should take 1-7 days. You will be emailed if your data is ready to be downloaded.

Afterwards copy the extracted folder into this directory.

## User data structure
Detailed explanation of the data : https://support.spotify.com/de/account_payment_help/privacy/understanding-my-data/

The following structure is based on the folder i received. There could be files missing or some additional files (the website is referencing a voiceinput and a conclusions file)

./my-spotify-data
- CarThing.json // Information about a (possibly existing) CarThing-device
- FamilyPlan.json // Information about family subscription
- Follow.json // Details about followers, or accounts/artist you follow
- Payments.json // Details about your payment method (if existing)
- Playlist.json  // Information about created and saved playlist included all saved songs
- ReadMeFirst.pdf // General information about the data
- SearchQueries.json // List with information about your search queries
- StreamingHistory.json // List of Elements you listened to in the last year
- Userdata.json  // Several different userdata
- YourLibrary.json // Information about saved songs in your library


## SearchSpecifics

The SearchSpecifics design the search query. There are two main queries: specific time or time period. The keys for either of them cannot be used together (e.g. `year`and `startYear`). Additional parameters described below can be added to both of them.
### Search for a specific time (a specific day, a year, a specific hour)
```python
#search for every song that was played on the 2nd of September in 2019 between 10 and 11.
payload = {
  "year": 2019,
  "month": 9,
  "day": 2,
  "hour": 10
}
#search for every song that was played on the 2nd of a month
payload = {
  "day": 2
}

#search for every song that was played in February 2020
payload = {
  "year": 2020
  "month": 2
}
```
### Search for timeperiod (from 2019-05-03 until 2019-07-22)
IMPORTANT: If any of the following parameters is used, every of the following parameters has to be used. They come as a bundle.
```
payload = {
        "startYear": 2019,
        "startMonth": 5,
        "startDay": 3,
        "endYear": 2019,
        "endMonth": 7,
        "endDay": 22,
    }
```
### Additional search parameters
`count` specifies how many items should be returned (`default=5`). `media` determines if the search result should include/exclude podcast/music (`default=all`). The podcasts are defined in [data/podcastFile.txt](./data/podcastFile.txt). Right now it's a collection of found podcasts in the example files. Future plans involve fetching a list of podcasts from a podcatcher [(feel free to contribute)](#contribution). `ratingCrit` is used to sort items per playtime or per clicks, because spotify is saving the ms played per song click (`default=clicks`).

```
payload = {
        ...
        "count": 3, #how many items should be returned
        "media": "podcast", #"podcast", "music", "all"
        "ratingCrit": "time", #"time", "clicks"
    }
```



## Plans

- add the possibility to sort for genre. Need external lib for that. Don't know if possible
- add the spotify audio analyze api for fancy stuff
- add multiple year support (if not already happened)
- add more analyzers (searchHistory analyzer, general information analyzer). Therefor maybe restructure the code


## Contributions are welcome!
<a name="contribution"></a>
If you want to contribute to this, please read the [Contribution guidelines](CONTRIBUTING.md)
