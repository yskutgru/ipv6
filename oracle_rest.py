import json
import logging
from typing import Optional, Dict, Any

import requests


def send_to(data: list, url: str, auth: Optional[tuple] = None, timeout: int = 10, verify: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Send data to a REST service and return parsed JSON.

    Args:
        data: List of dictionaries to send.
        url: Service URL.
        auth: Tuple (user, pass) for HTTP Basic Auth.
        timeout: Request timeout in seconds.
        verify: Path to CA file or False to disable SSL verification (not recommended).

    Returns:
        Parsed JSON as dict or None on error/empty response.
    """
    headers = {"Content-Type": "application/json; charset=utf-8"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth, timeout=timeout, verify=verify)
        response.raise_for_status()

        if response.text and response.text.strip():
            try:
                return response.json()
            except json.JSONDecodeError:
                logging.exception("JSON parse error. Response body: %s", response.text[:1000])
                return None
        else:
            logging.info("Server returned empty response (status=%s)", response.status_code)
            return None

    except requests.exceptions.RequestException:
        logging.exception("Request error when sending to %s", url)
        return None


if __name__ == "__main__":
    # Simple usage example
    service_url = "https://mis.gte.local/ords/mis/inv/mail/"
    json_data = [{"FILENAME": "DC-VS-01", "EMAIL": "test@example.local", "SUBJECT": "Test"}]

    result = send_to(data=json_data, url=service_url, timeout=15)
    if result:
        print("Data sent successfully! Server response:", result)
    else:
        print("Failed to send data or server did not return JSON.")
