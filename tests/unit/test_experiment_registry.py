from synthsea.experiments.registry import SplitManifest, manifest_fingerprint


def test_split_manifest_fingerprint_is_stable() -> None:
    manifest = SplitManifest(("a",), ("b",), ("c",))
    payload = {
        "train": manifest.train_ids,
        "validation": manifest.validation_ids,
        "test": manifest.test_ids,
    }
    assert manifest_fingerprint(payload) == manifest_fingerprint(payload)
