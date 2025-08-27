# Google Agents ADK Development – Module 1

## Welcome to the Second Lesson 🎉

### Lesson 2: Understanding the LlmAgent

    This lesson will guide you to have a deeper understanding of the **LlmAgent** and learn how to use its full potential.  
    📝 Official Documentation: [LlmAgent Docs](https://google.github.io/adk-docs/agents/llm-agents/)

---

### 📌 Prerequisites

- Basic understanding of **Large Language Models (LLMs)**
- Familiarity with **Python programming**

---

### 📖 Overview

In the previous lesson, we built our very **first AI Agent**.  
Now, it’s time to **deep dive** into the **LlmAgent**.  
We’ll explore different parameters that can help us configure and generate **better quality outputs**.

---

### ⚙️ LlmAgent Parameters

1. **Generate_Content_Config**  
   - *Optional configuration* that allows setting parameters like:
     - `max_no_of_tokens`  
     - `temperature`  
     - and other output customization options.

2. **BaseModel (from Pydantic)**  
   - Used to **define a schema/structure** for the agent’s output.

3. **OutputSchema**  
   - You can pass a `BaseModel` class to enforce that the agent’s **output follows a specific format**.

4. **Tools**  
   - Functions that allow the agent to **interact with the external environment**.  
   - These can be:
     - **Built-in tools** (provided by ADK)  
     - **Custom tools** (created by you)

5. **Planner**  
   - Enables the agent to leverage the **thinking capabilities** of the LLM.  

   Two common planners:
   - **BuiltInPlanner**  
     - Works with **Gemini 2.5 family models**, as they come with **built-in reasoning capabilities**.  
   - **ReACT Planner**  
     - Applicable to **any LLM**.  
     - Adds reasoning via the *ReAct* (Reason + Act) framework.  
     - 📖 References:  
       - [Prompting Guide – ReAct](https://www.promptingguide.ai/techniques/react)  
       - [ReAct Paper](https://arxiv.org/abs/2210.03629)  

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

- Learned what an **LlmAgent** is.  
- Explored the **parameters** (config, schema, tools, planners).  
- Understood how to use **BuiltInPlanner** and **ReAct Planner**.  
- Successfully set up and ran agents with ADK.  

---

🚀 Congratulations, you’ve leveled up your understanding of **LlmAgents**! 🎯

---
