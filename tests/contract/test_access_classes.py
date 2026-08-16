from synthsea.config.schemas import AccessClass, ArtifactRef
from synthsea.export.public_private import public_artifacts


def test_restricted_and_private_artifacts_are_excluded() -> None:
    artifacts = [
        ArtifactRef(
            artifact_id="pub",
            path="pub",
            kind="dataset",
            checksum="1",
            access_class=AccessClass.PUBLIC,
        ),
        ArtifactRef(
            artifact_id="res",
            path="res",
            kind="dataset",
            checksum="2",
            access_class=AccessClass.RESTRICTED,
        ),
        ArtifactRef(
            artifact_id="priv",
            path="priv",
            kind="dataset",
            checksum="3",
            access_class=AccessClass.PRIVATE,
        ),
    ]
    included, excluded = public_artifacts(artifacts)
    assert [artifact.artifact_id for artifact in included] == ["pub"]
    assert excluded == ["res", "priv"]
