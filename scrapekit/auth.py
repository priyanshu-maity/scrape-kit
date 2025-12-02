from datetime import datetime
import time

import imaplib
import email
from bs4 import BeautifulSoup


def get_magic_link(
        creds: dict[str, str],
        sender_email: str,
        link_text: str,
        request_time: datetime = datetime.now(),
        timeout: int = 15,
        check_interval: int = 0.5
) -> str | None:
    """
    Retrieves a magic link from the user's email inbox based on specified criteria.

    Args:
        creds (dict[str, str]): A dictionary containing the user's email credentials.
                                Example: {'email': 'user@gmail.com', 'password': 'aaaa bbbb cccc ddddd'}
        sender_email (str): The email address of the sender expected to send the magic link.
        link_text (str): The text of the hyperlink to identify the magic link in the email body.
        request_time (datetime): The minimum datetime to consider emails as valid.
                                 Defaults to the current datetime.
        timeout (int): The maximum time (in seconds) to wait for the email. Defaults to 15 seconds.
        check_interval (int): The interval (in seconds) between checks for new emails. Defaults to 0.5 seconds.

    Returns:
        str | None: The magic link if found within the timeout period, or None if not found.
    """
    start_time = datetime.now()

    while (datetime.now() - start_time).total_seconds() < timeout:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(creds['email'], creds['password'])
        mail.select('inbox')

        # Search for emails from sender_email
        status, messages = mail.search(None, f'FROM "{sender_email}"')
        if status != 'OK':
            time.sleep(check_interval)  # Wait before checking again
            continue

        # Get the latest email
        email_ids = messages[0].split()
        if not email_ids:
            time.sleep(check_interval)  # No email found, wait and retry
            continue

        latest_email_id = email_ids[-1]

        # Fetch the email content
        status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Fetch the last email date
        datetime_header = msg['Date']
        parsed_datetime = email.utils.parsedate_to_datetime(datetime_header)
        inbox_time = convert_utc_to_local(parsed_datetime).replace(tzinfo=None)

        # Check if the email is recent
        if inbox_time >= request_time:
            # Extract the magic link
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    soup = BeautifulSoup(part.get_payload(decode=True), 'html.parser')
                    link = soup.find('a', string=link_text)
                    if link:
                        return link['href']

        # Wait before the next check
        time.sleep(check_interval)

    # Timeout reached, return None
    return None


# if __name__ == '__main__':
#     import json
#
#     get_magic_link(
#         creds=json.load(open("creds.json")),
#         sender_email="noreply@medium.com",
#         link_text="Sign in to Medium"
#     )
