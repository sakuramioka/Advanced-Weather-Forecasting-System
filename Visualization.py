from bokeh.plotting import figure, show, curdoc
from bokeh.models import DatetimeTickFormatter, HoverTool
from datetime import datetime
import pandas as pd
import GeocodingAPI
import ForecastAPI

current_search_results = GeocodingAPI.get_geo_data("New York", 1)
city = GeocodingAPI.get_city_search_results()[0]
latitude = GeocodingAPI.get_latitude()
longitude = GeocodingAPI.get_longitude()

data = ForecastAPI.get_forecast(latitude,longitude,'temperature_2m','auto')

curdoc().theme = 'dark_minimal'

# Extract timestamps and temperatures
timestamps = data['hourly']['time']
temperatures = data['hourly']['temperature_2m']

# Convert timestamps to datetime objects
timestamps = [datetime.fromisoformat(timestamp) for timestamp in timestamps]

# Create a pandas DataFrame
df = pd.DataFrame({'timestamps': timestamps, 'temperatures': temperatures})

# Output to an HTML file (optional)
# output_file("temperature_plot.html")

# Create a Bokeh figure
p = figure(
    x_axis_type="datetime",
    title=f"Temperature data for {city}, Timezone: {data['timezone_abbreviation']} - {data['timezone']}, Generation Time: {data['generationtime_ms']}",
    x_axis_label="Date",
    y_axis_label="Temperature (°C)",
    width=1495,
    height=715,
)

# Plot the temperature data as a line
p.line(df['timestamps'], df['temperatures'], legend_label="Temperature (°C)", line_width=2, color='skyblue', line_join='round')


# Format the x-axis labels
p.xaxis.formatter = DatetimeTickFormatter(hours="%H:%M")

hover = HoverTool()
hover.tooltips = [("Date", "@x{%Y-%m-%d}"),("Time", "@x{%H:%M}"),("Temperature", "@y{0.0} °C")]
hover.formatters = {'@x': 'datetime'}
hover.mode = 'vline'
p.add_tools(hover)

# Show the plot in full screen
show(p, full_screen=True)





