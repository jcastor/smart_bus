python gtfs_routes.py transit_data/routes.txt
python gtfs_stops.py transit_data/stops.txt
python gtfs_trips.py transit_data/trips.txt
split -l 100000 transit_data/stop_times.txt transit_data/split_times/x
for file in transit_data/split_times/*; do python gtfs_stop_times.py "$file"; done
