import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def calculate_table_with_fixed_first(n):
    """Calculate the table of permutations and unique rotations for a given length n with the first position fixed to '1'."""
    table = []
    for k in range(n + 1):
        if k == 0:
            perms = 1
            unique_rots = 1
        else:
            perms = len(list(itertools.combinations(range(n-1), k-1)))
            unique_rots = len(unique_permutations_with_fixed_first(n, k))
        table.append([k, perms, unique_rots])
    return table

def display_table(table, n, output_file):
    """Display the table of permutations and unique rotations as an image."""
    df = pd.DataFrame(table, columns=['k1', 'Permutations', 'Unique Rotations'])
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    ax.axis('tight')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    fig.suptitle(f"Table of Permutations and Unique Rotations (Length {n})", fontsize=16)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')

# Calculate and display the table for 12 positions
n = 12
table = calculate_table_with_fixed_first(n)
display_table(table, n, 'table.png')
