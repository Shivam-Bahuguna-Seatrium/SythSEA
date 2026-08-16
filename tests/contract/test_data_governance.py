from synthsea.config.schemas import AccessClass, ArtifactRef
from synthsea.export.public_private import public_artifacts


def test_public_artifacts_exclude_restricted_records() -> None:
    artifacts = [
        ArtifactRef(
            artifact_id="public-1",
            path="public.json",
            kind="dataset",
            checksum="a",
            access_class=AccessClass.PUBLIC,
        ),
        ArtifactRef(
            artifact_id="restricted-1",
            path="restricted.json",
            kind="dataset",
            checksum="b",
            access_class=AccessClass.RESTRICTED,
        ),
    ]
    included, excluded = public_artifacts(artifacts)
    assert [item.artifact_id for item in included] == ["public-1"]
    assert excluded == ["restricted-1"]
