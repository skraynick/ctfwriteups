import glob
import os

import pandas as pd
import folium

"""
this was for a ctf challenge. Gave you RSSI data and you had to map it to find the starting/end points.
Was quite a challenge, and as you can see, not easy... but maybe there was a more manual way of doing it. 
With python it provided a more elegant solution and didn't disappoint. For me it was coming up with a solution to
solve the problem logically was probably the hardest. Then putting that into code was a whole other cup of tea.. 
"""


def load_rssi_data(folder_path: str) -> pd.DataFrame:
    files = glob.glob(os.path.join(folder_path, "rx_*.txt"))
    dfs = []

    for file in files:
        receiver_id = os.path.splitext(os.path.basename(file))[0] 
        df = pd.read_csv(file, header=None, names=['timestamp', 'rssi'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['receiver_id'] = receiver_id
        dfs.append(df)

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame(columns=['timestamp', 'rssi', 'receiver_id'])


def load_rssi_with_positions(rssi_folder: str, positions_csv: str) -> pd.DataFrame:
    positions_df = pd.read_csv(positions_csv, encoding="utf-8-sig")
    positions_df['receiver_id'] = positions_df['id'].apply(lambda x: f"rx_{int(x):03d}")

    files = glob.glob(os.path.join(rssi_folder, "rx_*.txt")) + glob.glob(os.path.join(rssi_folder, "rx_*.TXT"))
    if not files:
        print("No RSSI files found in folder:", rssi_folder)
        return pd.DataFrame(columns=['timestamp', 'rssi', 'receiver_id', 'lat', 'lon'])

    dfs = []
    for file in files:
        receiver_id = os.path.splitext(os.path.basename(file))[0]
        df = pd.read_csv(file, header=0, names=['timestamp', 'rssi'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['receiver_id'] = receiver_id
        dfs.append(df)

    rssi_df = pd.concat(dfs, ignore_index=True)

    combined_df = rssi_df.merge(
        positions_df[['receiver_id', 'lat', 'lon']],
        on='receiver_id',
        how='left'
    )

    print(f"Processed {len(files)} RSSI files, total rows: {len(rssi_df)}")
    combined_df.to_csv("combined_rssi.csv", index=False)


def plot_rssi_map(combined_df: pd.DataFrame, output_file: str = "rssi_map.html"):
    if combined_df.empty:
        print("No data to plot")
        return

    map_center = [combined_df['lat'].mean(), combined_df['lon'].mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    rssi_min = combined_df['rssi'].min()
    rssi_max = combined_df['rssi'].max()

    def rssi_to_color(rssi):
        norm = (rssi - rssi_min) / (rssi_max - rssi_min) if rssi_max != rssi_min else 0
        r = int(255 * (1 - norm))
        g = int(255 * norm)
        return f'#{r:02x}{g:02x}00'

    for _, row in combined_df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=6,
            color=rssi_to_color(row['rssi']),
            fill=True,
            fill_opacity=0.7,
            popup=f"Receiver: {row['receiver_id']}<br>RSSI: {row['rssi']:.2f}"
        ).add_to(m)

    m.save(output_file)
    print(f"Map saved to {output_file}")


def plot_travel_path_with_start_finish(csv_file, map_file="travel_path.html"):
    # Read CSV
    df = pd.read_csv(csv_file, header=0)
    df.columns = df.columns.str.strip().str.lower()
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    if df.empty:
        print("No data to plot.")
        return None

    strongest_df = df.loc[df.groupby('timestamp')['rssi'].idxmax()].sort_values('timestamp')

    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=13)

    points = strongest_df[['lat', 'lon']].values.tolist()
    folium.PolyLine(points, color='blue', weight=3, opacity=0.7).add_to(m)

    for idx, row in strongest_df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=4,
            color='gray',
            fill=True,
            fill_opacity=0.5,
            popup=f"{row['receiver_id']}<br>{row['timestamp']}"
        ).add_to(m)

    start = strongest_df.iloc[0]
    folium.Marker(
        location=[start['lat'], start['lon']],
        popup=f"Start: {start['receiver_id']}<br>{start['timestamp']}",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)

    finish = strongest_df.iloc[-1]
    folium.Marker(
        location=[finish['lat'], finish['lon']],
        popup=f"Finish: {finish['receiver_id']}<br>{finish['timestamp']}",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)

    m.save(map_file)
    print(f"Travel path map with start/finish saved to {map_file}")
    return m


def read_combined_csv(csv_file):
    df = pd.read_csv(csv_file, header=0)
    df.columns = df.columns.str.strip().str.lower()
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    return df


if __name__ == "__main__":

    load_rssi_with_positions("rssi", "receivers.csv")

    plot_df = pd.read_csv("combined_rssi.csv")
    plot_df['timestamp'] = pd.to_datetime(plot_df['timestamp'])
    agg_df = plot_df.groupby(['receiver_id', 'lat', 'lon'], as_index=False)['rssi'].mean()

    combined_csv = "combined_rssi.csv"
    map_obj = plot_travel_path_with_start_finish(combined_csv, map_file="path_map.html")
