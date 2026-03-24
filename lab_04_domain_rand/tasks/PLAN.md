# Lab 04 Domain Randomization — Plan

## Goal
Implement the Lab 04 brief as a deterministic, testable scaffold for physics randomization, observation noise, ADR, and robustness evaluation.

## Execution Steps
1. Create the Lab 04 package and match the plan structure around `robust_grasp/`, `eval/`, and `agents/`.
2. Model the randomization, observation-noise, perturbation, and curriculum settings as typed dataclasses loaded from YAML.
3. Implement deterministic event sampling, observation noise injection, and episode scoring.
4. Train a vanilla baseline and a domain-randomized policy profile with ADR.
5. Evaluate both policies on the fixed nominal/heavy/slippery/noisy configs and write comparison artifacts.
6. Add tests, scripts, docs, and project-status updates.
