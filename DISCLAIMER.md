# EdgeResilience Disclaimer

EdgeResilience is a research and engineering validation project focused on predictive cyber-physical resilience for connected vehicles.

## Intended Use

This repository is provided for research, experimentation, demonstration, and engineering evaluation. It is not a production automotive safety controller and must not be used to control, actuate, or modify a real vehicle.

## Validation Scope

The current implementation has been evaluated through software simulation, virtual laboratory workflows, and Snapdragon X Elite CRD profiling using Qualcomm AI Hub and Qualcomm QNN HTP.

No physical vehicle testing, external CAN transmission, or direct vehicle actuation has been performed as part of this project.

The current Snapdragon hardware evidence is from a Snapdragon X Elite CRD reference device. Validation on a physical HP Snapdragon-powered PC has not been performed.

## Numerical Validation

The complete CPU-to-Snapdragon numerical comparison has been executed. The current implementation did not meet the established numerical-equivalence threshold. No end-to-end CPU-to-Snapdragon numerical-equivalence claim is made.

## Safety and Cybersecurity

This project does not claim certification or compliance with automotive functional-safety or cybersecurity standards. Any future vehicle integration would require appropriate automotive safety, cybersecurity, verification, validation, and regulatory processes.

## Performance Measurements

Reported Snapdragon performance measurements are workload-specific profile results from the Snapdragon X Elite CRD. They should not be interpreted as complete vehicle-system latency, sustained vehicle-system throughput, power consumption, thermal performance, or production-system performance.

## General Notice

Use of this repository and its software is at the user's own risk. The authors make no representation that the implementation is suitable for any specific production, safety-critical, automotive, or commercial application.
