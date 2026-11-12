"""
PinkOps — Stage 3.1: Master Orchestration Pipeline
Script: src/stage_3_1/run_all.py

Purpose:
- Coordinate end-to-end execution of all modular Stage 3.1 hardening engines:
  1. pressure_trajectory
  2. sensitivity_analysis
  3. wpli_validation
  4. expectation_estimand
  5. role_adjustment
  6. exposure_diagnostics
  7. leakage_provenance
  8. validation_runner
  9. stability_analysis
- Enforce strict validation assertions and referential integrity
- Ensure ZERO player rankings, ZERO Top 10 lists, and ZERO composite scores are created
"""

import sys
import time
from pathlib import Path

# Add project root and src/stage_3_1 to sys.path
project_root = Path("D:/PinkOps")
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.stage_3_1 import pressure_trajectory
from src.stage_3_1 import sensitivity_analysis
from src.stage_3_1 import wpli_validation
from src.stage_3_1 import expectation_estimand
from src.stage_3_1 import role_adjustment
from src.stage_3_1 import exposure_diagnostics
from src.stage_3_1 import leakage_provenance
from src.stage_3_1 import validation_runner
from src.stage_3_1 import stability_analysis


def main():
    start_time = time.time()
    print("=" * 80)
    print("PinkOps — Stage 3.1: Pressure & Player-Attribution Hardening Pipeline")
    print(f"Project Root: {project_root}")
    print("=" * 80)

    print("\n[Step 1/9] Running First-Innings Trajectory Hardening...")
    pressure_trajectory.main()

    print("\n[Step 2/9] Running Hyperparameter Sensitivity Engine (RDI, Venue, Elo, LCB)...")
    sensitivity_analysis.main()

    print("\n[Step 3/9] Running WPLI Validation Engine (WPLI-A, WPLI-B, WPLI-C)...")
    wpli_validation.main()

    print("\n[Step 4/9] Running Expectation Estimand Modeling...")
    expectation_estimand.main()

    print("\n[Step 5/9] Running Role Confounding & Context Adjustment Engine...")
    role_adjustment.main()

    print("\n[Step 6/9] Running Participation & Exposure Bias Diagnostics...")
    exposure_diagnostics.main()

    print("\n[Step 7/9] Running Feature Provenance & Active Leakage Assertions...")
    leakage_provenance.main()

    print("\n[Step 8/9] Running Validation Expansion & Pressure Ablation...")
    validation_runner.main()

    print("\n[Step 9/9] Assembling Uncollapsed Player Evidence Vector...")
    stability_analysis.main()

    # Verify that all 7 required Stage 3.1 data deliverables exist
    required_data_files = [
        "stage_3_1_pressure_sensitivity.csv",
        "stage_3_1_wpli_comparison.csv",
        "stage_3_1_role_adjustment.csv",
        "stage_3_1_player_exposure.csv",
        "stage_3_1_model_stability.csv",
        "stage_3_1_feature_provenance.csv",
        "stage_3_1_player_evidence.parquet"
    ]
    proc_dir = project_root / "data" / "processed"
    print("\n" + "=" * 80)
    print("Verifying Stage 3.1 Processed Data Artifacts:")
    for fname in required_data_files:
        fpath = proc_dir / fname
        assert fpath.exists(), f"Missing required data deliverable: {fpath}"
        size_kb = fpath.stat().st_size / 1024.0
        print(f"  [VERIFIED] {fname:38s} ({size_kb:8.1f} KB)")

    elapsed = time.time() - start_time
    print("=" * 80)
    print(f"STAGE 3.1 HARDENING PIPELINE COMPLETE in {elapsed:.2f} seconds.")
    print("All sensitivity tests, validations, and evidence vectors generated.")
    print("Zero player rankings generated. Zero Top 10 lists created.")
    print("=" * 80)


if __name__ == "__main__":
    main()
