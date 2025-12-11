# Comprehensive DLP Strategy & Architecture

## Executive Vision
To shift from a "Block-Everything" posture to a "risk-adaptive" security model that enables business productivity while protecting critical intellectual property and customer data compliant with GDPR, CCPA, and FedRAMP.

## 3-Pillar Architecture

### 1. Endpoint DLP (The Edge)
Agents deployed on all corporate laptops/desktops.
*   **Focus:** Data in Use (Copy/Paste, Screenshot), Data in Motion (USB, Printing), Data at Rest (Local discovery).
*   **Oracle Relevance:** Protecting source code repositories locally and preventing upload to personal GitHub accounts.

### 2. Network DLP (The Perimeter)
Integration with Web Proxies (SWG) and Email Gateways (MTA).
*   **Focus:** HTTP/HTTPS/FTP traffic and SMTP.
*   **Strategy:** SSL Inspection is mandatory. Integration with CASB for Shadow IT visibility.

### 3. Cloud DLP (The Backend/SaaS)
API-based integration with OCI Buckets, OneDrive, Slack, and Salesforce.
*   **Focus:** Data at Rest in the cloud.
*   **Strategy:** Scan OCI Object Storage for publicly accessible buckets containing PII. Automated remediation (auto-quarantine).

## Incident Response Integration
DLP is not a silo. It must feed into the broader SOC ecosystem.
*   **SIEM Integration:** All DLP alerts forwarded to Splunk/Sentinel.
*   **SOAR Automation:** High-confidence L4 alerts trigger automated ticket creation (Jira/ServiceNow) and user account suspension if mass-exfiltration is detected.

## Success Metrics (KPIs)
1.  **False Positive Rate (FPR):** Target < 5%.
2.  **Mean Time To Detect (MTTD):** Target < 10 minutes.
3.  **Policy Coverage:** % of critical assets covered by active blocking policies.
