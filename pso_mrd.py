from itertools import product, combinations
import numpy as np
import galois


def generate_nonzero_vectors(F, k):
    """Generate all nonzero vectors in F^k as galois field arrays."""
    elements = F.elements
    vectors = []
    for combo in product(elements, repeat=k):
        if any(x != 0 for x in combo):
            vectors.append(F(combo))  # Returns a galois field array
    return vectors


def rank_distance(G):
    """Compute minimum rank of nonzero codewords from generator matrix G."""
    F = type(G[0, 0])
    k, n = G.shape
    vectors = generate_nonzero_vectors(F, k)
    min_rank = n
    for x in vectors:
        cw = x @ G  # codeword in F^n
        # Expand each element in cw into its vector representation over F_q
        M = np.vstack([cw[i].vector() for i in range(n)])  # Shape: n x m
        r = np.linalg.matrix_rank(M)
        min_rank = min(min_rank, r)
        if min_rank == 1:
            break
    return min_rank


def generalized_rank_weight(G, r=2):
    """Simple estimate of generalized rank weight for dimension r."""
    F = type(G[0, 0])
    k, n = G.shape
    vectors = generate_nonzero_vectors(F, k)
    weights = []
    for comb in combinations(vectors, r):
        M = np.vstack([(x @ G)[0].vector() for x in comb])
        weights.append(np.linalg.matrix_rank(M))
    return min(weights)


def initialize_particles(F, num_particles, k, n):
    return [F.Random((k, n)) for _ in range(num_particles)]


def update_velocity(pos, vel, p_best, g_best, w, c1, c2):
    """Velocity is a float matrix, not a field element."""
    r1, r2 = np.random.rand(*vel.shape), np.random.rand(*vel.shape)
    vel = w * vel + c1 * r1 * (p_best != pos) + c2 * r2 * (g_best != pos)
    return vel


def position_update(pos, vel, F, mutation_rate=0.3):
    """
    Apply element-wise probabilistic mutation using velocity as influence.
    """
    new_pos = pos.copy()
    for i in range(pos.shape[0]):
        for j in range(pos.shape[1]):
            if np.random.rand() < mutation_rate * abs(vel[i, j]):
                new_pos[i, j] = F.Random()
    return new_pos


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


if __name__ == "__main__":
    print("Testing the Implemented PSO-Guided Construction of MRD Codes in Rank Metric")
    best_G, best_score = pso_mrd_field(q=2, m=3, k=2, n=4, d_target=3, use_generalized_weight=True)
    print("Best Generator Matrix:\n", best_G)
    print("Minimum Rank Distance:", best_score)

# Expected Result:
# Testing the Implemented PSO-Guided Construction of MRD Codes in Rank Metric
# Generalized Rank Weight (r=2): 0
# Best Generator Matrix:
#  [[0 4 3 3]
#  [5 2 3 5]]
# Minimum Rank Distance: 2
