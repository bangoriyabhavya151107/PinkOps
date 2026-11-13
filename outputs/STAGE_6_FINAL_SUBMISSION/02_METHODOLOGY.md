{
  "manifest_id": "STAGE_5_FROZEN_METHODOLOGY_MANIFEST",
  "project": "Operation Pink Panther",
  "brand": "PinkOps",
  "competition": "Rajasthan Royals SupeRR Selector Season 2 — Round 1",
  "tagline": "Finding the Next Legend",
  "working_slogan": "Zero Choke. All Smoke.",
  "inherited_stage": "Stage 4.1.1 Final Repository Truth Reconciliation",
  "stage_5_authorization_status": "AUTHORIZED",
  "governance_freeze_timestamp": "2026-11-13T18:35:00+05:30",
  "governance_rules": {
    "raw_data_immutability": "STRICTLY READ-ONLY (SHA-256 verified)",
    "no_fabricated_data": "TRUE (All missing values marked UNKNOWN or NOT OBSERVABLE)",
    "no_reputation_bias": "TRUE (Data-driven selection only)",
    "no_single_metric_selection": "TRUE (Multidimensional evaluation across performance, pressure, uncertainty, sample, role, downside, robustness)",
    "no_premature_scalar_score": "TRUE (No PinkOps Score, IceVein Score, or scalar composite)"
  },
  "canonical_population": {
    "raw_deliveries": 200999,
    "super_over_deliveries": 38,
    "normal_modeling_deliveries": 200961,
    "first_innings_deliveries": 105727,
    "second_innings_deliveries": 95234,
    "contested_matches": 867,
    "total_players_in_evidence_system": 1535,
    "batters_in_evidence_system": 888,
    "bowlers_in_evidence_system": 647
  },
  "frozen_operating_parameters": {
    "expectation_model": {
      "model_type": "Spec B Contextual Expectation (Zero Endogenous Self-Conditioning)",
      "excluded_features": ["recent_12_deliveries_runs", "recent_12_deliveries_wickets"]
    },
    "empirical_bayes_shrinkage": {
      "primary_k": 100.0,
      "sensitivity_k_values": [50.0, 200.0],
      "population_sigma": 1.10
    },
    "lower_uncertainty_bound": {
      "formula": "LUB_p = mu_EB - z_p * SE_EB",
      "primary_percentile": 20,
      "primary_z_score": 0.842,
      "alternative_percentiles": [10, 15, 25, 30],
      "alternative_z_scores": [1.282, 1.036, 0.674, 0.524]
    },
    "pressure_formulation": {
      "metric": "Continuous Pressure Intensity (PI)",
      "primary_cutoff_percentile": 80,
      "primary_cutoff_threshold": 0.5898,
      "alternative_cutoff_percentiles": [70, 85],
      "alternative_cutoff_thresholds": [0.5000, 0.6400],
      "rdi_epsilon": 0.15,
      "rdi_epsilon_alternatives": [0.10, 0.20]
    },
    "venue_baseline": {
      "method": "Strictly Pre-Match Historical Expanding Cumulative Sums (Excluding Current & Future Matches)",
      "shrinkage_k": 500,
      "prior_mean": 1.30
    },
    "opponent_strength": {
      "metric": "Pre-Match Team Elo (Strictly Pre-Match)",
      "k_factor": 32,
      "mapping_rule": "Opponent Elo mapped from actual opponent bowling team (bowling_team_id)"
    },
    "evidence_tiers": {
      "Robust Evidence": {
        "min_total_deliveries": 150,
        "min_pressure_deliveries": 40
      },
      "Moderate Evidence": {
        "min_total_deliveries": 50,
        "min_pressure_deliveries": 15
      },
      "Low / Sparse Evidence": {
        "min_total_deliveries": 0,
        "min_pressure_deliveries": 0
      }
    },
    "attribution_accounting": {
      "wides": "Charged to bowler runs conceded; 0 balls to batter",
      "byes_legbyes": "Charged to batter balls faced; 0 runs conceded to bowler",
      "penalties": "0 runs to bowler; 0 balls to batter",
      "run_outs": "0 wickets to bowler; isolated from individual execution",
      "retired_hurt": "0 wickets to team or bowler; zero downside penalty"
    },
    "super_over_policy": "Strict isolation in descriptive stress register; 0 deliveries in ordinary models"
  },
  "tactical_roles": {
    "batters": [
      "Top-Order Anchor / Powerplay Batter",
      "Middle-Overs Accelerator",
      "Finisher / Death Specialist"
    ],
    "bowlers": [
      "Powerplay Specialist (Pace)",
      "Powerplay Specialist (Spin)",
      "Middle Enforcer (Pace)",
      "Middle Enforcer (Spin)",
      "Death Specialist (Pace)",
      "Death Specialist (Spin)"
    ]
  },
  "selection_gates": [
    "GATE 1: Valid player evidence (finite numeric metrics)",
    "GATE 2: Valid role evidence (sufficient role exposure)",
    "GATE 3: Evidence strength (Robust or Moderate preferred, Sparse labeled)",
    "GATE 4: Positive contextual performance (positive value-added relative to expectations)",
    "GATE 5: Uncertainty acceptability (LUB20 penalizes sample sparsity)",
    "GATE 6: Downside risk containment (Early dismissal <= 0.20 for batters, Blowout <= 0.20 for bowlers)",
    "GATE 7: Pressure resilience (positive pressure value-added / clutch evidence)",
    "GATE 8: Multiverse robustness (supported across genuine performance specifications)"
  ],
  "multiverse_taxonomy": {
    "total_specifications": 15,
    "full_recomputations": 6,
    "partial_recomputations": 6,
    "descriptor_alternatives": 3
  }
}
