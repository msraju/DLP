# Scenario: Accidental Cloud Exposure (S3 / GitHub)

## The Threat
Well-meaning developers often commit secrets to public code repos or misconfigure S3 buckets to "Public Read", exposing millions of records.

## 1. Detection
*   **Vector 1 (GitHub):** Cloud DLP scans public GitHub commits for regex matches of our internal `API_KEY` patterns.
*   **Vector 2 (AWS S3):** Cloud Security Posture Management (CSPM) tool alerts on `S3_Bucket_Policy_Change` where `Effect: Allow, Principal: *`.

## 2. Automated Response (Bot-Driven)
Manual response is too slow for cloud speeds.
1.  **Auto-Remediation (S3):**
    *   Lambda function triggers on the alert.
    *   Reverts the Bucket Policy to "Private".
    *   Tags the bucket `Quarantine:True`.
2.  **Auto-Revocation (GitHub Keys):**
    *   If an internal API Key is found on public GitHub:
    *   Call IAM API to **deactivate** that key immediately.
    *   Slack the developer: "Your key was leaked and has been nuked."

## 3. Human Analysis
*   **Impact Assessment:**
    *   How long was the bucket public? (Check Access Logs).
    *   Did anyone *other than the scanner* download the data?
*   **Root Cause:**
    *   Was it a Terraform misconfiguration?
    *   Lack of peer review?

## 4. Prevention
*   **Pre-Commit Hooks:** Install `git-secrets` on all developer laptops to block commits locally.
*   **CI/CD Gates:** Fail build pipelines if high-entropy strings are detected in the code.
