import requests
import slack


def create_slack_channel(company_name):
    # Initialize the Slack client using your API token
    client = slack.WebClient(token='T066NRAU00H')
    
    # Create the Slack channel
    response = client.conversations_create(name=company_name)
    
    # Retrieve the channel name
    channel_name = response['channel']['name']
    
    return channel_name

def send_slack_notification(channel, message, is_update=False):
    slack_token = "xoxb-6226860952017-6200046803719-zuoRCmZqvNJSBl1dU4v56Ymp"  # Replace with your Slack API token
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": channel,
        "text": message
    }
    if is_update:
        payload["text"] = f"[Update] {message}"
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()