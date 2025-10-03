# Google Agents ADK Development – Module 3

## Welcome to Module 3 🎉

### Understanding Session, State, and Memory

This module guides you through the concepts of Session, State, and Memory, and how to build and run them using the ADK.

📝 Official Documentation: [Session, State and Memory](https://google.github.io/adk-docs/sessions/)

---

## 📌 Prerequisites

- Basic understanding of Large Language Models (LLMs)
- Familiarity with Python programming

---

## 📖 Overview

In previous modules, we built our first AI Agent and explored the LlmAgent. Workflow Agents were then implemented and discussed.

This module introduces Session, State, Events, and Memory, as well as runners – which are essential to running agents in context.

---

## What are Session, State, and Memory?

Imagine a chatbot helping users book flights:

**Without these concepts:**

- ❌ Agent forgets the user's destination after mention
- ❌ Every message is treated as a new conversation
- ❌ User repeats themselves every turn

**With these concepts:**

- ✅ Agent remembers conversation context
- ✅ Tracks what the user already said
- ✅ Recalls info from previous conversations

---

### Session

- A Session represents a single, ongoing interaction between a user and your agent.
- Contains the chronological sequence of messages and actions during that conversation.
- A session is the entire history of one conversation.

**Example:**
Session 1 (Morning)
User: "I want to book a flight to Paris"
Agent: "Great! When would you like to travel?"
User: "Next Monday"
Agent: "Perfect, I'll search for flights..."

Session 2 (Afternoon – NEW conversation)
User: "What was the price of that flight?"
Agent: "I don't have information about previous flights..."

---

### State

- Data stored within a specific session, tracking all relevant info for the current conversation.
- Functions like dynamic variables that update during dialogue.

**Example Conversation:**

You: "I want to order a pizza"
Agent: "What size?"
You: "Large"
Agent: "What toppings?"
You: "Pepperoni and mushrooms"
Agent: "Delivery or pickup?"
You: "Delivery"

**Corresponding State:**

state = {
"size": "large",
"toppings": ["pepperoni", "mushrooms"],
"delivery_method": "delivery",
"order_step": "address_needed",
"price": 15.99
}

- State means current working data, changes during the conversation. So in one statement, State is the collection of important variables that change during the conversation and help the agent make decisions.

---

### Memory

- Memory is a store for information that can span multiple sessions or pull from external knowledge.
- Functions as a knowledge base for retrieving context, even after restarting the application.

**Example:**

Week 1, Session 1:
User: "My favorite destination is Tokyo"
[Saved to Memory]

Week 2, Session 2 (NEW conversation):
User: "Can you suggest a trip for me?"
Agent: [Finds "Tokyo" preference in Memory]
Agent: "Based on your love for Tokyo, how about exploring Kyoto?"

- Memory helps provide continuity and recall beyond immediate sessions.

---

## How Do These Work Together?

1. User starts conversation → **Session created**
2. User: "Book me a flight to Paris"  
   → **State** stores: `{'destination': 'Paris'}`  
   → **Events** log: [UserMessage, AgentResponse]
3. User: "Make it for 2 people"  
   → **State** updates: `{'destination': 'Paris', 'passengers': 2}`  
   → **Events** log: [Previous..., UserMessage, AgentResponse]
4. Conversation ends  
   → **Session** information saved to **Memory**
5. Next week, NEW Session starts  
   → Agent can search **Memory** for past preferences  
   → **State** starts fresh (empty)

---

### Event

- An Event is a record of something that happened in the conversation; think of it as a single diary entry.

**Example:**

You: "I have a headache" (Event 1)
Doctor: "How long have you had it?" (Event 2)
You: "3 days" (Event 3)
Doctor: "Take this medicine" (Event 4)

---

### What are Runners?

- Runners are orchestrators; they manage sessions, coordinate state, handle events, and execute the agent for you.

**Responsibilities:**

- Manage sessions (create, retrieve, update)
- Handle events (user, agent, tool, save)
- Update state (inject, collect, apply changes)
- Execute agent (pass messages/context, trigger callbacks)
- Stream responses (real-time event updates)

**Example:**  
You (Producer): "Make a movie scene!"  
Director (Runner):  

- Calls actors (agents/tools)  
- Sets the scene (session/state)  
- Records everything (events)  
- Manages script (instructions)  
- Coordinates timing (callbacks)  
- Saves footage (session_service)  
You get to watch the result.

---

## Different Types of Sessions and Memories

### Types of Session Services

1. **InMemorySessionService**  
   - Stores all session data in application memory (RAM).  
   - Fast, but temporary – all data lost on restart.  
   - No persistent storage.

2. **DatabaseSessionService**  
   - Stores session data in databases (SQLite, MySQL, PostgreSQL).
   - Persistent storage for retrieval after restart.
   - Good for self-hosted, controlled environments.

3. **VertexAiSessionService**  
   - Stores sessions using Google Cloud's Vertex AI infrastructure.
   - Professional, scalable, managed by Google.
   - Paid, with persistent cloud storage.

### Types of Memory Services

1. **InMemoryMemoryService**  
   - Stores information in application memory, performs keyword search.
   - Temporary, no persistent storage.

2. **VertexAiMemoryBankService**  
   - Uses Google Vertex AI for permanent, semantic memory storage.
   - Paid, production-grade, intelligent retrieval.

#### In Short

**Session Services** – Where conversations are stored

- InMemory: Temporary, for development  
- Database: Self-hosted, for control  
- VertexAI: Cloud-based, for production

**Memory Services** – Long-term knowledge storage

- InMemory: Basic, temporary, keyword based  
- VertexAI Memory Bank: Permanent, semantic, intelligent search

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

Method 1:

1. Change directory to your **parent folder**:
2. Start the ADK web interface using the command adk web
3. Select your agent from the top-left dropdown (it will auto-select if only one exists).  
4. Open the **localhost URL** in your browser and enter an input to test the agent.

Method 2:

Change to the agent folder and run the agent directly using the command: python agent.py
---

## ✅ Summary

- Learned about **Session**, **State**, **Memory**, and **Events**.  
- Understood the role of **Runners** in managing agents.
- Explored different types of session and memory services.  
- Successfully set up and ran agents with ADK.

---

🚀 Congratulations, you’ve leveled up your understanding of **Session, State, Memory, and Events**! 🎯

---
