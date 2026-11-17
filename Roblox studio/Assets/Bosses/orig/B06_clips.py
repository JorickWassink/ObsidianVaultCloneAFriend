# Paladin Rhino (Boss 6) clips, original quadruped skeleton (ADR 0017). Names, lengths, Hold and Event_ match the old
# clips (Strike impact 0.55; SpecialHit impact 0.1 / stomp 0.6; Intro roar 2.4 / pound 3.35) + Hurt.
# Paladin Stampede: SpecialWind scrapes the ground with a front hoof (head low, horn forward) and holds; Charge is a looping
# gallop; SpecialHit = slams through at 0.1, rears up and stomps at 0.6. Strike = horn toss.
# Body pivot is near the middle (front hips ~3.8 studs ahead, back hips ~5 behind); rearing lifts the Body so the back feet stay down.
from clipkit import *

L4 = LEGS4
def Q(*ts): return G(*ts, legs=L4)

def stand(sway=0, breathe=0.0):
    return {"Body": [0, sway, 0, 0, breathe, 0], "Head": [-4, -sway * 1.5, 0], "Tail": [10, sway * 3, 0]}

clips = {}
clips["Idle"] = clip("Boss6Idle", 2.8, loop=True, priority="Idle", expressions="0:Grumpy,1.6:Blink,1.75:Grumpy", keys=[
    [0,   Q(stand(0, 0.0))],
    [0.7, Q(stand(3, 0.15), {"Head": [-10, -6, 0]})],
    [1.4, Q(stand(0, 0.0), {"Head": [-2, 0, 0], "Tail": [10, 14, 0]})],
    [2.1, Q(stand(-3, 0.15), {"Head": [-10, 6, 0]})],
    [2.8, Q(stand(0, 0.0))],
])

def walk(s):
    # diagonal pairs: LF+RB forward when s=1
    return Q({"Body": [0, 2 * s, 2 * s, 0, -0.1, 0], "Head": [-6, -3 * s, 0], "Tail": [10, -8 * s, 0],
              "LeftFrontLeg": [22 * s, 0, 0], "RightBackLeg": [22 * s, 0, 0],
              "RightFrontLeg": [-22 * s, 0, 0], "LeftBackLeg": [-22 * s, 0, 0]})
def wpass(s):
    return Q({"Body": [0, 0, 0, 0, 0.15, 0], "Head": [-4, 0, 0], "Tail": [10, 0, 0],
              "LeftFrontLeg": [-14 * s, 0, 0, 0, 0.5, 0], "RightBackLeg": [-14 * s, 0, 0, 0, 0.5, 0],
              "RightFrontLeg": [6 * s, 0, 0], "LeftBackLeg": [6 * s, 0, 0]})
clips["Walk"] = clip("Boss6Walk", 1.0, loop=True, priority="Movement", expressions="0:Grumpy", keys=[
    [0, walk(1)], [0.25, wpass(-1)], [0.5, walk(-1)], [0.75, wpass(1)], [1.0, walk(1)]])

# gallop: gather (all legs under) -> extend (front reach, back push) ; body pitches and bounces
def gather():
    return merge({"Body": [-4, 0, 0, 0, 0.9, 0], "Head": [-18, 0, 0], "Tail": [-10, 0, 0],
                  "LeftFrontLeg": [-30, 0, 0], "RightFrontLeg": [-20, 0, 0], "LeftBackLeg": [34, 0, 0], "RightBackLeg": [24, 0, 0]})
def extend():
    return merge({"Body": [6, 0, 0, 0, 0.3, 0], "Head": [-24, 0, 0], "Tail": [-20, 0, 0],
                  "LeftFrontLeg": [40, 0, 0], "RightFrontLeg": [30, 0, 0], "LeftBackLeg": [-36, 0, 0], "RightBackLeg": [-26, 0, 0]})
clips["Charge"] = clip("Boss6Charge", 0.5, loop=True, expressions="0:Angry", keys=[
    [0, gather()], [0.25, extend()], [0.5, gather()]])

clips["Strike"] = clip("Boss6Strike", 1.05, events={"impact": 0.55}, expressions="0:Angry,0.95:Grumpy", keys=[
    [0,    Q(stand())],
    [0.3,  Q({"Body": [-6, 10, 0, 0, -0.5, 0.4], "Head": [-28, 14, 0], "Tail": [16, 0, 0],
              "LeftFrontLeg": [10, 0, 0], "RightFrontLeg": [10, 0, 0]})],
    [0.45, Q({"Body": [-8, 6, 0, 0, -0.7, 0.2], "Head": [-34, 10, 0], "Tail": [16, 0, 0]})],
    [0.55, Q({"Body": [6, -14, 0, 0, 0.2, -0.8], "Head": [26, -18, 0], "Tail": [-6, -10, 0],
              "LeftFrontLeg": [-10, 0, 0], "RightFrontLeg": [-10, 0, 0]})],
    [0.7,  Q({"Body": [4, -12, 0, 0, 0.1, -0.6], "Head": [20, -14, 0], "Tail": [0, -8, 0]})],
    [1.05, Q(stand())],
])

def scrape(up):
    # right front hoof paws backward along the ground; head low, horn forward
    leg = [-30, 0, 0, 0, 0.8, 0] if up else [24, 0, 0, 0, 0.2, 0]
    return Q({"Body": [-6, 0, 0, 0, -0.5, 0], "Head": [-30, 0, 0], "Tail": [20, 0, 0],
              "RightFrontLeg": leg, "LeftBackLeg": [6, 0, 0], "RightBackLeg": [6, 0, 0]})
clips["SpecialWind"] = clip("Boss6SpecialWind", 1.5, hold=True, expressions="0:Angry", keys=[
    [0, Q(stand())], [0.3, scrape(1)], [0.55, scrape(0)], [0.8, scrape(1)], [1.05, scrape(0)],
    [1.5, Q({"Body": [-8, 0, 0, 0, -0.7, 0], "Head": [-32, 0, 0], "Tail": [24, 0, 0],
             "LeftBackLeg": [10, 0, 0], "RightBackLeg": [10, 0, 0]})],
])

clips["SpecialHit"] = clip("Boss6SpecialHit", 1.1, events={"impact": 0.1, "stomp": 0.6}, expressions="0:Angry,0.35:Roar,0.8:Angry", keys=[
    [0,    extend()],
    [0.1,  Q({"Body": [-6, 0, 0, 0, -0.4, -0.6], "Head": [10, 0, 0], "Tail": [-10, 0, 0],
              "LeftFrontLeg": [30, 0, 0], "RightFrontLeg": [30, 0, 0], "LeftBackLeg": [-10, 0, 0], "RightBackLeg": [-10, 0, 0]})],
    [0.4,  merge({"Body": [34, 0, 0, 0, 3.0, 0], "Head": [10, 0, 0], "Tail": [30, 0, 0],
                  "LeftFrontLeg": [30, 0, 0], "RightFrontLeg": [50, 0, 0], "LeftBackLeg": [-28, 0, 0, 0, -3.0, 0], "RightBackLeg": [-28, 0, 0, 0, -3.0, 0]})],
    [0.6,  Q({"Body": [-8, 0, 0, 0, -0.8, 0], "Head": [-14, 0, 0], "Tail": [6, 0, 0],
              "LeftFrontLeg": [6, 0, 0], "RightFrontLeg": [6, 0, 0]})],
    [0.75, Q({"Body": [-6, 0, 0, 0, -0.6, 0], "Head": [-10, 0, 0]})],
    [1.1,  Q(stand())],
])

clips["Intro"] = clip("Boss6Intro", 4.2, events={"roar": 2.4, "pound": 3.35}, expressions="0:Grumpy,2.2:Roar,3.0:Angry", keys=[
    [0,    Q(stand(), {"Head": [-16, 0, 0]})],
    [0.7,  Q(stand(4), {"Head": [-6, -24, 0]})],
    [1.3,  Q(stand(-4), {"Head": [-6, 24, 0]})],
    [1.6,  scrape(1)], [1.85, scrape(0)],
    [2.4,  merge({"Body": [28, 0, 0, 0, 2.5, 0], "Head": [30, 0, 0], "Tail": [30, 0, 0],
                  "LeftFrontLeg": [30, 0, 0], "RightFrontLeg": [44, 0, 0], "LeftBackLeg": [-24, 0, 0, 0, -2.5, 0], "RightBackLeg": [-24, 0, 0, 0, -2.5, 0]})],
    [2.9,  merge({"Body": [30, 0, 0, 0, 2.6, 0], "Head": [32, 0, 0], "Tail": [32, 0, 0],
                  "LeftFrontLeg": [44, 0, 0], "RightFrontLeg": [30, 0, 0], "LeftBackLeg": [-26, 0, 0, 0, -2.6, 0], "RightBackLeg": [-26, 0, 0, 0, -2.6, 0]})],
    [3.35, Q({"Body": [-8, 0, 0, 0, -0.8, 0], "Head": [-16, 0, 0], "Tail": [6, 0, 0]})],
    [3.6,  Q({"Body": [-4, 0, 0, 0, -0.4, 0], "Head": [-10, 0, 0]})],
    [4.2,  Q(stand())],
])

clips["Defeat"] = clip("Boss6Defeat", 1.4, hold=True, expressions="0:Hurt,0.55:Dazed", keys=[
    [0,    REST],
    [0.3,  Q({"Body": [6, 0, 6, 0, 0.3, 0], "Head": [20, 10, 0], "Tail": [20, 0, 0]})],
    [0.7,  merge({"Body": [-8, 0, -4, 0, -1.6, 0], "Head": [-10, -8, 0], "Tail": [30, 0, 0],
                  "LeftFrontLeg": [60, 0, 0], "RightFrontLeg": [60, 0, 0], "LeftBackLeg": [-30, 0, 0], "RightBackLeg": [-30, 0, 0]})],
    [1.05, merge({"Body": [0, 0, -8, 0, -3.0, 0], "Head": [-20, 6, 8], "Tail": [40, 10, 0],
                  "LeftFrontLeg": [70, 0, -10], "RightFrontLeg": [70, 0, 10], "LeftBackLeg": [-70, 0, -10], "RightBackLeg": [-70, 0, 10]})],
    [1.4,  merge({"Body": [0, 0, -8, 0, -2.9, 0], "Head": [-18, 4, 10], "Tail": [38, 10, 0],
                  "LeftFrontLeg": [68, 0, -10], "RightFrontLeg": [68, 0, 10], "LeftBackLeg": [-68, 0, -10], "RightBackLeg": [-68, 0, 10]})],
])

clips["Hurt"] = clip("Boss6Hurt", 0.6, expressions="0:Hurt,0.5:Grumpy", keys=[
    [0,    Q(stand())],
    [0.08, Q({"Body": [6, 6, 0, 0, -0.3, 0.5], "Head": [18, 12, 0], "Tail": [30, 0, 0]})],
    [0.25, Q({"Body": [-2, -2, 0, 0, -0.2, 0], "Head": [-8, -4, 0]})],
    [0.6,  Q(stand())],
])

if __name__ == "__main__":
    emit("B06", clips)
