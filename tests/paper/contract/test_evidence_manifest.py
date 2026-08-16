from synthsea.paper.evidence import verify_manifest
from synthsea.paper.models import EvidenceManifest, EvidenceStatus


def test_verified_manifest_is_accepted() -> None:
    manifest = EvidenceManifest(
        manifest_id="evidence-1",
        manifest_version="v1",
        artifact_refs=["artifact-1"],
        experiment_ids=["run-1"],
        language_profiles=["singlish", "malay", "tamil", "singapore_mandarin"],
        conditions=["tier_b", "tier_c"],
        checksums={"artifact-1": "sha256"},
        access_summary={"public": 1, "restricted": 0, "private": 0},
    )
    assert verify_manifest(manifest).verification_status is EvidenceStatus.VERIFIED
