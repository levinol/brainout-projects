settings = {
    'bot': 'Brain/out bot',
    'id': 2546,
    'profile_id': 848518443926028288,
    'prefix': '/',
    'submit_channel': 404334763957288970,
    'submit_final_channel': 404334846026973194,
    'suggest_channel': 821103535982379028,
    'suggest_server_channel': 829067982239039554,
    'online_channel': 906470596085432341
}

update_url = r'https://game-vgold.brainout.org/status'

roles = {
    "helper": 298060949053767701,
    "moderator": 287659705860358144,
    "admin": 285497610100277258,
    "designers": 906472351368105984,
    "dev": 285496926470668288
}

dumb_emoji_dict = {'dev': '👨‍💻Dev', 'designers':'👨‍🎨Designer', 'admin': '🛌Admin', 'moderator': '👨‍⚖️Mod', 'helper': '🦸‍♂️Helper' }

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
     {'inline': False, 'name': 'For suggestion commands usage', 'value': 'Please select `\'Suggestion\' commands`'},
     {'inline': False, 'name': 'If you do not know where to get the message_id', 'value': 'Please select `How to get message_id`'}],
      'color': 4521728, 'type': 'rich',
      'description': 'The bot is designed to create and manage game suggestions/submissions', 
      'title': 'Help page'}

help_embed_slash_disabled = {'fields': 
    [{'inline': False, 'name': 'Usage:\n', 'value': 'If you see this help page, then you have disabled slash commands. To use commands, enable them in the settings.'}],
      'color': 4521728, 'type': 'rich',
      'description': 'The bot is designed to create and manage game suggestions/submissions', 
      'title': 'Help page'}

message_id_embed = {'fields': 
    [{'inline': False, 'name': 'Usage:\n', 'value': 'To get an ID of message, copy its number from the embed footer'}],
      'color': 10158985, 'type': 'rich',
      'description': 'The bot is designed to create and manage game suggestions/submissions', 
      'title': 'Help page'}
