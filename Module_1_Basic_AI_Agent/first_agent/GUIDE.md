# Google Agents ADK Development – Module 1

## Welcome to the First Module 🎉

### Lesson 1: Make Your First AI Agent

This lesson will guide you through creating an AI Agent using the **Google Agent Development Kit (ADK)**.
📝 Official Documentation: [LlmAgent Docs](https://google.github.io/adk-docs/agents/llm-agents/)

---

### 📌 Prerequisites

- Basic understanding of **Large Language Models (LLMs)**
- Familiarity with **Python programming**

---

### 🤖 What is an AI Agent?

An **AI Agent** is a combination of:

- **LLM** (the brain for reasoning and language)  
- **Memory** (to retain context and past interactions)  
- **Tools** (to interact with external data and systems)  
- **Loop** (cycle of perceiving input, generating output, and refining behavior)  

This enables the agent to perceive its environment, act on it, and continuously improve its decisions.

---

### 💡 Example

Imagine you bought a new **Air Conditioner (AC):**

- Every day, between **4pm and 6pm**, you turn it on after coming home.  
- After a week, the AC **learns your routine**—when you return, what temperature you like, how long you run it.  
- On day 8, it **automatically turns on** the AC before you arrive, at your desired temperature, and switches off after the usual duration.  
- It could even **connect with your phone’s location** and cool your home **before you enter**.

In this analogy:

- **LLM** = the brain that observes and reasons about your actions  
- **Memory** = stores the historical patterns (your routine)  
- **Tools** = phone connectivity, sensors, etc.  
- **Loop** = observes → reacts → learns → adjusts  

---

### 🧠 LlmAgent in ADK

In **Google ADK**, the `LlmAgent` is the **core component** of your application.  
It uses an **LLM** for:

- Reasoning  
- Natural Language Processing (NLP)  
- Decision Making  

Unlike deterministic workflow agents (with fixed rules), an `LlmAgent` is **non-deterministic**—it can act dynamically and adapt instead of following a rigid script.

---

### 🌐 Supported Models

Google Agents ADK supports:
- **Gemini (Google’s models)**  
- **OpenAI models**  
- **Anthropic Claude**, etc.  

(We’ll keep this lesson simple and use **Gemini 2.0 Flash** without tools or memory.)

---

### 📂 Folder Structure (IMPORTANT)

Your agent project should follow this structure:

```
parent_folder/
│── agent_folder/     # Your agent's package directory
│   ├── __init__.py   # Must import agent.py
│   ├── agent.py      # Must define root_agent
│   └── .env          # Environment variables
```

### ⚙️ Environment Variables (`.env` file)

GOOGLE_GENAI_USE_VERTEXAI=FALSE # We are not using Vertex AI Studio
GEMINI_API_KEY=YOUR_API_KEY # Your Gemini API Key

👉 **Note:** Get your Gemini API Key from **Google AI Studio**.

---

### ▶️ Running Your Agent

1. Change directory to your **parent folder**:
2. Start the ADK web interface using the command adk web
3. Select your agent from the top-left dropdown (it will auto-select if only one exists).  
4. Open the **localhost URL** in your browser and enter an input to test the agent.

---

## ✅ Summary

- Learned what an AI Agent is.  
- Understood how **LlmAgent** works in the ADK.  
- Set up the **project structure** and `.env`.  
- Ran the agent using **ADK web**.  

---

🚀 Congratulations, you’ve just built your **first AI Agent using Google ADK**!  

---
