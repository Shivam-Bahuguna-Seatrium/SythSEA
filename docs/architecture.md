# SynthSEA Architecture

This diagram shows the complete research pipeline from language-aware inputs to the reproducible report package.

```mermaid
flowchart TD
    A[Research inputs] --> B[Language profiles]
    B --> C[Resource discovery]
    C --> D[Topic and cultural context]

    subgraph G[Multi-agent generation]
        D --> E[Instruction generation]
        OA[Local Ollama on Apple Silicon] --> E
        E --> F[Language specialists]
        F --> H[Code-switch control]
    end

    H --> I[Cultural validation]
    I --> J[Semantic and factual validation]
    J --> K[Diversity and difficulty checks]
    K --> L[Adversarial critic]
    L --> M[Judge and aggregator]
    M --> N{Quality gate}
    N -- Revise --> O[Refinement]
    O --> E
    N -- Pass --> P[Deduplication]

    P --> Q[Synthetic instruction dataset]
    Q --> FT[MLX-LM fine-tuning on Apple Silicon]
    FT --> R[Baseline, ablation, and downstream experiments]
    R --> S[Per-language evaluation]
    S --> T[Evidence manifest and checksums]

    subgraph V[Research and publication]
        T --> U[Claim-to-evidence matrix]
        U --> W[Readiness validation]
        W --> X[Reproducible report package]
    end

    S --> Y[Metrics, human review, statistics, and error analysis]
    Y --> T

    X --> Z[Manuscript, tables, figures, and appendix]

    OA --> CHAT[Ollama local chat and generation]
```

The four language settings remain separate throughout evaluation:
Singapore English/Singlish, Malay, Tamil, and Singapore-context Mandarin.
