"""Verifier boundary: generated code may only cross this interface as data."""

from __future__ import annotations

from typing import Protocol

from ..schemas import CandidatePatch, RepairRequest, VerificationResult


class Verifier(Protocol):
    def baseline(self, request: RepairRequest) -> VerificationResult: ...

    def verify(self, request: RepairRequest, candidate: CandidatePatch) -> VerificationResult: ...

    def cancel(self) -> None: ...
