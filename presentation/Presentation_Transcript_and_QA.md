# IEEE ComNetSat 2026 — Virtual Presentation Kit

**Paper:** Enhancing Trust in Federated Learning Through Blockchain-Based Model Verification and Zero-Knowledge Proofs  
**Authors:** Kiet Dao-Anh, Nguyen Tran-Bui-Nhat, Thuat Nguyen-Khanh, Dung Tran-Thi, Quan Le-Trung  
**Affiliation:** University of Information Technology (UIT), Vietnam National University Ho Chi Minh City (VNU-HCM)  
**Conference:** 2026 IEEE International Conference on Communication, Networks and Satellite (ComNetSat 2026)  
**Session Format:** 10-minute video presentation + 5-minute live Q&A (total 15 minutes)

---

## Part 1: Slide-by-Slide Spoken Transcript

*Target pace: 120–130 words per minute. Total: ~1,250 words across 10 minutes.*

---

### Slide 1 — Title & Introduction (0:00 – 0:40)

> **[Display: Paper title, all five authors, UIT affiliation, presenter photos]**
>
> "Good morning, distinguished session chairs, reviewers, and fellow researchers.
>
> My name is **Kiet Dao-Anh**, and alongside my co-presenter **Nguyen Tran-Bui-Nhat**, we are honored to present our paper on behalf of our research team at the University of Information Technology, VNU Ho Chi Minh City.
>
> Our paper is titled: *Enhancing Trust in Federated Learning Through Blockchain-Based Model Verification and Zero-Knowledge Proofs.*
>
> In this work, we present a decoupled framework that separates lightweight cryptographic verification from statistical optimization, achieving edge-feasible Byzantine defense under realistic non-IID data conditions."

---

### Slide 2 — Roadmap (0:40 – 1:10)

> **[Display: 8-item agenda grid]**
>
> "Our presentation covers eight sections. We begin with the motivation behind our research and the three core challenges we address. Then we introduce our four-tier decoupled architecture, followed by our lightweight Groth16 gatekeeper design and our reputation-based anomaly detection system.
>
> After that, we describe our experimental deployment on Azure Kubernetes Service, present convergence and Byzantine defense results, compare against recent literature, and conclude with future directions."

---

### Slide 3 — Motivation & Research Problem (1:10 – 2:15)

> **[Display: Three challenge cards]**
>
> "Federated Learning enables distributed clients to collaboratively train models without sharing raw data. However, practical deployment faces three fundamental challenges.
>
> **First, statistical heterogeneity.** In real deployments, each client collects data with different class distributions. This non-IID skew causes severe client drift — local models diverge significantly from the global objective.
>
> **Second, Byzantine and adversarial attacks.** Since the server never sees the raw training data, malicious participants can submit corrupted updates — including label-flipping, gradient explosion, or random noise injection — to sabotage the global model.
>
> **Third, the blockchain storage problem.** Blockchain provides an immutable audit trail, but storing multi-megabyte model parameters directly on-chain violates EVM gas limits. And critically, blockchain alone cannot verify *whether* an update was correctly trained — only that it was submitted.
>
> Existing ZKP approaches like VPFL attempt to prove the entire backpropagation process inside arithmetic circuits. But verifying non-linear activations like ReLU requires millions of R1CS constraints and gigabytes of RAM — making this entirely impractical for resource-constrained edge devices.
>
> This leads us to our central question: *How can we deliver both cryptographic verification and Byzantine defense while remaining feasible on edge hardware?*"

---

### Slide 4 — Proposed 4-Tier Architecture (2:15 – 3:15)

> **[Display: Architecture diagram + 4 tier cards]**
>
> "Our answer is a deliberately decoupled, four-tier design.
>
> **Tier 1** handles edge client optimization. Each client trains locally using FedProx with a proximal regularization term that bounds client drift under non-IID conditions.
>
> **Tier 2** is our cryptographic gatekeeper. Instead of proving backpropagation, each client generates an ultra-lightweight Groth16 proof — just 67 R1CS constraints — that verifies identity credentials and enforces a strict parameter magnitude ceiling to block gradient explosion.
>
> **Tier 3** manages storage and the blockchain ledger. Model weights stay off-chain in IPFS. Only the 32-byte Content Identifier and verification metadata are recorded on the smart contract, preventing ledger bloat.
>
> **Tier 4** performs trust-aware aggregation. The server computes relative Euclidean distances and applies dynamic IQR fences to screen for outliers, maintains EMA reputation scores, and integrates accepted updates via reputation-weighted FedAdam."

---

### Slide 5 — Operational Workflow (3:15 – 4:00)

> **[Display: Pipeline diagram]**
>
> "Each communication round follows this lifecycle:
>
> The server broadcasts the current global model. Edge clients perform local FedProx training and generate their Groth16 proof. Model artifacts are published to IPFS, and the resulting CID along with proof metadata is submitted to the smart contract.
>
> The server verifies each proof in under 50 milliseconds. Only proof-verified updates proceed to anomaly filtering. Outliers detected by the IQR fence are penalized, and the remaining updates are aggregated via FedAdam's momentum-based optimization."

---

### Slide 6 — Groth16 ZKP Gatekeeper (4:00 – 5:00)

> **[Display: Problem vs Solution comparison cards]**
>
> "Let me elaborate on our cryptographic design choice.
>
> Proving full gradient backpropagation inside a zk-SNARK circuit generates over ten million R1CS constraints for even a modest neural network. This demands 16 to 32 gigabytes of RAM and minutes of compute — completely beyond what any edge device can handle.
>
> We take a different approach. We deliberately decouple what ZKP is responsible for. Our Groth16 circuit evaluates a formal relation that checks two things: first, an identity commitment proving the client holds authorized credentials; and second, a magnitude bound ensuring the absolute sum of parameters stays below a ceiling of five billion, blocking overflow and gradient explosion.
>
> Compiled with Circom 2.2 over the BN-128 curve, this circuit has **exactly 67 R1CS constraints**: 2 for identity verification, 60 for a bit-level comparator, and 5 for boolean enforcement. The complexity is strictly O(1) — completely independent of the neural network's size. On our 2-vCPU edge nodes, proof generation takes just 0.35 seconds using under 50 megabytes of RAM."

---

### Slide 7 — Reputation & Non-IID Fairness (5:00 – 6:00)

> **[Display: Three mechanism cards]**
>
> "While ZKP blocks credential fraud and magnitude overflow, subtle statistical poisoning requires a second layer of defense.
>
> The server computes a **scale-invariant relative distance** for each client — normalizing the Euclidean distance by the global model norm. This prevents false alarms as weights naturally contract during training.
>
> We then apply **dynamic IQR fences** — using the interquartile range of the round's cohort distances to set an adaptive outlier threshold. This expands automatically when all clients experience higher variance from non-IID data.
>
> Each client maintains an EMA reputation score driven by a composite behavioral score that weighs cosine similarity with the global direction, normalized distance, accuracy, loss, and an IQR outlier indicator. Crucially, benign non-IID clients naturally maintain positive cosine similarity with the global descent, while adversarial updates exhibit negative or near-zero alignment — allowing our system to distinguish genuine data heterogeneity from actual attacks."

---

### Slide 8 — Experimental Setup (6:00 – 6:40)

> **[Display: Deployment diagram + hardware specs]**
>
> "We deployed and evaluated the complete framework on **Microsoft Azure Kubernetes Service** across four isolated namespaces.
>
> Each edge client pod runs on nodes with **2 vCPUs — Intel Xeon Platinum 8272CL at 2.4 GHz — and 7.0 GiB of RAM** running Linux containers. This profile matches typical commercial edge gateways.
>
> We benchmark on the **EMNIST Balanced dataset** — 47 handwritten character classes, 131,600 total samples — distributed across 5 clients over 40 communication rounds. We evaluate under both IID and non-IID partitioning."

---

### Slide 9 — Convergence Results (6:40 – 7:25)

> **[Display: Accuracy/loss curves + key findings card]**
>
> "Our convergence results show that under the IID setting, the framework achieves **75.2% top-1 accuracy**, and under non-IID conditions, it reaches **71.2%** — a drop of only 4 percentage points.
>
> The training loss curves decrease monotonically under both settings, with no oscillations or divergence despite the ZKP gating and reputation re-weighting. This confirms that the combination of FedProx regularization with FedAdam's adaptive momentum effectively stabilizes learning across heterogeneous client data."

---

### Slide 10 — Reputation & Overhead (7:25 – 8:00)

> **[Display: Reputation evolution + blockchain overhead charts]**
>
> "Looking at operational trust: client reputations stabilize reliably between 0.76 and 0.77 across training rounds, establishing consistent aggregation baselines.
>
> Regarding overhead — server-side proof verification and smart contract operations take under 0.20 seconds per round, less than 3% of the total round time. Client-side proof generation adds only 0.35 seconds, under 3.5% of local training time. On-chain storage is limited to a single 32-byte IPFS CID per client per round."

---

### Slide 11 — Byzantine Attack Resilience (8:00 – 8:50)

> **[Display: Attack accuracy curves + reputation trajectories]**
>
> "To evaluate adversarial resilience, we subjected the system to Byzantine attacks where malicious clients inject high-variance Gaussian noise and execute label-flipping.
>
> The results are definitive. An unprotected baseline — standard FedProx plus FedAdam without any defense — **collapses catastrophically to 21.8% accuracy**. In contrast, our proposed framework **maintains 71.2% accuracy** — identical to the normal non-adversarial convergence.
>
> As shown in the reputation trajectories, our anomaly detector immediately flags the diverging updates. The malicious clients' reputation scores drop from 0.76 to 0.10 within just a few rounds, effectively isolating them from the FedAdam aggregation."

---

### Slide 12 — Ablation & SOTA Comparison (8:50 – 9:30)

> **[Display: Two comparison tables]**
>
> "Our ablation study demonstrates that each defense layer contributes meaningfully. Reputation scoring alone achieves 62.4% under Byzantine attack — an improvement over the unprotected 21.8% — but it remains vulnerable to magnitude explosion. The complete system, adding ZKP magnitude bounds, achieves the full 71.2%.
>
> Comparing against recent literature — VPFL, zkFL, VerifBFL, and BFLP — we acknowledge an honest engineering trade-off. While VPFL and zkFL provide exhaustive in-circuit gradient proofs, they incur O(P) constraint complexity with over a million constraints, demanding significant proving latency and memory. Our framework achieves an edge-feasible O(1) circuit with just 67 constraints, paired with off-chain IPFS storage, simultaneously delivering edge efficiency, non-IID tolerance, and Byzantine resilience."

---

### Slide 13 — Conclusion & Q&A (9:30 – 10:00)

> **[Display: Summary + Thank You]**
>
> "To summarize our contributions:
>
> First, we decouple cryptographic gatekeeping from statistical optimization, avoiding the constraint explosion of in-circuit backpropagation. Second, our 67-constraint Groth16 circuit achieves edge feasibility with just 0.35 seconds of proving time. Third, IPFS off-chain storage eliminates on-chain bloat. And fourth, our combined ZKP and reputation defense maintains 71.2% accuracy under active Byzantine attacks, compared to a 21.8% collapse without defense.
>
> For future work, we are exploring recursive SNARKs and chunked Poseidon Merkle-tree commitments to enable layer-wise verification for deep architectures like Transformers.
>
> Thank you for your attention. We look forward to your questions."

---

## Part 2: Q&A Defense Guide

*Prepare for 5–10 minutes of tough reviewer and session-chair questions. Answers are structured as concise, academic-tone responses.*

---

### Q1: "Your Groth16 circuit only has 67 constraints. Doesn't this mean a malicious client can still pass the ZKP while submitting poisoned updates?"

> **Answer:** "That is correct, and it is by design. We explicitly acknowledge this trade-off in Section V of our paper.
>
> Prior works like VPFL attempt to verify the full backward pass inside arithmetic circuits. But proving non-linear activations like ReLU requires bit-decomposition into 32–64 constraints *per neuron*, leading to over ten million total constraints for even a modest network — consuming gigabytes of RAM and minutes of proving time. Edge devices simply cannot support this.
>
> Our approach employs **defense in depth**:
> 1. The **Groth16 circuit** acts as a first-pass cryptographic gatekeeper: it enforces identity authorization and a strict parameter magnitude ceiling to block gradient explosion and NaN injection.
> 2. **Statistical poisoning** — such as label-flipping or subtle directional attacks — is caught by our **server-side anomaly detection** using relative Euclidean distances, dynamic IQR fences, and cosine similarity scoring in the reputation system.
>
> This decoupling allows us to achieve edge feasibility while maintaining 71.2% accuracy under active Byzantine attacks, compared to a 21.8% collapse in the unprotected baseline."

---

### Q2: "Under non-IID conditions, honest clients produce naturally diverse gradients. How do you avoid penalizing legitimate clients?"

> **Answer:** "We address this through three complementary mechanisms:
>
> 1. **FedProx regularization** with mu=0.001 adds a proximal term that bounds local parameter drift, keeping honest updates within a compact neighborhood of the global model — even under skewed data.
> 2. **Relative distance normalization:** Instead of raw Euclidean distance, we normalize by the global model norm and the median cohort distance. As training progresses and the model stabilizes, this scaling factor contracts naturally.
> 3. **Dynamic IQR fences:** Our outlier threshold is Q3 + 1.5 × IQR — it's *relative* to the current round's cohort variance, not a fixed static value. When all clients experience higher variance from non-IID skew, the threshold expands proportionally.
>
> Additionally, benign non-IID clients maintain positive cosine similarity with the global descent direction, whereas adversarial updates exhibit near-zero or negative similarity — providing a reliable discriminator."

---

### Q3: "How does proof generation scale if you move from this 2-layer CNN to ResNet-50 or a Transformer?"

> **Answer:** "Because our circuit checks aggregate parameter bounds and identity commitments — not the training computation itself — the circuit size is O(1). It remains exactly 67 constraints whether the model has 100,000 or 100 million parameters. Proving time stays at approximately 0.35 seconds.
>
> However, we recognize that for deep architectures, *granular* layer-wise verification becomes desirable. This is precisely our future work direction:
> 1. **Chunked Poseidon Merkle trees:** Partitioning the weight tensor into discrete chunks committed to a hash tree, allowing clients to prove bounds on sampled sub-layers with sub-linear overhead.
> 2. **Recursive SNARKs** using folding schemes like Nova or Halo2: incrementally verifying layer transformations in step-wise O(1) recursion without constraint explosion."

---

### Q4: "Why IPFS instead of storing model weights on-chain?"

> **Answer:** "On Ethereum and EVM-compatible chains, persistent storage via SSTORE costs 20,000 gas per 32 bytes. A 5 MB model would require over 3 billion gas — roughly 100 times the entire Ethereum block gas limit of 30 million.
>
> By pairing IPFS with smart contracts, raw model weights are distributed off-chain across IPFS nodes. Only the 32-byte cryptographic Content Identifier is recorded on-chain — that's a single storage slot, O(1) overhead. This preserves immutable auditability while keeping gas costs minimal."

---

### Q5: "Can a penalized client recover its reputation?"

> **Answer:** "Yes, absolutely. That is precisely why we use an Exponential Moving Average with alpha = 0.3. A single bad round reduces the reputation, but does not permanently blacklist the client. If the client submits valid, high-quality updates in subsequent rounds, its reputation gradually recovers toward the cohort average of approximately 0.76.
>
> This is observable in our reputation trajectory figures — penalized clients demonstrate smooth recovery once reliable updates resume."

---

### Q6: "Why did you use Azure Kubernetes instead of physical edge devices like Raspberry Pi?"

> **Answer:** "We configured Azure Kubernetes Service specifically to emulate resource-constrained edge environments with deterministic, reproducible isolation. Each client pod was capped at 2 vCPUs and 7.0 GiB RAM — matching the profile of standard commercial edge gateways such as Raspberry Pi 5 or NVIDIA Jetson Nano.
>
> AKS allowed us to deploy 15 isolated pods running asynchronous IPFS daemons, Ethereum JSON-RPC connections, and the complete FL pipeline simultaneously — something that would be logistically complex with 15 physical devices. The resource constraints are the same; the infrastructure is more manageable for reproducibility."

---

### Q7: "How does the system prevent Sybil attacks?"

> **Answer:** "Sybil defense operates at two layers:
> 1. **Cryptographic identity commitment:** The Groth16 circuit enforces w_id^3 + w_id = x_hash, meaning each client must prove ownership of a pre-registered identity in the smart contract registry. Forging a valid identity commitment without pre-authorization is computationally infeasible.
> 2. **Behavioral reputation accumulation:** Even if an adversary operates multiple accounts, each must independently build behavioral reputation over multiple rounds. If their updates carry identical adversarial noise, the IQR detector flags the entire cluster and suppresses their collective aggregation weights."

---

### Q8: "Why FedAdam instead of FedAvg for server aggregation?"

> **Answer:** "While FedProx stabilizes local training, standard FedAvg on the server simply computes a weighted average. Under non-IID skew combined with dynamic reputation weighting, raw updates can exhibit erratic oscillations.
>
> FedAdam introduces adaptive first-moment (momentum) and second-moment (adaptive learning rate) estimators at the server level. This smooths high-frequency gradient noise, accelerates convergence, and prevents individual round fluctuations from destabilizing the global trajectory."

---

### Q9: "What is the Byzantine attack model in your experiments?"

> **Answer:** "We use a label-flipping attack model where malicious clients flip the true label y to 61 − y, combined with high-variance Gaussian perturbation of parameters. The number of faulty clients fluctuates dynamically per round following a Poisson process with intensity Lambda = 1.0, simulating realistic intermittent adversarial behavior rather than a fixed worst-case scenario.
>
> Under this attack, the unprotected baseline collapses to 21.8% accuracy, while our framework maintains 71.2%."

---

### Q10: "Does your framework provide differential privacy guarantees?"

> **Answer:** "Our current framework focuses on **model integrity, parameter validation, and Byzantine fault tolerance** through ZKP and reputation scoring. Groth16 guarantees zero-knowledge — the private witness is never disclosed by the proof — but raw model parameters are still shared with the server via IPFS for FedAdam aggregation.
>
> However, because our architecture is modular, Local Differential Privacy — such as Gaussian or Laplacian noise addition to gradients — can be integrated directly into the client training tier before proof generation. The magnitude bound W_max in the circuit would simply be adjusted to accommodate the added noise."

---

## Part 3: Video Recording Instructions & ComNetSat Guidelines

> [!IMPORTANT]
> **Can you use Voice-Over PowerPoint without showing your face?**  
> **YES, ABSOLUTELY 100%!**  
> The official IEEE ComNetSat guidelines explicitly state:  
> *"You have to prepare a 10-minutes video presentation, make you present it to the camera **OR your voice-over PowerPoint** OR a combination of other creative presentation methods. You can also use several screens, one for PowerPoint presentations and smaller ones including you as a presenter."*  
> 
> The keyword is **"OR"** — you are completely free to record a clean, professional **voice-over PowerPoint (slides + spoken audio)** without any webcam or talking-head video. Having your portrait photo on **Slide 1** satisfies the author identification requirement, so showing your face during the rest of the presentation is completely optional.

### Recommended Ways to Record Your 10-Minute Presentation:

#### Method A: Built-in Microsoft PowerPoint Record (Easiest & Cleanest)
1. Open `ComNetSat2026_Presentation.pptx` in Microsoft PowerPoint.
2. Go to the **Record** tab (or **Slide Show** -> **Record Slide Show**).
3. Select your microphone. Make sure the webcam is set to **Off** (audio-only voice-over).
4. Click **Record** and narrate slide by slide using the Part 1 transcript.
   * *Tip:* PowerPoint records audio slide-by-slide, meaning if you stumble on Slide 4, you can re-record only Slide 4 without starting over!
5. When finished, go to **File** -> **Export** -> **Create a Video** -> select **Full HD (1080p)** -> click **Create Video** (`.mp4`).

#### Method B: OBS Studio / Zoom / Clipchamp
1. Set resolution to 1920x1080 (16:9) at 30 fps.
2. Capture the PowerPoint presentation in full-screen Slide Show mode.
3. Record audio via headset or external microphone (no webcam required).
4. Ensure total video length is **between 9:20 and 9:55** (strictly under 10:00).

### Final Pre-Submission Checklist:
1. **Slide 1 Photos:** Paste portrait photos of both presenters (Kiet Dao-Anh and Nguyen Tran-Bui-Nhat) into the two photo boxes on Slide 1.
2. **Video Duration:** Strictly **under 10 minutes** (aim for 9:45).
3. **Audio Quality:** Clear, audible voice with minimal echo/background noise.
4. **File Format:** `.mp4` (H.264 video codec, AAC audio).
5. **Submission:** Upload the `.pptx` slide deck and the `.mp4` video file via EDAS / the conference portal before the deadline.
