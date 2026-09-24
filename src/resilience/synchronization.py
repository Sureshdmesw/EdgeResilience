from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from src.resilience.connectivity import (
    ConnectivityState,
    should_synchronize,
)


@dataclass(frozen=True)
class SynchronizationRecord:
    event_id: str
    payload_digest: str
    sequence_number: int


@dataclass(frozen=True)
class RecoveryDecision:
    recovered: bool
    synchronization_allowed: bool
    records_available: int
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "recovered": self.recovered,
            "synchronization_allowed": self.synchronization_allowed,
            "records_available": self.records_available,
            "reason": self.reason,
        }


def evaluate_recovery(
    previous_state: ConnectivityState,
    current_state: ConnectivityState,
    buffered_records: Iterable[Mapping[str, Any]],
) -> RecoveryDecision:
    records = list(buffered_records)

    recovered = should_synchronize(
        previous_state,
        current_state,
    )

    if recovered and records:
        return RecoveryDecision(
            recovered=True,
            synchronization_allowed=True,
            records_available=len(records),
            reason="CONNECTIVITY_RECOVERED_BUFFER_READY",
        )

    if recovered and not records:
        return RecoveryDecision(
            recovered=True,
            synchronization_allowed=False,
            records_available=0,
            reason="CONNECTIVITY_RECOVERED_NO_BUFFERED_RECORDS",
        )

    if current_state != ConnectivityState.CONNECTED:
        return RecoveryDecision(
            recovered=False,
            synchronization_allowed=False,
            records_available=len(records),
            reason="CONNECTIVITY_NOT_RECOVERED",
        )

    return RecoveryDecision(
        recovered=False,
        synchronization_allowed=False,
        records_available=len(records),
        reason="NO_RECOVERY_TRANSITION",
    )


def prepare_synchronization_batch(
    records: Iterable[Mapping[str, Any]],
) -> list[SynchronizationRecord]:
    """
    Convert buffered evidence into a deterministic synchronization
    manifest.

    This function does not transmit data.
    """
    batch: list[SynchronizationRecord] = []

    for sequence_number, record in enumerate(records):
        event_id = str(record.get("event_id", ""))
        payload_digest = str(
            record.get(
                "record_sha256",
                record.get(
                    "digest",
                    record.get("payload_digest", "")
                ),
            )
        )

        if not event_id:
            raise ValueError(
                "Buffered record is missing event_id"
            )

        if not payload_digest:
            raise ValueError(
                f"Buffered record {event_id} is missing a digest"
            )

        batch.append(
            SynchronizationRecord(
                event_id=event_id,
                payload_digest=payload_digest,
                sequence_number=sequence_number,
            )
        )

    return batch


def validate_synchronization_batch(
    batch: Iterable[SynchronizationRecord],
) -> bool:
    records = list(batch)

    sequence_numbers = [
        record.sequence_number
        for record in records
    ]

    event_ids = [
        record.event_id
        for record in records
    ]

    return (
        sequence_numbers
        == list(range(len(records)))
        and len(event_ids) == len(set(event_ids))
        and all(
            record.event_id and record.payload_digest
            for record in records
        )
    )
