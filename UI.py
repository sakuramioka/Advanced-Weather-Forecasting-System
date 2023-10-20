import tkinter as tk
from tkinter import PhotoImage, LabelFrame
from PIL import Image, ImageTk
import time
import GeocodingAPI
import ForecastAPI
import Visualization

y_alignment = 60

wmo_codes = {
  # Index : [Name, type]
    0:['Clear sky', 'clear'],
    1:['Mainly clear', 'clear'],
    2:['Partly cloudy', 'cloudy'],
    3:['Overcast', 'overcast'],
    45:['Fog', 'fog'],
    48:['Rime fog', 'rime_fog'],
    51:['Light drizzle','drizzle'],
    53:['Moderate drizzle', 'drizzle'],
    55:['Dense drizzle', 'drizzle'],
    56:['Light, freezing drizzle', 'freezing_drizzle'],
    57:['Dense, freezing drizzle', 'freezing_drizzle'],
    61:['Slight rain', 'rain'],
    63:['Moderate rain', 'rain'],
    65:['Heavy rain', 'rain'],
    66:['Freezing light rain', 'freezing_rain'],
    67:['Freezing heavy rain', 'freezing_rain'],
    71:['Slight snow fall', 'snow'],
    73:['Moderate snow fall', 'snow'],
    75:['Heavy snow fall', 'snow'],
    77:['Snow grains', 'snow'],
    80:['Slight rain showers', 'rain'],
    81:['Moderate rain showers', 'rain'],
    82:['Violent rain showers', 'rain'],
    85:['Slight snow showers', 'snow'],
    86:['Heavy snow showers', 'snow'],
    95:['Thunderstorm', 'thunder'],
    96:['Slight hailstorm', 'hail'],
    99:['Heavy hailstorm', 'hail']
}

# Create the main window
root = tk.Tk()
root.title("Weather Forecasting Application")
root.geometry("1920x1080")
root.attributes('-fullscreen', True)

# Load and resize the background image to fit the window
background_image = Image.open("images//bg.jpg")  # Replace with your image path
background_image = background_image.resize((1920, 1080), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas for the background image
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack()

# Set the background image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

def try_destroying(element):
    try:
        element.destroy()
    except Exception:
        pass

images = []
weathe
def display_results(latitude, longitude):
    global images
    images.clear()
    canvas.delete('info_text')
    canvas.delete('existing')
    data = ForecastAPI.get_forecast(latitude,longitude,'temperature_2m','weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max','auto')
    x0, y0 = 17, root.winfo_screenheight()/2 - 50
    x1, y1 = 217, root.winfo_screenheight() - 37
    padx = 17
    days = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
    current_day_index =days.index(str(time.strftime('%A')).upper())
    canvas.create_text(root.winfo_screenwidth()//2, 330, text=f"{str(data['latitude'])[:5]}°N {str(data['longitude'])[:5]}°E, {data['elevation']}m above sea level",
                       font=('Dubai', '18', 'bold'), fill='grey20', tags='info_text')
    canvas.create_text(root.winfo_screenwidth()//2, 355, text=f"Generated in {str(data['generationtime_ms'])[:5]}ms, time in {data['timezone_abbreviation']} [{data['timezone']}]",
                       font=('Dubai', '14'), fill='grey20', tags='info_text')
    for i in range(1,8):
        if current_day_index >= 7:
            current_day_index = current_day_index - 7
        canvas.create_rectangle(x0,y0,x1,y1,fill='white',outline='white', tags='existing')
        canvas.create_rectangle(x0,y0,x1,y0+50, fill='pink', outline='pink', tags='existing')
        canvas.create_rectangle(x1,y1,x0,y1-35, fill='skyblue', outline='skyblue', tags='existing')
        canvas.create_text((x1+x0)/2, (root.winfo_screenheight()//2 - 45), text=days[current_day_index], anchor=tk.N, justify='center',
                           font=('Dubai', '20', 'bold'), fill='white', tags='existing')
        if i == 1:
            canvas.create_text((x1+x0)/2, (root.winfo_screenheight() - 50 - 20), text='TODAY', anchor=tk.N, justify='center',
                           font=('Dubai', '15', 'bold'), fill='white', tags='existing')
        else:
            date = data['daily']['time'][i-1]
            canvas.create_text((x1+x0)/2, (root.winfo_screenheight() - 50 - 20), text=date, anchor=tk.N, justify='center',
                           font=('Dubai', '15', 'bold'), fill='white', tags='existing')
            
        weathercode = data['daily']['weathercode'][i-1]
        icon = Image.open(f"images\\icons\\{wmo_codes[weathercode][1]}.png")
        icon = icon.resize((160,160), Image.Resampling.LANCZOS)
        icon = ImageTk.PhotoImage(icon)
        images.append(icon)
        canvas.create_image(x0+20, y0+60, image=icon, anchor = tk.NW)

        canvas.create_text((x1+x0)/2, y0+240, text=wmo_codes[weathercode][0], anchor=tk.N, justify='center',
                           font=('Dubai', '15'), fill='black', tags='existing')
        canvas.create_text((x1+x0)/2 - 25, y0+280, text="""MAX TEMP:
MIN TEMP:
SUNRISE:
SUNSET:
CHANCE OF RAIN:""", 
                        anchor=tk.N, justify='left', font=('Dubai', '11', 'bold'), fill='grey', tags='existing')
        canvas.create_text((x1+x0)/2 + 65, y0+280, 
text=f"""{data['daily']['temperature_2m_max'][i-1]}°C
{data['daily']['temperature_2m_min'][i-1]}°C
{data['daily']['sunrise'][i-1][-5:]}
{data['daily']['sunset'][i-1][-5:]}
{data['daily']['precipitation_probability_max'][i-1]}%""", 
                        anchor=tk.N, justify='right', font=('Dubai', '11', 'bold'), fill='black', tags='existing')
        
        graph_button = tk.Button(canvas, text="Display temperature graph", width=4, height=1, font=('Dubai', '14'), relief='flat', command=Visualization.display_graph(data))
        graph_button.place(x=(root.winfo_screenwidth() - 300)// 2, y= root.winfo_screenheight() - 30, width=300, height=23)
        x0 = x0 + 200 + padx
        x1 = x1 + 200 + padx
        current_day_index = current_day_index+1
        
result_list = None
result_data = None
selected_index = None

def callback(event):
    global selected_index
    curtext = entry.get()
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        entry.delete(0, tk.END)
        entry.insert(0, data)
        selected_index = index
    else:
        entry.delete(0, tk.END)
        entry.insert(0, curtext)


def search_results():

    global result_list
    global result_data
    global selected_index

    keywd = entry.get()  
    try:
        canvas.delete('info_text')
        result_list.destroy()
    except Exception:
        pass  

    if selected_index !=  None:
        canvas.create_text(root.winfo_screenwidth()/2, root.winfo_screenheight()/2, anchor=tk.N, text="Please wait... fetching information!",
                                   font=('Century Gothic', '20', 'bold'), fill='white', tags='info_text')
        latitude = GeocodingAPI.get_latitude(selected_index)
        longitude = GeocodingAPI.get_longitude(selected_index)
        display_results(latitude, longitude)
        selected_index = None
        return None
    
    result_data = GeocodingAPI.get_geo_data(keywd, 6)
    list_items = GeocodingAPI.get_city_search_results()
    var = tk.Variable(value=list_items)
    result_list = tk.Listbox(canvas, listvariable=var, justify='center', font=('Century Gothic', '15'), selectbackground='#87ceeb', selectforeground='#000000', highlightthickness=0)
    result_list.place(x=(root.winfo_screenwidth() - 600) // 2 - 30, y=360 - y_alignment, width=600, height=len(list_items*24))
    result_list.bind("<<ListboxSelect>>", callback)
    canvas.create_text((root.winfo_screenwidth())// 2 - 30, 365+len(list_items*24) - y_alignment, font=('Century Gothic', '15', 'bold'), text=f"Your query produced {len(list_items)} results!", anchor=tk.NE
                       ,tags='info_text')

# Function to clear the default text when clicked
def clear_default_text(event):
    if entry.get() == "Enter a city name":
        entry.delete(0, tk.END)

x_spacing = 70
y_spacing = 5
frame_width = root.winfo_screenwidth()
frame_height = root.winfo_screenheight()
canvas_width = 5 * (frame_width + x_spacing) + x_spacing
canvas_height = 2 * (frame_height + y_spacing) + y_spacing
canvas_x = (root.winfo_screenwidth() - canvas_width) // 2
canvas_y = (root.winfo_screenheight() - canvas_height) // 2
canvas.configure(width=canvas_width, height=canvas_height)
canvas.pack_propagate(0)

# Top image
top_image_width = 1000
top_image_height = 200
top_image_path = "images\\logo.png"
top_image = Image.open(top_image_path)
top_image = top_image.resize((1000, 200), Image.Resampling.LANCZOS)
top_image = ImageTk.PhotoImage(top_image)
canvas.create_image((root.winfo_screenwidth() - top_image_width) // 2, y_spacing+30, image=top_image, anchor=tk.NW)

entry = tk.Entry(canvas, width=40, font=('Century Gothic', 20), relief='flat', justify='center')
entry.insert(0, "Enter a city name")
entry.place(x=(root.winfo_screenwidth() - 600) // 2 - 30, y=300 - y_alignment, width=600, height=60)
search_button = tk.Button(canvas, text="🔎", width=4, height=1, font=('Century Gothic', 20), relief='flat', command=search_results)
search_button.place(x=(root.winfo_screenwidth() - 600) // 2 + 570, y=300 - y_alignment, width=60, height=60)

# Bind the click event to clear the default text
entry.bind("<Button-1>", clear_default_text)

# Start the tkinter main loop
root.mainloop()
