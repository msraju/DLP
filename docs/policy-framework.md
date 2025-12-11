# Global Policy Framework & Classification Standards

## 1. Classification Methodology
We follow a 4-tier data classification model aligned with NIST 800-53 and ISO 27001.

| Class | Tag | Definition | Examples | DLP Action |
| :--- | :--- | :--- | :--- | :--- |
| **C1** | `PUBLIC` | Information intended for public consumption. | Marketing brochures, Press releases. | **Monitor Only** |
| **C2** | `INTERNAL` | Business operations data. | Org charts, Internal Wikis, Policies. | **Monitor & Watermark** |
| **C3** | `CONFIDENTIAL` | Sensitive business data; significant harm if leaked. | Start-up configs, Pricing models, Customer lists. | **Block (External)** |
| **C4** | `RESTRICTED` | Regulatory/Legal impact; notification required upon breach. | SSN, Credit Cards, ePHI, Encryption Keys. | **Block & Quarantine** |

## 2. Technical Rule Definitions

### A. Pattern Matching (Regex Library)

**1. GDPR: EU IBAN (International Bank Account Number)**
*Rationale*: Financial compliance for EU operations.
```regex
\b[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?!(?:[ ]?[0-9]){3})(?:[ ]?[0-9]{1,2})?\b
```

**2. AWS Access Key ID (Secrets)**
*Rationale*: Preventing cloud compromise.
```regex
\b(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}\b
```

**3. US & Canada Phones (Contextual)**
*Rationale*: High false positive potential. Must be near keywords.
```regex
(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})
```
*Proximity Keywords required (within 30 chars):* "Phone", "Mobile", "Cell", "Contact".

### B. Logical Combinations (Compound Rules)

**Rule: High-Confidence PCI Data**
> IF (Regex match "CreditCard")
> AND (Luhn Check == PASS)
> AND (Keyword match "CVC" OR "Expiry" OR "Visa" OR "Mastercard" within 50 chars)
> THEN Severity = CRITICAL

**Rule: Source Code Leakage**
> IF (File Extension IN `.py`, `.c`, `.cpp`, `.java`, `.go`)
> AND (Keyword match "INTERNAL_USE_ONLY" OR "Copyright 2024 Corp")
> AND (Destination != "github.com/corp-org/*")
> THEN Action = BLOCK

## 3. Policy Tuning Lifecycle
Policies are not static. We employ a weekly tuning cycle:
1.  **Monitor Mode**: Run new rule for 7 days without blocking.
2.  **FPR Analysis**: Analyst reviews sample alerts. If False Positive Rate > 5%, refine Regex or add logical AND conditions.
3.  **Active Blocking**: Promote to block mode only after FPR < 1%.
