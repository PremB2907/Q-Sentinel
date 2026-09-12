# Snapdragon QNN & ONNX Runtime Deployment Guide

**Q-Sentinel Edge**  
*Snapdragon® AI Lab Build & Present Challenge by Qualcomm*

---

## 1. Overview & Snapdragon Architecture

**Q-Sentinel Edge** is engineered for privacy-preserving, local-first operation on **Snapdragon-powered HP PCs**. 

The platform architecture cleanly decouples local AI intelligence from the cryptographic verifier:
- **Authoritative Verifier**: Deterministic QDS Teleportation Engine (Binomial $z$-score, Chi-Square, $p$-value, protocol context validation) — **Zero AI/ML**.
- **Edge AI Intelligence**: ONNX Runtime model executing locally on the **Qualcomm Hexagon NPU / QNN** for real-time telemetry analysis, triage prioritization, and grounded explanation generation.

---

## 2. Hardware Execution Provider Hierarchy

ONNX Runtime session manager (`SnapdragonRuntimeManager`) checks hardware capabilities dynamically:

1. **`QNNExecutionProvider` (Primary Target)**: Direct hardware acceleration via Qualcomm QNN SDK on Snapdragon Hexagon NPU.
2. **`DmlExecutionProvider` (Windows Fallback)**: DirectML GPU acceleration on Windows.
3. **`CPUExecutionProvider` (Ubuntu / Dev Fallback)**: OpenMP multi-threaded CPU execution for Linux/Ubuntu development environments.

> [!NOTE]
> **Truthful Hardware Reporting**: Q-Sentinel Edge queries active ONNX Runtime execution providers at runtime and displays exact hardware status on the dashboard (`QNN (Hexagon NPU)`, `DirectML GPU`, or `CPU Fallback`). It NEVER fabricates active NPU status on non-Snapdragon machines.

---

## 3. Ubuntu Development vs. Snapdragon Deployment

| Feature / Domain | Linux / Ubuntu Development (Antigravity) | Snapdragon HP PC Production (Windows ARM64) |
| :--- | :--- | :--- |
| **Deterministic QDS Core** | Full execution (Qiskit Aer + NumPy) | Full execution |
| **Edge AI Inference** | ONNX Runtime (`CPUExecutionProvider`) | ONNX Runtime (`QNNExecutionProvider`) |
| **Hardware Accelerator** | CPU / Host | Snapdragon Hexagon NPU |
| **Privacy Model** | 100% Local (Zero Cloud Offload) | 100% Local (Zero Cloud Offload) |
| **Model Format** | `.onnx` (12-feature Float32 tensor) | `.onnx` / QNN `.serialized` Graph |

---

## 4. Deploying to Snapdragon-Powered HP PCs

### Prerequisites on Windows Snapdragon
1. **Qualcomm QNN SDK**: Download and install Qualcomm Neural Processing SDK / QNN from Qualcomm Developer Network.
2. **ONNX Runtime QNN Package**: Install ONNX Runtime with QNN support:
   ```cmd
   pip install onnxruntime-qnn
   ```
3. **Set Environment Variables**:
   ```cmd
   set QNN_SDK_ROOT=C:\Qualcomm\QNN_SDK
   set PATH=%QNN_SDK_ROOT%\lib\aarch64-windows-msvc;%PATH%
   ```

### Launching Q-Sentinel Edge
```cmd
python wsgi.py
```
Navigate to `http://localhost:5000/edge` to interact with the Snapdragon AI Dashboard.

---

## 5. Qualcomm AI Hub Optimization Pipeline

To further compile and optimize the threat classifier using **Qualcomm AI Hub**:

```bash
# 1. Install Qualcomm AI Hub CLI
pip install qai-hub

# 2. Configure credentials
qai-hub configure --api_token <YOUR_QUALCOMM_AI_HUB_TOKEN>

# 3. Submit ONNX model for Snapdragon Hexagon NPU compilation
qai-hub compile \
  --model src/qds_detector/models/q_sentinel_threat_classifier.onnx \
  --target_runtime qnn \
  --device "Snapdragon X Elite CRD" \
  --output_dir src/qds_detector/models/qnn/
```
