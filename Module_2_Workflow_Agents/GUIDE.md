# Google Agents ADK Development – Module 2

## Welcome to Module 2 🎉

### Understanding the Workflow Agents

This module will guide you through understanding workflow agents and how to build them using the ADK.

📝 Official Documentation: [Workflow Docs](https://google.github.io/adk-docs/agents/workflow-agents/)

---

## 📌 Prerequisites

- Basic understanding of Large Language Models (LLMs)
- Familiarity with Python programming

---

## 📖 Overview

n previous modules, we built our first AI Agent and explored the LlmAgent deeply.
This module explores three workflow agent types: Sequential Agents, Loop Agents, and Parallel Agents.

---

## What are Workflow Agents?

A workflow defines the flow of a process from start to end. Think of baking a cake: buy ingredients, mix, prepare the mold, pour, bake, and decorate.
Similarly, in agent systems, workflows specify how agents should operate—for example, two agents running one after another, another receiving outputs and iterating, etc.
Workflow agents are specialized ADK components that orchestrate when and how sub-agents run, defining the control flow of a process.

---

## Types of Workflow Agents

1. Sequential Agents: Execute each sub-agent one after another in a defined sequence.
2. Parallel Agents: Execute multiple sub-agents concurrently at the same time.
3. Loop Agents: Iterate sub-agents multiple times until a limit or condition is met.

**Note**: There are few images taken from the Google ADK Official Documentation in these folders to understand the concepts better.

---

## Important Parameters

1. Name: Name of the workflow agent.
2. Description: One or two lines describing what the agent does.
3. Sub_agents: The list of sub-agents to be executed by the workflow agent; must be a list.
4. max_iterations: For Loop Agents, the number of times the sub-agents should iterate.

---

### 📂 Folder Structure (IMPORTANT)

Your agent project should follow this structure:

```bash

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

- Learned what a **Workflow Agent** is.  
- Understood about **Sequential Agent**, **Loop Agent**, and **Parallel Agent**.  
- Successfully set up and ran agents with ADK.

---

🚀 Congratulations, you’ve leveled up your understanding of **Workflow Agents**! 🎯

---
