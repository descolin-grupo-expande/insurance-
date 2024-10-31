from pyfcm import FCMNotification
from app.config import config
import logging

def send_plain_notification(token, payload, message=None, title=None):
    
    """
        Method to send a notification to a token.
        @param token string the token of the device that will receive the
        notification
        @param payload dictionary the data to be sent in the notification. If
        the message or the title are not received the function will try to get
        them from the payload
        @param message string the title of the notification
        @return dictionary the dictionary of received by using the function to
        send the notification. Described on the notification:
        response_dict = {
            # List of Unique ID (number) identifying the multicast message.
            'multicast_ids': list(),
            # Number of messages that were processed without an error.
            'success': 0,
            # Number of messages that could not be processed.
            'failure': 0,
            # Number of results that contain a canonical registration token.
            'canonical_ids': 0,
            # Array of dict objects representing the status of the messages
            # processed.
            'results': list(),
            'topic_message_id': None or str
        }
    """
    try:
        push_service = FCMNotification(project_id=config.GAE_APP_ID, service_account_file='ix/config/firebase_fcm_sa.json')

        if not title:
            title = payload.get('title', 'Seguros Cloud')
        
        if not message:
            message = payload.get('message', '')

        url = payload.get('url', config.SYSTEM_URL + '/admin/management')
        icon = payload.get('icon', '/assets/images/logo.png')

        payload = {key: str(value) for key, value in payload.items()}

        result = push_service.notify(
            fcm_token=token,
            notification_title=title,
            notification_body=message,
            data_payload=payload,
            android_config={
                "priority": "normal",
                "notification": {
                    "click_action": str(url)
                }
            },
            notification_image=icon
        )
        logging.info(result)

        return result
    except Exception as e:
        print (str(e))
        logging.info("Error send plain notification")
        logging.error(str(e))
        return {}
