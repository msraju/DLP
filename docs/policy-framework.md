# Enterprise Data Classification & Policy Framework

## Data Classification Levels

| Level | Label | Description | Examples | Handling Controls |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **Public** | Information intended for public release. | Press releases, Marketing material. | No restrictions. |
| **L2** | **Internal** | Data for internal operations only. | Employee directories, policies, internal memos. | Encryption at rest; Access Control Lists (ACLs). |
| **L3** | **Confidential** | Sensitive business data. Harmful if leaked. | Financial reports (pre-release), Customer lists, Source code. | DLP Enforced; Encryption in transit/rest; 2FA required. |
| **L4** | **Restricted** | Highly sensitive PII/PCI/PHI. Regulatory impact. | SSN, Credit Card #s, Health records, Encryption Keys. | Strict DLP Blocking; Just-in-Time access; Full Audit logging. |

## Detection Rules & Patterns (Regex)

Effective DLP requires precise detection to minimize False Positives. Below are standard definitions used in our policies.

### 1. Credit Card Numbers (PCI-DSS)
**Pattern:** Matches major card brands, utilizes Luhn algorithm check.
```regex
\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b
```

### 2. US Social Security Number (PII)
**Pattern:** Keying off structure `AAA-GG-SSSS`.
```regex
\b(?!000|666|9\d{2})[0-9]{3}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}\b
```
*Tuning:* Combine with keywords "SSN", "Social Security", "Tax ID" to reduce noise.

### 3. Oracle Cloud Infrastructure (OCI) Keys (Secret Detection)
**Pattern:** Detection of potential hardcoded API keys or private keys.
```regex
(?:ocid1\.user\.oc1\..+|[A-Fa-f0-9]{64})
```

## Policy Action Matrix

| Source Channel | L1 (Public) | L2 (Internal) | L3 (Confidential) | L4 (Restricted) |
| :--- | :--- | :--- | :--- | :--- |
| **Corporate Email** | Allow | Allow | Notify Manager | **Block & Alert** |
| **Web Upload (SaaS)** | Allow | Allow | **Block (Unsanctioned)** | **Block & Alert** |
| **USB Storage** | Allow | Read-Only | **Block** | **Block** |
| **Printer** | Allow | Allow | Watermark | **Block** |
