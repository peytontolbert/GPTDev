{ 
    "title": "Basic Web Server",
    "description": "A simple web server implemented in Python.",
    "code": {
        "*_python": {
            "# Import required libraries\n"
            : "import http.server",
            "\n# Define the port number for the web server\n"
            : "PORT = 8000,\n"
            ,
            "# Initialize the web server class\n"
            : "with http.server.HTTPServer(('localhost', PORT), \n"
            ,
            ": "    : "http.server.SimpleHTTPRequestHandler) as server:\n",
            "\n# Run the web server in an infinite loop\n"
            : "server.serve_forever()"
        }
    }
}

 

 
 

 


 