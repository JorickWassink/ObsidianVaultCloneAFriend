# Champ N Son (Boss 4) clips, original skeleton (ADR 0017). Names, lengths, Hold and Event_ match the old clips
# (Strike impact 0.55; Combo hit1 0.3 / hit2 0.65 / hit3 1.0 / joey 1.25 / uppercut 1.85; Intro roar 2.4 / pound 3.35) + Hurt.
# Boxer: bouncy guard Idle, two-footed kangaroo hop Walk, right cross Strike, Title Fight Combo.
from clipkit import *

def guard(k=0, bob=0.0):
    # gloves up by the chin, elbows tucked; k widens the gloves
    return merge({"Body": [-6, 0, 0, 0, bob, 0], "Head": [-4, 0, 0], "Tail": [14, 0, 0]},
                 arms(58, 18 - k, 58, -18 + k, 95, 95))

def jabL(): return arms(92, 8, 58, -18, 2, 95)
def crossR(): return arms(58, 22, 94, -6, 95, 2)

clips = {}
clips["Idle"] = clip("Boss4Idle", 2.0, loop=True, priority="Idle", expressions="0:Grumpy", keys=[
    [0,   G(guard(0, 0.0), {"Body": [-6, 6, 0, 0, 0.0, 0], "Head": [-4, -4, 0]})],
    [0.25, G(guard(2, -0.5), {"Body": [-8, 6, 0, 0, -0.5, 0]})],
    [0.5, G(guard(0, 0.2), {"Body": [-6, 0, 0, 0, 0.2, 0], "Tail": [10, 6, 0]})],
    [0.75, G(guard(2, -0.5), {"Body": [-8, -6, 0, 0, -0.5, 0]})],
    [1.0, G(guard(0, 0.0), {"Body": [-6, -6, 0, 0, 0.0, 0], "Head": [-4, 4, 0]})],
    [1.25, G(guard(2, -0.5), {"Body": [-8, -6, 0, 0, -0.5, 0]})],
    [1.5, G(guard(0, 0.2), {"Body": [-6, 0, 0, 0, 0.2, 0], "Tail": [10, -6, 0]})],
    [1.75, G(guard(2, -0.5), {"Body": [-8, 6, 0, 0, -0.5, 0]})],
    [2.0, G(guard(0, 0.0), {"Body": [-6, 6, 0, 0, 0.0, 0], "Head": [-4, -4, 0]})],
])

def crouch(): return G(guard(4), {"Body": [-14, 0, 0, 0, -0.9, 0], "Head": [6, 0, 0], "Tail": [24, 0, 0]})
def air(): return merge(guard(0), {"Body": [4, 0, 0, 0, 1.4, 0], "Head": [-8, 0, 0], "Tail": [-10, 0, 0],
                                    "LeftLeg": [-24, 0, 0], "RightLeg": [-24, 0, 0]})
def land(): return G(guard(2), {"Body": [-10, 0, 0, 0, -0.5, 0], "Tail": [18, 0, 0]})
clips["Walk"] = clip("Boss4Walk", 0.8, loop=True, priority="Movement", expressions="0:Grumpy", keys=[
    [0, crouch()], [0.2, merge(air(), {"Body": [0, 0, 0, 0, 0.8, 0]})], [0.4, air()], [0.6, land()], [0.8, crouch()]])

clips["Strike"] = clip("Boss4Strike", 1.05, events={"impact": 0.55}, expressions="0:Angry,0.95:Grumpy", keys=[
    [0,    G(guard())],
    [0.3,  G(guard(), arms(58, 18, 40, 10, 95, 120), {"Body": [-4, 24, 0, 0, -0.4, 0], "Head": [-4, -10, 0]})],
    [0.45, G(arms(58, 22, 70, -4, 95, 60), {"Body": [-10, 6, 0, 0, -0.5, 0], "Head": [-6, -4, 0], "Tail": [16, 0, 0]})],
    [0.55, G(crossR(), {"Body": [-16, -26, 0, 0, -0.6, -0.4], "Head": [-8, 10, 0], "Tail": [22, 8, 0]})],
    [0.7,  G(crossR(), {"Body": [-14, -24, 0, 0, -0.5, -0.3], "Head": [-6, 8, 0], "Tail": [20, 6, 0]})],
    [1.05, G(guard())],
])

clips["SpecialWind"] = clip("Boss4SpecialWind", 0.8, hold=True, expressions="0:Angry", keys=[
    [0,   G(guard())],
    [0.4, G(guard(-4), {"Body": [-14, 0, 0, 0, -0.8, 0], "Head": [8, 0, 0], "Tail": [26, 0, 0]})],
    [0.8, G(guard(-6), {"Body": [-16, 0, 0, 0, -1.0, 0], "Head": [10, 0, 0], "Tail": [28, 0, 0]})],
])

def hookL(): return arms(80, -50, 58, -18, 70, 95, ly=40)
clips["Combo"] = clip("Boss4Combo", 2.4, expressions="0:Angry,1.85:Roar,2.2:Angry",
    events={"hit1": 0.3, "hit2": 0.65, "hit3": 1.0, "joey": 1.25, "uppercut": 1.85}, keys=[
    [0,    G(guard(-6), {"Body": [-16, 0, 0, 0, -1.0, 0], "Head": [10, 0, 0], "Tail": [28, 0, 0]})],
    [0.18, G(guard(), {"Body": [-12, 10, 0, 0, -0.4, -0.6]})],
    [0.3,  G(jabL(), {"Body": [-14, 18, 0, 0, -0.4, -0.9], "Head": [-6, -8, 0]})],
    [0.45, G(guard(), {"Body": [-10, -6, 0, 0, -0.4, -0.6]})],
    [0.65, G(crossR(), {"Body": [-16, -28, 0, 0, -0.6, -1.0], "Head": [-8, 10, 0], "Tail": [22, 8, 0]})],
    [0.8,  G(arms(70, 40, 60, -20, 80, 95, ly=-20), {"Body": [-10, -30, 0, 0, -0.5, -0.8]})],
    [1.0,  G(hookL(), {"Body": [-12, 34, 0, 0, -0.5, -0.9], "Head": [-6, -12, 0]})],
    [1.12, G(guard(8), {"Body": [10, 0, 0, 0, -0.2, 0.2], "Head": [-14, 0, 0], "Tail": [34, 0, 0]})],
    [1.25, G(arms(40, -30, 40, 30, 90, 90), {"Body": [16, 0, 0, 0, -0.2, 0.4], "Head": [-16, 0, 0], "Tail": [38, 0, 0]})],
    [1.45, G(guard(), {"Body": [-6, 0, 0, 0, -0.6, 0]})],
    [1.65, G(arms(58, 18, 10, 20, 95, 110), {"Body": [-20, 16, 0, 0, -1.4, 0], "Head": [4, -6, 0], "Tail": [30, 0, 0]})],
    [1.85, G(arms(58, 18, 165, -10, 95, 40), {"Body": [10, -18, 0, 0, 0.8, -0.6], "Head": [18, 6, 0], "Tail": [8, 0, 0]})],
    [2.05, G(arms(58, 18, 160, -10, 95, 40), {"Body": [8, -16, 0, 0, 0.6, -0.5], "Head": [16, 6, 0]})],
    [2.4,  G(guard())],
])

clips["Intro"] = clip("Boss4Intro", 4.2, events={"roar": 2.4, "pound": 3.35}, expressions="0:Grumpy,2.2:Roar,3.0:Angry", keys=[
    [0,    G(arms(10, -8, 10, 8, 20, 20), {"Body": [-4, 0, 0], "Head": [-6, 0, 0], "Tail": [12, 0, 0]})],
    [0.6,  G(arms(10, -8, 10, 8, 20, 20), {"Body": [-4, 0, 0, 0, -0.6, 0], "Head": [-6, 0, 0]})],
    [0.9,  merge(arms(10, -8, 10, 8, 20, 20), {"Body": [2, 0, 0, 0, 1.6, 0], "LeftLeg": [-20, 0, 0], "RightLeg": [-20, 0, 0], "Tail": [-10, 0, 0]})],
    [1.2,  G(guard(), {"Body": [-10, 0, 0, 0, -0.6, 0]})],
    [1.5,  G(jabL(), {"Body": [-10, 14, 0, 0, -0.3, 0]})],
    [1.7,  G(crossR(), {"Body": [-12, -16, 0, 0, -0.3, 0]})],
    [1.95, G(guard(), {"Body": [-6, 0, 0, 0, 0, 0]})],
    [2.4,  G(arms(170, -20, 170, 20, 20, 20), {"Body": [14, 0, 0, 0, 0.3, 0], "Head": [24, 0, 0], "Tail": [30, 0, 0]})],
    [2.9,  G(arms(172, -24, 172, 24, 20, 20), {"Body": [16, 0, 0, 0, 0.35, 0], "Head": [26, 0, 0], "Tail": [32, 0, 0]})],
    [3.15, G(arms(60, 30, 60, -30, 90, 90), {"Body": [-8, 0, 0, 0, -0.3, 0], "Head": [-4, 0, 0]})],
    [3.35, G(arms(64, 40, 64, -40, 70, 70), {"Body": [-12, 0, 0, 0, -0.5, 0], "Head": [-6, 0, 0]})],
    [3.6,  G(arms(60, 30, 60, -30, 90, 90), {"Body": [-8, 0, 0, 0, -0.3, 0]})],
    [4.2,  G(guard())],
])

clips["Defeat"] = clip("Boss4Defeat", 1.4, hold=True, expressions="0:Hurt,0.55:Dazed", keys=[
    [0,    REST],
    [0.3,  G(arms(30, -40, 30, 40, 60, 60), {"Body": [14, 0, 6, 0, 0.2, 0.4], "Head": [22, 10, 0], "Tail": [30, 0, 0]})],
    [0.7,  merge(arms(25, -30, 25, 30, 30, 30), {"Body": [-6, 0, -6, 0, -2.0, 0], "Head": [-6, -8, 0], "LeftLeg": [40, 0, -10], "RightLeg": [40, 0, 10], "Tail": [40, 0, 0]})],
    [1.05, merge(arms(20, -50, 20, 50, 10, 10), {"Body": [-14, 0, 0, 0, -3.2, 0], "Head": [-24, 6, 0], "LeftLeg": [80, 0, -14], "RightLeg": [80, 0, 14], "Tail": [50, 0, 0]})],
    [1.4,  merge(arms(18, -52, 18, 52, 10, 10), {"Body": [-12, 0, 0, 0, -3.1, 0], "Head": [-22, 4, 4], "LeftLeg": [78, 0, -14], "RightLeg": [78, 0, 14], "Tail": [48, 0, 0]})],
])

clips["Hurt"] = clip("Boss4Hurt", 0.6, expressions="0:Hurt,0.5:Grumpy", keys=[
    [0,    G(guard())],
    [0.08, G(guard(10), {"Body": [8, 8, 0, 0, -0.3, 0.4], "Head": [16, 10, 0], "Tail": [30, 0, 0]})],
    [0.25, G(guard(2), {"Body": [-10, -2, 0, 0, -0.4, 0], "Head": [-4, -4, 0]})],
    [0.6,  G(guard())],
])

if __name__ == "__main__":
    emit("B04", clips)
