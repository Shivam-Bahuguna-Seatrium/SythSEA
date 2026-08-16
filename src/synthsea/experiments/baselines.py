"""Dataset tier labels used in comparisons."""

from enum import StrEnum


class DatasetTier(StrEnum):
    HUMAN_SEED = "tier_a_human"
    SINGLE_AGENT = "tier_b_single_agent"
    SYNTHSEA = "tier_c_synthsea"
    TRANSLATION = "tier_d_translation"
