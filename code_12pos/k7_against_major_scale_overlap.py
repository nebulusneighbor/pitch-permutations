import itertools
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define known scales and their binary representations
known_scales = {
    "Harmonic Minor": "101101011001",
    "Harmonic Major": "101011010011",
    "Hungarian Minor": "101101101001",
    "Hungarian Major": "101010111001",
    "Double Harmonic": "110101011001"
}

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

def calculate_dissimilarity(seq1, seq2):
    """Calculate the number of dissimilar positions between two sequences."""
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))

def find_min_dissimilarity(patterns, target_scale):
    """Find the minimum dissimilarity between rotations of the target scale and given patterns."""
    target_rotations = rotate(target_scale)
    
    min_dissimilarity_results = []
    
    for pattern in patterns:
        pattern_rotations = rotate(pattern)
        min_dissimilarity = float('inf')
        best_matches = []
        
        for pat_rot in pattern_rotations:
            for target_rot in target_rotations:
                dissimilarity = calculate_dissimilarity(pat_rot, target_rot)
                if dissimilarity < min_dissimilarity:
                    min_dissimilarity = dissimilarity
                    best_matches = [(pat_rot, target_rot)]
                elif dissimilarity == min_dissimilarity:
                    best_matches.append((pat_rot, target_rot))
        
        unique_matches = []
        seen_patterns = set()
        for pat_rot, target_rot in best_matches:
            pat_tuple = tuple(int(char) for char in pat_rot)
            if pat_tuple not in seen_patterns:
                seen_patterns.update(tuple(int(char) for char in rot) for rot in rotate(pat_rot))
                unique_matches.append((pat_rot, target_rot))
        
        min_dissimilarity_results.append((pattern, min_dissimilarity, unique_matches))
    
    return min_dissimilarity_results

def generate_overlap_matrix(patterns, ionian_pattern):
    """Generate an overlap matrix for the dissimilarity numbers."""
    num_patterns = len(patterns)
    overlap_matrix = np.zeros((num_patterns, num_patterns))
    
    ionian_rotations = rotate(ionian_pattern)
    
    for i, pattern in enumerate(patterns):
        min_dissimilarity = float('inf')
        for ionian_rot in ionian_rotations:
            dissimilarity = calculate_dissimilarity(pattern, ionian_rot)
            if dissimilarity < min_dissimilarity:
                min_dissimilarity = dissimilarity
        for j in range(num_patterns):
            overlap_matrix[i, j] = min_dissimilarity
    
    return overlap_matrix

def plot_overlap_matrix(overlap_matrix, output_file):
    """Plot the overlap matrix as a heatmap."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(overlap_matrix, annot=True, cmap='viridis', fmt='.0f', cbar=True)
    plt.title("Dissimilarity Overlap Matrix")
    plt.xlabel("Pattern Index")
    plt.ylabel("Pattern Index")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

# Define the major scale (Ionian) in binary representation
major_scale = "101011010101"

# Generate all unique 7-note patterns with 7 '1's in 12 positions
patterns = unique_permutations_with_fixed_first(12, 7)

# Find the minimum dissimilarity for each pattern
min_dissimilarity_results = find_min_dissimilarity(patterns, major_scale)

# Extract patterns for the overlap matrix
patterns_only = [result[0] for result in min_dissimilarity_results]

# Generate the overlap matrix
overlap_matrix = generate_overlap_matrix(patterns_only, major_scale)

# Define the output file for the overlap matrix
overlap_matrix_file = r"C:\Users\ptgyo\pitch-permutations-main\scales in 12 positions media\k7 compared to major scale\overlap_matrix.png"

# Plot the overlap matrix as a heatmap
plot_overlap_matrix(overlap_matrix, overlap_matrix_file)
