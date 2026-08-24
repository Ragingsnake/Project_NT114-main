import sys

with open("server/FL_Server/strategy.py", "r", encoding="utf-8") as f:
    content = f.read()

# Update history init
content = content.replace(
    'self.history = {\n            "global": {"round": [], "accuracy": [], "loss": [], "verification_time": [], "penalty_clients": [], "round_time": []},\n            "clients": {}\n        }',
    'self.history = {\n            "global": {"round": [], "accuracy": [], "loss": [], "verification_time": [], "penalty_clients": [], "round_time": [], "rejections_zkp": [], "rejections_rep": []},\n            "clients": {}\n        }'
)

# Update aggregate_fit
# Insert tracking counters at top of aggregate_fit
content = content.replace(
    'clients_info = []\n        round_verify_times = []\n        penalty_clients = []',
    'clients_info = []\n        round_verify_times = []\n        penalty_clients = []\n        zkp_rejections = 0\n        rep_rejections = 0'
)

# Insert ZKP rejection increment
content = content.replace(
    'if not verified:\n                print(f"? ZKP FAILED for Client {cid}")\n                reputation_manager.update_reputation(cid, -1.0) \n                # penalty_this_round.append(cid)\n                continue',
    'if not verified:\n                print(f"? ZKP FAILED for Client {cid}")\n                reputation_manager.update_reputation(cid, -1.0) \n                zkp_rejections += 1\n                continue'
)

# Insert Rep rejection increments
content = content.replace(
    'if score < -0.4 or reputation < 0.2:\n                print(f"?? Skip client {cid} (score={score:.3f}, rep={reputation:.3f})")\n                penalty_clients.append(cid)\n                continue',
    'if score < -0.4 or reputation < 0.2:\n                print(f"?? Skip client {cid} (score={score:.3f}, rep={reputation:.3f})")\n                penalty_clients.append(cid)\n                rep_rejections += 1\n                continue'
)

content = content.replace(
    'if delta < lower or delta > upper:\n\n                print(f"?? Outlier Client {cid} (?={delta:.4f})")\n\n                reputation *= 0.7\n\n                penalty_clients.append(cid)\n                continue',
    'if delta < lower or delta > upper:\n\n                print(f"?? Outlier Client {cid} (?={delta:.4f})")\n\n                reputation *= 0.7\n\n                penalty_clients.append(cid)\n                rep_rejections += 1\n                continue'
)

# Save the counts at the end of aggregate_fit
content = content.replace(
    'if round_verify_times:\n            self.history["global"]["verification_time"].append(float(np.mean(round_verify_times)))\n            self.history["global"]["penalty_clients"].append(penalty_clients)',
    'if round_verify_times:\n            self.history["global"]["verification_time"].append(float(np.mean(round_verify_times)))\n            self.history["global"]["penalty_clients"].append(penalty_clients)\n        self.history["global"]["rejections_zkp"].append(zkp_rejections)\n        self.history["global"]["rejections_rep"].append(rep_rejections)'
)

with open("server/FL_Server/strategy.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated strategy.py")
