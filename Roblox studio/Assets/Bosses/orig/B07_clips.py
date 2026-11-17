# Lion King (Boss 7) clips, original skeleton (ADR 0017). Names, lengths, Hold and Event_ match the old clips
# (Strike impact 0.55; SpecialHit impact 0.15; Walk tap 0; Intro roar 2.4 / pound 3.35) + Hurt.
# Regal lion with a scepter in the right hand: proud chest-out Idle, stately Walk (scepter taps the floor at 0),
# backhand scepter swing Strike, Royal Decree = SpecialWind raises the scepter high and holds, SpecialHit slams it down.
from clipkit import *

def regal(s=0, k=0.0):
    # chest out, chin up, left fist on hip, scepter planted at the right side
    return merge({"Body": [6, 3 * s, 0, 0, k, 0], "Head": [6, -4 * s, 0]},
                 arms(-10, -34, 18, 8, 80, 30))

clips = {}
clips["Idle"] = clip("Boss7Idle", 3.2, loop=True, priority="Idle", expressions="0:Grumpy,1.0:GlanceL,1.6:Grumpy,2.4:GlanceR,2.9:Grumpy", keys=[
    [0,   G(regal(0, 0.0))],
    [0.8, G(regal(1, 0.18), {"Head": [8, 14, 0]})],
    [1.6, G(regal(0, 0.0))],
    [2.4, G(regal(-1, 0.18), {"Head": [8, -14, 0]})],
    [3.2, G(regal(0, 0.0))],
])

def stride(s):
    # s=1: left foot forward; the scepter (right) plants with the right foot back
    return merge({"Body": [4, 6 * s, 2 * s, 0, -0.15, 0], "Head": [6, -6 * s, 0],
                  "LeftLeg": [24 * s - 4, 0, 0, 0, 0.15, 0], "RightLeg": [-24 * s - 4, 0, 0, 0, 0.15, 0]},
                 arms(-10 - 8 * s, -34, 18 + 22 * s, 8, 80, 30))
def spass():
    return merge({"Body": [4, 0, 0, 0, 0.15, 0], "Head": [6, 0, 0], "LeftLeg": [4, 0, 0], "RightLeg": [4, 0, 0]},
                 arms(-10, -34, 18, 8, 80, 30))
clips["Walk"] = clip("Boss7Walk", 1.3, loop=True, priority="Movement", events={"tap": 0}, expressions="0:Grumpy", keys=[
    [0, stride(1)], [0.325, spass()], [0.65, stride(-1)], [0.975, spass()], [1.3, stride(1)]])

clips["Strike"] = clip("Boss7Strike", 1.05, events={"impact": 0.55}, expressions="0:Angry,0.95:Grumpy", keys=[
    [0,    G(regal())],
    [0.3,  G(arms(10, -20, 100, -60, 40, 30, ry=-30), {"Body": [-4, 26, 0, 0, -0.4, 0], "Head": [0, -14, 0]})],
    [0.45, G(arms(10, -20, 110, -50, 40, 20, ry=-20), {"Body": [-8, 18, 0, 0, -0.5, 0], "Head": [-2, -10, 0]})],
    [0.55, G(arms(10, -30, 90, 50, 30, 10, ry=40), {"Body": [-14, -28, 0, 0, -0.6, -0.4], "Head": [-4, 12, 0]})],
    [0.7,  G(arms(10, -30, 80, 60, 30, 10, ry=46), {"Body": [-12, -32, 0, 0, -0.5, -0.3], "Head": [-2, 14, 0]})],
    [1.05, G(regal())],
])

def raised(k=0):
    return G(arms(40, -40, 176, -4, 20, 10), {"Body": [12 + k, 0, 0, 0, 0.3, 0], "Head": [20 + k, 0, 0]})
clips["SpecialWind"] = clip("Boss7SpecialWind", 2.0, hold=True, expressions="0:Angry,0.6:Roar,1.4:Angry", keys=[
    [0,   G(regal())],
    [0.5, G(arms(30, -30, 120, -10, 30, 40), {"Body": [6, 0, 0, 0, 0.1, 0], "Head": [10, 0, 0]})],
    [1.0, raised(0)],
    [1.5, raised(4)],
    [2.0, raised(2)],
])

clips["SpecialHit"] = clip("Boss7SpecialHit", 1.1, events={"impact": 0.15}, expressions="0:Roar,0.6:Angry", keys=[
    [0,    raised(2)],
    [0.15, G(arms(20, -30, 50, -4, 20, 0), {"Body": [-22, 0, 0, 0, -1.0, -0.3], "Head": [0, 0, 0]})],
    [0.4,  G(arms(18, -30, 48, -4, 20, 0), {"Body": [-20, 0, 0, 0, -0.9, -0.3], "Head": [4, 0, 0]})],
    [0.75, G(arms(0, -34, 30, 6, 60, 20), {"Body": [-4, 0, 0, 0, -0.3, 0], "Head": [6, 0, 0]})],
    [1.1,  G(regal())],
])

clips["Intro"] = clip("Boss7Intro", 4.2, events={"roar": 2.4, "pound": 3.35}, expressions="0:Grumpy,2.2:Roar,3.0:Angry", keys=[
    [0,    G(regal(), {"Head": [-8, 0, 0]})],
    [0.7,  G(regal(1), {"Head": [10, 28, 0]})],
    [1.3,  G(regal(-1), {"Head": [10, -28, 0]})],
    [1.9,  G(arms(-10, -34, 18, 8, 80, 30), {"Body": [-6, 0, 0, 0, -0.5, 0], "Head": [-8, 0, 0]})],
    [2.4,  G(arms(40, -60, 160, 10, 30, 10), {"Body": [16, 0, 0, 0, 0.3, 0], "Head": [28, 0, 0]})],
    [2.9,  G(arms(40, -62, 164, 10, 30, 10), {"Body": [18, 0, 0, 0, 0.35, 0], "Head": [30, 0, 0]})],
    [3.15, G(arms(30, -40, 120, -6, 30, 30), {"Body": [4, 0, 0, 0, 0.2, 0], "Head": [10, 0, 0]})],
    [3.35, G(arms(20, -36, 40, -4, 30, 0), {"Body": [-16, 0, 0, 0, -0.7, 0], "Head": [0, 0, 0]})],
    [3.6,  G(arms(10, -36, 36, 0, 40, 10), {"Body": [-10, 0, 0, 0, -0.4, 0]})],
    [4.2,  G(regal())],
])

clips["Defeat"] = clip("Boss7Defeat", 1.4, hold=True, expressions="0:Hurt,0.55:Dazed", keys=[
    [0,    REST],
    [0.3,  G(arms(10, -40, 10, 40, 20, 20), {"Body": [14, 0, 6, 0, 0.2, 0.4], "Head": [22, 10, 0]})],
    [0.7,  merge(arms(25, -20, 25, 20, 25, 25), {"Body": [-6, 0, -6, 0, -2.0, 0], "Head": [-6, -8, 0], "LeftLeg": [40, 0, -10], "RightLeg": [40, 0, 10]})],
    [1.05, merge(arms(35, -10, 35, 10, 15, 15), {"Body": [-14, 0, 0, 0, -3.2, 0], "Head": [-24, 6, 0], "LeftLeg": [80, 0, -14], "RightLeg": [80, 0, 14]})],
    [1.4,  merge(arms(32, -10, 32, 10, 15, 15), {"Body": [-12, 0, 0, 0, -3.1, 0], "Head": [-22, 4, 4], "LeftLeg": [78, 0, -14], "RightLeg": [78, 0, 14]})],
])

clips["Hurt"] = clip("Boss7Hurt", 0.6, expressions="0:Hurt,0.5:Grumpy", keys=[
    [0,    G(regal())],
    [0.08, G(arms(-16, -40, 0, 20, 40, 30), {"Body": [12, 6, 0, 0, -0.3, 0.3], "Head": [18, 10, 0]})],
    [0.25, G(regal(), {"Body": [-4, -2, 0, 0, -0.2, 0], "Head": [0, -4, 0]})],
    [0.6,  G(regal())],
])

if __name__ == "__main__":
    emit("B07", clips)
