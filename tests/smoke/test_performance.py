from time import perf_counter

from synthsea.config.schemas import AccessClass, ArtifactRef
from synthsea.export.public_private import public_artifacts


def test_ten_thousand_record_cpu_access_filter_benchmark() -> None:
    start = perf_counter()
    artifacts = [
        ArtifactRef(
            artifact_id=f"record-{index}",
            path=f"data/record-{index}.json",
            kind="dataset_record",
            checksum=str(index),
            access_class=AccessClass.PUBLIC,
        )
        for index in range(10_000)
    ]
    included, excluded = public_artifacts(artifacts)
    elapsed = perf_counter() - start
    assert len(included) == 10_000
    assert excluded == []
    assert elapsed < 60
