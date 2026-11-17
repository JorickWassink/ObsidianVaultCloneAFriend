# Grave Wyrm (Boss 9) and Obsidian Dragon (Boss 10) clips: winged bipeds on the original skeletons (ADR 0017).
# Names, lengths, Hold and Event_ match the old clips + Hurt:
#  B09: Strike impact 0.55 | SpecialWind 1.2 H | FlyUp 1.0 liftoff 0.3 | Hover 1.0 loop flap 0 | SpecialDive 0.6 |
#       SpecialHit 1.1 impact 0.1 | Walk 0.9 | Idle 3.2 | Intro 4.2 roar 2.4 / pound 3.35 | Defeat 1.4 H
#  B10: Strike 0.55 | SpecialWind 1.6 H roar 0.5 | FlyUp 1.2 liftoff 0.35 | Hover 1.2 loop flap 0 | SpecialDive 0.7 |
#       SpecialHit 1.2 impact 0.1 | Cast 1.0 erupt 0.45 | Walk 1.8 stomp 0 / stomp2 0.9 | Idle 4.0 | Intro | Defeat
# Wings: left wing up = -rz, right wing up = +rz (same as arms out); ry sweeps them back (+ for left, - for right).
# Neither has a Roar mouth set, so faces use Angry.
#   python dragon_clips.py            (emits B09 and B10)
from clipkit import *

def wings(up, back=0, fold=0):
    """up: + raises both wings (deg), back: sweep back, fold: extra tuck (rx)"""
    return {"LeftWing": [fold, back, -up], "RightWing": [fold, -back, up]}

def build(tag, N, heavy):
    k = 1.25 if heavy else 1.0          # B10 moves a bit slower and bigger
    head = -6 if heavy else 4           # Obsidian Dragon carries its head low, Grave Wyrm snakes it up
    pre = f"Boss{N}"
    def stand(s=0, br=0.0, w=0):
        return merge({"Body": [-6, 4 * s, 0, 0, br, 0], "Head": [head, -8 * s, 0], "Tail": [10, 14 * s, 0]},
                     arms(20, -12, 20, 12, 40, 40), wings(10 + w, 20, 0))
    clips = {}
    L = 4.0 if heavy else 3.2
    clips["Idle"] = clip(pre + "Idle", L, loop=True, priority="Idle", expressions="0:Grumpy,1.2:GlanceL,1.7:Grumpy,2.6:Blink,2.75:Grumpy", keys=[
        [0, G(stand(0))], [L * 0.25, G(stand(1, -0.2, 8))], [L * 0.5, G(stand(0))],
        [L * 0.75, G(stand(-1, -0.2, 8))], [L, G(stand(0))]])

    W = 1.8 if heavy else 0.9
    def step(s):
        return merge({"Body": [-8, 6 * s, 3 * s, 0, -0.4 * k, 0], "Head": [head + 4, -8 * s, 0], "Tail": [10, 20 * s, 0],
                      "LeftLeg": [26 * s + 8, 0, 0, 0, 0.4 * k, 0], "RightLeg": [-26 * s + 8, 0, 0, 0, 0.4 * k, 0]},
                     arms(20 - 14 * s, -12, 20 + 14 * s, 12, 40, 40), wings(6, 22))
    def spass():
        return merge({"Body": [-8, 0, 0, 0, 0.1, 0], "Head": [head + 4, 0, 0], "Tail": [10, 0, 0],
                      "LeftLeg": [8, 0, 0], "RightLeg": [8, 0, 0]}, arms(20, -12, 20, 12, 40, 40), wings(12, 22))
    clips["Walk"] = clip(pre + "Walk", W, loop=True, priority="Movement",
                         events={"stomp": 0, "stomp2": 0.9} if heavy else {}, expressions="0:Grumpy", keys=[
        [0, step(1)], [W / 4, spass()], [W / 2, step(-1)], [W * 3 / 4, spass()], [W, step(1)]])

    clips["Strike"] = clip(pre + "Strike", 1.05, events={"impact": 0.55}, expressions="0:Angry,0.95:Grumpy", keys=[
        [0,    G(stand())],
        [0.3,  G(arms(20, -12, 130, 30, 40, 70, ry=-30), wings(40, 10), {"Body": [4, 22, 0, 0, 0.1, 0], "Head": [head + 10, -14, 0], "Tail": [16, -20, 0]})],
        [0.45, G(arms(20, -12, 140, 24, 40, 50, ry=-20), wings(44, 8), {"Body": [6, 16, 0, 0, 0.2, 0], "Head": [head + 12, -10, 0]})],
        [0.55, G(arms(10, -20, 60, -10, 30, 10, ry=30), wings(20, 30), {"Body": [-18, -24, 0, 0, -0.6 * k, -0.5], "Head": [head - 8, 12, 0], "Tail": [10, 26, 0]})],
        [0.7,  G(arms(10, -20, 50, -14, 30, 10, ry=36), wings(18, 30), {"Body": [-16, -28, 0, 0, -0.5 * k, -0.4], "Head": [head - 6, 14, 0], "Tail": [10, 28, 0]})],
        [1.05, G(stand())],
    ])

    # screech / roar with wings spread wide, holds
    SW = 1.6 if heavy else 1.2
    spread = lambda a: G(arms(40, -50, 40, 50, 30, 30), wings(55 + a, -10), {"Body": [14, 0, 0, 0, 0.3, 0], "Head": [head + 26 + a / 4, 0, 0], "Tail": [24, 0, 0]})
    clips["SpecialWind"] = clip(pre + "SpecialWind", SW, hold=True, events={"roar": 0.5} if heavy else {}, expressions="0:Angry", keys=[
        [0, G(stand())],
        [SW * 0.3, G(arms(30, -20, 30, 20, 60, 60), wings(20, 30), {"Body": [-14, 0, 0, 0, -0.6, 0], "Head": [head - 10, 0, 0], "Tail": [10, 0, 0]})],
        [SW * 0.55, spread(0)], [SW * 0.8, spread(6)], [SW, spread(3)]])

    # FlyUp: crouch, big downflap at liftoff, legs dangle as it rises
    FU, LO = (1.2, 0.35) if heavy else (1.0, 0.3)
    def airborne(up, legs=-24, body=4):
        return merge({"Body": [body, 0, 0, 0, 0, 0], "Head": [head + 6, 0, 0], "Tail": [20, 0, 0],
                      "LeftLeg": [legs, 0, -6], "RightLeg": [legs, 0, 6]}, arms(30, -16, 30, 16, 50, 50), wings(up, 10))
    clips["FlyUp"] = clip(pre + "FlyUp", FU, events={"liftoff": LO}, expressions="0:Angry", keys=[
        [0, G(stand())],
        [LO * 0.6, G(arms(10, -20, 10, 20, 30, 30), wings(70, 0), {"Body": [-18, 0, 0, 0, -1.2 * k, 0], "Head": [head - 6, 0, 0], "Tail": [16, 0, 0]})],
        [LO, airborne(-55, -10, 10)],
        [LO + (FU - LO) * 0.45, airborne(60, -24)],
        [FU, airborne(-20, -28)]])

    # Hover loop: flap event at 0 = wings driving down; body bobs opposite the wings
    HV = 1.2 if heavy else 1.0
    def hov(up, bob):
        return merge(airborne(up), {"Body": [4, 0, 0, 0, bob, 0], "Tail": [24 - up * 0.15, 0, 0],
                                    "LeftLeg": [-24 + bob * 6, 0, -6], "RightLeg": [-24 + bob * 6, 0, 6]})
    clips["Hover"] = clip(pre + "Hover", HV, loop=True, events={"flap": 0}, expressions="0:Angry", keys=[
        [0, hov(30, -0.3)], [HV * 0.25, hov(-55, 0.4)], [HV * 0.5, hov(-10, 0.2)], [HV * 0.75, hov(55, -0.2)], [HV, hov(30, -0.3)]])

    # SpecialDive: tucked dive, wings swept back, claws forward
    DV = 0.7 if heavy else 0.6
    dive = lambda t: merge({"Body": [-40 - t, 0, 0, 0, 0, 0], "Head": [10, 0, 0], "Tail": [-10, 0, 0],
                            "LeftLeg": [50, 0, -8], "RightLeg": [50, 0, 8]}, arms(110, -10, 110, 10, 20, 20), wings(5, 70, 0))
    clips["SpecialDive"] = clip(pre + "SpecialDive", DV, expressions="0:Angry", keys=[
        [0, hov(55, -0.2)], [DV * 0.4, dive(0)], [DV, dive(8)]])

    # SpecialHit: lands at 0.1 with a slam, wings flare, recovers to stand
    SH = 1.2 if heavy else 1.1
    clips["SpecialHit"] = clip(pre + "SpecialHit", SH, events={"impact": 0.1}, expressions="0:Angry,0.9:Grumpy", keys=[
        [0, dive(8)],
        [0.1, G(arms(60, 10, 60, -10, 10, 10), wings(50, 0), {"Body": [-28, 0, 0, 0, -1.6 * k, -0.6], "Head": [head - 10, 0, 0], "Tail": [30, 0, 0]})],
        [0.35, G(arms(56, 8, 56, -8, 14, 14), wings(36, 10), {"Body": [-24, 0, 0, 0, -1.4 * k, -0.5], "Head": [head - 4, 0, 0], "Tail": [26, 0, 0]})],
        [SH * 0.7, G(stand(), {"Body": [-10, 0, 0, 0, -0.4, 0]})],
        [SH, G(stand())]])

    if heavy:
        # Cast (while hovering): both claws thrust down, runes erupt at 0.45; wings keep beating
        clips["Cast"] = clip(pre + "Cast", 1.0, events={"erupt": 0.45}, expressions="0:Angry", keys=[
            [0, hov(30, -0.3)],
            [0.3, merge(hov(-20, 0.4), arms(150, -30, 150, 30, 30, 30), {"Head": [head + 20, 0, 0]})],
            [0.45, merge(hov(50, 0.1), arms(40, 20, 40, -20, 0, 0), {"Body": [-14, 0, 0, 0, 0.1, 0], "Head": [head - 16, 0, 0]})],
            [0.7, merge(hov(-30, 0.3), arms(44, 16, 44, -16, 6, 6), {"Head": [head - 10, 0, 0]})],
            [1.0, hov(30, -0.3)]])

    clips["Intro"] = clip(pre + "Intro", 4.2, events={"roar": 2.4, "pound": 3.35}, expressions="0:Blink,0.5:Grumpy,2.2:Angry", keys=[
        [0,    G(stand(), wings(-6, 50, 0), {"Head": [head - 20, 0, 0], "Body": [-14, 0, 0, 0, -0.6, 0]})],
        [0.7,  G(stand(1), wings(0, 40), {"Head": [head + 4, -28, 0]})],
        [1.3,  G(stand(-1), wings(0, 40), {"Head": [head + 4, 28, 0]})],
        [1.9,  G(arms(30, -20, 30, 20, 60, 60), wings(20, 30), {"Body": [-14, 0, 0, 0, -0.7, 0], "Head": [head - 10, 0, 0]})],
        [2.4,  G(arms(40, -60, 40, 60, 30, 30), wings(62, -10), {"Body": [16, 0, 0, 0, 0.3, 0], "Head": [head + 30, 0, 0], "Tail": [30, 0, 0]})],
        [2.9,  G(arms(40, -62, 40, 62, 30, 30), wings(66, -12), {"Body": [18, 0, 0, 0, 0.35, 0], "Head": [head + 32, 0, 0], "Tail": [32, 0, 0]})],
        [3.15, G(arms(60, -10, 60, 10, 30, 30), wings(30, 10), {"Body": [-4, 0, 0, 0, 0, 0], "Head": [head, 0, 0]})],
        [3.35, G(arms(50, 10, 50, -10, 10, 10), wings(-10, 30), {"Body": [-16, 0, 0, 0, -0.7, 0], "Head": [head - 8, 0, 0], "Tail": [24, 0, 0]})],
        [3.6,  G(arms(40, 0, 40, 0, 20, 20), wings(10, 20), {"Body": [-10, 0, 0, 0, -0.4, 0]})],
        [4.2,  G(stand())]])

    clips["Defeat"] = clip(pre + "Defeat", 1.4, hold=True, expressions="0:Hurt,0.55:Dazed", keys=[
        [0,    REST],
        [0.3,  G(arms(10, -40, 10, 40, 20, 20), wings(50, 0), {"Body": [14, 0, 6, 0, 0.2, 0.4], "Head": [22, 10, 0], "Tail": [20, 0, 0]})],
        [0.7,  merge(arms(25, -20, 25, 20, 25, 25), wings(20, 30), {"Body": [-6, 0, -6, 0, -2.0, 0], "Head": [-6, -8, 0], "LeftLeg": [40, 0, -10], "RightLeg": [40, 0, 10], "Tail": [30, 0, 0]})],
        [1.05, merge(arms(35, -10, 35, 10, 15, 15), wings(-20, 40), {"Body": [-14, 0, 0, 0, -3.2, 0], "Head": [-24, 6, 0], "LeftLeg": [80, 0, -14], "RightLeg": [80, 0, 14], "Tail": [40, 10, 0]})],
        [1.4,  merge(arms(32, -10, 32, 10, 15, 15), wings(-24, 42), {"Body": [-12, 0, 0, 0, -3.1, 0], "Head": [-22, 4, 4], "LeftLeg": [78, 0, -14], "RightLeg": [78, 0, 14], "Tail": [38, 10, 0]})]])

    clips["Hurt"] = clip(pre + "Hurt", 0.6, expressions="0:Hurt,0.5:Grumpy", keys=[
        [0,    G(stand())],
        [0.08, G(arms(-10, -24, -10, 24, 30, 30), wings(40, -6), {"Body": [8, 8, 0, 0, -0.3, 0.3], "Head": [head + 16, 12, 0], "Tail": [24, 0, 0]})],
        [0.25, G(stand(), {"Body": [-10, -2, 0, 0, -0.35, 0], "Head": [head - 4, -4, 0]})],
        [0.6,  G(stand())]])
    emit(tag, clips)

if __name__ == "__main__":
    build("B09", 9, False)
    build("B10", 10, True)
