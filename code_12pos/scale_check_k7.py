import itertools
import numpy as np
import matplotlib.pyplot as plt

# Define the known heptatonic scales and their binary representations
known_scales = {
    "Ionian (Major Scale)": "101011010101",
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
    # Adjust k since we are fixing the first position to '1'
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

def match_known_scales(sequences, known_scales):
    """Match the given sequences to known scales and their rotations."""
    matches = []
    for seq in sequences:
        for scale_name, scale in known_scales.items():
            if seq in rotate(scale):
                matches.append((seq, scale_name))
                break
    return matches

def visualize_rotations(n, k, output_file, known_scales):
    """Visualize the unique rotations for a given n and k."""
    unique_rots = unique_permutations_with_fixed_first(n, k)
    num_rots = len(unique_rots)
    
    fig, axs = plt.subplots(num_rots, 1, figsize=(12, num_rots * 1.5))  # Increase width and spacing
    matches = match_known_scales(unique_rots, known_scales)
    for i, rot in enumerate(unique_rots):
        rot_array = np.array([int(char) for char in rot])
        axs[i].imshow(rot_array.reshape(1, -1), cmap='binary', aspect='auto')
        axs[i].axis('off')
        matched = next((name for seq, name in matches if seq == rot), None)
        if matched:
            axs[i].set_title(f"{rot} ({matched})", fontsize=8, color='red')  # Highlight known scales in red
        else:
            axs[i].set_title(rot, fontsize=8)  # Add title for each row
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

# Given sequences
sequences = [
    "111111100000", "111111010000", "111111001000", "111111000100", "111111000010", "111110110000",
    "111110101000", "111110100100", "111110100010", "111110011000", "111110010100", "111110010010",
    "111110001100", "111110001010", "111110000110", "111101110000", "111101101000", "111101100100",
    "111101100010", "111101011000", "111101010100", "111101010010", "111101001100", "111101001010",
    "111101000110", "111100111000", "111100110100", "111100110010", "111100101100", "111100101010",
    "111100100110", "111100011100", "111100011010", "111100010110", "111100001110", "111011101000",
    "111011100100", "111011100010", "111011011000", "111011010100", "111011010010", "111011001100",
    "111011001010", "111011000110", "111010111000", "111010110100", "111010110010", "111010101100",
    "111010101010", "111010100110", "111010011100", "111010011010", "111010010110", "111001110010",
    "111001101100", "111001101010", "111001100110", "111001011010", "111001010110", "111000110110",
    "110110110100", "110110110010", "110110101100", "110110101010", "110110011010", "110101101010"
]

# Match sequences to known scales
matches = match_known_scales(sequences, known_scales)

# Print matches
for seq, scale_name in matches:
    print(f"Sequence: {seq} matches scale: {scale_name}")

# Visualize rotations for n=12 and k=7
n = 12
k = 7
output_file = "rotations_k7.png"
visualize_rotations(n, k, output_file, known_scales)
