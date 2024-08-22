from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from geopy.geocoders import Nominatim

class RequestHandler(BaseHTTPRequestHandler):
    location_data = None

    def do_POST(self):
        if self.path == '/location':
            print("POST request received")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            latitude = data['latitude']
            longitude = data['longitude']

            # Initialize Nominatim geocoder
            geolocator = Nominatim(user_agent="GetLoc")

            # Get address using geopy
            location = geolocator.reverse(f"{latitude}, {longitude}")
            print("Location object created:", location)

            if location:
                print("Location address:", location.address)

            # Create response
            response = {
                "address": location.address if location else "Address not found",
                "latitude": latitude,
                "longitude": longitude
            }

            # Store location data
            RequestHandler.location_data = response

            # Print the address to the console
            print(response['address'])

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/location':
            if RequestHandler.location_data:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(RequestHandler.location_data).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Add CORS header
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No location data available"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

# if __name__ == '__main__':
#     run()