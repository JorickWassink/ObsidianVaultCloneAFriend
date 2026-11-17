# RoboJawsh (Boss 8) clips, original skeleton (ADR 0017). Names, lengths, Hold and Event_ match the old clips
# (Strike impact 0.55; SpecialThrow release 0.05; SpecialHit launch 0.3 / impact 0.8; Walk stomp 0 / stomp2 0.7;
# Intro roar 2.4 / pound 3.35) + Hurt.
# Heavy robot shark mech: servo-stiff Idle with a slow scan, stomping Walk, hammer-fist Strike, Full Payload =
# SpecialWind braces with both arm launchers forward and holds, SpecialThrow is one torpedo's recoil (alternating feel via
# body twist), SpecialHit is the booster jump (crouch, launch 0.3, airborne, slam 0.8).
from clipkit import *

def mech(s=0, k=0.0):
    return merge({"Body": [-4, 4 * s, 0, 0, -0.3 + k, 0], "Head": [0, -10 * s, 0]},
                 arms(24, -14, 24, 14, 50, 50))

clips = {}
clips["Idle"] = clip("Boss8Idle", 3.0, loop=True, priority="Idle", expressions="0:Grumpy,1.4:GlanceL,1.9:GlanceR,2.4:Grumpy", keys=[
    [0,    G(mech(0))],
    [0.75, G(mech(1, -0.12))],
    [1.5,  G(mech(0))],
    [2.25, G(mech(-1, -0.12))],
    [3.0,  G(mech(0))],
])

def stomp(s):
    # planted foot takes the weight: body dips and jolts
    return merge({"Body": [-6, 6 * s, 3 * s, 0, -0.7, 0], "Head": [2, -4 * s, 0],
                  "LeftLeg": [20 * s + 6, 0, 0, 0, 0.7, 0], "RightLeg": [-20 * s + 6, 0, 0, 0, 0.7, 0]},
                 arms(24 - 16 * s, -14, 24 + 16 * s, 14, 50, 50))
def lift(s):
    # opposite leg high (knee-up feel), body rises
    return merge({"Body": [-4, 3 * s, 0, 0, 0.2, 0], "Head": [0, 0, 0],
                  "LeftLeg": [-30 * s + 4, 0, 0, 0, 0.6 if s < 0 else 0, 0], "RightLeg": [30 * s + 4, 0, 0, 0, 0.6 if s > 0 else 0, 0]},
                 arms(24, -14, 24, 14, 50, 50))
clips["Walk"] = clip("Boss8Walk", 1.4, loop=True, priority="Movement", events={"stomp": 0, "stomp2": 0.7}, expressions="0:Grumpy", keys=[
    [0, stomp(1)], [0.35, lift(1)], [0.7, stomp(-1)], [1.05, lift(-1)], [1.4, stomp(1)]])

clips["Strike"] = clip("Boss8Strike", 1.05, events={"impact": 0.55}, expressions="0:Angry,0.95:Grumpy", keys=[
    [0,    G(mech())],
    [0.3,  G(arms(166, -10, 166, 10, 30, 30), {"Body": [10, 0, 0, 0, 0.3, 0], "Head": [12, 0, 0]})],
    [0.45, G(arms(176, -6, 176, 6, 20, 20), {"Body": [14, 0, 0, 0, 0.45, 0], "Head": [14, 0, 0]})],
    [0.55, G(arms(56, 6, 56, -6, 0, 0), {"Body": [-24, 0, 0, 0, -1.2, -0.4], "Head": [-4, 0, 0]})],
    [0.7,  G(arms(52, 6, 52, -6, 4, 4), {"Body": [-22, 0, 0, 0, -1.1, -0.4], "Head": [-2, 0, 0]})],
    [1.05, G(mech())],
])

def brace(tw=0):
    return G(arms(84, 6, 84, -6, 6, 6), {"Body": [-10, tw, 0, 0, -0.9, 0.3], "Head": [-2, 0, 0],
                                          "LeftLeg": [10, 0, -6], "RightLeg": [-8, 0, 6]})
clips["SpecialWind"] = clip("Boss8SpecialWind", 1.0, hold=True, expressions="0:Angry", keys=[
    [0,   G(mech())],
    [0.5, G(arms(70, 4, 70, -4, 30, 30), {"Body": [-8, 0, 0, 0, -0.6, 0.2]})],
    [1.0, brace()],
])

clips["SpecialThrow"] = clip("Boss8SpecialThrow", 0.4, events={"release": 0.05}, expressions="0:Angry", keys=[
    [0,    brace()],
    [0.05, G(arms(104, 6, 100, -6, 0, 0), {"Body": [4, 0, 0, 0, -0.7, 0.9], "Head": [8, 0, 0],
                                            "LeftLeg": [10, 0, -6], "RightLeg": [-8, 0, 6]})],
    [0.18, G(arms(92, 6, 90, -6, 4, 4), {"Body": [-4, 0, 0, 0, -0.8, 0.6], "Head": [2, 0, 0],
                                          "LeftLeg": [10, 0, -6], "RightLeg": [-8, 0, 6]})],
    [0.4,  brace()],
])

clips["SpecialHit"] = clip("Boss8SpecialHit", 1.5, events={"launch": 0.3, "impact": 0.8}, expressions="0:Angry,0.3:Angry,1.1:Angry", keys=[
    [0,    brace()],
    [0.2,  G(arms(-30, -30, -30, 30, 10, 10), {"Body": [-24, 0, 0, 0, -1.6, 0], "Head": [10, 0, 0]})],
    [0.3,  merge(arms(-40, -40, -40, 40, 0, 0), {"Body": [8, 0, 0, 0, 1.0, 0], "Head": [14, 0, 0],
                                                  "LeftLeg": [-20, 0, 0], "RightLeg": [-20, 0, 0]})],
    [0.55, merge(arms(150, -20, 150, 20, 20, 20), {"Body": [10, 0, 0, 0, 1.8, 0], "Head": [6, 0, 0],
                                                    "LeftLeg": [40, 0, 0], "RightLeg": [40, 0, 0]})],
    [0.8,  G(arms(40, -40, 40, 40, 10, 10), {"Body": [-26, 0, 0, 0, -1.8, 0], "Head": [-6, 0, 0]})],
    [1.0,  G(arms(36, -36, 36, 36, 14, 14), {"Body": [-24, 0, 0, 0, -1.6, 0], "Head": [0, 0, 0]})],
    [1.5,  G(mech())],
])

clips["Intro"] = clip("Boss8Intro", 4.2, events={"roar": 2.4, "pound": 3.35}, expressions="0:Blink,0.6:Grumpy,2.2:Angry,3.0:Angry", keys=[
    [0,    G(arms(0, -6, 0, 6, 0, 0), {"Body": [-30, 0, 0, 0, -1.2, 0], "Head": [-30, 0, 0]})],
    [0.6,  G(arms(0, -6, 0, 6, 0, 0), {"Body": [-30, 0, 0, 0, -1.2, 0], "Head": [-30, 0, 0]})],
    [1.1,  G(mech(), {"Head": [0, 30, 0]})],
    [1.6,  G(mech(), {"Head": [0, -30, 0]})],
    [1.95, G(mech(), {"Body": [-6, 0, 0, 0, -0.5, 0]})],
    [2.4,  G(arms(100, -50, 100, 50, 30, 30), {"Body": [16, 0, 0, 0, 0.3, 0], "Head": [26, 0, 0]})],
    [2.9,  G(arms(104, -54, 104, 54, 30, 30), {"Body": [18, 0, 0, 0, 0.35, 0], "Head": [28, 0, 0]})],
    [3.15, G(arms(70, 30, 70, -30, 90, 90), {"Body": [-6, 0, 0, 0, -0.3, 0]})],
    [3.35, G(arms(64, 40, 64, -40, 70, 70), {"Body": [-12, 0, 0, 0, -0.6, 0]})],
    [3.6,  G(arms(70, 30, 70, -30, 90, 90), {"Body": [-6, 0, 0, 0, -0.3, 0]})],
    [4.2,  G(mech())],
])

clips["Defeat"] = clip("Boss8Defeat", 1.4, hold=True, expressions="0:Hurt,0.55:Dazed", keys=[
    [0,    REST],
    [0.3,  G(arms(10, -40, 10, 40, 20, 20), {"Body": [14, 0, 6, 0, 0.2, 0.4], "Head": [22, 10, 0]})],
    [0.7,  merge(arms(25, -20, 25, 20, 25, 25), {"Body": [-6, 0, -6, 0, -2.0, 0], "Head": [-6, -8, 0], "LeftLeg": [40, 0, -10], "RightLeg": [40, 0, 10]})],
    [1.05, merge(arms(35, -10, 35, 10, 15, 15), {"Body": [-14, 0, 0, 0, -3.2, 0], "Head": [-24, 6, 0], "LeftLeg": [80, 0, -14], "RightLeg": [80, 0, 14]})],
    [1.4,  merge(arms(32, -10, 32, 10, 15, 15), {"Body": [-12, 0, 0, 0, -3.1, 0], "Head": [-22, 4, 4], "LeftLeg": [78, 0, -14], "RightLeg": [78, 0, 14]})],
])

clips["Hurt"] = clip("Boss8Hurt", 0.6, expressions="0:Hurt,0.5:Grumpy", keys=[
    [0,    G(mech())],
    [0.08, G(arms(-6, -24, -6, 24, 30, 30), {"Body": [8, 8, 0, 0, -0.3, 0.3], "Head": [14, 12, 0]})],
    [0.25, G(mech(), {"Body": [-8, -2, 0, 0, -0.4, 0]})],
    [0.6,  G(mech())],
])

if __name__ == "__main__":
    emit("B08", clips)
