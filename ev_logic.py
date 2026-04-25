import pandas as pd

df = pd.read_csv("C:\EV_Project\last_ev_dataset_realistic.csv")

def best_station():
    best = df.sort_values(by="Score", ascending=False).iloc[0]
    return f"✅ Best station: {best['Station_Name']} | Wait: {best['Waiting_Time']} mins | Distance: {best['Distance_km']} km"

def nearest_low_queue():
    filtered = df[df['Queue_Length'] <= 2]
    if len(filtered) == 0:
        return "⚠️ No low queue stations available"
    best = filtered.sort_values(by="Distance_km").iloc[0]
    return f"📍 Nearest low queue station: {best['Station_Name']} | Queue: {best['Queue_Length']}"

def peak_hour():
    peak = df['Hour'].value_counts().idxmax()
    return f"⏰ Peak demand hour: {peak}:00"
def low_demand_hour():
    hourly_counts = df['Hour'].value_counts().sort_index()
    low_hour = hourly_counts.idxmin()
    return f"🌙 Best time to charge (lowest demand): {low_hour}:00"
def lowest_queue_station():
    min_queue = df['Queue_Length'].min()
    stations = df[df['Queue_Length'] == min_queue]['Station_Name'].unique()

    station_list = ", ".join(stations)
    return f"🟢 Stations with lowest queue ({min_queue}): {station_list}"
def station_feedback(station_name):
    station = df[df['Station_Name'].str.lower() == station_name.lower()]

    if station.empty:
        return "❌ Station not found"

    avg_rating = station['Rating'].mean()
    avg_queue = station['Queue_Length'].mean()
    avg_wait = station['Waiting_Time'].mean()

    return f"""
📍 Station: {station_name}
⭐ Rating: {round(avg_rating,2)}
⏳ Avg Waiting Time: {round(avg_wait,2)} mins
🚗 Avg Queue Length: {round(avg_queue,2)}
"""