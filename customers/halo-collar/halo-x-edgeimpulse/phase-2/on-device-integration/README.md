# On-Device Integration

**Weeks 25–32 · Status: 🔲 Not started**

## Objective

Deploy the optimized model to STM32 hardware and validate real-world inference performance. Bridge the gap between offline model accuracy and on-device behavior — covering ONNX export, STM32Cube.AI conversion, memory validation, and latency profiling.

## Tasks

- [ ] Export optimized model to ONNX format
- [ ] Convert via STM32Cube.AI and validate memory fit (51KB flash, 1.1KB RAM)
- [ ] Profile inference latency on target hardware
- [ ] Validate on-device output matches offline predictions (target: <1% gap)
- [ ] Integrate application logic (temporal smoothing, state machine) into firmware
- [ ] Run end-to-end on-device tests with real IMU data

## Acceptance Criteria

- Model runs within STM32 memory and latency constraints
- On-device vs. offline prediction gap < 1%
- Application logic integrated and producing smooth activity reports
- Firmware integration guide delivered to Halo

## Dependencies

- Model optimization workstream outputs (optimized model)
- Application logic design from Phase 1 WS5
- Halo firmware team availability for integration support
- STM32 development hardware access

## Notes

_Detailed scope defined at Phase 1 → Phase 2 gate._
