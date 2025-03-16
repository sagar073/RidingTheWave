# RidingTheWave

SustainLens - Local AI Deployment with NPU Optimization

Overview

This document outlines the steps taken to integrate a sustainability classification AI model into the SustainLens web application, focusing on optimizing performance using an NPU (Neural Processing Unit). The project involved multiple attempts at resolving dependency conflicts, configuring ONNX models, and running the AI model on local hardware for efficient inference.

1. Resolving Dependency Conflicts

Issue:

Conflicts between Python dependencies when installing Hugging Face's transformers, tokenizer, onnx, onnxruntime, and onnxscript.

Resolution:

Downgraded and upgraded various libraries iteratively to find non-conflicting versions.

Identified ONNX requirements for Python and NumPy versions and adjusted accordingly.

2. Setting Up Local Deployment

Steps Taken:

Installed LM Studio for local LLM deployment.

Downloaded models and installed Ollama.

Successfully ran LLaMA 3.2 locally.

Verified the ability to integrate LM Studio models into the application using the OpenAI SDK.

3. NPU Optimization Efforts

Attempted Approaches:

Converted LLM model into an NPU-optimized format.

Extracted model weights from LM Studio and attempted conversion to ONNX.

Encountered multiple errors:

'.model' errors.

Issues with ondevice='npu'.

Could not use QNNExecutionProvider in the ONNX runtime provider list.

Installed NP SDK, attempted QNN SDK/QAIRT for NPU execution.

Created multiple virtual environments to test different configurations.

Pulled NPU-compatible models from LM Studio but still did not hit NPU.

Observed high memory, compute, and GPU usage, but no NPU utilization.

Attempted to run Genie runtime via QAIRT SDK:

Installed QAI Hub models.

Generated compatible context binaries.

Upgraded PyTorch to use llama_v3_8b_chat_quantized.export.

Removed genie_bundle(prompt, token).

Used AI Hub repository to configure the environment.

Encountered errors when running genie-t2t-run.

Tried C++ restabilizer using Visual Studio Installer.

4. Successful NPU Execution - "Anything LLM"

Discovery:

Successfully ran "Anything LLM", which hit the NPU.

However, integrating it into SustainLens was realized too late in the development cycle.

Final Approach:

Created a basic OpenAI-based NLP categorization for local execution without NPU or RAG.

Attempted to integrate it with Anything LLM.

Followed "Chat App Using Anything LLM" setup steps.

Encountered challenges running the repository locally for parallel execution.

Next Steps

Further optimize NPU execution for sustainability classification models.

Improve integration with Anything LLM for local, high-performance inference.

Refine the deployment process to streamline future development.
