import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import GeocodingAPI
import ForecastAPI

# Create the main window
root = tk.Tk()
root.title("City Name Entry")
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

def display_results(latitude, longitude):
    info_text = canvas.create_text(root.winfo_screenwidth()/2, root.winfo_screenheight()/2, anchor=tk.N, text="Please wait... fetching information!",
                                   font=('Century Gothic', '20', 'bold'), fill='white', tags='info_text')
    data = ForecastAPI.get_forecast(latitude,longitude,'temperature_2m','auto')

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
        
    result_data = GeocodingAPI.get_geo_data(keywd, 6)

    if selected_index !=  None:
        latitude = GeocodingAPI.get_latitude(selected_index)
        longitude = GeocodingAPI.get_longitude(selected_index)
        display_results(latitude, longitude)
        selected_index = None
        return None
    
    list_items = GeocodingAPI.get_city_search_results()
    var = tk.Variable(value=list_items)
    result_list = tk.Listbox(canvas, listvariable=var, justify='center', font=('Century Gothic', '15'), selectbackground='#87ceeb', selectforeground='#000000', highlightthickness=0)
    result_list.place(x=(root.winfo_screenwidth() - 600) // 2 - 30, y=360, width=600, height=len(list_items*24))
    result_list.bind("<<ListboxSelect>>", callback)
    canvas.create_text((root.winfo_screenwidth())// 2 - 30, 365+len(list_items*24), font=('Century Gothic', '15', 'bold'), text=f"Your query produced {len(list_items)} results!", anchor=tk.NE
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
entry.place(x=(root.winfo_screenwidth() - 600) // 2 - 30, y=300, width=600, height=60)
search_button = tk.Button(canvas, text="🔎", width=4, height=1, font=('Century Gothic', 20), relief='flat', command=search_results)
search_button.place(x=(root.winfo_screenwidth() - 600) // 2 + 570, y=300, width=60, height=60)

# Bind the click event to clear the default text
entry.bind("<Button-1>", clear_default_text)

# Start the tkinter main loop
root.mainloop()
