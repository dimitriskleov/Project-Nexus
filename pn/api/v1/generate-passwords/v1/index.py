import random
import string
import json
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import httpagentparser
import base64

# Password Generation Function
def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Custom HTTP Request Handler
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Parse query parameters
            parsed_path = parse.urlparse(self.path)
            query_params = parse.parse_qs(parsed_path.query)

            # Extract 'length' and 'num' from query parameters (defaults if not provided)
            length = int(query_params.get('length', [12])[0])  # Default to 12 characters
            num_passwords = int(query_params.get('num', [1])[0])  # Default to 1 password

            # Validate the parameters
            if length <= 0 or num_passwords <= 0:
                self.send_error(400, "Invalid parameters! 'length' and 'num' must be positive integers.")
                return

            # Generate passwords
            passwords = [generate_random_password(length) for _ in range(num_passwords)]

            # Prepare the response data
            response_data = {
                'passwords': passwords
            }

            # Set response headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Write the JSON response
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Internal server error: {e}")
            print(f"Error: {e}")
            traceback.print_exc()

    def log_message(self, format, *args):
        # Log request details (for debugging purposes)
        user_agent = self.headers.get('User-Agent')
        print(f"Request from User-Agent: {user_agent}")
        super().log_message(format, *args)

# Start the server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
