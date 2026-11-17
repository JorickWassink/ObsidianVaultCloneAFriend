# Le Ape (Boss 5) clips, original skeleton (ADR 0017). Names, lengths, Hold and Event_ match the old clips
# (Strike impact 0.55; SpecialThrow release 0.12; SpecialHit impact 0.15; Intro roar 2.4 / pound 3.35) + Hurt.
# Gorilla chef: heavy swaying Idle, lumbering Walk, rolling-pin smash (right hand), Kitchen Catastrophe =
# SpecialWind (scoops flour from the apron, holds), SpecialThrow (flour bomb, once per bomb), SpecialHit (two-fist slam).
from clipkit import *

def stance(s=0, k=0.0):
    # heavy gorilla stance: hunched, long arms hanging a bit forward and out
    return merge({"Body": [-14, 5 * s, 2 * s, 0, -0.4 + k, 0], "Head": [10, -6 * s, 0]},
                 arms(14, -10, 14, 10, 18, 18))

clips = {}
clips["Idle"] = clip("Boss5Idle", 2.6, loop=True, priority="Idle", expressions="0:Grumpy,1.2:Blink,1.35:Grumpy", keys=[
    [0,    G(stance(1, 0.0))],
    [0.65, G(stance(0, -0.15), arms(18, -14, 18, 14, 24, 24), {"Head": [6, 0, 0]})],
    [1.3,  G(stance(-1, 0.0))],
    [1.95, G(stance(0, -0.15), arms(18, -14, 18, 14, 24, 24), {"Head": [6, 0, 0]})],
    [2.6,  G(stance(1, 0.0))],
])

def step(s):
    # s = +1: left foot forward, right arm forward (heavy contralateral swing), body rolls over the planted foot
    return merge({"Body": [-16, 8 * s, 4 * s, 0, -0.5, 0], "Head": [12, -8 * s, 0],
                  "LeftLeg": [26 * s - 16, 0, 0, 0, 0.5, 0], "RightLeg": [-26 * s - 16, 0, 0, 0, 0.5, 0]},
                 arms(14 - 26 * s, -12, 14 + 26 * s, 12, 20, 20))
def passing():
    return merge({"Body": [-16, 0, 0, 0, 0.0, 0], "Head": [12, 0, 0], "LeftLeg": [16, 0, 0], "RightLeg": [16, 0, 0]},
                 arms(14, -10, 14, 10, 22, 22))
clips["Walk"] = clip("Boss5Walk", 1.3, loop=True, priority="Movement", expressions="0:Grumpy", keys=[
    [0, step(1)], [0.325, passing()], [0.65, step(-1)], [0.975, passing()], [1.3, step(1)]])

clips["Strike"] = clip("Boss5Strike", 1.05, events={"impact": 0.55}, expressions="0:Angry,0.95:Grumpy", keys=[
    [0,    G(stance())],
    [0.3,  G(arms(30, -20, 170, -10, 30, 70), {"Body": [6, -12, 0, 0, 0.2, 0], "Head": [14, 8, 0]})],
    [0.45, G(arms(26, -20, 178, -6, 30, 40), {"Body": [10, -14, 0, 0, 0.35, 0], "Head": [18, 8, 0]})],
    [0.55, G(arms(10, -24, 70, 4, 10, 4), {"Body": [-24, 10, 0, 0, -0.9, -0.4], "Head": [2, -6, 0]})],
    [0.7,  G(arms(8, -24, 62, 4, 10, 6), {"Body": [-22, 8, 0, 0, -0.8, -0.3], "Head": [4, -4, 0]})],
    [1.05, G(stance())],
])

clips["SpecialWind"] = clip("Boss5SpecialWind", 1.2, hold=True, expressions="0:Angry", keys=[
    [0,   G(stance())],
    [0.4, G(arms(40, 20, 40, -20, 70, 70), {"Body": [-24, 0, 0, 0, -0.6, 0], "Head": [-6, 0, 0]})],
    [0.8, G(arms(120, -10, 30, -10, 60, 80), {"Body": [4, 10, 0, 0, 0.1, 0], "Head": [14, -6, 0]})],
    [1.2, G(arms(150, -14, 26, -12, 70, 80), {"Body": [8, 14, 0, 0, 0.2, 0], "Head": [16, -8, 0]})],
])

clips["SpecialThrow"] = clip("Boss5SpecialThrow", 0.55, events={"release": 0.12}, expressions="0:Angry", keys=[
    [0,    G(arms(150, -14, 26, -12, 70, 80), {"Body": [8, 14, 0, 0, 0.2, 0], "Head": [16, -8, 0]})],
    [0.12, G(arms(70, -4, 20, -14, 10, 60), {"Body": [-14, -10, 0, 0, -0.4, 0], "Head": [-2, 6, 0]})],
    [0.3,  G(arms(30, -10, 18, -12, 14, 50), {"Body": [-20, -16, 0, 0, -0.55, 0], "Head": [-6, 8, 0]})],
    [0.55, G(arms(150, -14, 26, -12, 70, 80), {"Body": [8, 14, 0, 0, 0.2, 0], "Head": [16, -8, 0]})],
])

clips["SpecialHit"] = clip("Boss5SpecialHit", 1.1, events={"impact": 0.15}, expressions="0:Roar,0.5:Angry", keys=[
    [0,    G(arms(176, -8, 176, 8, 20, 20), {"Body": [12, 0, 0, 0, 0.4, 0], "Head": [20, 0, 0]})],
    [0.15, G(arms(60, 10, 60, -10, 0, 0), {"Body": [-30, 0, 0, 0, -1.6, -0.4], "Head": [4, 0, 0]})],
    [0.35, G(arms(56, 12, 56, -12, 2, 2), {"Body": [-28, 0, 0, 0, -1.5, -0.4], "Head": [8, 0, 0]})],
    [0.7,  G(arms(30, -4, 30, 4, 10, 10), {"Body": [-20, 0, 0, 0, -0.8, 0], "Head": [10, 0, 0]})],
    [1.1,  G(stance())],
])

def chest(k):
    # chest-pound: fists alternate onto the chest
    return arms(70 if k else 40, 40 if k else 20, 40 if k else 70, -20 if k else -40, 110, 110)
clips["Intro"] = clip("Boss5Intro", 4.2, events={"roar": 2.4, "pound": 3.35}, expressions="0:Grumpy,2.2:Roar,3.0:Angry", keys=[
    [0,    G(stance(), {"Head": [-10, 0, 0]})],
    [0.7,  G(stance(), {"Head": [6, 30, 0]}, {"Body": [-14, 14, 0, 0, -0.4, 0]})],
    [1.3,  G(stance(), {"Head": [6, -30, 0]}, {"Body": [-14, -14, 0, 0, -0.4, 0]})],
    [1.9,  G(arms(30, -20, 30, 20, 40, 40), {"Body": [-20, 0, 0, 0, -0.8, 0], "Head": [-6, 0, 0]})],
    [2.4,  G(arms(30, -70, 30, 70, 40, 40), {"Body": [16, 0, 0, 0, 0.4, 0], "Head": [26, 0, 0]})],
    [2.9,  G(arms(30, -72, 30, 72, 40, 40), {"Body": [18, 0, 0, 0, 0.45, 0], "Head": [28, 0, 0]})],
    [3.15, G(chest(1), {"Body": [4, 0, 0, 0, 0, 0], "Head": [10, 0, 0]})],
    [3.35, G(chest(0), {"Body": [6, 0, 0, 0, 0, 0], "Head": [12, 0, 0]})],
    [3.5,  G(chest(1), {"Body": [4, 0, 0, 0, 0, 0], "Head": [10, 0, 0]})],
    [3.65, G(chest(0), {"Body": [6, 0, 0, 0, 0, 0], "Head": [12, 0, 0]})],
    [4.2,  G(stance())],
])

clips["Defeat"] = clip("Boss5Defeat", 1.4, hold=True, expressions="0:Hurt,0.55:Dazed", keys=[
    [0,    REST],
    [0.3,  G(arms(10, -40, 10, 40, 20, 20), {"Body": [14, 0, 6, 0, 0.2, 0.4], "Head": [22, 10, 0]})],
    [0.7,  merge(arms(25, -24, 25, 24, 25, 25), {"Body": [-6, 0, -6, 0, -2.0, 0], "Head": [-6, -8, 0], "LeftLeg": [40, 0, -10], "RightLeg": [40, 0, 10]})],
    [1.05, merge(arms(35, -14, 35, 14, 15, 15), {"Body": [-14, 0, 0, 0, -3.2, 0], "Head": [-24, 6, 0], "LeftLeg": [80, 0, -14], "RightLeg": [80, 0, 14]})],
    [1.4,  merge(arms(32, -14, 32, 14, 15, 15), {"Body": [-12, 0, 0, 0, -3.1, 0], "Head": [-22, 4, 4], "LeftLeg": [78, 0, -14], "RightLeg": [78, 0, 14]})],
])

clips["Hurt"] = clip("Boss5Hurt", 0.6, expressions="0:Hurt,0.5:Grumpy", keys=[
    [0,    G(stance())],
    [0.08, G(arms(-10, -20, -10, 20, 20, 20), {"Body": [6, 6, 0, 0, -0.5, 0.3], "Head": [16, 10, 0]})],
    [0.25, G(stance(), {"Body": [-16, -2, 0, 0, -0.45, 0], "Head": [6, -4, 0]})],
    [0.6,  G(stance())],
])

if __name__ == "__main__":
    emit("B05", clips)
