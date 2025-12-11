# Comprehensive DLP Architecture & Strategy

## 1. Architectural Philosophy
The modern DLP stack must move beyond simple regex matching. This framework implements a **Zero Trust Data Security** model, assuming that the network perimeter is porous. We enforce controls at the data level itself.

## 2. Global Architecture Diagram
This high-level design illustrates the flow of data and inspection points across the enterprise.

```mermaid
graph TB
    subgraph "Endpoint Layer (The Edge)"
        Laptop[Corp Laptop] -->|Writes| USB[USB Storage]
        Laptop -->|Prints| Printer
        Laptop -->|Uploads| Web[Web Browser]
        Agent[DLP Agent] -.->|Intercepts| Laptop
    end

    subgraph "Network Layer (The Pipe)"
        Web --> Proxy[SWG / CASB Proxy]
        Proxy -->|ICAP| DLPServer[DLP Inspection Engine]
        Email[Corp Email] -->|SMTP| MTA[Email Gateway]
        MTA -->|ICAP| DLPServer
    end

    subgraph "Cloud & SaaS (The Backend)"
        API[API Integration] -->|Scans| O365[Office 365]
        API -->|Scans| Slack
        API -->|Scans| AWS[AWS/GCP/Azure]
    end

    subgraph "Security Operations"
        DLPServer -->|Alerts| SIEM[SIEM (Splunk/Sentinel)]
        Agent -->|Telemetry| SIEM
        SIEM -->|Triggers| SOAR[SOAR Playbooks]
    end

    classDef protect fill:#f9f,stroke:#333;
    class Agent,DLPServer,API protect;
```

## 3. Detailed Prevention Layers

### A. Endpoint DLP (Data-in-Use)
*   **Capabilities**:
    *   **Clipboard Hooking**: Prevent copying >50 records of PII to clipboard.
    *   **Application Control**: Block upload to unsanctioned apps (e.g., WhatsApp Desktop, Personal Dropbox).
    *   **Offline Enforcement**: Rules must persist when the device is disconnected from VPN.
*   **Technique**: Kernel-level drivers for file system filtering (Mini-filter drivers on Windows).

### B. Network DLP (Data-in-Motion)
*   **Capabilities**:
    *   **SSL Interception**: Inspection of encrypted traffic (HTTPS) via SWG.
    *   **Email Sanitization**: Removing attachments or replacing them with secure links.
*   **Protocol Support**: SMTP, HTTP/S, FTP, SMB.

### C. Cloud DLP (Data-at-Rest)
*   **Capabilities**:
    *   **API Scanning**: Asynchronous scanning of data stored in SaaS.
    *   **Configuration Audits**: Detecting public link sharing shares (e.g., "Anyone with the link").
*   **Latency**: Near real-time (API event hooks) vs Scheduled (Crawler).

## 4. Advanced Detection Logic (Beyond Regex)

To solve the "False Positive" crisis, we employ:

| Technique | Description | Use Case |
| :--- | :--- | :--- |
| **Exact Data Match (EDM)** | Hashing a structured DB (e.g., SQL dump) and matching data against these hashes. | Customer DBs, Employee Payroll with 100% accuracy. |
| **Indexed Document Matching (IDM)** | Fingerprinting unstructured text/files (rolling hash). | Detecting leakage of specific Whitepapers, Source Code, or Design Docs. |
| **Optical Character Recognition (OCR)** | Extracting text from images (PNG, JPEG, PDF). | Screenshots of sensitive data, Scanned IDs. |
| **Vector Machine Learning** | ML models trained on "sensitive" vs "non-sensitive" document corpuses. | Legal contracts, M&A documents that vary in format. |
