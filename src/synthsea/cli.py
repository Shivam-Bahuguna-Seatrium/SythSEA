"""Command-line entry point for the CPU-first SynthSEA workflow."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from synthsea import __version__
from synthsea.config.loader import load_yaml
from synthsea.config.schemas import RunStatus
from synthsea.data.models import SourceDataset
from synthsea.data.storage import write_json
from synthsea.experiments.config import ExperimentConfig
from synthsea.experiments.runner import ExperimentRunner
from synthsea.export.reports import write_publication_package
from synthsea.generation.adapters import DeterministicAdapter, GenerationAdapter, OllamaAdapter
from synthsea.generation.runner import GenerationConfig, GenerationRunner
from synthsea.paper.builder import detect_document_tools
from synthsea.paper.compliance import validate_venue
from synthsea.paper.evidence import verify_manifest
from synthsea.paper.models import EvidenceManifest, VenueFormat, VenueProfile
from synthsea.paper.package import write_paper_package
from synthsea.paper.renderer import render_manuscript
from synthsea.paper.sections import assemble_sections
from synthsea.research.claims import validate_claim_links
from synthsea.research.dossier import build_dossier, write_dossier_package
from synthsea.research.evidence import load_evidence_records, verify_records, write_evidence_report
from synthsea.research.io import load_artifact, write_artifact
from synthsea.research.matrix import build_matrix, load_matrix, write_matrix
from synthsea.research.models import (
    ClaimEvidenceLink,
    ResearchDossier,
)
from synthsea.research.package import write_research_package
from synthsea.research.readiness import build_readiness
from synthsea.research.sources import load_sources
from synthsea.tracking.catalog import Catalog

app = typer.Typer(no_args_is_help=True, help="SynthSEA research pipeline CLI")
data_app = typer.Typer(help="Dataset registration commands")
experiment_app = typer.Typer(help="Experiment commands")
paper_app = typer.Typer(help="Paper package commands")
research_app = typer.Typer(help="Research dossier and final report commands")
DEFAULT_OUTPUT = Path("experiments/generated.json")
app.add_typer(data_app, name="data")
app.add_typer(experiment_app, name="experiment")
app.add_typer(paper_app, name="paper")
app.add_typer(research_app, name="research")


@app.command()
def version() -> None:
    """Print the installed SynthSEA version."""

    typer.echo(__version__)


@data_app.command("register")
def register_dataset(config: str = typer.Argument(..., help="Dataset configuration path")) -> None:
    """Validate and register a dataset configuration."""

    dataset = SourceDataset.model_validate(load_yaml(Path(config)))
    catalog = Catalog(Path("experiments/catalog.duckdb"))
    catalog.register_run(dataset.dataset_id, RunStatus.PLANNED)
    catalog.close()
    typer.echo(dataset.dataset_id)


@app.command()
def generate(
    prompt: Annotated[str, typer.Option(help="Prompt to generate")] = "Explain hello",
    profile: Annotated[str, typer.Option(help="Language profile ID")] = "singlish",
    adapter: Annotated[str, typer.Option(help="Generation adapter: fixture or ollama")] = "fixture",
    model: Annotated[str, typer.Option(help="Ollama model tag")] = "qwen2.5:3b",
    ollama_host: Annotated[str, typer.Option(help="Local Ollama server URL")] = (
        "http://127.0.0.1:11434"
    ),
    temperature: Annotated[float, typer.Option(help="Ollama sampling temperature")] = 0.2,
    output: Annotated[Path, typer.Option(help="Output artifact")] = DEFAULT_OUTPUT,
) -> None:
    """Run deterministic fixture generation or local Ollama generation."""

    selected_adapter: GenerationAdapter
    if adapter == "fixture":
        selected_adapter = DeterministicAdapter()
        model_version = "fixture-0.1.0"
    elif adapter == "ollama":
        selected_adapter = OllamaAdapter(host=ollama_host, temperature=temperature)
        model_version = model
    else:
        raise typer.BadParameter("adapter must be either 'fixture' or 'ollama'")
    result = GenerationRunner(selected_adapter).run(
        [prompt],
        GenerationConfig(
            "cli-run", profile, "tier_b_single_agent", 13, model_version=model_version
        ),
    )
    write_json(output, {"records": [record.model_dump(mode="json") for record in result.records]})
    typer.echo(str(output))


@app.command(name="filter")
def filter_records(
    output: Annotated[Path, typer.Option(help="Filtering report path")] = Path(
        "reports/filter.json"
    ),
) -> None:
    """Write a filtering report for the current fixture input."""

    write_json(output, {"pass": 0, "fail": 0, "flag": 0, "abstain": 0, "excluded": 0})
    typer.echo(str(output))


@experiment_app.command("run")
def run_experiment() -> None:
    """Run a deterministic experiment fixture."""

    config = ExperimentConfig(
        experiment_id="cli-experiment",
        condition_id="tier_b_single_agent",
        language_profiles=["singlish"],
        dataset_versions=["fixture:v1"],
        seeds=[13],
        metrics=["quality_pass_rate"],
    )
    result = ExperimentRunner().run(config, [])
    typer.echo(json.dumps({"run_id": result.fingerprint.run_id, "status": result.status.value}))


@app.command()
def evaluate(
    output: Annotated[Path, typer.Option(help="Evaluation package path")] = Path(
        "reports/evaluation.json"
    ),
) -> None:
    """Write a fixture evaluation package."""

    write_publication_package(
        output,
        {"methods": {}, "results": {}, "limitations": [], "provenance": {}, "manifest": {}},
    )
    typer.echo(str(output))


@app.command()
def export(
    output: Annotated[Path, typer.Option(help="Publication package path")] = Path(
        "reports/publication.json"
    ),
) -> None:
    """Write a fixture publication package."""

    write_publication_package(
        output,
        {"methods": {}, "results": {}, "limitations": [], "provenance": {}, "manifest": {}},
    )
    typer.echo(str(output))


@paper_app.command("venue-profile")
def paper_venue_profile(
    config: Annotated[Path, typer.Argument(help="Venue YAML configuration")],
    output: Annotated[Path, typer.Option(help="Profile output path")] = Path(
        "reports/paper-packages/venue-profile.json"
    ),
) -> None:
    """Validate and write a new venue profile artifact."""

    profile = VenueProfile.model_validate(load_yaml(config))
    write_json(output, profile.model_dump(mode="json"))
    typer.echo(str(output))


@paper_app.command("evidence-check")
def paper_evidence_check(
    manifest: Annotated[Path, typer.Argument(help="Evidence manifest JSON")],
) -> None:
    """Validate an evidence manifest without modifying it."""

    evidence = EvidenceManifest.model_validate(__import__("json").loads(manifest.read_text()))
    typer.echo(verify_manifest(evidence).verification_status.value)


@paper_app.command("generate")
def paper_generate(
    output: Annotated[Path, typer.Option(help="Paper package output root")] = Path(
        "reports/paper-packages"
    ),
) -> None:
    """Generate a deterministic fixture manuscript package."""

    manuscript = render_manuscript(assemble_sections({"results": "[MISSING EVIDENCE]"}))
    build = detect_document_tools()
    root = write_paper_package(output, "fixture-paper", manuscript, "", build, [])
    typer.echo(str(root))


@paper_app.command("validate")
def paper_validate(
    output: Annotated[Path, typer.Option(help="Validation report path")] = Path(
        "reports/paper-packages/validation.json"
    ),
) -> None:
    """Write a fixture paper readiness report."""

    profile = VenueProfile(
        venue_id="fixture",
        venue_name="Fixture Venue",
        requirements_source="fixture://cfp",
        accessed_at="2026-08-13",
        format_family=VenueFormat.MANUAL_REVIEW,
        template_reference="fixture://template",
        page_limit=10,
        author_mode="anonymous",
        required_sections=["abstract"],
        reference_style="springer",
        anonymization_rule="fixture",
        version="v1",
    )
    result = validate_venue(profile, [])
    write_json(
        output,
        {
            "blocking_issues": result.blocking_issues,
            "release_status": result.release_status,
        },
    )
    typer.echo(str(output))


@paper_app.command("build")
def paper_build() -> None:
    """Report whether optional PDF tools are available."""

    typer.echo(detect_document_tools().status)


@research_app.command("dossier")
def research_dossier(
    sources: Annotated[Path, typer.Option(help="Source-record directory")] = Path(
        "research/sources"
    ),
    output: Annotated[Path, typer.Option(help="Dossier JSON output path")] = Path(
        "research/dossiers/synthsea-regicon-2026.json"
    ),
) -> None:
    """Build a source-backed research dossier and literature matrix."""

    source_records = load_sources(sources)
    dossier, questions = build_dossier(source_records)
    write_dossier_package(output.parent, dossier, questions, source_records)
    write_artifact(
        output,
        {
            "dossier": dossier.model_dump(mode="json"),
            "research_questions": [question.model_dump(mode="json") for question in questions],
        },
    )
    typer.echo(str(output))


@research_app.command("matrix")
def research_matrix(
    dossier: Annotated[Path, typer.Option(help="Research dossier JSON path")],
    output: Annotated[Path, typer.Option(help="Readiness matrix JSON output path")] = Path(
        "research/matrices/synthsea-readiness.json"
    ),
) -> None:
    """Build the experiment and claim-evidence readiness matrix."""

    value = load_artifact(dossier)
    raw_dossier = value.get("dossier", value)
    parsed_dossier = ResearchDossier.model_validate(raw_dossier)
    write_matrix(output, build_matrix(parsed_dossier))
    typer.echo(str(output))


@research_app.command("evidence-check")
def research_evidence_check(
    manifest: Annotated[Path, typer.Option(help="Evidence manifest JSON path")],
    source_root: Annotated[Path, typer.Option(help="Artifact root directory")] = Path("."),
    output: Annotated[Path | None, typer.Option(help="Optional verification report path")] = None,
) -> None:
    """Verify evidence checksums and reproducibility metadata without changing artifacts."""

    records = verify_records(load_evidence_records(manifest), source_root)
    if output is not None:
        write_evidence_report(output, records)
    typer.echo(json.dumps({"records": [record.model_dump(mode="json") for record in records]}))


@research_app.command("report")
def research_report(
    dossier: Annotated[Path, typer.Option(help="Research dossier JSON path")],
    matrix: Annotated[Path, typer.Option(help="Research matrix JSON path")],
    output: Annotated[Path, typer.Option(help="Research report package root")] = Path(
        "reports/research-packages"
    ),
    sources: Annotated[Path, typer.Option(help="Source-record directory")] = Path(
        "research/sources"
    ),
    evidence: Annotated[Path | None, typer.Option(help="Evidence manifest JSON path")] = None,
    evidence_root: Annotated[Path, typer.Option(help="Evidence artifact root directory")] = Path(
        "."
    ),
    venue_profile: Annotated[
        Path | None, typer.Option(help="Approved venue profile JSON path")
    ] = None,
    ethics_reviewed: Annotated[bool, typer.Option(help="Mark ethics review as recorded")] = False,
) -> None:
    """Generate a report package and readiness report from declared inputs."""

    dossier_value = load_artifact(dossier)
    parsed_dossier = ResearchDossier.model_validate(dossier_value.get("dossier", dossier_value))
    matrix_value = load_matrix(matrix)
    source_records = load_sources(sources)
    raw_evidence = matrix_value.get("evidence", [])
    matrix_evidence = [load_evidence_records(Path(item)) for item in raw_evidence]
    manifest_evidence = (
        [verify_records(load_evidence_records(evidence), evidence_root)] if evidence else []
    )
    flattened_evidence = [
        record for group in matrix_evidence + manifest_evidence for record in group
    ]
    raw_claims = matrix_value.get("claims", [])
    claims = [ClaimEvidenceLink.model_validate(claim) for claim in raw_claims]
    validated_claims, _ = validate_claim_links(claims, flattened_evidence, source_records)
    approved_venue = False
    if venue_profile is not None:
        profile = VenueProfile.model_validate(load_artifact(venue_profile))
        approved_venue = profile.status.value == "approved"
    readiness = build_readiness(
        parsed_dossier.dossier_id,
        parsed_dossier,
        validated_claims,
        flattened_evidence,
        source_records,
        venue_approved=approved_venue,
        ethics_reviewed=ethics_reviewed,
    )
    package = write_research_package(
        output, parsed_dossier, matrix_value, flattened_evidence, source_records, readiness
    )
    typer.echo(str(package))


@research_app.command("readiness")
def research_readiness(
    package: Annotated[Path, typer.Option(help="Research report package directory")],
    output: Annotated[Path, typer.Option(help="Readiness report output path")] = Path(
        "reports/research-packages/readiness.json"
    ),
) -> None:
    """Copy and print the readiness report for an existing research package."""

    readiness = load_artifact(package / "readiness.json")
    write_artifact(output, readiness)
    typer.echo(json.dumps(readiness, sort_keys=True))


if __name__ == "__main__":
    app()
