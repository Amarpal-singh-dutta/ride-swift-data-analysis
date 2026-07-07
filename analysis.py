import trip_pb2
import pandas as pd

# Create protobuf object
trip_batch = trip_pb2.TripBatch()

# Read binary protobuf data
with open("trips.pb", "rb") as f:
    trip_batch.ParseFromString(f.read())

# Convert protobuf records into dictionaries
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


# Create DataFrame
df = pd.DataFrame(records)

# Show all columns
pd.set_option(
    "display.max_columns",
    None
)

# Convert Unix time
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    unit="s"
)


print("\n"+"="*50)
print("DATA PREVIEW")
print("="*50)

print(df.head())


print("\n"+"="*50)
print("DATASET INFORMATION")
print("="*50)

print(df.info())


print("\n"+"="*50)
print("NUMERICAL SUMMARY")
print("="*50)

print(df.describe())


print("\n"+"="*50)
print("ZERO FARE INVESTIGATION")
print("="*50)

print(
    df[df["fare"]==0]["status"]
    .value_counts()
)


print("\n"+"="*50)
print("DUPLICATE TRIP ID CHECK")
print("="*50)

print(
    "trip id duplicated:",
    df["trip_id"]
    .duplicated()
    .sum()
)


print("\n"+"="*50)
print("STATUS DISTRIBUTION")
print("="*50)

print(
    df["status"]
    .value_counts()
)


print("\n"+"="*50)
print("CANCELLED TRIP FARE ANALYSIS")
print("="*50)

print(
    df[
        df["status"]=="CANCELLED"
    ]["fare"]
    .describe()
)


print("\n"+"="*50)
print("CANCELLED TRIP FARE VALUES")
print("="*50)

print(
    df[
        df["status"]=="CANCELLED"
    ]["fare"]
    .value_counts()
    .head(20)
)


print("\n"+"="*50)
print("CANCELLED TRIP DISTANCE ANALYSIS")
print("="*50)

print(
    df[
        df["status"]=="CANCELLED"
    ]["distance_km"]
    .describe()
)


print("\n"+"="*50)
print("FARE VS DISTANCE CORRELATION")
print("="*50)

print(
    df[
        ["fare","distance_km"]
    ]
    .corr()
)


print("\n"+"="*50)
print("TOP 10 HIGHEST FARE TRIPS")
print("="*50)

print(
    df.nlargest(
        10,
        "fare"
    )[
        [
            "fare",
            "distance_km",
            "vehicle_type",
            "city",
            "status"
        ]
    ]
)


print("\n"+"="*50)
print("COMPLETED TRIP FARE ANALYSIS")
print("="*50)

print(
    df[
        df["status"]=="COMPLETED"
    ]["fare"]
    .describe()
)


print("\n"+"="*50)
print("VEHICLE TYPE AVERAGES")
print("="*50)

print(
    df.groupby(
        "vehicle_type"
    )[
        ["fare","distance_km"]
    ]
    .mean()
)


# Extract hour from timestamp
df["hour"] = df["timestamp"].dt.hour


print("\n"+"="*50)
print("HOURLY TRIP DISTRIBUTION")
print("="*50)

print(
    df["hour"]
    .value_counts()
    .sort_index()
)


print("\n"+"="*50)
print("UNIQUE HOURS PRESENT")
print("="*50)

print(
    df["timestamp"]
    .dt.hour
    .unique()
)


print("\n"+"="*50)
print("CITY DISTRIBUTION")
print("="*50)

print(
    df["city"]
    .value_counts()
)


print("\n"+"="*50)
print("CITY FARE SUMMARY")
print("="*50)

print(
    df.groupby("city")
    ["fare"]
    .agg(
        ["count","mean","median"]
    )
    .sort_values(
        "count",
        ascending=False
    )
)


print("\n"+"="*50)
print("CITY CANCELLATION RATE")
print("="*50)

print(
(
df.groupby("city")
["status"]
.apply(
lambda x:
(x=="CANCELLED").mean()*100
)
.sort_values(
ascending=False
)
)
)


print("\n"+"="*50)
print("VEHICLE TYPE STATUS BREAKDOWN")
print("="*50)

print(
pd.crosstab(
df["vehicle_type"],
df["status"],
normalize="index"
)*100
)


print("\n"+"="*50)
print("SPEARMAN CORRELATION")
print("="*50)

print(
df[
["fare","distance_km"]
]
.corr(
method="spearman"
)
)


print("\n"+"="*50)
print("TOTAL REVENUE BY CITY")
print("="*50)

print(
df.groupby(
"city"
)["fare"]
.sum()
.sort_values(
ascending=False
)
)


print("\n"+"="*50)
print("TOTAL REVENUE BY VEHICLE TYPE")
print("="*50)

print(
df.groupby(
"vehicle_type"
)["fare"]
.sum()
.sort_values(
ascending=False
)
)


print("\n"+"="*50)
print("VEHICLE TYPE DISTRIBUTION")
print("="*50)

print(
df["vehicle_type"]
.value_counts()
)


print("\n"+"="*50)
print("HOURLY CANCELLATION RATE")
print("="*50)

print(
(
df.groupby("hour")
["status"]
.apply(
lambda x:
(x=="CANCELLED").mean()*100
)
).sort_values(
ascending=False
)
)


print("\n"+"="*50)
print("HOURLY REVENUE")
print("="*50)

print(
df[
df["status"]=="COMPLETED"
]
.groupby(
"hour"
)["fare"]
.sum()
.sort_values(
ascending=False
)
)


print("\n"+"="*50)
print("What is the average trip fare and distance per city? ")
print("="*50)


avg_city = (
    df.groupby("city")
    .agg(
        avg_fare=("fare","mean"),
        avg_distance=("distance_km","mean")
    )
    .sort_values("avg_fare",ascending=False)
)

print(avg_city)

print("\n"+"="*50)
print("Which driver completes the most trips? (top 10 drivers?")
print("="*50)

top_drivers = (
    df[df["status"]=="COMPLETED"]
    .groupby("driver_id")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print(top_drivers)


print("\n"+"="*50)
print("What percentage of trips were completed vs cancelled?")
print("="*50)


trip_percent = (
    df["status"]
    .value_counts(normalize=True)
    *100
)

print(trip_percent)



print("\n"+"="*50)
print("Which hour of day has peak ride demand?")
print("="*50)

# Trips per hour
hourly_trips = (
    df.groupby("hour")
    .size()
    .sort_values(ascending=False)
)

print(hourly_trips)

# Peak hour only
peak_hour = hourly_trips.idxmax()
peak_trips = hourly_trips.max()

print(f"\nPeak ride demand hour: {peak_hour}:00")
print(f"Number of trips: {peak_trips}")



print("\n"+"="*50)
print("Flag any trips where fare per km exceeds ₹50")
print("="*50)



# Create fare per km column
df["fare_per_km"] = df["fare"] / df["distance_km"]

# Flag suspicious trips
high_fare_km = df[
    df["fare_per_km"] > 50
]

print(high_fare_km[
    ["trip_id",
     "city",
     "vehicle_type",
     "fare",
     "distance_km",
     "fare_per_km",
     "status"]
])

print("\nTotal flagged trips:",
      len(high_fare_km))




print(
(
high_fare_km["vehicle_type"]
.value_counts(normalize=True)
*100
).round(2)
)


print(
high_fare_km.groupby("vehicle_type")
["distance_km"]
.describe()[["mean","50%","min","max"]]
)