from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Sequence
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.ai.hcrl_cyber_features import extract_cyber_features


CYBER_STATE_FEATURES = (
    "cyber_message_rate",
    "cyber_unique_can_id_count",
    "cyber_can_id_entropy",
    "cyber_mean_interarrival_ms",
    "cyber_std_interarrival_ms",
    "cyber_max_interarrival_ms",
    "cyber_interarrival_cv",
    "cyber_payload_change_rate",
    "cyber_mean_hamming_distance",
    "cyber_dominant_can_id_fraction",
)


@dataclass(frozen=True)
class CyberState:
    message_rate: float
    unique_can_id_count: float
    can_id_entropy: float
    mean_interarrival_ms: float
    std_interarrival_ms: float
    max_interarrival_ms: float
    interarrival_cv: float
    payload_change_rate: float
    mean_hamming_distance: float
    dominant_can_id_fraction: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


def build_cyber_state(frames: Sequence) -> CyberState:
    """
    Convert a chronological CAN-frame window into the
    EdgeResilience cyber-state representation.

    Labels are intentionally ignored as model inputs.
    """

    features = extract_cyber_features(frames)

    return CyberState(
        message_rate=float(
            features["cyber_message_rate"]
        ),
        unique_can_id_count=float(
            features["cyber_unique_can_id_count"]
        ),
        can_id_entropy=float(
            features["cyber_can_id_entropy"]
        ),
        mean_interarrival_ms=float(
            features["cyber_mean_interarrival_ms"]
        ),
        std_interarrival_ms=float(
            features["cyber_std_interarrival_ms"]
        ),
        max_interarrival_ms=float(
            features["cyber_max_interarrival_ms"]
        ),
        interarrival_cv=float(
            features["cyber_interarrival_cv"]
        ),
        payload_change_rate=float(
            features["cyber_payload_change_rate"]
        ),
        mean_hamming_distance=float(
            features["cyber_mean_hamming_distance"]
        ),
        dominant_can_id_fraction=float(
            features["cyber_dominant_can_id_fraction"]
        ),
    )


def cyber_state_feature_vector(
    state: CyberState,
):
    return [
        state.message_rate,
        state.unique_can_id_count,
        state.can_id_entropy,
        state.mean_interarrival_ms,
        state.std_interarrival_ms,
        state.max_interarrival_ms,
        state.interarrival_cv,
        state.payload_change_rate,
        state.mean_hamming_distance,
        state.dominant_can_id_fraction,
    ]


if __name__ == "__main__":
    print("CYBER_STATE_FEATURE_COUNT =", len(CYBER_STATE_FEATURES))
    print("CYBER_STATE_FEATURES =")

    for index, name in enumerate(
        CYBER_STATE_FEATURES,
        start=1,
    ):
        print(f"  {index:02d}. {name}")

    assert len(CYBER_STATE_FEATURES) == 10

    print("LABEL_USED_AS_FEATURE = False")
    print("CYBER_STATE_SCHEMA = PASS")
