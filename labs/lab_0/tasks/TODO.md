# Lab 0: TODO

## Current Focus

Phase 1 - Instance selection and SSH setup

## Blockers

None

---

## Phase 1: Instance Selection and SSH Setup
- [ ] Select RTX 4090 instance on Vast.ai (EU preferred, >95% reliability)
- [ ] Configure SSH key authentication
- [ ] Verify SSH connection
- [ ] Set idle auto-shutdown timeout
- [ ] Verify nvidia-smi shows RTX 4090

## Phase 2: Run setup_instance.sh
- [ ] Transfer/clone repo to instance
- [ ] Run setup_instance.sh
- [ ] Verify log has no errors
- [ ] Activate conda env: `conda activate isaaclab`

## Phase 3: Run validate_setup.sh
- [ ] Run validate_setup.sh
- [ ] All critical checks pass (zero FAIL)
- [ ] If headless test fails first time, retry after shader compilation

## Phase 4: VNC Setup (Optional)
- [ ] Run setup_vnc.sh
- [ ] Create SSH tunnel for VNC
- [ ] Verify VNC desktop renders
- [ ] Test GPU rendering: `vglrun glxgears`

## Phase 5: First Isaac Lab Training
- [ ] Run CartPole headless training (100 iterations, 2048 envs)
- [ ] Verify rewards are improving
- [ ] Check GPU utilization with nvidia-smi
- [ ] Save training curve to media/

## Phase 6: Documentation and Evidence
- [ ] nvidia-smi screenshot -> media/
- [ ] validate_setup.sh output -> docs/
- [ ] CartPole training evidence -> media/
- [ ] Write English documentation (docs/)
- [ ] Write Turkish documentation (docs-turkish/)
- [ ] Git push all results
