import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer

class PrettyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the query string of the URL
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        if 'xss' in query_components:
            encoded_data = query_components['xss'][0]  # Get the 'data' value from the query string
            print("Encoded data:", encoded_data)  # Debugging: print the encoded data
            decoded_data = urllib.parse.unquote(encoded_data)  # Decode URL-encoded data
            print("Decoded data:", decoded_data)  # Debugging: print the decoded data

            # Prettify the decoded data in a <pre> block for readable formatting
            response = f"""
            <html>
                <head><title>Pretty URL Response</title></head>
                <body>
                    <h1>Decoded Data</h1>
                    <pre>{decoded_data}</pre>
                </body>
            </html>
            """
        else:
            # Default message if 'data' is not in the query string
            response = """
            <html>
                <head><title>No 'data' Parameter</title></head>
                <body>
                    <h1>No 'data' parameter found in query string.</h1>
                </body>
            </html>
            """

        # Send the HTTP response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

# Set up the server on a specific port (e.g., 8000)
if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, PrettyHTTPRequestHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
