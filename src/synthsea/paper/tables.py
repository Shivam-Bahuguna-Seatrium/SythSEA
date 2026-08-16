"""Evidence-derived table metadata."""

from synthsea.config.schemas import AccessClass
from synthsea.paper.models import PaperArtifact


def result_table(
    artifact_id: str, source_ref: str, output_path: str, profiles: list[str]
) -> PaperArtifact:
    return PaperArtifact(
        artifact_id=artifact_id,
        title="Experiment results",
        caption="Results derived from verified experiment artifacts.",
        source_refs=[source_ref],
        transformation="language_slice_table",
        language_slices=profiles,
        version="v1",
        access_class=AccessClass.PUBLIC,
        output_path=output_path,
        validation_status="verified",
    )
