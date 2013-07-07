Robodomo
========

Robodomo is a server that collects stats. It's designed to be super flexible.

Servers are registered through a JSON post with Name, Type and any Tags to /api/servers. The response contains the server id, date created and what ever data was submitted.

Stats are sent as JSON to /api/servers/{{ server_id }}. Stats can be anything in the format of a name and integer value (ex: {"cpu":30})

At least.. that's how I think this will all work out.

Things that have been done
--------------------------
* Registering servers and stats works
* The response for a server contains a nicely formatted list of stats organized by type and then with date and value pairs
* Basic data validation/error handling
* Basic front end using Flot for charts

Things that need to be done
---------------------------

* More error handling and data validation on the API
* Authentication of some sort
* Filtering and searching using the API (ex Tags, Date ranges, etc)
* Make frontend prettier
