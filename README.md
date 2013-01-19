This is a Django project for the Spring 2013 CENG/ELEC/SENG 499 Project group Smart Bus Systems.

The goal is to have a system that is able to keep track of bus schedules, and coordinate this information with real time bus location data.  The bus location data is provided through a text communication system in which Busses send their latitude and longitude locations to a number that is designated to be the server this application is running on.

The system will then update the location of the bus according to its coordinates and for the route with which that number is associated.  The server will also update the appropriate bus stops with the location of the bus so that they can update their displays.
