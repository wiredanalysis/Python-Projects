import requests
from bs4 import BeautifulSoup
import csv

# Make a request to the IMDb top 250 page
url = "https://www.imdb.com/chart/top/"
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the table that contains the movie data
table = soup.find("tbody", {"class": "lister-list"})

# Open a CSV file to write the data
with open("imdb_top_250.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(["Movie Name", "Year", "Rating", "Runtime", "Genre"])

    # Iterate through each row of the table and extract the movie data
    for row in table.find_all("tr"):
        # Get the movie name
        name = row.find("td", {"class": "titleColumn"}).find("a").text

        # Get the year of release
        year = row.find("span", {"class": "secondaryInfo"}).text.strip("()")

        # Get the movie rating
        rating = row.find("td", {"class": "ratingColumn"}).find("strong").text

        # Get the movie runtime if available, otherwise set runtime to "N/A"
        runtime_element = row.find("span", {"class": "runtime"})
        runtime = runtime_element.text.strip() if runtime_element is not None else "N/A"

        # Get the movie genre if available, otherwise set genre to "N/A"
        genre_element = row.find("span", {"class": "genre"})
        genre = genre_element.text.strip() if genre_element is not None else "N/A"

        # Write the data to the CSV file
        writer.writerow([name, year, rating, runtime, genre])

 
   

