# OpenVals

> AI Trust Intelligence Platform for LLMs, SLMs, Private AI, and Enterprise AI Systems

**Evaluate • Benchmark • Trust Intelligence**

OpenVals is an enterprise-grade AI evaluation and trust platform designed to help organizations measure, compare, validate, and deploy AI systems with confidence.

Unlike traditional AI benchmarks that focus only on accuracy, OpenVals evaluates performance, trustworthiness, factuality, reliability, safety, hallucination risk, governance readiness, and deployment confidence.

# OpenVals

[![PyPI Version](https://img.shields.io/pypi/v/openvals)](https://pypi.org/project/openvals/)
[![Python](https://img.shields.io/pypi/pyversions/openvals)](https://pypi.org/project/openvals/)
[![License](https://img.shields.io/badge/license-DPCL--CE-blue)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/openvals)](https://pypi.org/project/openvals/)
[![GitHub Stars](https://img.shields.io/github/stars/vishwanathakuthota/openvals)](https://github.com/vishwanathakuthota/openvals)

> Trust Infrastructure for AI

---

## What is OpenVals?

OpenVals is an AI Trust Intelligence Platform that helps enterprises evaluate, validate, benchmark, and govern AI systems before production deployment.

OpenVals answers one question:

**Can you trust your AI?**

## Why OpenVals?

Most AI models perform well in demonstrations.

Production environments require something different:

- Can the model be trusted?
- Is the response factually correct?
- How reliable is the model under repeated execution?
- What is the hallucination risk?
- Is the dataset itself trustworthy?
- Is the model ready for enterprise deployment?

OpenVals was built to answer these questions.
## Why OpenVals?

| Capability | Traditional Benchmarking | OpenVals |
|------------|------------|------------|
| Accuracy | ✓ | ✓ |
| Latency | ✓ | ✓ |
| Semantic Similarity | ✓ | ✓ |
| Hallucination Detection | Limited | ✓ |
| Factuality Analysis | Limited | ✓ |
| Trust Scoring | ✗ | ✓ |
| Governance Readiness | ✗ | ✓ |
| Executive Reporting | ✗ | ✓ |
| Enterprise Validation | ✗ | ✓ |

---

## Enterprise Use Cases

### AI Model Selection

Compare GPT, Claude, Llama, Mistral, and private models before deployment.

### Private AI Validation

Validate enterprise AI running on Ollama, vLLM, or self-hosted infrastructure.

### AI Procurement

Benchmark vendor AI solutions before purchasing decisions.

### AI Governance

Measure AI readiness against organizational trust and governance requirements.

### AI Red Teaming Foundation

Identify hallucination risk, factual weaknesses, and trust gaps.

### Executive Reporting

Generate trust dashboards and executive-level AI readiness reports.


## Core Platform Capabilities

### AI Evaluation Engine

Evaluate AI systems using multiple dimensions:

- Accuracy
- Semantic Similarity
- Reliability
- Safety
- Consistency
- Variance
- Latency
- Factuality
- Hallucination Risk

---

### Decision Reliability Score (DRS)

OpenVals introduces the Decision Reliability Score (DRS), a deployment-focused trust metric designed to determine whether an AI system is suitable for real-world production environments.

DRS combines:

- Accuracy
- Semantic Intelligence
- Reliability
- Safety
- Consistency
- Variance
- Latency
- Hallucination Risk
- Factuality

Traditional leaderboards answer:

"Which model scored highest?"

DRS answers:

"Which model can be trusted in production?"

---

### Factuality Engine

OpenVals includes a dedicated factuality scoring engine capable of:

- Semantic factual alignment
- Numeric consistency validation
- Contradiction detection
- Factual risk classification

Output:

```text
Factuality Score
Risk Level
Issues Detected
```

---

### Hallucination Probability Index (HPI)

OpenVals introduces HPI (Hallucination Probability Index).

HPI estimates the probability that a model response contains hallucinated or unreliable content.

Risk Levels:

- Low
- Medium
- High
- Critical

---

### Dataset Intelligence

Trust the dataset before trusting the model.

Dataset Validation CLI includes:

- Schema validation
- Quality validation
- Duplicate detection
- Missing field detection
- Dataset Health Score (DHS)

## 60-Second Quick Start

Install:

```bash
pip install openvals
```

Benchmark:

```bash
openvals benchmark \
  --dataset finance \
  --models mistral,llama3
```

Output:

```text
Model      Accuracy    DRS
--------------------------------
llama3     91.4        89.2
mistral    87.8        82.4
QWEN       70.7        69.7
```

### validate-dataset examples

```bash
openvals validate-dataset finance
```

```bash
openvals validate-dataset ./customer_dataset.json
```

```bash
openvals validate-dataset ./customer_dataset.csv
```

```bash
openvals validate-dataset finance
```

### Benchmark multiple models:

```bash
openvals benchmark \
  --dataset finance \
  --models mistral,llama3 \
  --config finance
```
### Parallel Execution Engine

OpenVals supports parallel model execution for faster benchmarking.

```bash
openvals benchmark \
  --dataset finance \
  --models mistral,llama3 \
  --parallel \
  --max-workers 2
```

Benefits:

- Reduced benchmark runtime
- Better scalability
- Future SaaS readiness


Show version:

```bash
openvals version
```
---

## Example Output

```text
===================================================
OpenVals Trust Intelligence Report
===================================================

Model: llama3

Accuracy Score      : 91.4
Semantic Score      : 89.1
Factuality Score    : 92.3
Safety Score        : 95.2
Latency Score       : 83.0

Hallucination Risk  : LOW

Decision Reliability Score (DRS)

89.2 / 100

Deployment Status:

READY FOR PRODUCTION
```
## Screenshots

### Trust Dashboard

<img src="./docs/images/dashboard.png">

### Sample Evaluation Report

<img src="./docs/images/sample-report.html">

### Dataset Validation

<img src="./docs/images/dataset-validation.png">

### Multi-Model Benchmarking

Compare multiple models under identical conditions.

Supported:

- Ollama Models
- Local Models
- Private AI
- Enterprise AI
- Future API-based providers

Capabilities:

- Side-by-side comparison
- Normalized ranking
- DRS ranking
- Trust Intelligence reporting

---

## Supported Benchmark Domains

Current datasets:

- Finance
- Healthcare
- Cybersecurity
- Legal
- Insurance(coming soon)
- Manufacturing(coming soon)
- Retail(coming soon)
- Enterprise Operations
- Software Engineering
- Math
- Reasoning

---

## OpenVals Architecture

Enterprise Dataset
        ↓
Dataset Validation
        ↓
AI Evaluation Engine
        ↓
Trust Intelligence Layer
        ↓
Factuality Engine
        ↓
Hallucination Detection
        ↓
Decision Reliability Score
        ↓
Executive Reporting

---

## OpenVals Ecosystem

OpenVals is part of a larger AI Trust & Assurance ecosystem.

### OpenVals

AI Validation & Trust Intelligence

### AI Compass

AI Maturity & Readiness Assessment

### DrPinnacle

AI Strategy, Governance & Advisory

### OpenVals Cloud (Coming Soon)

Continuous AI Validation Platform

---

## Vision

OpenVals is building the Trust Intelligence Layer for AI.

The future of AI is not determined by which model is largest.

The future belongs to AI systems that can be measured, validated, governed, and trusted.

## Evaluation vs Validation

Most platforms evaluate AI.

OpenVals validates trust.

Evaluation answers:

"How well does the model perform?"

Validation answers:

"Can the model be trusted in production?"

OpenVals was built around this distinction.

---

## Contributing

Contributions are welcome.

- Fork the repository
- Create a feature branch
- Submit a pull request

---

## License

Dr.Pinnacle Community Edition License (DPCL-CE)

---

## Developed By

DrPinnacle -- AI Trust, Validation & Governance Initiative

[DrPinnacle](drpinnacle.com)

[OpenVals](openvalidations.com)
---

## Keywords

AI Evaluation Platform, AI Trust Platform, LLM Evaluation, AI Benchmarking, AI Governance, AI Validation, Factuality Scoring, Hallucination Detection, DRS Score, AI Trust Intelligence, Enterprise AI Validation, Private AI Evaluation, Ollama Benchmarking, AI Reliability Testing, OpenVals, Vishwanath Akuthota