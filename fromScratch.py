import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import html  # For handling Unicode escape characters

# Car class to hold each car's details
class Car:
    def __init__(self, title, km, engine, gearbox, fuel, year, price):
        self.title = title
        self.km = km
        self.engine = engine
        self.price = price
        self.gearbox = gearbox
        self.fuel = fuel
        self.year = year

    # Convert Car object to dictionary so it can be easily written to JSON
    def to_dict(self):
        return {
            'title': self.title,
            'km': self.km,
            'engine': self.engine,
            'price': self.price,
            'gearbox': self.gearbox,
            'fuel': self.fuel,
            'year': self.year,
        }

# Add headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to scrape car data from a page
def scrape_cars(page_number):
    url = f'https://www.standvirtual.com/carros?page={page_number}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Request successful for page {page_number}")
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Loop through each car's section on the page
        car_sections = soup.find_all('section', class_='ooa-ljs66p en1x5vy0')  

        cars = []  # List to store car objects

        for car_section in car_sections:
            # Extract each car's details
            title = car_section.find('h2', class_='e123dwbo0 ooa-ezpr21')  
            km = car_section.find('dd', attrs={'data-parameter': 'mileage'})  
            engine = car_section.find('p', class_='e1kj25my0 ooa-nxfgg7') 
            gearbox = car_section.find('dd', attrs={'data-parameter': 'gearbox'})  
            fuel = car_section.find('dd', attrs={'data-parameter': 'fuel_type'})  
            year = car_section.find('dd', attrs={'data-parameter': 'first_registration_year'})  
            price = car_section.find('h3', class_='eg88ra81 ooa-3ewd90') 

            # Use html.unescape() to handle Unicode characters
            car = Car(
                title=html.unescape(title.text.strip()) if title else 'No Title',
                km=html.unescape(km.text.strip()) if km else 'No KM data',
                engine=html.unescape(engine.text.strip()) if engine else 'No Engine data',
                gearbox=html.unescape(gearbox.text.strip()) if gearbox else 'No gearbox',
                fuel=html.unescape(fuel.text.strip()) if fuel else 'No fuel',
                year=html.unescape(year.text.strip()) if year else 'No year',
                price=html.unescape(price.text.strip()) if price else 'No Price',
            )

            # Append the car object to the cars list
            cars.append(car)

        return cars  # Return the list of car objects
    else:
        print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
        return []

# Function to save car data to a JSON file
def save_to_json(cars, filename='cars_data.json'):
    # Convert each car object to a dictionary and save to JSON
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump([car.to_dict() for car in cars], json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

# Loop through pages and scrape car data
page_number = 1  # Start with page 1
all_cars = []  # List to store all cars data from multiple pages

while True:
    cars = scrape_cars(page_number)
    if not cars:  # If no cars were found, stop scraping
        break
    all_cars.extend(cars)  # Add the cars from the current page to the list
    if page_number <= 2:
        page_number += 1  # Move to the next page
    else: break
# Save all cars to a JSON file with dynamic filename including current date
current_date = datetime.now().strftime('%Y-%m-%d')
filename = f'cars_data_{current_date}.json'

# Save the collected car data
save_to_json(all_cars, filename)
