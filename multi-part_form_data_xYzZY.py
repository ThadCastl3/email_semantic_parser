import base64
import email
import re
from email.policy import default
from thefuzz import fuzz


def lambda_handler(event, context):
    if event.get('isBase64Encoded', False):
        # print("Event body is base64 encoded.")
        captured_parts = parse_email(event)
        classify_email(captured_parts)
        # print("Email parsed and classified.")
        # print(captured_parts)
        return captured_parts


# Decode the base64-encoded email body
def parse_email(event):
    body_bytes = base64.b64decode(event['body'])

    # Ensure the boundary is properly specified to match the data
    boundary = 'xYzZY'

    # Use email package to parse the multipart data from bytes
    msg = email.message_from_bytes(
        b'Content-Type: multipart/form-data; boundary="' + boundary.encode() + b'"\n\n' + body_bytes,
        policy=default)

    # dictionary to store the parts
    captured_parts = {}

    # Iterate through the parts
    for part in msg.iter_parts():
        # get the name of the parameter from the content-disposition header
        part_name = part.get_param('name', header='Content-Disposition')

        if part_name in ['from', 'subject', 'text']:
            charset = part.get_content_charset('utf-8')
            part_content = part.get_payload(decode=True).decode(charset)

            if part_name == 'text':
                print("Processing text part")

                # extract shipment details
                details_pattern = r"\*\s+(.*?):\s+(.*)"
                matches = re.findall(details_pattern, part_content)
                shipment_details = {match[0]: match[1].strip() for match in matches}
                # print(shipment_details)

                # update captured_parts with shipment details
                captured_parts.update(shipment_details)

                # print("now we split the text at 'From:'")
                text_content = part_content.split("\nFrom:", 1)[0].strip()
                # clean new lines and line breaks from text and replace with spaces
                cleaned_text = text_content.replace('\n', ' ').replace('\r', ' ')
                captured_parts['text'] = cleaned_text

                # print(text_content)

            # store the part content in the dictionary
            else:
                captured_parts[part_name] = part_content

    return captured_parts


def classify_email(captured_parts):
    # categories for classification
    categories = {'Confirmed': ['yes', 'yeah', 'we can', 'fine', 'have capacity', 'can do that', 'can cover that', 'pick up', 'can cover', 'can take'],
                  'Negotiated': ['do you have', 'could you', 'how much', 'how many']}
    response_text = captured_parts.get('text', '').lower()
    print(response_text)
    classified_category = set()

    for category, keywords in categories.items():
        for keyword in keywords:
            sim_score = fuzz.partial_ratio(keyword, response_text)
            if sim_score > 80:
                classified_category.add(category)
    if 'Negotiated' in classified_category:
        # flag for negotiation
        print("Email classified as Negotiated")
        captured_parts['classification'] = 'Negotiated'

    elif 'Confirmed' in classified_category:
        # flag for confirmation
        print("Email classified as Confirmed")
        captured_parts['classification'] = 'Confirmed'

    else:
        # flag for unknown
        print("Email classified as Unknown")
        captured_parts['classification'] = 'Unknown'

    print(captured_parts)
    return captured_parts

#lambda_handler(event, context)
