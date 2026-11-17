# python record_ids.py Name=id Name=id ...  -> merges into published_ids.json
import json, sys, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "published_ids.json")
d = json.load(open(p)); d.update(dict(a.split("=") for a in sys.argv[1:])); json.dump(d, open(p, "w"), indent=1); print(len(d))
