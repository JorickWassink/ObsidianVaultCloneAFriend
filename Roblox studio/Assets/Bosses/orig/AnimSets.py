
def biped_core(tag, k=1.0, arms_out=6, walk_swing=20, walk_roll=3, heavy=1.0, extra_idle=None, extra=None, intro_roar=None, skip=(), crouch=1.0):
    """Idle / Walk / Intro / Defeat for a two-legged boss. k = size (translations scale with it).
    extra(pose_name, pose) can add per-boss bits (tail, wings) to every pose."""
    X = extra or (lambda n, p: p)
    IDLE = X("IDLE", P(None, B=[0,0,0], H=[0,0,0], LUA=[4,0,-arms_out], RUA=[4,0,arms_out], LLA=[8,0,0], RLA=[8,0,0]))
    BREATH = X("BREATH", P(drop(IDLE, -0.22*k, 2), H=[4,0,0], LUA=[6,0,-arms_out-4], RUA=[6,0,arms_out+4]))
    LOOK = X("LOOK", P(BREATH, H=[2,12,0]))
    if "Idle" not in skip:
        keys = [(0,IDLE,"IO"),(1.2,BREATH,"IO"),(2.4,IDLE,"IO")]
        if extra_idle: keys = extra_idle(IDLE, BREATH, LOOK)
        make(tag, "Idle", keys[-1][0], keys, loop=True)
    s, r = walk_swing, walk_roll
    STEP_L = X("STEP_L", P(IDLE, B=[0,0,r,0,-0.15*k*heavy,0], LL=[s+4,0,-r,0,0.5*k,0], RL=[-s,0,-r,0,0.35*k,0], LUA=[-s,0,-arms_out-6], RUA=[s,0,arms_out+6], H=[0,0,-2]))
    PASS = X("PASS", P(IDLE, B=[0,0,0,0,0.3*k*heavy,0], LUA=[4,0,-arms_out-4], RUA=[4,0,arms_out+4]))
    STEP_R = X("STEP_R", P(IDLE, B=[0,0,-r,0,-0.15*k*heavy,0], LL=[-s,0,r,0,0.35*k,0], RL=[s+4,0,r,0,0.5*k,0], LUA=[s,0,-arms_out-6], RUA=[-s,0,arms_out+6], H=[0,0,2]))
    if "Walk" not in skip:
        make(tag, "Walk", 1.2, [(0,STEP_L,"IO"),(0.3,PASS,"IO"),(0.6,STEP_R,"IO"),(0.9,PASS,"IO"),(1.2,STEP_L,"IO")], loop=True)
    DORMANT = X("DORMANT", P(drop(IDLE, 1.0*k*crouch, -16), H=[-8,0,0], LUA=[10,0,-arms_out-2], RUA=[10,0,arms_out+2], LLA=[0,0,0], RLA=[0,0,0]))
    WAKE = X("WAKE", P(drop(IDLE, -0.3*k, 0), H=[10,0,0]))
    ROAR = intro_roar or X("ROAR", P(drop(IDLE, -0.5*k, 10), H=[10,0,0], LUA=[110,0,-50], RUA=[110,0,50], LLA=[40,0,0], RLA=[40,0,0]))
    POUND = X("POUND", P(drop(IDLE, 1.0*k*crouch, -16), H=[8,0,0], LUA=[62,0,-12], RUA=[62,0,12], LLA=[10,0,0], RLA=[10,0,0]))
    if "Intro" not in skip:
        make(tag, "Intro", 4.2, [(0,DORMANT,"IO"),(0.9,P(DORMANT,H=[-4,0,0]),"OUT"),(1.8,WAKE,"IO"),
            (2.4,ROAR,"IO"),(2.7,P(ROAR,H=[9,0,3]),"IO"),(3.0,P(ROAR,H=[10,0,-3]),"IN"),(3.35,POUND,"OUT"),(3.6,POUND,"IO"),(4.2,IDLE,"LIN")],
            events={"roar":2.4, "pound":3.35})
    HIT = X("HIT", P(drop(IDLE, -0.2*k, 10, 5), H=[8,0,0], LUA=[30,0,-45], RUA=[30,0,45]))
    SLUMP = X("SLUMP", P(drop(IDLE, 1.0*k*crouch, -14, 6), H=[-8,0,5], LUA=[5,0,-25], RUA=[5,0,25], LLA=[0,0,0], RLA=[0,0,0]))
    if "Defeat" not in skip:
        make(tag, "Defeat", 1.4, [(0,IDLE,"OUT"),(0.2,HIT,"IN"),(0.65,SLUMP,"OUT"),(1.4,P(SLUMP,H=[-12,0,6]),"LIN")], hold=True)
    return dict(IDLE=IDLE, BREATH=BREATH, STEP_L=STEP_L, PASS=PASS, STEP_R=STEP_R, DORMANT=DORMANT, ROAR=ROAR, POUND=POUND, SLUMP=SLUMP)
