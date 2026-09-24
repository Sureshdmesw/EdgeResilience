# Stage 4 Provenance

## Stage 4D: EdgeResilience Predictive Engine

### New artifact

Path:
`src/ai/predictive_engine.py`

Classification:
`new EdgeResilience artifact`

Purpose:
Provide a clean EdgeResilience-native predictive inference interface while preserving the verified 59-feature / 12-timestep temporal model contract from the inherited project.

### Inherited reference

Source:
`inherited/Predictive-Cyber-Physical-Resilience`

Reference implementation:
`src/ai/predictive_detection_inherited.py`

Classification:
`inherited/reference`

The inherited implementation was inspected to establish:
- feature names and ordering
- 59-feature model input contract
- 12-timestep observation window
- temporal Transformer architecture
- Y3 and Y6 output heads
- probability-to-risk-level mapping
- feature matrix construction behavior

### Model boundary

The historical Transformer checkpoint remains frozen and is not embedded, modified, retrained, fine-tuned, or replaced by this artifact.

The EdgeResilience predictive engine provides architecture-compatible model code and an explicit checkpoint-loading interface.

No Snapdragon-specific acceleration or hardware performance is claimed by this stage.

### Validation performed

Python syntax compilation:
`python -m py_compile .\src\ai\predictive_engine.py`

Model interface test:
`(1, 12, 59) -> (1,), (1,)`

Feature contract test:
- feature count: 59
- unique feature names: true
- observation steps: 12

### Safety boundary

This stage performs predictive inference only.

It does not:
- control a vehicle
- transmit external CAN traffic
- actuate a physical system
- connect to a production vehicle

Experiment type:
`software test`
