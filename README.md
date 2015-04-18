ACSBridge
===========

This is a Python script that uses a python SimpleHTTPRequestHandler to listen on a port specified by the user for HTTP GET/POST requests, then writes the request into the specified directory as formatted CSV. It will also watch a directory for new .log files (an indication of failure on CCure's part), and if one appears, it will send it as an email to a configurable address.

Currently working:
* HTTP listening
* Logging
* CSV file writing

Still needs to be implemented:
* Log-file watching
* Emailing error reports
* Mapping between FSM field names and CCure field names
