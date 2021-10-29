settings = {
    'bot': 'Brain/out bot',
    'id': 2546,
    'prefix': '/',
    'submit_desc_channel': 873835758098718800,
    'submit_channel': 873835757926756381,
    'submit_final_channel': 873835757926756380,
    'suggest_desc_channel': 873900855676526643,
    'suggest_channel': 873835758098718802,
    'suggest_server_channel': 873835758098718803,
    'online_channel': 893602540481044570 
}

update_url = r'link'

roles = {
    "helper": 873835757276655679,
    "moderator": 873835757276655680,
    "admin": 873835757276655681,
    "designers": 878059187479908402,
    "dev": 873835757276655682
}

submission_embed = {'fields': 
    [{'inline': False, 'name': 'Usage:\n/submission main [artwork name] [description] [mandatory attachment]', 'value': 'Make a submission.'},
        {'inline': False, 'name': '/submission add [message id] [message] [mandatory attachment]', 'value': 'Add an attachment to a submission.'},
        {'inline': False, 'name': '/submission addition [message id] [message]', 'value': 'Add an addition to a submission.'},
        {'inline': False, 'name': '/submission clear [message id]', 'value': 'Clear all optional description fields.'},
        {'inline': False, 'name': '/submission remove [message id]', 'value': 'Remove a submission.'}],
    'color': 10158985, 'type': 'rich', 
    'description': "Make submission.\n**Communicate with the bot using `ONLY` slash commands**",
    'title': "Help page for 'Submission' commands"}

suggestion_embed = {'fields': 
    [{'inline': False, 'name': 'Usage:\n/suggestion main|server [suggestion topic] [description] [optional attachment]', 'value': 'Make a suggestion.'},
        {'inline': False, 'name': '/suggestion add [message id] [message] [mandatory attachment]', 'value': 'Add an attachment to a suggestion.'},
        {'inline': False, 'name': '/suggestion addition [message id] [message]', 'value': 'Add an addition to a suggestion.'},
        {'inline': False, 'name': '/suggestion clear [message id]', 'value': 'Clear all optional description fields.'},
        {'inline': False, 'name': '/suggestion remove [message id]', 'value': 'Remove a suggestion.'}],
    'color': 10158985, 'type': 'rich', 
    'description': "Make suggestion.\n**Communicate with the bot using `ONLY` slash commands**",
    'title': "Help page for 'Suggestion' commands"}

help_embed = {'fields': 
    [{'inline': False, 'name': 'Usage:\nFor submission commands usage', 'value': 'Please select `\'Submission\' commands`'},
     {'inline': True, 'name': 'For suggestion commands usage', 'value': 'Please select `\'Suggestion\' commands`'}],
      'color': 4521728, 'type': 'rich',
      'description': 'The bot is designed to create and manage game suggestions/submissions', 
      'title': 'Help page'}

help_embed_slash_disabled = {'fields': 
    [{'inline': False, 'name': 'Usage:\n', 'value': 'If you see this help page, then you have disabled slash commands. To use commands, enable them in the settings.'}],
      'color': 4521728, 'type': 'rich',
      'description': 'The bot is designed to create and manage game suggestions/submissions', 
      'title': 'Help page'}
