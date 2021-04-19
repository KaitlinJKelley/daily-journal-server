from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from entries import get_all_entries, get_single_entry, get_entries_by_word
from moods import get_all_moods

class HandleRequests(BaseHTTPRequestHandler):
    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()
    
    def parse_url(self, path):
       
        path_params = path.split("/")
        resource = path_params[1] #entries?q=html
        key = None
        
        value = None

        # Try to get the item at index 2
        try:
          
            value = int(path_params[2])
            return (resource, value)  # This is a tuple
        except IndexError:
            # pass  # No route parameter exists
            if "?" in path:
                if path_params[1] != "":
                    key = resource.split("?q=")[0]
                    value = resource.split("?q=")[1]
                    return (key, value)
        except ValueError:
            # Request had trailing slash: /entries/ OR something was passed that can't be converted to an integer
            pass
        return (resource, value)
                    
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, value) = self.parse_url(self.path)

        if resource == "entries":
            if type(value) == int:
                response = f"{get_single_entry(value)}"
            elif type(value) == str:
                response = get_entries_by_word(value)

            else:
                response = f"{get_all_entries()}"
        if resource == "moods":
            response = get_all_moods()

        self.wfile.write(response.encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()