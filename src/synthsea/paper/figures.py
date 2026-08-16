"""Evidence-derived figure metadata."""

from synthsea.config.schemas import AccessClass
from synthsea.paper.models import PaperArtifact


def result_figure(
    artifact_id: str, source_ref: str, output_path: str, profiles: list[str]
) -> PaperArtifact:
    return PaperArtifact(
        artifact_id=artifact_id,
        title="Language-specific results",
        caption="Figure derived from verified language-sliced results.",
        source_refs=[source_ref],
        transformation="language_slice_figure",
        language_slices=profiles,
        version="v1",
        access_class=AccessClass.PUBLIC,
        output_path=output_path,
        validation_status="verified",
    )
