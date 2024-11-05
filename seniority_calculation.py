import matplotlib.pyplot as plt
import numpy as np

def get_seniority_calculation(event_sequence, network):
    """
    Get the seniority calculation for the reverter and reverted.
    
    The seniority calculation is the absolute difference between the log10 of the number of edits the reverter and reverted have made.
    """    
    abs_diff_seqs = []
    for seq in event_sequence.values():
        for s in seq:
            abs_diff_seqs.append(abs(s[0]['reverter_seniority'] - s[0]['reverted_seniority']))
    
    abs_diff_rest = []
    for edge in network:
        abs_diff_rest.append(abs(edge['reverter_seniority'] - edge['reverted_seniority']))
    
    return (abs_diff_seqs, abs_diff_rest)

def plot_seniority_calculation(abs_diff_seqs, abs_diff_rest):
    """
    Plot the seniority calculation for the reverter and reverted.
    
    The seniority calculation is the absolute difference between the log10 of the number of edits the reverter and reverted have made.
    """
    # Plot a histogram of abs_diff_seqs
    plt.hist(abs_diff_seqs, bins=50, alpha=0.7, label='AB-BA')

    # Plot a histogram of abs_diff_rest
    plt.hist(abs_diff_rest, bins=50, alpha=0.5, label='Other')

    plt.xlabel('Absolute Difference in Seniority')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show()

def print_mean(abs_diff_seqs, abs_diff_rest):
    """ Print the mean of the absolute seniority difference for reverts in AB-BA sequences and all."""
    print("Mean of absolute seniority difference for reverts in AB-BA sequences: ",np.mean(abs_diff_seqs))
    print("Mean of absolute seniority difference for all other reverts: ", np.mean(abs_diff_rest))