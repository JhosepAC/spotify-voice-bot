from spotify.device import validate_active_device

device = validate_active_device()

print("Dispositivo activo:")
print(device["name"])