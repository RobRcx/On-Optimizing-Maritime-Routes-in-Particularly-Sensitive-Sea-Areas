import random, numpy as np

SEED = 42           
random.seed(SEED)
np.random.seed(SEED)

ships = 5
ports = 4
edges = 44
horizon = 144
# velocità media percorribile in assenza di eventi  (nm per timeslot)
NOMINAL_SPEED = 22
edge_list = [None,
             (1, 2), (1, 2), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 4),
             (2, 1), (2, 1), (2, 3), (2, 4), (2, 4),
             (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 2), (3, 4), (3, 4), (3, 4), (3, 4), (3, 4), (3, 4),
             (4, 1), (4, 2), (4, 2), (4, 3), (4, 3), (4, 3), (4, 3), (4, 3), (4, 3)]
adj_list = [
    None,
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [14, 15, 16, 17, 18],
    [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
    [36, 37, 38, 39, 40, 41, 42, 43, 44]
]

# -------------------------------
# 10 – sea-leg catalog
#    [sl_id] = (length_km, risk_class)
# risk_class → 0 = None, 1 = NW, 2 = PS, 3 = SoB, 4 = CC, 5 = Speed Reduction during piloting over the Strait
# -------------------------------
sea_legs = {
    1: (20, 1), 2: (21, 1), 3: (37, 1), 4: (64, 1), 5: (32, 1),
    6: (16, 4), 7: (23, 4), 8: (62, 4), 9: (73, 4), 10: (68, 4),
    11: (25, 0), 12: (12, 0), 13: (31, 0), 14: (41, 0), 15: (69, 0),
    16: (175, 0), 17: (241, 0), 18: (33, 4), 19: (157, 1), 20: (164, 1),
    21: (176, 0), 22: (12, 1), 23: (71, 1), 24: (154, 1), 25: (167, 1),
    26: (195, 1), 27: (122, 1), 28: (126, 1), 29: (180, 2), 30: (142, 2),
    31: (127, 2), 32: (127, 2), 33: (12, 2), 34: (8, 2), 35: (33, 3),
    36: (31, 3), 37: (32, 3), 38: (32, 5), 39: (17, 3), 40: (18, 3),
    41: (40, 2), 42: (57, 2), 43: (106, 2), 44: (21, 0), 45: (67, 0),
    46: (26, 2), 47: (98, 0), 48: (205, 0), 49: (27, 0), 50: (27, 0),
    51: (33, 0)
}

N_leg = max(sea_legs)            # numero totale di sea-leg censite

# -------------------------------
# 11 – matrice arco × sea-leg
#    0 padding dove non c’è nulla
# -------------------------------
arc_sl_map = [
    # dummy row 0 per mantenere la stessa convenzione di Pyomo
    [0]*9,
    [ 4,  5, 28, 29,  0,  0,  0,  0,  0],
    [ 4,  6, 27, 29,  0,  0,  0,  0,  0],
    [ 4,  7, 25, 33, 37, 38, 40, 46, 45],
    [ 4,  7, 25, 33, 37, 38, 39, 47,  0],
    [ 3,  8, 24, 34, 36, 38, 40, 46, 45],
    [ 3,  8, 24, 34, 36, 38, 39, 47,  0],
    [ 2,  9, 21, 22, 35, 38, 40, 46, 45],
    [ 2,  9, 21, 22, 35, 38, 39, 47,  0],
    [ 4,  5, 26, 33, 37, 38, 40, 46, 45],
    [ 4,  5, 26, 33, 37, 38, 39, 47,  0],
    [ 4,  5, 28, 30, 43, 44,  0,  0,  0],
    [ 4,  6, 27, 30, 43, 44,  0,  0,  0],
    [ 1, 10, 12, 11,  0,  0,  0,  0,  0],
    [29, 28,  5,  4,  0,  0,  0,  0,  0],
    [29, 27,  6,  4,  0,  0,  0,  0,  0],
    [42, 44,  0,  0,  0,  0,  0,  0,  0],
    [41, 31, 19, 18, 14, 13, 11,  0,  0],
    [41, 32, 20, 15, 13, 11,  0,  0,  0],
    [45, 46, 40, 38, 37, 33, 25,  7,  4],
    [47, 39, 38, 37, 33, 25,  7,  4,  0],
    [45, 46, 40, 38, 36, 34, 24,  8,  3],
    [47, 39, 38, 36, 34, 24,  8,  3,  0],
    [45, 46, 40, 38, 35, 22, 21,  9,  2],
    [47, 39, 38, 35, 22, 21,  9,  2,  0],
    [45, 46, 40, 38, 37, 33, 26,  5,  4],
    [47, 39, 38, 37, 33, 26,  5,  4,  0],
    [44, 43, 30, 28,  5,  4,  0,  0,  0],
    [44, 43, 30, 27,  6,  4,  0,  0,  0],
    [44, 42,  0,  0,  0,  0,  0,  0,  0],
    [45, 46, 40, 38, 35, 23, 16, 13, 11],
    [45, 46, 40, 38, 35, 22, 17, 13, 11],
    [47, 39, 38, 35, 23, 16, 13, 11,  0],
    [47, 39, 38, 35, 22, 17, 13, 11,  0],
    [44, 43, 32, 20, 15, 13, 11,  0,  0],
    [48, 49, 50, 51,  0,  0,  0,  0,  0],
    [11, 12, 10,  1,  0,  0,  0,  0,  0],
    [11, 13, 14, 18, 19, 31, 41,  0,  0],
    [11, 13, 15, 20, 32, 41,  0,  0,  0],
    [11, 13, 16, 23, 35, 38, 40, 46, 45],
    [11, 13, 17, 22, 35, 38, 40, 46, 45],
    [11, 13, 16, 23, 35, 38, 39, 47,  0],
    [11, 13, 17, 22, 35, 38, 39, 47,  0],
    [11, 13, 15, 20, 32, 43, 44,  0,  0],
    [51, 50, 49, 48,  0,  0,  0,  0,  0],
]
assert len(arc_sl_map) == edges+1 and all(len(r)==9 for r in arc_sl_map)

# --------------------------------------------------
# archi che contengono almeno una sea-leg di rischio 5
# --------------------------------------------------
arcs_risk5 = [e for e in range(1, edges+1)
              if any(sea_legs[sl][1] == 5 for sl in arc_sl_map[e] if sl != 0)]

# -------------------------------
# 20 – n[e]:  quante sea-leg ha l’arco e
# 21 – l_e_j[e][j]: lunghezza della j-esima sea-leg sull’arco e
# -------------------------------
n       = [0] * (edges+1)         # indice 0 inutilizzato
l_e_j   = [None] * (edges+1)      # lista di liste (e)→[None]+lunghezze

for e in range(1, edges+1):
    ids = [sl for sl in arc_sl_map[e] if sl != 0]
    n[e] = len(ids)
    l_e_j[e] = [0] + [sea_legs[sl][0] for sl in ids]   # prepend 0 per j=0

# -------------------------------
# 22 – dist_min (qui a 0)  e  dist_max con rischio proporzionato
# -------------------------------

l_e = [None] + [ sum(l_e_j[e][1:]) for e in range(1, edges+1) ]

mathcalE = [None,
            [None, [],     [1, 2], [3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [13]],
            [None, [14, 15],    [],  [16], [17, 18]],
            [None, [19, 20, 21, 22, 23, 24, 25, 26, 27, 28], [29], [], [30, 31, 32, 33, 34, 35]],
            [None, [36], [37, 38], [39, 40, 41, 42, 43, 44], []]]

import random, numpy as np
EVENT_RATE_BASE      = 0.0        # eventi per nm per rischio 2
RISK_MULTIPLIER      = {0: 0.0, 1: 0.5, 2: 1.0, 3: 1.5, 4: 2.0, 5: 0.0}
MAX_EVENT_DURATION   = 6
SLOW_FACTOR_RANGE    = (0.4, 0.6)

# --------------------------------------------------
# dist_min = 0 (non vincolante)
# dist_max = velocità_nominale × modificatore_meteo
# --------------------------------------------------
dist_min = [None]
dist_max = [None]

for e in range(1, edges + 1):
    dist_min_e, dist_max_e = [None], [None]

    for j, sl_id in enumerate(arc_sl_map[e], start=1):
        if sl_id == 0:                   # padding oltre n[e]
            break
        length, risk = sea_legs[sl_id]   # lunghezza, classe di rischio

        # --- dist_min: sempre 0
        dist_min_e.append([None] + [0]*horizon)

        # --- profilo meteo → modificatore_t
        mod = [1.0]*(horizon + 1)        # indice 0 dummy
        lam = EVENT_RATE_BASE * RISK_MULTIPLIER[risk] * length
        for _ in range(np.random.poisson(lam)):
            start  = random.randint(1, horizon)
            dur    = random.randint(1, MAX_EVENT_DURATION)
            fac    = random.uniform(*SLOW_FACTOR_RANGE)
            for t in range(start, min(horizon + 1, start + dur)):
                mod[t] *= fac           # riduce la velocità

        # --- dist_max per ciascun t = velocità effettiva in km/slot
        dist_max_e.append(
            [None] + [max(1, int(NOMINAL_SPEED * mod[t]))
                       for t in range(1, horizon + 1)]
        )

    dist_min.append(dist_min_e)
    dist_max.append(dist_max_e)

mathcalR = [None,
    [0, 1, 2, 3],
    [0, 3, 2, 1],
    [0, 4, 1, 2, 3],
    [0, 4, 1, 3, 2],
    [0, 3, 4, 1, 2]
]
R = [None] + [len(x) - 1 for x in mathcalR[1:]]

# --------------------------------------------------
# Delta automatico: permanenza minima in porto = 0
# ⇒ Δ = (# sea-leg fra i due porti) + 1
# --------------------------------------------------
Delta = [None]                      # indice 0 dummy

for s in range(1, ships + 1):
    row = [None]                   # Delta[s][0] non usato

    # --- per ogni TRATTA prev→nxt (i = 1 … R[s]−1)
    for i in range(1, R[s]):       # R[s] − 1 tratte
        prev = mathcalR[s][i]
        nxt  = mathcalR[s][i + 1]
        seg  = len(mathcalE[prev][nxt])    # sea-leg da percorrere
        row.append(seg + 1)                # permanenza minima = 0

    # --- per l’ULTIMO PORTO (i = R[s]) non c’è navigazione dopo
    #     metti la permanenza minima che preferisci, es. 1 timeslot
    row.append(1)

    Delta.append(row)

# verifica lunghezza: deve essere R[s] + 1 (padding incluso)
for s in range(1, ships + 1):
    assert len(Delta[s]) - 1 == R[s], f"Delta row {s} malformata"

m = [None,
    [None, 5, 60, 85],
    [None, 5, 30, 85],
    [None, 10, 30, 60, 90],
    [None, 5, 28, 80, 110],
    [None, 5, 60, 100, 160]
]
# Error checking: |m[s]| - 1 == R[s]
assert(len(m) == len(R))
for s in range(1, len(R)):
    assert len(m[s]) - 1 == R[s]

unit_cost = 3.37

M = 100000000

# 0 padding  | nave1 | nave2 | nave3 | nave4 | nave5
vessels_type = [0,      2,      2,      2,      1,      2]

forbidden = [[1 for e in range(edges + 1)] for s in range(ships + 1)]

# --------------------------------------------------
# blocco di transito ai tipi di nave vietati (tipo 1) sugli archi risk-5
# --------------------------------------------------
for s in range(1, ships + 1):
    if vessels_type[s] == 1:                  # tipo vietato
        for e in arcs_risk5:
            forbidden[s][e] = 0               # inammissibile: x[s,e] ≤ 0

# vessels_type is $\tau_{v}$; 1 for forbidden access, 2 for regular container ship

# -----------------------------------------------------------
# CAPACITY 1 per sea-leg con rischio 2, 3 o 4
# -----------------------------------------------------------
capacity_constrained_edges = []        # lista di archi e
capacity_constrained_sea_legs = {}     # e → [j1, j2, …]
max_capacity = {}                      # (e, j) → 1

for e in range(1, edges + 1):
    ids = [sl for sl in arc_sl_map[e] if sl != 0]          # sea-leg IDs sull’arco
    risky_idx = [j+1 for j, sl in enumerate(ids)           # j parte da 1
                 if sea_legs[sl][1] in (2, 3, 4)]          # rischio ≥2
    if risky_idx:                                          # almeno una sea-leg “rischiosa”
        capacity_constrained_edges.append(e)
        capacity_constrained_sea_legs[e] = risky_idx
        for j in risky_idx:
            max_capacity[(e, j)] = 1                       # capacità = 1
