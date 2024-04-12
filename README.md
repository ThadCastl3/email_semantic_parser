# README for `multi-part_form_data_xYzZY.py`

This Python script is designed to handle multipart form data, specifically in the context of email content. It includes functionality to parse and classify email content based on certain criteria.

## Functions

The script contains the following functions:

- `lambda_handler(event, context)`: This is the main function that is triggered when the script is run. It checks if the event body is base64 encoded, and if so, it parses and classifies the email content.

- `parse_email(event)`: This function decodes the base64-encoded email body and parses the multipart data using the email package. It iterates through the parts of the email, capturing and storing relevant parts in a dictionary.

- `classify_email(captured_parts)`: This function classifies the email content based on predefined categories. It uses the `fuzz` library to calculate similarity scores between the email content and the keywords associated with each category. The email is then classified into the category with the highest similarity score.

## Usage

This script is designed to be used as a Lambda function in AWS, but it can also be run locally for testing purposes. To run the script, you need to pass an event object to the `lambda_handler` function. The event object should contain a 'body' key with a base64-encoded string representing the email content.

## Dependencies

This script requires the following Python packages:

- `base64`
- `email`
- `re`
- `thefuzz`

Please ensure these dependencies are installed before running the script.
