import random
import itertools
import time

class UnDirectedGraph:
    def __init__(self):
        self.graph = {}
    def get_vertices(self):
        return list(self.graph.keys())
    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []
    def add_edge(self, u, v):
        if u == v:
            return
        self.graph.setdefault(u, []).append(v)
        self.graph.setdefault(v, []).append(u)
    def adj(self, v):
        return self.graph[v]

def create_random_graph(n, m):
    g = UnDirectedGraph()
    for i in range(n):
        g.add_vertex(i)
    added = 0
    while added < m:
        u, v = random.randrange(n), random.randrange(n)
        if v not in g.adj(u):
            g.add_edge(u, v)
            added += 1
    return g

def check_valid(g, assign):
    for u in g.get_vertices():
        for v in g.adj(u):
            if assign[u] == assign[v]:
                return False
    return True

def brute_force_coloring(g, k):
    verts = g.get_vertices()
    for prod in itertools.product(range(k), repeat=len(verts)):
        assign = {verts[i]: prod[i] for i in range(len(verts))}
        if check_valid(g, assign):
            return assign
    return None

def backtracking_coloring(g, k):
    verts = sorted(g.get_vertices(), key=lambda v: len(g.adj(v)), reverse=True)
    assign = {}
    return assign if dfs_color(g, verts, assign, 0, k) else None

def dfs_color(g, verts, assign, idx, k):
    if idx == len(verts):
        return True
    u = verts[idx]
    for c in range(k):
        if all(assign.get(nb) != c for nb in g.adj(u)):
            assign[u] = c
            if dfs_color(g, verts, assign, idx + 1, k):
                return True
            del assign[u]
    return False

if __name__ == '__main__':
    N = 50
    V, E = 10, 20
    Ks = [2, 3, 4]
    results = []

    for i in range(N):
        G = create_random_graph(V, E)
        for k in Ks:
            t0 = time.perf_counter()
            bf_sol = brute_force_coloring(G, k)
            t1 = time.perf_counter()
            bt_sol = backtracking_coloring(G, k)
            t2 = time.perf_counter()

            results.append({
                'trial': i + 1,
                'k': k,
                'bf_time': (t1 - t0) * 1000,
                'bt_time': (t2 - t1) * 1000,
                'bf_ok': bf_sol is not None,
                'bt_ok': bt_sol is not None,
                'bf_sol': bf_sol,
                'bt_sol': bt_sol
            })

    # Diferencias de tiempos
    print("\nResumen promedio:")
    for k in Ks:
        times_bf = [r['bf_time'] for r in results if r['k'] == k]
        times_bt = [r['bt_time'] for r in results if r['k'] == k]
        ok_bf = sum(r['bf_ok'] for r in results if r['k'] == k)
        ok_bt = sum(r['bt_ok'] for r in results if r['k'] == k)
        avg_bf = sum(times_bf) / len(times_bf)
        avg_bt = sum(times_bt) / len(times_bt)
        print(f"k={k}: fuerza bruta ≈ {avg_bf:.3f}ms ({ok_bf}/{N} casos resueltos), "
              f"backtracking ≈ {avg_bt:.3f}ms ({ok_bt}/{N} casos resueltos)")

    # Guardar resultados
    with open("resultados.txt", "w") as f:
        f.write("Trial | k | BF_solution               | BT_solution\n")
        f.write("------|---|---------------------------|---------------------------\n")
        for r in results:
            bf_str = str(r['bf_sol']) if r['bf_sol'] is not None else ""
            bt_str = str(r['bt_sol']) if r['bt_sol'] is not None else ""
            f.write(f"{r['trial']:5d} | {r['k']:1d} | {bf_str:<25s} | {bt_str:<25s}\n")