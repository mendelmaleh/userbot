import tekore as tk

cfg = {k: input("{k}: ").strip() for k in ('client_id', 'client_secret', 'redirect_uri')}

cred = tk.RefreshingCredentials(*cfg.values())

print('Open in browser for Spotify login:')
print(cred.user_authorisation_url(tk.scope.every))

redirected = input('Please paste redirect URL: ').strip()
code = tk.parse_code_from_url(redirected)

print('\n', cred.request_user_token(code), sep='')
