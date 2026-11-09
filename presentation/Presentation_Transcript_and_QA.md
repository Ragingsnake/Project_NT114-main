# IEEE ComNetSat 2026 — Official Presentation Transcript & Q&A Defense Guide

**Paper Title:** Enhancing Trust in Federated Learning Through Blockchain-Based Model Verification and Zero-Knowledge Proofs  
**Authors:** Kiet Dao-Anh, Nguyen Tran-Bui-Nhat, Thuat Nguyen-Khanh, Dung Tran-Thi, Quan Le-Trung  
**Affiliation:** UiTiOt Research Group, Faculty of Computer Networks and Communications, University of Information Technology (UIT), VNU-HCM, Viet Nam  
**Conference:** The 14th IEEE International Conference on Communications, Networks, and Satellite (COMNETSAT 2026) | Dec. 3–5, 2026  
**Session Format:** 10-Minute Video Presentation (Voice-Over or Video) + 5-Minute Live Q&A  

### Presenter Allocation:
* **Part 1 (Slides 1 – 8):** Presented by **Mr. Kiet Dao-Anh** (`23520810@gm.uit.edu.vn`)
* **Part 2 (Slides 9 – 13):** Presented by **Mr. Nguyen Tran-Bui-Nhat** (`23521059@gm.uit.edu.vn`)

---

## Part 1: Slide-by-Slide Spoken Transcript (10:00 Total)

*(Speaking pace: 125 words per minute. Perfectly timed for 9:45 – 9:55 minutes).*

---

### [PRESENTER 1: Kiet Dao-Anh] (Slides 1 to 8: ~0:00 – 6:45)

#### Slide 1 — Title Slide & Introduction (0:00 – 0:45)
> **[Display: Slide 1 — Title, Conference Badge, Authors, UIT Affiliation, Presenter Badges]**
>
> "Good morning, distinguished session chairs, reviewers, and fellow attendees.
>
> My name is **Kiet Dao-Anh**, and together with my co-author and co-presenter **Nguyen Tran-Bui-Nhat**, we represent the UiTiOt Research Group at the University of Information Technology, Vietnam National University Ho Chi Minh City.
>
> Today, we are honored to present our paper: 
> *'Enhancing Trust in Federated Learning Through Blockchain-Based Model Verification and Zero-Knowledge Proofs.'*
>
> In this presentation, I will cover the background, state-of-the-art comparison, our decoupled architecture, and the experimental setup. Then, my colleague **Nguyen Tran-Bui-Nhat** will take over to present our empirical scenarios, Byzantine attack resilience, and final conclusions."

---

#### Slide 2 — Outline (0:45 – 1:15)
> **[Display: Slide 2 — 5-Section Outline Grid]**
>
> "Our presentation is organized into five key sections:
> First, I will introduce the core background and the fundamental trust challenges in distributed edge learning.
> Second, we will review related works and highlight how our scheme overcomes existing limitations.
> Third, I will detail our four-tier decoupled methodology and Azure Kubernetes deployment.
> Fourth, we will dive into our experimental results—covering dataset partitioning, evaluation metrics, normal convergence, and Byzantine attack defense.
> Finally, we will summarize our conclusions and future outlook."

---

#### Slide 3 — 1. Introduction: Background, Challenges & Contributions (1:15 – 2:30)
> **[Display: Slide 3 — Three Columns: Background, Challenges, Key Contributions]**
>
> "Let us begin with the introduction.
>
> **1. Background:** Federated Learning allows distributed edge clients to collaboratively train a shared model without exposing raw, private data. Clients train locally and transmit parameter updates to a central aggregation server.
>
> **2. Challenges:** However, real-world deployments face three critical roadblocks:
> - *Non-IID Data:* Skewed data distributions across edge clients cause severe client drift, destabilizing convergence under standard FedAvg.
> - *Malicious Updates:* The central server cannot inspect private local training data, making FL highly vulnerable to Byzantine model poisoning, label-flipping, and exploding gradients.
> - *Verification Limitations:* While blockchain provides immutability and auditability, it cannot independently verify whether an off-chain update was computed legitimately.
>
> **3. Key Contributions:** To solve these issues, our paper makes three contributions:
> - *Learning Optimization:* We combine client-side FedProx regularization with adaptive server-side FedAdam momentum to stabilize non-IID learning.
> - *Secure Model Verification:* We decouple cryptographic gatekeeping using a lightweight Groth16 zk-SNARK with off-chain IPFS storage, eliminating on-chain ledger bloat.
> - *Trust Management:* We formulate dynamic IQR anomaly detection and exponential moving average reputation to isolate malicious nodes."

---

#### Slide 4 — 2. Related Works: Comparative Analysis (2:30 – 3:30)
> **[Display: Slide 4 — Table I & Table II Literature Benchmarks]**
>
> "In Tables I and II, we compare our approach against leading blockchain-based verifiable FL schemes from recent literature: VPFL, zkFL, VerifBFL, and BFLP.
>
> As shown in Table I, existing frameworks like VPFL and zkFL enforce in-circuit gradient backpropagation. Proving non-linear activations like ReLU generates over $10^6$ constraints, creating an $\mathcal{O}(P)$ bottleneck that requires gigabytes of RAM—completely infeasible on edge hardware. Furthermore, storing parameters on-chain in VerifBFL causes severe EVM block gas exhaustion.
>
> In Table II, we see that most existing schemes assume IID distributions and offer weak or static Byzantine thresholds.
>
> In contrast, our proposed framework introduces a pragmatic design trade-off: we deploy an edge-feasible $\mathcal{O}(1)$ Groth16 circuit with **exactly 67 constraints** to enforce identity authorization and parameter sanity bounds ($W_{\max} = 5 \times 10^9$). We store weights off-chain in IPFS with a single 32-byte CID on-chain, while delegating statistical anomaly detection to dynamic IQR fences, cosine similarity, and reputation weighting."

---

#### Slide 5 — 3. Our Methodology: Proposed Framework Architecture (3:30 – 4:30)
> **[Display: Slide 5 — 4-Tier Workflow Diagram & Tier Descriptions]**
>
> "Now let us examine our four-tier decoupled methodology:
>
> - **1. Local Optimization:** Clients train locally using **FedProx**, where a proximal regularization penalty ($\mu = 0.001$) bounds local client drift within an admissible optimization ball under non-IID data skew.
> - **2. Cryptographic Verification:** Clients compile an ultra-lightweight Groth16 zk-SNARK proof over the BN-128 elliptic curve. The server verifies the proof in under 0.05 seconds. Model weights are stored off-chain in **IPFS**, and only the 32-byte CID and proof metadata are recorded on the **Ganache** smart contract.
> - **3. Trust Evaluation:** The server evaluates the scale-invariant relative Euclidean distance and applies dynamic **Interquartile Range (IQR)** fences to filter out suspicious deviations. It then updates each client's Exponential Moving Average (EMA) reputation score.
> - **4. Adaptive Aggregation:** The server weights accepted updates proportional to their reputation score and integrates them into the global model via **FedAdam's** adaptive first- and second-order momentum."

---

#### Slide 6 — 3. Our Methodology: Azure Kubernetes Service Deployment (4:30 – 5:30)
> **[Display: Slide 6 — AKS Cloud Architecture Diagram & 4 Namespaces]**
>
> "To validate our architecture under realistic distributed conditions, we deployed the framework on **Microsoft Azure Kubernetes Service (AKS)** across four isolated namespaces:
>
> - **1. `fl-clients` (StatefulSet):** Hosts edge client pods. Each pod is allocated **2 vCPUs (Intel Xeon Platinum 8272CL @ 2.4 GHz) and 7.0 GiB of RAM**, matching commercial edge IoT gateways. Clients execute FedProx local training and run Circom/SnarkJS to generate proofs.
> - **2. `ipfs` (StatefulSet):** Operates the decentralized IPFS daemon, storing multi-megabyte model parameters and providing deterministic retrieval via content addressing.
> - **3. `blockchain` (StatefulSet):** Runs our Ganache EVM node, handling smart contracts for registrar authorization, proof verification, and immutable reputation recording.
> - **4. `fl-server` (Deployment):** Coordinates the communication rounds, retrieves verified models, applies anomaly filtering, and executes FedAdam global aggregation."

---

#### Slide 7 — 4. Experimental Results: Dataset & Data Distribution (5:30 – 6:15)
> **[Display: Slide 7 — EMNIST Heatmaps (Labels 0-22 and Labels 23-46) & Specs]**
>
> "We evaluated the framework on the **EMNIST Balanced benchmark**, comprising 47 character classes and 131,600 total handwritten images across 5 edge clients over 40 communication rounds.
>
> As visualized in our class distribution heatmaps:
> - In the **IID setting (top)**: every client receives an equal, uniform distribution across all 47 classes.
> - In the **Non-IID setting (bottom)**: we simulate severe real-world data skew using a Dirichlet distribution ($\alpha = 0.5$). Each client receives samples from only a restricted subset of classes, inducing significant client drift and local model divergence."

---

#### Slide 8 — 4. Experimental Results: Evaluation Metrics & Handover (6:15 – 7:00)
> **[Display: Slide 8 — Three Metric Cards: Model Performance, Malicious Detection, Reputation]**
>
> "To rigorously measure system effectiveness, we established three evaluation pillars:
>
> 1. **Model Performance:** We measure global top-1 classification accuracy, training loss trajectory, and convergence stability across rounds.
> 2. **Malicious Update Detection:** We compute the scale-invariant relative distance $\Delta_i^t = \frac{\|w_i^t - w_t\|_2}{\|w_t\|_2 + \epsilon}$ to avoid weight contraction bias, and apply dynamic IQR fences ($Q_3 + 1.5 \times \mathrm{IQR}$) alongside directional cosine similarity ($\mathrm{sim} > 0.1$) to classify valid versus rejected updates.
> 3. **Reputation Mechanism:** We evaluate client reliability through a composite score $S_i^t$ and update reputation scores $R_i \in [0.1, 1.0]$ via an EMA update coefficient ($\alpha = 0.3$).
>
> Now, I would like to hand over the presentation to my co-author and co-presenter, **Mr. Nguyen Tran-Bui-Nhat**, who will present our empirical scenario results, Byzantine attack resilience, and final conclusions."

---

### [PRESENTER 2: Nguyen Tran-Bui-Nhat] (Slides 9 to 13: ~7:00 – 10:00)

#### Slide 9 — 4. Experimental Results: Normal Training Scenarios (IID vs. Non-IID) (7:00 – 8:00)
> **[Display: Slide 9 — Accuracy/Loss Curves, Average Reputation Chart, Milestone Cards]**
>
> "Thank you, Kiet. 
>
> Distinguished session chairs and attendees, my name is **Nguyen Tran-Bui-Nhat**, and I will now walk you through our empirical scenarios and experimental findings.
>
> In Scenario 1, we evaluate system performance under normal, non-adversarial conditions across both IID and Non-IID partitions.
>
> **1. Model Convergence:** As shown in the left figure, our framework reaches **75.2% top-1 accuracy** in the IID setting, and **71.2%** under the highly skewed Non-IID setting. Notice that the accuracy degradation under extreme Dirichlet skew is **only 4.0 percentage points**. The loss curves decrease monotonically without oscillations, confirming that FedProx local regularization paired with FedAdam's adaptive momentum effectively stabilizes client drift.
>
> **2. Reputation Stabilization:** In the right figure, the average client reputation stabilizes rapidly between **0.76 and 0.77** across all benign clients, establishing consistent and fair aggregation baselines.
>
> **3. System Overhead:** Edge Groth16 proof generation takes only **0.35 seconds** per client—accounting for **less than 3.5%** of local training time and consuming under 50 MB of RAM. Server-side proof verification and smart contract execution complete in **under 0.20 seconds** (< 3% of total round time). Off-chain IPFS storage keeps on-chain transactions to a single 32-byte CID, completely preventing EVM block gas exhaustion."

---

#### Slide 10 — 4. Experimental Results: Byzantine Attack Resilience & Defense (8:00 – 9:00)
> **[Display: Slide 10 — Attack Accuracy Curves, Reputation Drop Chart, Defense Breakdown]**
>
> "In Scenario 2, we evaluate robustness against active **Byzantine adversaries**.
>
> In this attack, malicious clients inject high-variance Gaussian perturbations ($w_i + \mathcal{N}(0, 3.0^2)$) and execute label-flipping ($y \to 61 - y$). Faulty client occurrences follow a Poisson arrival process with intensity $\Lambda = 1.0$.
>
> **1. Catastrophic Baseline Collapse:** As illustrated in the left chart, an unprotected baseline—standard FedProx plus FedAdam without ZKP or trust scoring—**collapses catastrophically to 21.8% accuracy**!
>
> **2. Proposed Framework Resilience:** In stark contrast, our proposed system **maintains 71.2% robust accuracy**, tracking the clean non-adversarial convergence trajectory almost identically!
>
> **3. Rapid Malicious Node Isolation:** In the right chart, you can see our reputation dynamics in action. The moment a malicious client submits corrupted parameters, its update violates our dynamic IQR fences. Its reputation score plummets from **0.76 down to 0.10 by round 5**, effectively neutralizing its aggregation weight in FedAdam.
>
> **4. Ablation Quantification:** Our ablation study confirms the necessity of both defense layers: reputation scoring alone achieves 62.4% but remains vulnerable to exploding weights; adding our 67-constraint Groth16 magnitude bound delivers full 71.2% robust convergence."

---

#### Slide 11 — 5. Conclusions & Future Work (9:00 – 9:40)
> **[Display: Slide 11 — Two Cards: Conclusions & Future Work]**
>
> "To summarize our findings:
>
> **Conclusions:**
> - We developed a secure, blockchain-enabled FL framework integrating FedProx, FedAdam, Groth16 ZKP, IPFS, and dynamic reputation scoring.
> - We verified model updates cryptographically while ensuring complete privacy and transparent auditability.
> - We demonstrated high training stability under both IID (75.2%) and Non-IID (71.2%) data skew.
> - We achieved negligible overhead: 0.35-second edge proof generation and 32-byte on-chain storage.
> - We proved robust Byzantine resilience, preserving 71.2% accuracy under active attacks where unprotected baselines collapse to 21.8%.
>
> **Future Work:**
> - We plan to evaluate the framework on large real-world domain datasets including Healthcare, Smart Cities, IoT networks, and Finance.
> - We will extend deployment to cross-organization enterprise environments.
> - We are investigating **Recursive SNARKs (such as Nova)** and **Chunked Poseidon Merkle Trees** to verify deep neural architectures like ResNet and Transformers in step-wise $\mathcal{O}(1)$ recursion.
> - We are integrating Local Differential Privacy directly into the client training tier."

---

#### Slide 12 — 6. References (9:40 – 9:48)
> **[Display: Slide 12 — 12 Key Literature References]**
>
> "Here are the key references supporting our work, including foundational papers on federated optimization, poisoning surveys, and recent zero-knowledge verifiable FL architectures."

---

#### Slide 13 — Acknowledgments & Q&A (9:48 – 10:00)
> **[Display: Slide 13 — Center Card with Thank You, Presenter Info, Grant Acknowledgment]**
>
> "This research is funded by the University of Information Technology, Vietnam National University Ho Chi Minh City under grant number CS4-2026-80290.
>
> On behalf of my co-author Kiet Dao-Anh, our supervisors, and the UiTiOt Research Group, thank you very much for your attention.
>
> We are now delighted to open the floor and welcome your questions."

---

## Part 2: Q&A Defense Guide (Key Technical Answers)

*(Toughest questions session chairs and reviewers might ask, with concise answers).*

### Q1: *"Why does your Groth16 circuit have only 67 constraints? Isn't that too small to verify deep neural network training?"*
> **Answer:** "Yes, and that is our deliberate design contribution. Prior schemes like VPFL attempt to prove multi-epoch backpropagation inside zk-SNARKs. However, non-linear activations like ReLU require bit-decomposition into 32–64 R1CS constraints per neuron, generating over $10^7$ constraints for even a modest network and requiring 16–32 GB of RAM—which crashes edge devices.  
> We decouple cryptographic sanity from statistical learning: our Groth16 circuit acts as an $\mathcal{O}(1)$ gatekeeper checking client identity authorization and parameter magnitude bounds ($W_{\max} = 5 \times 10^9$) to block overflow and gradient explosion in just 0.35 seconds. Directional correctness and subtle poisoning are handled by our server-side dynamic IQR fences and reputation system."

### Q2: *"Under extreme Non-IID skew ($\alpha = 0.5$), how do you avoid falsely penalizing honest clients with unique data distributions?"*
> **Answer:** "We provide three protections:
> 1. **Client-side FedProx Regularization:** A proximal penalty $\mu = 0.001$ bounds local parameter drift within an admissible optimization neighborhood.
> 2. **Dynamic Cohort IQR Fences:** The upper outlier threshold $Q_3 + 1.5 \times \mathrm{IQR}$ expands adaptively when all clients experience higher variance, avoiding rigid static threshold false positives.
> 3. **Directional Cosine Similarity:** Benign Non-IID updates maintain positive cosine similarity ($\mathrm{sim} > 0.1$) with the global descent vector, whereas adversarial poisoning flips direction."

### Q3: *"How does on-chain storage scale with round count?"*
> **Answer:** "Because raw model weights remain strictly off-chain in IPFS, the smart contract records only a 32-byte cryptographic Content Identifier (CID), client ID, and verification timestamp per update. This requires a single $\mathcal{O}(1)$ storage slot per transaction, completely avoiding EVM block gas exhaustion regardless of model size."

---

## Part 3: Video Recording Instructions

> [!IMPORTANT]
> **Recording with Voice-Over Only (NO Camera Required):**  
> Under IEEE ComNetSat guidelines, you may present using **voice-over PowerPoint without turning on your webcam** (*"make you present it to the camera OR your voice-over PowerPoint OR a combination of other creative presentation methods"*). The title slide displays full author and presenter credentials and university affiliations, which fully satisfies all conference identification requirements.
>
> **Recommended Recording Method (Microsoft PowerPoint):**  
> 1. Open `ComNetSat2026_Presentation.pptx`.  
> 2. Click **Record** $\rightarrow$ **Record Slide Show**.  
> 3. Ensure **Camera is set to OFF** (Audio only).  
> 4. Kiet records Slides 1 to 8; Nhat records Slides 9 to 13 following the transcript above.  
> 5. Export to **Full HD (1080p)** `.mp4`. Total duration should be between **9:30 and 9:55 minutes**.
