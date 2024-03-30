import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib
import warnings

warnings.filterwarnings("ignore", message="X does not have valid feature names")


# Load the trained Random Forest model
random_forest_models = joblib.load(r'C:\Users\harsh\OneDrive\Desktop\MGIT Hackathon\random_forest_model.pkl')

# Dictionary mapping countries to integers
country_mapping = {
    'Angola': 0, 'Argentina': 1, 'Australia': 2, 'Bangladesh': 3, 'Brazil': 4,
    'Burkina Faso': 5, 'Burundi': 6, 'Cameroon': 7, 'Canada': 8, 'Central African Republic': 9,
    'Chile': 10, 'Colombia': 11, 'Dominican Republic': 12, 'Ecuador': 13, 'Egypt': 14,
    'El Salvador': 15, 'Germany': 16, 'Ghana': 17, 'Greece': 18, 'Guatemala': 19,
    'Guinea': 20, 'Haiti': 21, 'Honduras': 22, 'India': 23, 'Indonesia': 24, 'Iraq': 25,
    'Italy': 26, 'Jamaica': 27, 'Japan': 28, 'Kazakhstan': 29, 'Kenya': 30, 'Madagascar': 31,
    'Malawi': 32, 'Mali': 33, 'Mauritania': 34, 'Mexico': 35, 'Morocco': 36, 'Mozambique': 37,
    'Nicaragua': 38, 'Niger': 39, 'Pakistan': 40, 'Papua New Guinea': 41, 'Peru': 42, 'Rwanda': 43,
    'Saudi Arabia': 44, 'South Africa': 45, 'Spain': 46, 'Sri Lanka': 47, 'Thailand': 48, 'Turkey': 49,
    'Uganda': 50, 'United Kingdom': 51, 'Uruguay': 52, 'Zambia': 53, 'Zimbabwe': 54
}

# Dictionary mapping crop items to integers
crop_mapping = {
    'Cassava': 0, 'Maize': 1, 'Potatoes': 2, 'Rice, paddy': 3, 'Sweet potatoes': 4,
    'Wheat': 5, 'Sorghum': 6, 'Soybeans': 7, 'Yams': 8, 'Plantains and others': 9
}

import requests

def get_weather_data(city_name, api_key):
    # API request URL
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

    try:
        # Send GET request to the API
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # Extract temperature and rainfall data from the response
            temperature = data['main']['temp']
            rainfall = data['rain']['1h'] if 'rain' in data and '1h' in data['rain'] else 0
            return temperature, rainfall
        else:
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None

# Example usage:
# api_key = 'YOUR_API_KEY'
# city_name = 'Hyderabad'
# temperature, rainfall = get_weather_data(city_name, api_key)
# if temperature is not None and rainfall is not None:
#     print("Temperature:", temperature)
#     print("Rainfall:", rainfall)
# else:
#     print("Failed to retrieve weather data.")




# Example usage:
city_name = 'Bengaluru'  # Example city name
fah, rainfall = get_weather_data(city_name, api_key='93d41c53f17b178cedb49d07ed543ce2')
temperature = (fah-32)*5/9
if temperature is not None and rainfall is not None:
    print(f"Average Temperature: {temperature}°C")
    print(f"Average Rainfall: {rainfall} mm")
else:
    print("Failed to retrieve weather data.")


def predict_yield(country, crop, year, rainfall, pesticides, temperature):
    # Map country and crop to integers
    country_encoded = country_mapping.get(country, -1)
    crop_encoded = crop_mapping.get(crop, -1)

    # Check if country or crop is not found
    if country_encoded == -1 or crop_encoded == -1:
        return 'Invalid country or crop'

    # Perform prediction
    prediction = random_forest_models.predict([[country_encoded, crop_encoded, year, rainfall, pesticides, temperature]])
    return round(prediction[0],2)

def on_predict():
    try:
        country = country_var.get()
        crop = crop_var.get()
        year = float(year_entry.get())
        #rainfall = float(rainfall_entry.get())
        pesticides = float(pesticides_entry.get())
        #temperature = float(temperature_entry.get())
        # area = float(area_entry.get())

        predicted_yield = predict_yield(country, crop, year, rainfall, pesticides, temperature)
        output_label.config(text=f'Predicted Yield: {predicted_yield}')
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Tkinter GUI setup
root = tk.Tk()
root.title('Crop Yield Prediction')


# Set window size
root.geometry('400x350')



# Country Selection
country_label = tk.Label(root, text="Country:")
country_label.grid(row=0, column=0, padx=5, pady=5)
country_var = tk.StringVar(value="India")  # Set default value to "India"
country_dropdown = tk.OptionMenu(root, country_var, *country_mapping.keys())
country_dropdown.grid(row=0, column=1, padx=5, pady=5)

# Year Input
year_label = tk.Label(root, text="Year:")
year_label.grid(row=2, column=0, padx=5, pady=5)
year_entry = tk.Entry(root)
year_entry.insert(0, "2024")  # Set default value to "2024"
year_entry.grid(row=2, column=1, padx=5, pady=5)

# Crop Selection
crop_label = tk.Label(root, text="Crop:")
crop_label.grid(row=1, column=0, padx=5, pady=5)
crop_var = tk.StringVar()
crop_dropdown = tk.OptionMenu(root, crop_var, *crop_mapping.keys())
crop_dropdown.grid(row=1, column=1, padx=5, pady=5)


# # Rainfall Input
# rainfall_label = tk.Label(root, text="Average Rainfall (mm_per_year):")
# rainfall_label.grid(row=3, column=0, padx=5, pady=5)
# rainfall_entry = tk.Entry(root)
# rainfall_entry.grid(row=3, column=1, padx=5, pady=5)

# Pesticides Input
pesticides_label = tk.Label(root, text="Pesticides (Tonnes):")
pesticides_label.grid(row=4, column=0, padx=5, pady=5)
pesticides_entry = tk.Entry(root)
pesticides_entry.grid(row=4, column=1, padx=5, pady=5)

# Temperature Input
# temperature_label = tk.Label(root, text="Average Temperature (°C):")
# temperature_label.grid(row=5, column=0, padx=5, pady=5)
# temperature_entry = tk.Entry(root)
# temperature_entry.grid(row=5, column=1, padx=5, pady=5)


# # Area Input
# area_label = tk.Label(root, text="Area (Ha):")
# area_label.grid(row=6, column=0, padx=5, pady=5)
# area_entry = tk.Entry(root)
# area_entry.grid(row=6, column=1, padx=5, pady=5)

# Predict Button
predict_button = tk.Button(root, text="Predict", command=on_predict)
predict_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Output Label
output_label = tk.Label(root, text="")
output_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
