import itertools
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def rotate(sequence):
    """Generate all rotations of a given sequence."""
    return [sequence[i:] + sequence[:i] for i in range(len(sequence))]

def unique_permutations_with_fixed_first(n, k):
    """Find all unique permutations of k '1's in n positions under rotation, with the first position fixed to '1'."""
    if k == 0:
        return ['0' * n]
    if k == n:
        return ['1' * n]
    
    # Adjust k and n since we are fixing the first position to '1'
    k = k - 1
    n = n - 1
    
    combinations = list(itertools.combinations(range(n), k))
    unique = []

    for combo in combinations:
        sequence = ['0'] * n
        for index in combo:
            sequence[index] = '1'
        sequence = '1' + ''.join(sequence)  # Ensure the first position is '1'
        rotations = rotate(sequence)
        
        if not any(rot in unique for rot in rotations):
            unique.append(sequence)
    
    return unique

def count_overlaps(perm1, perm2):
    """Count how many times perm1 is found within any rotation of perm2."""
    k1 = perm1.count('1')
    n = len(perm2)
    overlap_count = 0
    for rot in rotate(perm2):
        for i in range(n):
            if all(perm1[j] == rot[(i + j) % n] for j in range(k1)):
                overlap_count += 1
    return overlap_count

def permutation_overlap_matrix_with_fixed_first(n):
    """Generate the overlap matrix for permutations of '1's in n positions with the first position fixed to '1'."""
    all_permutations = [unique_permutations_with_fixed_first(n, k) for k in range(n + 1)]
    
    matrix = np.zeros((n + 1, n + 1), dtype=int)
    
    for k1 in range(n + 1):
        perms_k1 = all_permutations[k1]
        for k2 in range(n + 1):
            perms_k2 = all_permutations[k2]
            for perm1 in perms_k1:
                for perm2 in perms_k2:
                    matrix[k1][k2] += count_overlaps(perm1, perm2)

    return matrix

def visualize_heatmap(matrix, n):
    """Visualize the relationship matrix as a heatmap."""
    plt.figure(figsize=(12, 10))
    sns.heatmap(matrix, annot=True, cmap='viridis', fmt='d')
    plt.title(f"Overlap Matrix for 0 to {n} '1's in {n} Positions")
    plt.xlabel("k2 (Number of '1's)")
    plt.ylabel("k1 (Number of '1's)")
    plt.show()

# Generate the overlap matrix for 12 positions with the first position fixed to '1'
positions = 12
overlap_matrix = permutation_overlap_matrix_with_fixed_first(positions)

# Visualize the overlap matrix as a heatmap
visualize_heatmap(overlap_matrix, positions)

# Print the overlap matrix for verification
print("Overlap Matrix:")
print(overlap_matrix)
