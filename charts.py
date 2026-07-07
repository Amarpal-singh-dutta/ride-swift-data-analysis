import trip_pb2
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# LOAD PROTOBUF DATA
# ==================================================

# Create protobuf object
trip_batch = trip_pb2.TripBatch()

# Read binary protobuf data
with open("trips.pb", "rb") as f:
    trip_batch.ParseFromString(f.read())

# ==================================================
# CONVERT PROTOBUF RECORDS TO DICTIONARIES
# ==================================================

records = []

for trip in trip_batch.trips:

    records.append({

        "trip_id": trip.trip_id,

        "driver_id": trip.driver_id,

        "rider_id": trip.rider_id,

        "city": trip.city,

        "vehicle_type":
        trip_pb2.VehicleType.Name(
            trip.vehicle_type
        ),

        "fare": trip.fare,

        "distance_km": trip.distance_km,

        "timestamp": trip.timestamp,

        "status":
        trip_pb2.TripStatus.Name(
            trip.status
        )
    })

# ==================================================
# CREATE DATAFRAME
# ==================================================

df = pd.DataFrame(records)

# Show all columns
pd.set_option(
    "display.max_columns",
    None
)

# ==================================================
# DATASET OVERVIEW
# ==================================================

print("\n" + "="*50)
print("DATASET OVERVIEW")
print("="*50)

print(df.head())

print("\n" + "="*50)
print("DATASET INFORMATION")
print("="*50)

print(df.info())

print("\n" + "="*50)
print("SUMMARY STATISTICS")
print("="*50)

print(df.describe())

# ==================================================
# MISSING VALUE ANALYSIS
# ==================================================

print("\n" + "="*50)
print("MISSING VALUE ANALYSIS")
print("="*50)

print(df.isnull().sum())

# ==================================================
# DUPLICATE ANALYSIS
# ==================================================

print("\n" + "="*50)
print("DUPLICATE ANALYSIS")
print("="*50)

print("Duplicate Trip IDs:",
      df["trip_id"].duplicated().sum())

print("Duplicate Rows:",
      df.duplicated().sum())

# ==================================================
# FEATURE ENGINEERING
# ==================================================

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    unit="s"
)

# Extract hour from timestamp
df["hour"] = df["timestamp"].dt.hour

# Create fare per km column
df["fare_per_km"] = (
    df["fare"] /
    df["distance_km"]
)

print("\n" + "="*50)
print("FEATURE ENGINEERING")
print("="*50)

print(df[[
    "timestamp",
    "hour",
    "fare",
    "distance_km",
    "fare_per_km"
]].head())

# ==================================================
# TRIP STATUS DISTRIBUTION
# ==================================================

print("\n" + "="*50)
print("TRIP STATUS DISTRIBUTION")
print("="*50)

status_percent = (
    df["status"]
    .value_counts(normalize=True)
    *100
)

print(status_percent)

# ==================================================
# FARE-DISTANCE CORRELATION
# ==================================================

print("\n" + "="*50)
print("FARE-DISTANCE CORRELATION")
print("="*50)

print(
    df[["fare", "distance_km"]]
    .corr()
)

# ==================================================
# TOP 10 HIGHEST FARE RIDES
# ==================================================

print("\n" + "="*50)
print("TOP 10 HIGHEST FARE RIDES")
print("="*50)

print(
    df.nlargest(10, "fare")[[
        "fare",
        "distance_km",
        "vehicle_type",
        "city",
        "status"
    ]]
)

# ==================================================
# CHARTS / VISUALIZATIONS
# ==================================================

# --------------------------------------------------
# 1. Trip Status Distribution
# --------------------------------------------------

df["status"].value_counts().plot(
    kind="bar",
    figsize=(6,4),
    title="Trip Status Distribution"
)

plt.ylabel("Number of Trips")
plt.xticks(rotation=0)

plt.savefig(
    "trip_status_distribution.png",
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 2. Trips by Hour
# --------------------------------------------------

df["hour"].value_counts().sort_index().plot(
    kind="bar",
    figsize=(10,4),
    title="Trips by Hour"
)

plt.ylabel("Number of Trips")

plt.savefig(
    "trips_by_hour.png",
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 3. Revenue by City
# --------------------------------------------------

df.groupby("city")["fare"].sum().sort_values().plot(
    kind="barh",
    figsize=(8,5),
    title="Revenue by City"
)

plt.xlabel("Total Revenue")

plt.savefig(
    "revenue_by_city.png",
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 4. Revenue by Vehicle Type
# --------------------------------------------------

df.groupby("vehicle_type")["fare"].sum().sort_values().plot(
    kind="bar",
    figsize=(6,4),
    title="Revenue by Vehicle Type"
)

plt.ylabel("Revenue")
plt.xticks(rotation=0)

plt.savefig(
    "revenue_by_vehicle.png",
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 5. Fare vs Distance Scatter Plot
# --------------------------------------------------

df.plot.scatter(
    x="distance_km",
    y="fare",
    figsize=(7,5),
    title="Fare vs Distance"
)

plt.savefig(
    "fare_vs_distance.png",
    bbox_inches="tight"
)

plt.close()