# Requirements
# Install the galois library: pip install galois (if you use pip)

import numpy as np
import galois

def generate_nonzero_vectors(F, k):
    """Generate all nonzero vectors in F^k"""
    N = F.order ** k
    vectors = []
    for i in range(1, N):  # skip zero vector
        x = F.Vector(np.array(list(np.base_repr(i, base=F.order).zfill(k)), dtype=int))
        if len(x) < k:
            x = np.concatenate((np.zeros(k - len(x), dtype=int), x))
        vectors.append(F(x))
    return vectors

def rank_distance(G):
    """Compute minimum rank of nonzero codewords from generator matrix G."""
    F = type(G[0,0])
    k, n = G.shape
    vectors = generate_nonzero_vectors(F, k)
    min_rank = n
    for x in vectors:
        cw = x @ G  # codeword in F^n
        M = np.vstack([cw[i].vector() for i in range(n)])  # expand to F_q^m
        r = np.linalg.matrix_rank(M)
        min_rank = min(min_rank, r)
        if min_rank == 1:
            break
    return min_rank

def generalized_rank_weight(G, r=2):
    """Simple estimate of generalized rank weight for dimension r."""
    F = type(G[0,0])
    from itertools import combinations
    k, n = G.shape
    vectors = generate_nonzero_vectors(F, k)
    weights = []
    for comb in combinations(vectors, r):
        M = np.vstack([(x @ G).reshape(1, -1)[0].vector() for x in comb])
        weights.append(np.linalg.matrix_rank(M))
    return min(weights)

def initialize_particles(F, num_particles, k, n):
    return [F.Random((k, n)) for _ in range(num_particles)]

def update_velocity(pos, vel, p_best, g_best, w, c1, c2):
    r1, r2 = np.random.rand(), np.random.rand()
    return w * vel + c1 * r1 * (p_best - pos) + c2 * r2 * (g_best - pos)

def position_update(pos, vel, F):
    """Thresholded random mutation from velocity, reprojected to field."""
    sigmoid = 1 / (1 + np.exp(-vel))
    binary_matrix = (np.random.rand(*pos.shape) < sigmoid).astype(int)
    return F(binary_matrix)

def pso_mrd_field(q=2, m=3, k=2, n=4, d_target=3, num_particles=8, max_iter=50, use_generalized_weight=False):
    F = galois.GF(q**m)
    particles = initialize_particles(F, num_particles, k, n)
    velocities = [np.zeros((k, n)) for _ in range(num_particles)]
    p_bests = particles[:]
    p_best_scores = [rank_distance(p) for p in particles]

    g_best_idx = int(np.argmax(p_best_scores))
    g_best = p_bests[g_best_idx]
    g_best_score = p_best_scores[g_best_idx]

    w, c1, c2 = 0.5, 1.5, 1.5

    for _ in range(max_iter):
        for i in range(num_particles):
            velocities[i] = update_velocity(particles[i], velocities[i], p_bests[i], g_best, w, c1, c2)
            particles[i] = position_update(particles[i], velocities[i], F)
            score = rank_distance(particles[i])

            if score > p_best_scores[i]:
                p_bests[i] = particles[i]
                p_best_scores[i] = score

                if score > g_best_score:
                    g_best = particles[i]
                    g_best_score = score

            if g_best_score >= d_target:
                break

    if use_generalized_weight:
        grw = generalized_rank_weight(g_best)
        print("Generalized Rank Weight (r=2):", grw)

    return g_best, g_best_score

# Example usage
best_G, best_score = pso_mrd_field(q=2, m=3, k=2, n=4, d_target=3, use_generalized_weight=True)
print("Best Generator Matrix:\n", best_G)
print("Minimum Rank Distance:", best_score)
