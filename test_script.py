import yaml
import json

with open('./ressources/map/items.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data["2"])


print(json.dumps(data, indent=1))  # pretty-print JSON with indents

