import tekore as tk

cfg = {'client_id': '', 'client_secret': '', 'redirect_uri': ''}

for k in cfg:
    cfg[k] = input(f'Input {k}: ').strip()

cred = tk.RefreshingCredentials(cfg['client_id'], cfg['client_secret'], cfg['redirect_uri'])

print('Open in browser for Spotify login:')
print(cred.user_authorisation_url(tk.scope.every))

redirected = input('Please paste redirect URL: ').strip()
code = tk.parse_code_from_url(redirected)

print('\n', cred.request_user_token(code), sep='')
