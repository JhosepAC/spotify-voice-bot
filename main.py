from commands.parser import parse_command
from commands.router import route_command

text = "pon blinding lights"

parsed = parse_command(text)

response = route_command(
    parsed["intent"],
    parsed["entities"]
)

print(response)