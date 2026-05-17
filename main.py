from spotify.auth import get_spotify_client

sp = get_spotify_client()

current_user = sp.current_user()

print("Usuario autenticado:")
print(current_user["display_name"])