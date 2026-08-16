from synthsea.paper.models import EvidenceManifest


def test_evidence_limitations_are_retained() -> None:
    manifest = EvidenceManifest(
        manifest_id="e1",
        manifest_version="v1",
        artifact_refs=["a1"],
        language_profiles=["singlish"],
        checksums={"a1": "hash"},
        access_summary={"public": 1},
        limitations=["restricted source"],
    )
    assert manifest.limitations == ["restricted source"]
