# 🧠 BrainForge — Multi-Agent AI Research System

## 📌 Project Overview

**BrainForge** is an AI-powered research system designed to automate the process of researching a topic, collecting information from the web, generating a structured report, and evaluating the quality of that report.

Traditional research often requires manually searching multiple websites, reading their content, collecting useful information, and organizing everything into a report.

BrainForge simplifies this workflow by dividing the research process into specialized tasks handled by different AI components.

### 🔄 Core Workflow

**Search → Scrape → Generate → Evaluate → Refine → Final Report**

This project provided practical experience with **Multi-Agent AI Systems, LLMs, LangChain, Web Scraping, Prompt Engineering, LLM-based Evaluation, and Iterative AI Workflows.**

---

## 🎯 Objectives

- Automate web-based research using AI.
- Find relevant sources for a given research topic.
- Extract useful information from web pages.
- Generate structured research reports using an LLM.
- Evaluate the quality of generated reports.
- Identify strengths and areas that need improvement.
- Support iterative report refinement.
- Include the sources used during the research process.
- Demonstrate how specialized AI components can work together to complete a complex task.

---

## 🤖 Multi-Agent Architecture

BrainForge follows a modular architecture where different components are responsible for different stages of the research process.

Instead of asking a single AI component to perform the entire task, the workflow is divided into specialized responsibilities:

| Component | Responsibility |
|-----------|----------------|
| 🔎 Research Agent | Finds relevant web sources and URLs |
| 🌐 Scraping Agent | Extracts useful content from web pages |
| 📝 Report Generation Chain | Generates a structured research report |
| 📊 Report Evaluation Chain | Reviews and evaluates the generated report |
| 🔄 Refinement Loop | Allows the report to be regenerated when improvement is required |

This separation makes the system easier to understand, maintain, and extend.

---

## 🔍 How BrainForge Works

### 1. 🔎 Research

The user provides a research topic.

The **Research Agent** searches the web and identifies relevant sources and URLs related to the topic.

### 2. 🌐 Content Extraction

The collected URLs are passed to the **Scraping Agent**.

Using **BeautifulSoup**, the agent extracts useful textual content from the web pages so that it can be processed by the next stage.

### 3. 📝 Report Generation

The extracted information is passed to the **Report Generation Chain**.

An LLM processes the collected information and generates a structured and readable research report.

### 4. 📊 Report Evaluation

The generated report is passed to a separate **Report Evaluation Chain**.

The evaluator reviews the report and provides:

- Quality score
- Strengths
- Issues
- Areas for improvement

### 5. 🔄 Report Refinement

If the generated report receives a score of **7 or below**, BrainForge asks the user whether they want to regenerate the report.

If the user chooses to continue, the system generates another version.

This creates an iterative workflow:

**Generate → Evaluate → Refine**

### 6. 📄 Final Report

Once the report is ready, BrainForge presents the final research report along with the sources used during the research process.

---

## 📊 System Workflow

```text
                    User Research Topic
                            │
                            ▼
                    ┌─────────────────┐
                    │ Research Agent  │
                    └────────┬────────┘
                             │
                             ▼
                  Find Relevant Web Sources
                             │
                             ▼
                    ┌─────────────────┐
                    │ Scraping Agent  │
                    └────────┬────────┘
                             │
                             ▼
                     Extract Web Content
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Report Generation     │
                  │ Chain                │
                  └──────────┬───────────┘
                             │
                             ▼
                  Generate Research Report
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Report Evaluation     │
                  │ Chain                │
                  └──────────┬───────────┘
                             │
                             ▼
                   Evaluate Report Quality
                             │
                             ▼
                        Score ≤ 7?
                       /          \
                     Yes           No
                      │             │
                      ▼             ▼
                 Regenerate     Final Report
                      │             │
                      └──────┐      │
                             │      │
                             ▼      ▼
                        Improved   Sources
                         Report





🛠️ Technologies Used
Python
LangChain
Large Language Models (LLMs)
BeautifulSoup
Web Search
Prompt Engineering
Multi-Agent Architecture

Live Link:    https://brainforge-multiagent-researcher-by-nabeel.streamlit.app/

🤝 Feedback

Suggestions, improvements, and feedback are always welcome.

If you find this project useful or interesting, feel free to ⭐ the repository and share your feedback.

👨‍💻 Author

Nabeel Shahid

BS Computer Science | University of Gujrat
