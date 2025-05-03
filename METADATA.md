# Mapping of the variable names in "instance.json" to the paper notation.

ships : n_S ships, S = {1, … , n_S} with n_S ≥ 1

ports : set of nP ports, P = {1, … , n_P} with n_P ≥ 2

edges : E = {1, … , n_E}, set of n_E directed edges in the graph

horizon : time horizon partitioned into K time slots of equal duration, T = {1, … , K}

NOMINAL_SPEED : speed of the ships without any PSSA constraint

edge_list[e] : head and tail of every directed edge

adj_list : index of every edge

sea_legs[sl_id] = (len, risk): sea leg index, length and risk class

N_leg : total number of sea legs

arc_sl_map[e][j] = sl_id: sea leg indexes that constitute every edge

arcs_risk5 : edges that have a risk class 5 (forbidden area for specific types of ships) sea leg

n[e] : number of sea legs of edge e

l_e[e]: length of edge e

l_e_j[e][j] : length of the j-th sea leg of edge e

mathcalE[p][q]: edges that connect port p with port q

EVENT_RATE_BASE: events every 100 nm

RISK_MULTIPLIER: scale factor of the event rate for every risk class area

MAX_EVENT_DURATION: number of timeslots in which the effect of the disruption persists

SLOW_FACTOR_RANGE: range of speed reduction if a disruption event occurs

dist_min[e][j][t]: minimum distance covered by a ship on the seal leg j of the edge e in the timeslot t

dist_max[e][j][t]: maximum distance covered by a ship on the seal leg j of the edge e in the timeslot t

mathcalR[s]: ordered sequence of distinct ports of call (port rotation)

R[s]: number of port call for each ship

Delta[s][p]: duration of port operations

m: deadline ms,i, denoting the largest time slot within which ship s must complete operations at its i-th port of call, namely ps,i, to avoid penalty costs

M: big M

vessels_type: wS ∈ W be the type of ship s ∈ S

forbidden[s][e]: 0 if a ship type cannot enter that edge

capacity_constrained_edges: edges that have at least a capacity constrained sealeg

capacity_constrained_sea_legs: j-th sealeg that is capacity constrained for each edge
