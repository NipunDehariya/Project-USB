import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from geopy.geocoders import Nominatim

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/location':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            latitude = data['latitude']
            longitude = data['longitude']

            # Initialize Nominatim geocoder
            geolocator = Nominatim(user_agent="GetLoc")

            # Get address using geopy
            location = geolocator.reverse(f"{latitude}, {longitude}")

            # Create response
            response = {
                "address": location.address,
                "latitude": latitude,
                "longitude": longitude
            }

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

# if __name__ == '__main__':
#     run()