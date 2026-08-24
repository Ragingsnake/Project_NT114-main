import os

with open("shared/plot_results.py", "a", encoding="utf-8") as f:
    f.write('''
# Plot Rejections
if "rejections_zkp" in global_data and "rejections_rep" in global_data:
    zkp_rej = global_data["rejections_zkp"]
    rep_rej = global_data["rejections_rep"]
    r_len = min(len(zkp_rej), len(rep_rej))
    rounds_rej = np.arange(1, r_len + 1)
    
    plt.figure(figsize=(10, 6))
    plt.bar(rounds_rej, zkp_rej[:r_len], label='Rejected by ZKP (Range Bound)', color='red')
    plt.bar(rounds_rej, rep_rej[:r_len], bottom=zkp_rej[:r_len], label='Rejected by Reputation (Cosine/IQR)', color='orange')
    plt.xlabel("Round")
    plt.ylabel("Number of Clients Rejected")
    plt.title("Client Rejections per Round")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ensure y-axis shows integer ticks
    max_rej = max(max(zkp_rej) + max(rep_rej), 1)
    plt.yticks(np.arange(0, max_rej + 2, 1))
    
    plt.savefig(os.path.join(SAVE_DIR, "rejections_stacked_bar.png"))
    plt.close()
''')
print("Appended rejection plot to plot_results.py")
