# Apple Silicon Models

The Fine-Tuning workspace defaults to `mlx-community/Qwen3-8B-4bit`. On an
Apple Silicon Mac with `mlx-lm` installed, MLX-LM downloads this model into its
local cache when the first training job starts; no separate manual download is
needed. Plan sufficient free disk space and unified memory before queuing an
8B run.

When a job succeeds, open Local Chat and select the **Fine-tuned models** tab.
The workbench invokes `mlx_lm.generate` with the recorded base model and adapter
path. This model stays local and every chat response remains exploratory until
it is explicitly reviewed and promoted.

# Apple Silicon MLX-LM and Ollama Pilot

This guide runs SynthSEA locally on an Apple Silicon MacBook. MLX-LM is the
fine-tuning engine; Ollama is the local chat and generation runtime. It is for
small pilot experiments, quality checks, and ablation validation. It is not
evidence for the final paper until datasets, language review, and the complete
evaluation protocol are approved.

## 1. Install the project

```bash
git clone <your-synthsea-repository-url>
cd SynthSEA
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the deterministic checks first:

```bash
pytest -q
ruff check src tests
mypy src
```

## 2. Install MLX-LM for fine-tuning

MLX is designed for efficient machine learning on Apple Silicon. MLX-LM supports
low-rank and full fine-tuning of compatible models, including quantized models.

```bash
python -m pip install mlx-lm
mlx_lm.lora --help
```

Before starting a job, record the MLX-LM version, base model or adapter,
model-license terms, dataset and split versions, seed, adapter configuration,
macOS version, and available unified memory. The FastAPI workbench job service
will own the command, logs, checkpoint, cancellation state, and artifact record.

## 3. Install and start Ollama for chat or generation

Install Ollama for macOS from [ollama.com/download](https://ollama.com/download).
Then download a small multilingual-capable model appropriate for available
unified memory. The initial profile uses `qwen2.5:3b`.

```bash
ollama pull qwen2.5:3b
ollama serve
```

In another terminal, confirm the local API is available:

```bash
ollama list
curl http://127.0.0.1:11434/api/tags
```

## 4. Run a local generation pilot

```bash
source .venv/bin/activate
synthsea generate \
  --adapter ollama \
  --model qwen2.5:3b \
  --profile singlish \
  --prompt "Write one culturally appropriate customer-support instruction in Singlish." \
  --temperature 0.2 \
  --output experiments/ollama-pilot/singlish.json
```

The command uses Ollama's local `/api/generate` endpoint with `stream: false`.
It records the model tag, seed, input tokens, output tokens, and zero remote
cost. Keep the model tag fixed for an experiment and retain generated artifacts
and manifests.

## 5. Pilot research sequence

1. Run MLX-LM fine-tuning only with an approved dataset, compatible model, and
  recorded license and configuration.
2. Run the same prompt set with `--adapter fixture` and `--adapter ollama` for
  exploratory generation comparison.
3. Use one language profile at a time: Singlish, Malay, Tamil, and
   Singapore-context Mandarin.
4. Run monolingual controls before English-mixing conditions.
5. Review a small sample with qualified language or cultural reviewers.
6. Run filtering, deduplication, and provenance checks before downstream use.
7. Treat any model output as provisional until the approved experiment protocol,
   evidence manifest, and claim checks succeed.

## Apple Silicon notes

- MLX-LM is the fine-tuning engine; Ollama is not used to train models.
- MLX uses Apple Silicon's unified memory. Begin with a small compatible model
  and a small adapter configuration; increase only after recording memory and
  runtime behavior.
- Ollama uses the local machine's available Apple Silicon acceleration for chat
  and generation.
- Begin with a small model and a batch size of one; increase only after checking
  memory pressure, latency, and output quality.
- Keep the laptop connected to power for longer experiments and record the model
  tag, macOS version, available unified memory, MLX-LM version, and Ollama
  version where used in the run environment metadata.
- Do not mix results from different model tags, quantizations, MLX-LM versions,
  adapter settings, or Ollama versions inside one comparison condition.

## Official references

- [Ollama macOS installation](https://docs.ollama.com/mac)
- [Ollama generate API](https://docs.ollama.com/api/generate)
- [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
- [MLX documentation](https://ml-explore.github.io/mlx/build/html/index.html)
- [MLX-LM project](https://github.com/ml-explore/mlx-lm)