This is a Django project for the Spring 2013 CENG/ELEC/SENG 499 Project group Smart Bus Systems.

The goal is to have a system that is able to keep track of bus schedules, and coordinate this information with real time bus location data.  The bus location data is provided through a text communication system in which Busses send their latitude and longitude locations to a number that is designated to be the server this application is running on.

The system will then update the location of the bus according to its coordinates and for the route with which that number is associated.  The server will also update the appropriate bus stops with the location of the bus so that they can update their displays.

We have support for Twilio (http://www.twilio.com) text messaging, in order for users to get next stop times by the stop_id, as well as update bus locations via text message in case GPRS data is not working from your module.

DISCLAIMERS:

Before using the transit data included in this repo, please review the terms and conditions here: http://www.bctransit.com/data/terms.cfm

Route and arrival data used in this product or service is provided by permission of BC Transit. BC Transit assumes no responsibility for the accuracy or currency of the Data used in this product or service.

As this is a school project, we provide no warranty on its use.
