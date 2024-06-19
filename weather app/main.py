from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import requests
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

# Function to resize image
def resize_image(image_path, width, height):
    try:
        image = Image.open(image_path)
        resized_image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error resizing image {image_path}: {e}")
        return None

def getweather():
    city = text_field.get()
    if not city:
        messagebox.showerror("Error", "City field cannot be empty")
        return

    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        if location is None:
            messagebox.showerror("Error", "City not found")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Weather API
        api_key = "8fda3e32e0f425c4fdf0073e0c5b885d"
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(api_url)
        json_data = response.json()

        if response.status_code == 200:
            condition = json_data['weather'][0]['main']
            description = json_data["weather"][0]["description"]
            temp = int(json_data['main']['temp'] - 273.15)  # Convert from Kelvin to Celsius
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']

            t.config(text=f"{temp}°C")
            c.config(text=f"{condition} | FEELS LIKE {temp}°C")
            w.config(text=f"{wind} m/s")
            h.config(text=f"{humidity} %")
            d.config(text=f"{description}")
            p.config(text=f"{pressure} hPa")
        else:
            messagebox.showerror("Error", f"Failed to get weather data: {json_data['message']}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather data: {e}")

# Define the path to your image and desired dimensions
image_path = "C:/Users/SMITH/Desktop/gitpython/pythonbegineersclassactivity/smith/weather app/assets/searchbar.png"
image_path1 = "C:/Users/SMITH/Desktop/gitpython/pythonbegineersclassactivity/smith/weather app/assets/search.png"
image_path2 = "C:/Users/SMITH/Desktop/gitpython/pythonbegineersclassactivity/smith/weather app/assets/cloud.png"
image_path3 = "C:/Users/SMITH/Desktop/gitpython/pythonbegineersclassactivity/smith/weather app/assets/box.png"
new_width = 350
new_height = 50
new_width1 = 34
new_height1 = 34
new_width2 = 200
new_height2 = 200
new_width3 = 800
new_height3 = 140

# Resize the images
resized_image = resize_image(image_path, new_width, new_height)
resized_image1 = resize_image(image_path1, new_width1, new_height1)
resized_image2 = resize_image(image_path2, new_width2, new_height2)
resized_image3 = resize_image(image_path3, new_width3, new_height3)

# Check if images were resized correctly
if not all([resized_image, resized_image1, resized_image2, resized_image3]):
    print("One or more images failed to resize")
else:
    # Create a label widget to display the image
    myimage = Label(root, image=resized_image)
    myimage.place(x=20, y=20)

    # Create the text field
    text_field = Entry(root, justify="center", width=15, font=("poppins", 25, "bold"), bg="honeydew", border=0, fg="black")
    text_field.place(x=39, y=28)
    text_field.focus()

    # Create the search button
    search_icon = Button(root, image=resized_image1, bg="dodger blue", command=getweather)
    search_icon.place(x=320, y=27)

    # Create the logo
    icon_image = Label(root, image=resized_image2)
    icon_image.place(x=250, y=80)

    # Create the bottom box
    frame_image = Label(root, image=resized_image3, bg="honeydew")
    frame_image.pack(padx=5, pady=5, side=BOTTOM)

    # Time and weather labels
    name = Label(root, font=("arial", 15, "bold"))
    name.place(x=30, y=100)
    clock = Label(root, font=("Helvetica", 20))
    clock.place(x=30, y=130)

    # Additional labels
    label1 = Label(root, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="royal blue")
    label1.place(x=90, y=360)

    label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="royal blue")
    label2.place(x=230, y=360)

    label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="royal blue")
    label3.place(x=420, y=360)

    label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="royal blue")
    label4.place(x=650, y=360)

    t = Label(root, font=("arial", 70, "bold"), fg="#ee666d")
    t.place(x=500, y=90)
    c = Label(root, font=("arial", 15, "bold"))
    c.place(x=500, y=200)

    w = Label(root, text="...", font=("arial", 20, "bold"), bg="royal blue")
    w.place(x=90, y=400)
    h = Label(root, text="...", font=("arial", 20, "bold"), bg="royal blue")
    h.place(x=230, y=400)
    d = Label(root, text="...", font=("arial", 20, "bold"), bg="royal blue")
    d.place(x=420, y=400)
    p = Label(root, text="...", font=("arial", 20, "bold"), bg="royal blue")
    p.place(x=650, y=400)

root.mainloop()
