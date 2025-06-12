import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the data (if not already)
df = pd.read_excel("Road Accident Data.xlsx", sheet_name="Data")

# Drop rows with missing lat/lon
df_geo = df.dropna(subset=["Longitude", "Latitude"])

# Group by location and count
top_hotspots = df_geo.groupby(["Longitude", "Latitude"]).size().reset_index(name='Accident_Count')

# Top 100
top_100 = top_hotspots.sort_values(by='Accident_Count', ascending=False).head(100)

# Plot using Plotly
fig = px.scatter_mapbox(
    top_100,
    lat="Latitude",
    lon="Longitude",
    size="Accident_Count",
    color="Accident_Count",
    color_continuous_scale="Plasma",
    size_max=15,
    zoom=8,
    mapbox_style="carto-positron",
    title="Top 100 Accident Hotspots"
)
fig.show()
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
df = pd.read_excel("Road Accident Data.xlsx")

# Clean column names (remove spaces)
df.columns = df.columns.str.strip()

# Display all column names to confirm what they are
print("Column names:", df.columns)

# Use the correct column name for date (update this if different)
# Example: Replace 'Accident Date' with your actual column name from print output
df['Date'] = pd.to_datetime(df['Accident Date'])

# Extract month-year
df['Month'] = df['Date'].dt.to_period("M")

# Group by month and severity
monthly_trend = df.groupby(['Month', 'Accident_Severity']).size().reset_index(name="Count")

# Pivot the table for plotting
pivot_trend = monthly_trend.pivot(index='Month', columns='Accident_Severity', values='Count').fillna(0)

# Plot
pivot_trend.plot(figsize=(12, 6), linewidth=2, title='Monthly Accident Severity Trend')
plt.xlabel("Month")
plt.ylabel("Number of Accidents")
plt.grid(True)
plt.tight_layout()
plt.show()
# Load the data
df = pd.read_excel("Road Accident Data.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# OPTIONAL: print column names to choose what to pivot
print("Columns available:", df.columns)

# Check for NaN or blanks
print(df[['Weather_Conditions', 'Road_Type']].isna().sum())

# Create a pivot table for the heatmap (change columns based on your data)
heatmap_data = pd.crosstab(df['Weather_Conditions'], df['Road_Type'])

# Check if data is empty
if heatmap_data.empty:
    print("❌ Error: Heatmap data is empty. Check your column names or data.")
else:
    # Plot the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap="YlOrRd", annot=True, fmt="d", linewidths=0.5)
    plt.title("Accidents by Weather Conditions and Road Type")
    plt.tight_layout()
    plt.show()