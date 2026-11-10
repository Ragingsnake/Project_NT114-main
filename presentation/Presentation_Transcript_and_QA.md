# IEEE ComNetSat 2026 — Official Presentation Transcript & Q&A Defense Guide

**Paper Title:** Enhancing Trust in Federated Learning Through Blockchain-Based Model Verification and Zero-Knowledge Proofs  
**Authors:** Kiet Dao-Anh, Nguyen Tran-Bui-Nhat, Thuat Nguyen-Khanh, Dung Tran-Thi, Quan Le-Trung  
**Affiliation:** UiTiOt Research Group, Faculty of Computer Networks and Communications, University of Information Technology (UIT), VNU-HCM, Viet Nam  
**Conference:** The 14th IEEE International Conference on Communications, Networks, and Satellite (COMNETSAT 2026) | Dec. 3–5, 2026  
**Session Format:** 10-Minute Video Presentation (Voice-Over or Video) + 5-Minute Live Q&A  

### Presenter Allocation:
* **Part 1 (Slides 1 – 7):** Presented by **Mr. Kiet Dao-Anh** (`23520810@gm.uit.edu.vn`)
* **Part 2 (Slides 8 – 13):** Presented by **Mr. Nguyen Tran-Bui-Nhat** (`23521059@gm.uit.edu.vn`)

---

## Part 1: Slide-by-Slide Spoken Transcript (10:00 Total)

*(Speaking pace: ~130 words per minute. Perfectly timed for 9:30 – 9:50 minutes, leaving a safe buffer).*

---

### [PRESENTER 1: Kiet Dao-Anh] (Slides 1 to 7: ~0:00 – 5:45)

#### Slide 1 — Title Slide & Introduction (0:00 – 0:40)
> **[Display: Slide 1 — Title, Conference Badge, Authors, UIT Affiliation, Presenter Badges]**
>
> "Hello everyone, and welcome to our presentation.
>
> My name is **Kiet Dao-Anh**, and alongside my co-author **Nguyen Tran-Bui-Nhat**, we represent the UiTiOt Research Group at the University of Information Technology, VNU-HCM.
>
> Today, we're presenting our paper: 
> *'Enhancing Trust in Federated Learning Through Blockchain-Based Model Verification and Zero-Knowledge Proofs.'*
>
> For the first half of the talk, I'll walk you through our motivation, existing literature bottlenecks, our four-tier system architecture, our cloud deployment, and our dataset setup. Then, Nhat will take over from Slide 8 to walk through our evaluation metrics, experimental results, attack benchmarks, and key takeaways."

---

#### Slide 2 — Outline (0:40 – 1:10)
> **[Display: Slide 2 — 5-Section Outline Grid]**
>
> "Here is a quick roadmap of what we'll cover today:
>
> First, I'll explain the background and the core trust challenges in federated learning.
> Second, we'll look at where existing verifiable FL methods run into bottlenecks.
> Third, I'll introduce our four-tier decoupled architecture and our Azure Kubernetes deployment.
> Fourth, we'll dive into the experimental results—testing under both normal data distributions and active Byzantine attacks.
> And finally, we'll wrap up with our conclusions and future directions."

---

#### Slide 3 — 1. Introduction: Background, Challenges & Contributions (1:10 – 2:25)
> **[Display: Slide 3 — Three Columns: Background, Challenges, Key Contributions]**
>
> "Starting with our motivation on Slide 3—why is this problem important?
>
> Federated learning allows edge devices to collaboratively train a shared model without sending raw data to a central server.
>
> While that protects user privacy, deploying it in the real world hits three major hurdles:
> - **Non-IID Data:** Skewed data distributions across edge clients cause severe client drift, destabilizing convergence under standard FedAvg.
> - **Malicious Updates:** Because the server cannot inspect private training sets, an adversary can easily poison the model by injecting corrupt gradients or flipping labels.
> - **Blockchain Limitations:** Storing updates on a blockchain provides an immutable audit log, but it cannot verify whether an off-chain update was computed legitimately.
>
> Our work addresses these three gaps:
> We combine client-side FedProx regularization with adaptive server-side FedAdam momentum to handle data heterogeneity;
> We decouple cryptographic verification using lightweight Groth16 zero-knowledge proofs and off-chain IPFS storage;
> And we introduce dynamic IQR anomaly filtering paired with reputation tracking to isolate malicious nodes."

---

#### Slide 4 — 2. Related Works: Comparative Analysis (2:25 – 3:30)
> **[Display: Slide 4 — Table I & Table II Literature Benchmarks]**
>
> "On Slide 4, let's look at why previous verifiable FL systems struggle on the edge.
>
> Prior schemes like VPFL and zkFL try to prove the entire gradient backpropagation inside zero-knowledge circuits. But proving non-linear operations like ReLU inside an arithmetic circuit explodes into over a million constraints. That creates an $\mathcal{O}(P)$ memory bottleneck, demanding gigabytes of RAM that typical edge devices simply don't have.
>
> Other frameworks like VerifBFL store full model weights on-chain, which quickly runs into Ethereum block gas limits.
>
> Instead of trying to prove full local training in-circuit, our approach makes a practical engineering trade-off:
> We design a minimal, edge-friendly Groth16 circuit with **just 67 constraints** to verify client identity and clamp parameter magnitudes below 5 billion, preventing overflow attacks.
> We keep the actual model weights off-chain in IPFS and store only a 32-byte hash on-chain.
> And finally, we offload fine-grained anomaly detection to statistical IQR fences and reputation scoring on the server side."

---

#### Slide 5 — 3. Our Methodology: Proposed Framework Architecture (3:30 – 4:30)
> **[Display: Slide 5 — 4-Tier Workflow Diagram & Tier Descriptions]**
>
> "Moving to Slide 5, here is how our four-tier architecture works in practice:
>
> - **1. Local Optimization:** Clients train locally using **FedProx**. The proximal penalty term ($\mu = 0.01$) keeps local weight updates from drifting too far from the global model under Non-IID data.
> - **2. Cryptographic Verification:** Clients generate an ultra-lightweight Groth16 zk-SNARK proof over the BN-128 elliptic curve. The model weights are uploaded to **IPFS**, and only the 32-byte CID and proof metadata are submitted to our **Ganache** smart contract for instant on-chain verification.
> - **3. Trust Evaluation:** The server inspects accepted updates using dynamic **Interquartile Range (IQR)** fences and cosine similarity, updating each client's reputation score via an exponential moving average.
> - **4. Adaptive Aggregation:** The server weights verified updates proportional to their reputation score and integrates them into the global model using **FedAdam's** adaptive first- and second-order momentum."

---

#### Slide 6 — 3. Our Methodology: Azure Kubernetes Service Deployment (4:30 – 5:20)
> **[Display: Slide 6 — AKS Cloud Architecture Diagram & 4 Namespaces]**
>
> "On Slide 6, we validated this setup by deploying the entire pipeline on **Microsoft Azure Kubernetes Service (AKS)** across four isolated namespaces:
>
> - **`fl-clients`:** Hosts edge client pods. Each pod is allocated **2 vCPUs (Intel Xeon Platinum @ 2.4 GHz) and 7.0 GiB of RAM**, closely mirroring real-world edge IoT gateways. Clients run FedProx training and generate proofs via Circom and SnarkJS.
> - **`ipfs`:** Operates decentralized IPFS daemons, storing multi-megabyte model parameters and providing deterministic content-addressed retrieval.
> - **`blockchain`:** Hosts our private EVM node and smart contracts for client authorization, proof verification, and immutable reputation logging.
> - **`fl-server`:** Coordinates communication rounds, retrieves verified models, applies anomaly filtering, and executes FedAdam aggregation."

---

#### Slide 7 — 4. Experimental Results: Dataset & Data Distribution (5:20 – 5:45)
> **[Display: Slide 7 — EMNIST Heatmaps (Labels 0-22 and Labels 23-46) & Specs]**
>
> "Moving to Slide 7, here is our experimental setup.
>
> We evaluated the framework on the **EMNIST Balanced benchmark**, comprising 47 character classes and over 130,000 images distributed across 5 edge clients over 40 communication rounds.
>
> As shown in the class distribution heatmaps:
> - In the **IID setting (top)**: every client receives an equal, uniform distribution across all 47 classes.
> - In the **Non-IID setting (bottom)**: we simulate severe data skew using a Dirichlet distribution with $\alpha = 0.5$. Each client only sees a handful of character classes, creating heavy local model divergence.
>
> And with our dataset and distribution setup established, I'll hand things over to Nhat, who's going to walk through our evaluation metrics, experimental results, and attack resilience."

---

### [PRESENTER 2: Nguyen Tran-Bui-Nhat] (Slides 8 to 13: ~5:45 – 9:45)

#### Slide 8 — 4. Experimental Results: Evaluation Metrics (5:45 – 6:50)
> **[Display: Slide 8 — Three Columns: Model Performance, Malicious Update Detection, Reputation Mechanism]**
>
> "Thanks, Kiet. Hi everyone, I'm Nhat, and I'll take you through our evaluation metrics and experimental findings.
>
> Starting on Slide 8, to evaluate the system, we established three core metric pillars:
>
> First, **Model Performance**: We track global top-1 classification accuracy across 47 balanced EMNIST classes, monitoring loss convergence and descent stability across all 40 communication rounds under both IID and Non-IID distributions.
>
> Second, **Malicious Update Detection**: We evaluate the system's ability to accept valid client updates while intercepting poisoned updates through our two-stage gating—combining Groth16 zero-knowledge proof verification with dynamic Interquartile Range (IQR) fences.
>
> And third, **Reputation Dynamics**: We track how client trust scores evolve over time using an Exponential Moving Average with an inertia weight of $\alpha = 0.8$. These scores are bounded between 0.10 and 1.0, and directly scale the client's aggregation weight in FedAdam, allowing the system to dynamically down-weight suspicious participants."

---

#### Slide 9 — 4. Experimental Results: Normal Training Scenarios (IID vs. Non-IID) (6:50 – 7:55)
> **[Display: Slide 9 — Accuracy/Loss Curves, Average Reputation Chart, Benchmarked Overhead Note]**
>
> "Moving to Slide 9, Scenario 1 looks at normal training performance across both IID and Non-IID distributions.
>
> Looking at the chart on the left, our framework reaches **75.2% top-1 accuracy** on the uniform IID dataset, and **71.2%** under heavy Non-IID skew. What's really encouraging here is that extreme data heterogeneity only causes a **4-percentage-point drop** in accuracy. You can also see that both loss curves trend down smoothly across all 40 rounds, showing that FedProx and FedAdam are working together to keep client drift under control.
>
> Now turning to the right-hand plot, this shows client reputation over time. As clients reliably submit valid updates, their average reputation steadily rises from the initial 0.5 baseline and levels off around **0.76 to 0.77**. This confirms that honest participants build up trust consistently.
>
> Now, you'll notice the two plots here focus on accuracy, loss, and reputation trajectories—there's no overhead chart plotted on this slide, but it's important to highlight our timing benchmarks from the paper: on edge devices, Groth16 zero-knowledge proof generation takes only about **0.35 seconds**, which is less than 3.5% overhead on local training. And because we only store the 32-byte IPFS CID on-chain, smart contract verification finishes in under **0.20 seconds** per round with negligible gas costs."

---

#### Slide 10 — 4. Experimental Results: Byzantine Attack Resilience & Defense (7:55 – 8:55)
> **[Display: Slide 10 — Accuracy Curves (Normal vs. Byzantine), Reputation Dynamics Chart]**
>
> "Now, on Slide 10, here we evaluate our framework's robustness against active Byzantine attacks.
>
> In this scenario, malicious participants inject high-variance Gaussian noise—with a variance of $3.0^2$—and execute label-flipping attacks to try to disrupt training.
>
> Looking at the left chart, we compare the global model accuracy under normal settings against the same system under Byzantine attack. As you can see, our framework maintains stable convergence throughout training, tracking the normal run very closely and achieving comparable accuracy around 61 to 62% by round 40. The corrupted updates completely fail to derail or degrade the global model.
>
> The plot on the right explains why: our reputation-based anomaly detection in action. As soon as client 5 submits corrupted updates, the system flags the anomaly. Its reputation score plunges immediately to the minimum bound of 0.10 within the first few rounds, neutralizing its aggregation weight in FedAdam. Meanwhile, legitimate clients maintain high, stable reputation scores between 0.75 and 0.95, ensuring that only trustworthy updates drive the global model."

---

#### Slide 11 — 5. Conclusions & Future Work (8:55 – 9:30)
> **[Display: Slide 11 — Conclusions & Future Work Columns]**
>
> "To wrap up our presentation on Slide 11, here are our conclusions and future directions.
>
> In conclusion:
> - We developed a blockchain-enabled federated learning framework integrating FedProx, FedAdam, zero-knowledge proofs, IPFS, and reputation mechanisms.
> - We verify model updates using ZKP and smart contracts, ensuring complete transparency and traceability.
> - The framework improves training stability across both IID and Non-IID data distributions.
> - We achieve low blockchain verification overhead while maintaining stable learning performance.
> - And we successfully detect suspicious clients and minimize the impact of abnormal updates through reputation-based anomaly detection.
>
> Looking ahead to future work:
> - We plan to evaluate the framework on larger real-world applications in Healthcare, Smart Cities, IoT, and Finance.
> - We will extend deployment to cross-organization and edge computing environments.
> - We aim to improve blockchain scalability and trust management mechanisms.
> - And finally, we will explore advanced privacy-preserving techniques for large-scale federated learning systems."

---

#### Slide 12 — 6. References (9:30 – 9:40)
> **[Display: Slide 12 — 12 Key Literature References]**
>
> "Slide 12 highlights the key references that informed our optimization pipeline and verifiable federated learning architecture."

---

#### Slide 13 — Acknowledgments & Q&A (9:40 – 9:55)
> **[Display: Slide 13 — Center Card with Thank You, Presenter Info, Grant Acknowledgment]**
>
> "Finally, we'd like to thank the University of Information Technology, VNU-HCM, for funding this research under grant CS4-2026-80290.
>
> Thank you all for listening, and Kiet and I would be happy to take any questions you have."

---

## Part 2: Q&A Defense Guide (Key Technical Answers)

*(Toughest questions session chairs and reviewers might ask, with concise, natural answers).*

### Q1: *"Why does your Groth16 circuit have only 67 constraints? Isn't that too small to verify deep neural network training?"*
> **Answer:** "Yes, and that is our deliberate design choice. Prior schemes like VPFL attempt to prove multi-epoch backpropagation inside zk-SNARKs. However, non-linear activations like ReLU require bit-decomposition into 32 to 64 R1CS constraints per neuron, generating over $10^7$ constraints for even a modest network and requiring 16 to 32 GB of RAM—which crashes edge devices.  
> We decouple cryptographic sanity from statistical learning: our Groth16 circuit acts as an $\mathcal{O}(1)$ gatekeeper checking client identity authorization and parameter magnitude bounds ($W_{\max} = 5 \times 10^9$) to block overflow and gradient explosion in just 0.35 seconds. Directional correctness and subtle poisoning are handled by our server-side dynamic IQR fences and reputation system."

### Q2: *"Under extreme Non-IID skew ($\alpha = 0.5$), how do you avoid falsely penalizing honest clients with unique data distributions?"*
> **Answer:** "We provide three protections:
> 1. **Client-side FedProx Regularization:** A proximal penalty $\mu = 0.01$ bounds local parameter drift within an admissible optimization neighborhood.
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
> 4. Kiet records Slides 1 to 7; Nhat records Slides 8 to 13 following the transcript above.  
> 5. Export to **Full HD (1080p)** `.mp4`. Total duration should be between **9:30 and 9:55 minutes**.
