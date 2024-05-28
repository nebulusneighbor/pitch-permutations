import itertools
import numpy as np
import matplotlib.pyplot as plt

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

def visualize_rotations(n, k, output_file):
    """Visualize the unique rotations for a given n and k."""
    unique_rots = unique_permutations_with_fixed_first(n, k)
    num_rots = len(unique_rots)
    
    if num_rots == 1:
        fig, ax = plt.subplots(1, 1, figsize=(12, 1.5))  # Increase width
        rot_array = np.array([int(char) for char in unique_rots[0]])
        ax.imshow(rot_array.reshape(1, -1), cmap='binary', aspect='auto')
        ax.axis('off')
    else:
        fig, axs = plt.subplots(num_rots, 1, figsize=(12, num_rots * 1.5))  # Increase width and spacing
        for i, rot in enumerate(unique_rots):
            rot_array = np.array([int(char) for char in rot])
            axs[i].imshow(rot_array.reshape(1, -1), cmap='binary', aspect='auto')
            axs[i].axis('off')
            axs[i].set_title(rot, fontsize=8)  # Add title for each row
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

# Visualize unique rotations for n=12 (12 positions) and k=7
n = 12
k = 7
output_file = f"rotations_k{k}.png"
visualize_rotations(n, k, output_file)

# Get and print unique rotations
unique_rots = unique_permutations_with_fixed_first(n, k)
for seq in unique_rots:
    print(seq)
