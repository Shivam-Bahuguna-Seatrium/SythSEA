import hashlib

from synthsea.research.evidence import verify_record
from synthsea.research.models import EvidenceRecord, EvidenceState


def test_checksum_mismatch_marks_evidence_stale(tmp_path) -> None:
    artifact = tmp_path / "result.json"
    artifact.write_text("original", encoding="utf-8")
    record = EvidenceRecord(
        evidence_id="evidence",
        experiment_id="experiment",
        artifact_path="result.json",
        artifact_type="result",
        checksum=hashlib.sha256(b"different").hexdigest(),
        language_slice="singlish",
        condition_id="baseline",
        access_class="public",
        status=EvidenceState.VERIFIED,
        provenance_refs=["experiment"],
    )

    assert verify_record(record, tmp_path).status is EvidenceState.STALE