ACSBridge
===========

This is a Python script written to provide a bridge between a FSM client and a CCure server. It uses a Python-standard SimpleHTTPRequestHandler to listen on a port specified by the user for HTTP GET/POST requests (coming from the FSM client), then writes the request into the specified directory as formatted CSV (to be imported by CCure). It will also watch a directory for new .log files (an indication of failure on CCure's part), and if one appears, it will send the contents of the .log file as an email to a configurable address.

Currently working:
* HTTP listening
* Logging
* CSV file writing

Still needs to be implemented:
* Log-file watching
* Emailing error reports
* Mapping between FSM field names and CCure field names
