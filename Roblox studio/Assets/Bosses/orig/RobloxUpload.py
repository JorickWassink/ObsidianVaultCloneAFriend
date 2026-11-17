
# RobloxUpload: uploads the boss animations to Roblox through Open Cloud.
# 1. Studio dumps ReplicatedStorage.FightAnimations (sequences with PublishedId == "") as JSON
#    to http://127.0.0.1:35000/kfs_dump.json (the POST server started below).
# 2. build_rbxmx() writes export\anim_rbxmx\<name>.rbxmx, upload_all() uploads every one that is not
#    in export\published_ids.json yet (delete an entry there to upload a changed clip again).
# 3. Studio reads published_ids.json from http://127.0.0.1:34999 and fills in the PublishedId attributes.
# API key: Documents\CloneAFriendBosses\roblox_api_key.txt (Assets read + write). Creator: user 342830428.
import bpy, os, json, uuid, time, threading, urllib.request
from xml.sax.saxutils import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
ROOT = r"C:\Users\wassi\Documents\CloneAFriendBosses"
EXP = os.path.join(ROOT, "export"); OUT = os.path.join(EXP, "anim_rbxmx"); IDS = os.path.join(EXP, "published_ids.json")
USER_ID = "342830428"

def start_post_server():
    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0)); data = self.rfile.read(n)
            open(os.path.join(EXP, os.path.basename(self.path.strip("/")) or "post.json"), "wb").write(data)
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
        def log_message(self, *a): pass
    old = bpy.app.driver_namespace.get("postserver")
    if old:
        try: old.shutdown(); old.server_close()
        except Exception: pass
    srv = ThreadingHTTPServer(("127.0.0.1", 35000), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    bpy.app.driver_namespace["postserver"] = srv

def build_rbxmx():
    os.makedirs(OUT, exist_ok=True)
    data = json.load(open(os.path.join(EXP, "kfs_dump.json")))
    ref = [0]
    def r(): ref[0] += 1; return "RBX%d" % ref[0]
    f = lambda x: repr(float(x))
    names = ["X","Y","Z","R00","R01","R02","R10","R11","R12","R20","R21","R22"]
    def pose(p):
        cf = "".join(f"<{n}>{f(v)}</{n}>" for n, v in zip(names, p["c"]))
        return (f'<Item class="Pose" referent="{r()}"><Properties><string name="Name">{escape(p["n"])}</string>'
                f'<CoordinateFrame name="CFrame">{cf}</CoordinateFrame><token name="EasingStyle">{p["es"]}</token>'
                f'<token name="EasingDirection">{p["ed"]}</token><float name="Weight">{f(p["w"])}</float></Properties>'
                + "".join(pose(k) for k in p["k"]) + "</Item>")
    for k in data:
        ref[0] = 0; keys = ""
        for kf in k["keys"]:
            marks = "".join(f'<Item class="KeyframeMarker" referent="{r()}"><Properties><string name="Name">{escape(m[0])}</string><string name="Value">{escape(m[1])}</string></Properties></Item>' for m in kf["m"])
            keys += (f'<Item class="Keyframe" referent="{r()}"><Properties><string name="Name">{escape(kf["name"])}</string><float name="Time">{f(kf["t"])}</float></Properties>'
                     + "".join(pose(p) for p in kf["p"]) + marks + "</Item>")
        xml = ('<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">'
               f'<Item class="KeyframeSequence" referent="{r()}"><Properties><string name="Name">{escape(k["name"])}</string><bool name="Loop">{"true" if k["loop"] else "false"}</bool>'
               f'<token name="Priority">{k["pri"]}</token></Properties>{keys}</Item></roblox>')
        open(os.path.join(OUT, k["name"] + ".rbxmx"), "w", encoding="utf-8").write(xml)
    return len(data)

def _key(): return open(os.path.join(ROOT, "roblox_api_key.txt")).read().strip()

def upload(path, name):
    b = uuid.uuid4().hex
    req = json.dumps({"assetType": "Animation", "displayName": name, "description": "Clone a Friend boss animation " + name,
                      "creationContext": {"creator": {"userId": USER_ID}}})
    body = (f'--{b}\r\nContent-Disposition: form-data; name="request"\r\n\r\n{req}\r\n'
            f'--{b}\r\nContent-Disposition: form-data; name="fileContent"; filename="{os.path.basename(path)}"\r\nContent-Type: model/x-rbxm\r\n\r\n').encode() \
           + open(path, "rb").read() + f'\r\n--{b}--\r\n'.encode()
    rq = urllib.request.Request("https://apis.roblox.com/assets/v1/assets", data=body, method="POST",
                                headers={"x-api-key": _key(), "Content-Type": "multipart/form-data; boundary=" + b})
    try: return json.loads(urllib.request.urlopen(rq, timeout=60).read())
    except urllib.error.HTTPError as e: return {"error": e.code, "body": e.read().decode()[:500]}

def poll(op):
    for _ in range(30):
        d = json.loads(urllib.request.urlopen(urllib.request.Request("https://apis.roblox.com/assets/v1/" + op, headers={"x-api-key": _key()}), timeout=30).read())
        if d.get("done"): return d
        time.sleep(1.5)
    return d

def upload_all(budget=40):
    """uploads what's missing from published_ids.json; stops after `budget` seconds (call again to continue)"""
    ids = json.load(open(IDS)) if os.path.exists(IDS) else {}
    t0 = time.time(); ops = {}; errs = {}
    for fn in sorted(os.listdir(OUT)):
        name = fn[:-6]
        if name in ids: continue
        if time.time() - t0 > budget: break
        r = upload(os.path.join(OUT, fn), name)
        if "path" in r: ops[name] = r["path"]
        else: errs[name] = r
    for name, op in ops.items():
        d = poll(op)
        if d.get("done") and "response" in d: ids[name] = d["response"]["assetId"]
        else: errs[name] = d
    json.dump(ids, open(IDS, "w"), indent=1)
    left = len([f for f in os.listdir(OUT) if f[:-6] not in ids])
    return {"uploaded": len(ops), "left": left, "errors": errs}

bpy.app.driver_namespace["robloxupload"] = {"start_post_server": start_post_server, "build_rbxmx": build_rbxmx, "upload_all": upload_all}
