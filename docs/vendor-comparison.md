# DLP Vendor Evaluation Matrix

## Overview
This document serves as a decision framework for selecting an Enterprise DLP solution. It weighs technical capability against operational overhead.

## Scoring Methodology
*   **Weight (1-5):** Importance of the feature to our organization.
*   **Score (1-10):** Vendor performance.
*   **Weighted Score:** Weight x Score.

### 1. Vendor Comparison Table

| Service Feature | Weight | **Vendor A (Symantec)** | **Vendor B (Zscaler)** | **Vendor C (Purview)** |
| :--- | :--- | :--- | :--- | :--- |
| **Endpoint Agent Stability** | 5 | 9 (Robust) | 7 (Newer agent) | 8 (Built-in Win11) |
| **Exact Data Match (EDM)** | 5 | 10 (Gold Standard) | 8 (Good) | 6 (Limited Scale) |
| **Cloud/SaaS Integration** | 4 | 6 (Requires CASB) | 9 (Native Cloud) | 10 (Native O365) |
| **Mac/Linux Support** | 3 | 8 | 8 | 4 (Weak on Linux) |
| **SSL Inspection (Network)** | 4 | 7 ( Appliance) | 10 (Cloud Proxy) | 0 (Endpoint only) |
| **Total Weighted Score** | **-** | **172** | **179** | **160** |

### 2. Deep Dive Analysis

#### Vendor A (Symantec / Broadcom)
*   **Pros:** Best-in-class detection engine. The EDM hashing is incredibly fast and supports 100M+ rows.
*   **Cons:** High infrastructure cost (requires on-prem servers or heavy VM footprint). "Heavy" agent can crash developer IDEs.

#### Vendor B (Zscaler / Netskope - SSE Approach)
*   **Pros:** Zero infrastructure (Cloud Native). Follows the user everywhere without VPN. Exceptional SSL inspection at scale.
*   **Cons:** Endpoint agent (on-device) DLP is less mature than Symantec. Dependency on internet connectivity.

#### Vendor C (Microsoft Purview)
*   **Pros:** Frictionless deployment for Windows shops (built-in). Best-in-class classification for Office docs.
*   **Cons:** Difficult to manage on macOS/Linux. "Compliance Center" UI is slow and complex.

### 3. Recommendation
**Primary Choice: Vendor B (SSE Provider)**
*Rationale:* As a cloud-first organization with 50% remote workforce, the latency introduced by backhauling traffic to on-prem appliances (Vendor A) is unacceptable. Vendor B provides immediate visibility into Shadow IT and personal Webmail without VPN.
