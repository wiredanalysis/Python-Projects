import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt

# URL of the weather page
url = "https://weather.com/weather/monthly/l/10001:4:US"

# Send a request to the page
response = requests.get(url)

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the weather data
table = soup.find("table", class_="twc-table")

# Create a CSV file to store the weather data
with open("weather.csv", mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Date", "High Temperature (F)", "Low Temperature (F)", "Precipitation (in)"])

    # Iterate through each row of the table and extract the weather data
    for row in table.find_all("tr")[1:]:
        # Get the date
        date = row.find("td", class_="twc-sticky-col").text.strip()

        # Get the high temperature
        temp = row.find_all("td", class_="temp")[0].text.split("/")
        high_temp = temp[0].strip()

        # Get the low temperature
        low_temp = temp[1].strip()

        # Get the precipitation
        precipitation = row.find("td", class_="precip").text.strip()

        # Write the data to the CSV file
        writer.writerow([date, high_temp, low_temp, precipitation])

# Read the data from the CSV file
dates = []
high_temps = []
low_temps = []
precipitations = []
with open("weather.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader) # Skip the header row
    for row in reader:
        dates.append(row[0])
        high_temps.append(int(row[1]))
        low_temps.append(int(row[2]))
        precipitations.append(float(row[3]))

# Plot the high and low temperatures as a line chart
plt.plot(dates, high_temps, label="High Temperature")
plt.plot(dates, low_temps, label="Low Temperature")
plt.xlabel("Date")
plt.ylabel("Temperature (F)")
plt.title("New York Weather (Last 30 Days)")
plt.legend()
plt.show()

# Plot the precipitation as a bar chart
plt.bar(dates, precipitations)
plt.xlabel("Date")
plt.ylabel("Precipitation (in)")
plt.title("New York Weather (Last 30 Days)")
plt.show()
