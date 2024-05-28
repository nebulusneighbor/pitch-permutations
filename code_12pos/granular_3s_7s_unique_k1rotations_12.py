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
    """Count how many times perm1 overlaps within any rotation of perm2."""
    k1 = perm1.count('1')
    n = len(perm2)
    overlap_count = 0
    for rot in rotate(perm2):
        for i in range(n):
            if all(perm1[j] == rot[(i + j) % n] for j in range(k1)):
                overlap_count += 1
    return overlap_count

def permutation_overlap_counts_with_fixed_first(n, k1, k2):
    """Generate the overlap counts for permutations of k1 '1's in permutations of k2 '1's with the first position fixed to '1'."""
    perms_k1 = unique_permutations_with_fixed_first(n, k1)
    perms_k2 = unique_permutations_with_fixed_first(n, k2)
    
    overlap_counts = np.zeros((len(perms_k1), len(perms_k2)), dtype=int)
    
    for i, perm1 in enumerate(perms_k1):
        for j, perm2 in enumerate(perms_k2):
            overlap_counts[i][j] = count_overlaps(perm1, perm2)
    
    return overlap_counts

def visualize_heatmap(overlap_counts, k1, k2):
    """Visualize the overlap counts as a heatmap."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(overlap_counts, annot=True, cmap='viridis', fmt='d')
    plt.title(f"Overlap Counts of {k1} '1's in {k2} '1's with the First Position Fixed")
    plt.xlabel(f"Unique Permutations of {k2} '1's")
    plt.ylabel(f"Unique Permutations of {k1} '1's")
    plt.show()

# Calculate overlaps of 3 '1's in 7 '1's in 12 positions with the first position fixed to '1'
positions = 12
k1 = 3
k2 = 7
overlap_counts = permutation_overlap_counts_with_fixed_first(positions, k1, k2)

# Calculate the sum of all elements in the overlap counts matrix
total_overlaps = np.sum(overlap_counts)

# Print the total overlaps
print(f"Total Overlaps of {k1} '1's in {k2} '1's: {total_overlaps}")

# Visualize the overlap counts as a heatmap
visualize_heatmap(overlap_counts, k1, k2)