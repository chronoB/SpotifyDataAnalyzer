<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg" width="200" style="margin-right: 50px">


</div>

<h2 align="center">Spotify User Data Analyzer</h2>

<p align="center">
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href="https://github.com/chronoB/SpotifyDataAnalyzer/issues"><img alt="Open Issues" src="https://img.shields.io/github/issues/chronoB/SpotifyDataAnalyzer"></a>
  <a href="https://github.com/chronoB/SpotifyDataAnalyzer/releases"><img alt="Release" src="https://img.shields.io/github/release/chronoB/SpotifyDataAnalyzer"></a>
  <a href="https://dev.azure.com/chronoB/SpotifyDataAnalyzer/_build/latest?definitionId=1&branchName=master"><img alt="Azure Pipelines status" src="https://dev.azure.com/chronoB/SpotifyDataAnalyzer/_apis/build/status/vigonotion.pygti?branchName=master"></a>

</p>

<p><br /></p>

## About

This repository is build to analyze the user data spotify is collecting. The downloadable personal user data can be examined regarding different features. Right now it only analyses the streaming history of one or multiple users. Other analyses aren't planned at the moment.

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


## Progress

- [] 1. init //fills the dictionary with the items of the specified files
- [] 2. getPopularArtist //returns a list of popular artists based on search specifics
- [] 3. getPopularItem //returns a list of popular items based on search specifics
- [] 4. getNumberOfItems //returns a list with number of items per period based on search specifics
- [] 5. getNumberOfItemsPerDaytime //returns the number of items per daytime  
- [] 6. getNumberOfItemsPerYear //returns the number of items per year
- [] 7. getNumberOfItemsPerMonth //returns the number of items per month
- [] 8. getNumberOfItemsPerDay //returns the number of items per day
- [] 9. getGeneralInformation // Returns general Information (Name of User, number of played songs overall, Period of the recorded data,...)


## Contributions are welcome!

If you want to contribute to this, please read the [Contribution guidelines](CONTRIBUTING.md)