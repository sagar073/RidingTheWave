# 🌊 RidingTheWave: SustainLens - Local AI Deployment with NPU Optimization  

Welcome to **SustainLens**! 🚀 This guide takes you through our journey of integrating a sustainability classification AI model into the web application. Along the way, we tackled **dependency conflicts**, experimented with **NPU optimization**, and explored **local AI deployment**.  

---

## 🔧 **1. Resolving Dependency Conflicts**  

### 🚨 **The Problem:**  
When setting up the environment, we ran into **dependency conflicts**—particularly with Hugging Face's `transformers`, `tokenizer`, `onnx`, and `onnxruntime`.  

### ✅ **How We Fixed It:**  
✔️ Iteratively downgraded & upgraded various libraries to find compatible versions.  
✔️ Adjusted **Python** and **NumPy** versions to meet ONNX requirements.  

---

## 🏗️ **2. Setting Up Local Deployment**  

### 🔍 **Steps We Took:**  
✅ Installed **LM Studio** for local LLM deployment.  
✅ Downloaded models and installed **Ollama**.  
✅ Successfully ran **LLaMA 3.2 locally**! 🎉  
✅ Verified integration of LM Studio models into the application using the **OpenAI SDK**.  

---

## 🚀 **3. NPU Optimization Efforts**  

### 🔥 **What We Tried:**  
✅ Converted the LLM model into an **NPU-optimized format**.  
✅ Extracted model weights from LM Studio and attempted conversion to ONNX.  
✅ Installed NP SDK, tested **QNN SDK/QAIRT** for NPU execution.  
✅ Pulled NPU-compatible models from LM Studio—but still no NPU utilization. 🤯  

### ⚠️ **Challenges We Faced:**  
❌ `.model` errors.  
❌ Issues with `ondevice='npu'`.  
❌ Could not use `QNNExecutionProvider` in ONNX runtime.  
❌ High **memory, compute, and GPU usage**—but no NPU activity!  

### 🛠️ **Genie Runtime Attempts:**  
📌 Installed **QAI Hub models** & generated compatible context binaries.  
📌 Upgraded **PyTorch** for `llama_v3_8b_chat_quantized.export`.  
📌 Encountered errors while running **genie-t2t-run**.  

---

## 🎯 **4. The Breakthrough - "Anything LLM"**  

🎉 **Success!** We finally got **"Anything LLM"** running on the NPU.  

🔹 However, by the time we discovered this, we were **too late in the dev cycle** to fully integrate it into SustainLens.  

### 🚀 **Final Approach:**  
✅ Built a **basic OpenAI-based NLP categorization** for local execution (without NPU/RAG).  
✅ Attempted integration with **Anything LLM**.  
✅ Followed "Chat App Using Anything LLM" setup.  
🚧 Faced challenges running the repository locally for parallel execution.  

---

## ⏭️ **Next Steps**  

🔄 **Optimize** NPU execution for sustainability classification models.  
🤝 **Improve** integration with Anything LLM for high-performance inference.  
🔧 **Refine** the deployment process to streamline future development.  

**The journey continues!** 🚀🌿  

👨‍💻 **Authors**

**karna.j@northeastern.edu
**gehlot.v@northeastern.edu
**pant.e@northeastern.edu
**mittal.sag@northeastern.edu
**jami.ab@northeastern.edu

