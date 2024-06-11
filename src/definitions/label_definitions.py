# Define what labels can be set to set service based email settings.
email_labels = [
    {
        "label": "autoscale.additional_email_recipients_important_msgs",
        "value_type": "email_list",
        "required": False
    },
    {
        "label": "autoscale.additional_email_recipients_information_msgs",
        "value_type": "email_list",
        "required": False
    },
    {
        "label": "autoscale.additional_email_recipients_verbose_msgs",
        "value_type": "email_list",
        "required": False
    }
]

# Define what labels can be set to set service based telegram settings.
telegram_labels = [
    {
        "label": "autoscale.additional_telegram_recipients_important_msgs",
        "value_type": "telegram_chat_id_list",
        "required": False
    },
    {
        "label": "autoscale.additional_telegram_recipients_information_msgs",
        "value_type": "telegram_chat_id_list",
        "required": False
    },
    {
        "label": "autoscale.additional_telegram_recipients_verbose_msgs",
        "value_type": "telegram_chat_id_list",
        "required": False
    }
]
