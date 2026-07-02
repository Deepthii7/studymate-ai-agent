# 🧠 MindMesh AI

### A Multi-Agent Educational Assistant for Personalized Learning

Built with **Python, Streamlit, and Google Gemini** for the **Kaggle 5-Day AI Agents: Intensive Vibe Coding Course With Google Capstone Project**.

---

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-API-4285F4?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 🌐 Live Demo

https://mindmesh-ai.streamlit.app

## 🎥 Demo Video

https://youtu.be/qkOyJDPF_i0

--- 

## 📖 Overview

**MindMesh AI** is a multi-agent educational assistant that helps learners understand any topic through a coordinated team of specialized AI agents. Instead of relying on a single prompt to do everything, MindMesh AI breaks the learning process into distinct responsibilities — explaining a concept, testing understanding, and planning further study — each handled by its own dedicated agent.

A user simply enters a topic they want to learn. A **Coordinator Agent** then orchestrates the workflow, calling on the **Explainer**, **Quiz Generator**, and **Study Planner** agents in sequence to assemble a complete, ready-to-use learning package — all displayed in a clean, modern Streamlit interface.

This project was developed as the capstone submission for Kaggle's 5-Day AI Agents: Intensive Vibe Coding Course with Google, demonstrating how multiple AI agents can collaborate to create a structured and engaging learning experience.

---

## 💡 Why MindMesh AI?

Traditional AI assistants typically generate a single response, but they rarely guide users through an entire learning journey.

MindMesh AI addresses this limitation by using multiple specialized AI agents that collaborate to generate explanations, quizzes, and personalized study plans.

---

## 🎯 Problem Statement

Many learners struggle to organize information into a structured learning path. Traditional AI chatbots typically provide a single response, leaving users without a way to assess their understanding or plan what to learn next.

MindMesh AI addresses this challenge through a multi-agent architecture that generates beginner-friendly explanations, interactive quizzes, and personalized study plans, helping learners move from understanding to practice in a single workflow.

---

## ✨ Features

- 📚 **Beginner-friendly explanations** of any topic, written in simple, accessible language
- 💻 **Code examples when appropriate**, to reinforce technical concepts
- 📝 **Auto-generated quizzes**, including multiple-choice, true/false, and scenario-based questions
- 📅 **Personalized study plans**, structured as a practical 3-day learning roadmap
- 🤖 **Multi-agent architecture**, with a Coordinator Agent orchestrating specialized sub-agents
- 🎨 **Modern, responsive Streamlit UI** for a clean and intuitive user experience

---

## 🧩 Multi-Agent Architecture

MindMesh AI follows a coordinator-based multi-agent workflow. The Coordinator Agent receives the user's topic, delegates tasks to specialized agents, and combines their outputs into a complete learning package.

<p align="center">
  <img src="assets/architecture.png" alt="MindMesh AI Architecture" width="100%">
</p>

| Agent | Responsibility |
|---|---|
| **Coordinator Agent** | Orchestrates the overall workflow and routes the topic to each specialized agent |
| **Explainer Agent** | Produces a clear, beginner-friendly explanation of the chosen topic, including code examples when appropriate |
| **Quiz Generator Agent** | Creates a multiple-choice question, a true/false question, and a scenario-based question to test understanding |
| **Study Planner Agent** | Designs a personalized, practical 3-day study plan based on the explanation |

---

## 🔄 Workflow

1. User enters a learning topic.
2. Coordinator Agent receives the request.
3. Explainer Agent generates a beginner-friendly explanation.
4. Quiz Generator creates assessment questions.
5. Study Planner produces a personalized roadmap.
6. Results are combined into a complete learning package and displayed in Streamlit.

---

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **LLM:** Google Gemini API
- **Environment:** python-dotenv
- **Architecture:** Multi-Agent Workflow

---

## ⚙️ Installation

Follow these steps to set up MindMesh AI locally.

### 1. Clone the repository

```bash
git clone https://github.com/Deepthii7/mindmesh-ai-agent.git
cd mindmesh-ai-agent 
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your environment variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Running the Project

Once installed and configured, start the Streamlit app with:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (typically `http://localhost:8501`) in your browser.

---

## 📁 Project Structure

```
mindmesh-ai/
│
├── app.py              # Main Streamlit application and agent logic
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
├── README.md           # Project documentation
└── assets/             # Screenshots and static assets
```

---

## 🖼️ Screenshots

### 🏠 Home Page

![Home Page](assets/home.png)

### 📘 Explanation

![Explanation](assets/explanation.png)

### 📝 Quiz

![Quiz](assets/quiz.png)

### 📅 Study Plan

![Study Plan](assets/studyplan.png)


---

## 🚀 Future Improvements

- Add support for exporting the learning package as a PDF
- Allow users to track quiz scores and progress over time
- Add difficulty-level selection for explanations and quizzes
- Support multi-topic learning paths and longer study plans
- Add persistent history of previously generated topics
- Integrate Retrieval-Augmented Generation (RAG) for domain-specific learning.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 👤 Author

Deepthii Panchapakesan
B.Tech Computer Science & Engineering (Artificial Intelligence & Machine Learning)

Built for the **Kaggle 5-Day AI Agents: Intensive Vibe Coding Course With Google**

- GitHub: https://github.com/Deepthii7
- LinkedIn: http://linkedin.com/in/deepthii-panchapakesan-06ba0337b

---

⭐ If you found this project interesting, consider giving it a star on GitHub!