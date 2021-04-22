from entries.request import update_entry
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from entries import get_all_entries, get_single_entry, get_entries_by_word, create_entry
from moods import get_all_moods
from instructors import get_all_instructors
from tags import get_all_tags, get_all_entry_tags

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
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)
                    
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = get_single_entry(id)
                else:
                    response = get_all_entries()
            elif resource == "moods":
                response = get_all_moods()
            elif resource == "instructors":
                response = get_all_instructors()
            elif resource == "tags":
                response = get_all_tags()
            elif resource == "entrytags":
                response = get_all_entry_tags()

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "entries" and resource == "customers":
                response = f"{get_customers_by_email(value)}"
            if key == "location_id":
                if resource == "animals":
                    response = f"{get_animals_by_location(value)}"
                elif resource == "employees":
                    response = f"{get_employees_by_location(value)}"
            if key == "status" and resource == "animals":
                response = f"{get_animals_by_status(value)}"

        self.wfile.write(response.encode())
    
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, value) = self.parse_url(self.path)

        # response = {}

        if resource == "entries":
            update_entry(value, post_body)

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, value) = self.parse_url(self.path)

        response = {}

        if resource == "entries":
            response = create_entry(post_body)
        
        return self.wfile.write(response.encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()