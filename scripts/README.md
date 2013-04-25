The scripts in this directory are to asssit in loading data from the google_transit format into this program

Please put your calendar.txt, routes.txt, stops.txt, stop_times.txt, and trips.txt files into the transit_data directory

Once you have done that you can run the create_db script (once you django db has been initialized and populated with the models), this will add all of the data into the applications database and allow you to view your data online, and use the apis provided

This may take a long time to run depending on how big your transit files are, the current scripts split the stop_times.txt file into the folder transit_data/split_times/ in order to load properly (large files can cause db/memory issues depending on the db/how much memory you are using)
