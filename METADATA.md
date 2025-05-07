## Mapping of the variable names in "instance.json" to the notation used in the paper

<b>name of the variable in "instance.json" : notation used in the paper</b>

ships : n_S ships, S = {1, … , n_S} with n_S ≥ 1

ports : set of nP ports, P = {1, … , n_P} with n_P ≥ 2

edges : set E = {1, … , n_E} of n_E directed edges in the graph

horizon : time horizon partitioned into a set T = {1, … , K} of K ≥ 1 time slots of equal duration

NOMINAL_SPEED : speed of the ships without any PSSA constraint

edge_list[e] : head and tail of edge e

adj_list[p] : indices of the edges having p as head

sea_legs[sl_id] = (len, risk) : length and risk class corrisponding to the sea leg having index sl_id

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

dist_min[e][j][t]: minimum distance to be covered by a ship in the j-th sea leg of edge e in time slot t

dist_max[e][j][t]: maximum distance to be covered by a ship in the j-th sea leg of edge e in time slot t

mathcalR[s]: ordered sequence of distinct ports of call (port rotation) of ship s

R[s]: number of port call of ship s

Delta[s][p]: duration of port operation of ship s at port p

m[s][i]: deadline of ship s at port p, denoting the largest time slot within which ship s must complete operations at its i-th port of call to avoid penalty costs

M: big-M used for constraints

vessels_type[s]: type of ship s ∈ S

forbidden[s][e]: equal to 0 if ship s cannot enter edge e, and equal to 1 otherwise

capacity_constrained_edges: edges that have at least a capacity-constrained sealeg

capacity_constrained_sea_legs[e]: sea legs of e that are capacity-constrained
