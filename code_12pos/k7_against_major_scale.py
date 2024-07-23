import itertools
import numpy as np
import matplotlib.pyplot as plt
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

def match_scale_to_known(scale):
    """Match a scale to a known scale if possible."""
    for name, known_scale in known_scales.items():
        if scale in rotate(known_scale):
            return name
    return None

def rotate_to_ionian_start(pattern, ionian_pattern="101011010101"):
    """Rotate the pattern to start with the same sequence as the Ionian pattern."""
    rotations = rotate(pattern)
    for rot in rotations:
        if rot.startswith(ionian_pattern):
            return rot
    return pattern

def collect_visualizations(results, target_scale):
    """Collect the pattern matches with minimum dissimilarity as visualizations."""
    visualizations = []
    
    for pattern, min_dissimilarity, matches in results:
        for pat_rot, target_rot in matches:
            pat_rot = rotate_to_ionian_start(pat_rot)  # Ensure the pattern starts with the Ionian mode sequence
            target_rot = rotate_to_ionian_start(target_rot)  # Ensure the Ionian mode sequence is correctly aligned
            pat_rot_array = np.array([int(char) for char in pat_rot])
            target_rot_array = np.array([int(char) for char in target_rot])
            combined_array = np.vstack((target_rot_array, pat_rot_array))
            matched_scale = match_scale_to_known(pat_rot)
            visualizations.append((min_dissimilarity, combined_array, pattern, matched_scale))
    
    return visualizations

def plot_all_visualizations(visualizations, output_file):
    """Plot all visualizations in a single figure, sorted by dissimilarity."""
    visualizations.sort(key=lambda x: x[0])  # Sort by dissimilarity
    
    total_visualizations = len(visualizations)
    fig_height = total_visualizations * 2
    fig, axs = plt.subplots(total_visualizations, 1, figsize=(12, fig_height))
    
    for idx, (dissimilarity, combined_array, pattern, matched_scale) in enumerate(visualizations):
        axs[idx].imshow(combined_array, cmap='binary', aspect='auto')
        title = f"Pattern: {pattern}, Dissimilarity: {dissimilarity}"
        if matched_scale:
            title += f", Matches: {matched_scale}"
        axs[idx].set_title(title, fontsize=12)
        axs[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

# Define the major scale (Ionian) in binary representation
major_scale = "101011010101"

# Generate all unique 7-note patterns with 7 '1's in 12 positions
patterns = unique_permutations_with_fixed_first(12, 7)

# Find the minimum dissimilarity for each pattern
min_dissimilarity_results = find_min_dissimilarity(patterns, major_scale)

# Collect visualizations
visualizations = collect_visualizations(min_dissimilarity_results, major_scale)

# Define the output file
output_file = r"C:\Users\ptgyo\pitch-permutations-main\scales in 12 positions media\k7 compared to major scale\combined.png"

# Plot all visualizations in a single sorted figure
plot_all_visualizations(visualizations, output_file)
