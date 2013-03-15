The scripts in this directory are to asssit in loading data from the google_transit format into this program

Please put your routes.txt, stops.txt, stop_times.txt, and trips.txt files into the transit_data directory

Once you have done that you can run the create_db script (once you django db has been initialized and populated with the models), this
will add all of the data into the applications database and allow you to view your data online, and use the apis provided
