# 🔪 Mise No Mess: AI-Powered Restaurant Menu Optimization 🍽️

**Mise No Mess** is an AI-driven system designed to analyze Indian restaurant menus, identify operational inefficiencies, and recommend precise optimizations to improve kitchen workflows and profitability.

The name is a playful nod to **Mise en place** (French for "everything in its place")—our goal is to bring order and intelligence to the often chaotic kitchen environment.

---

## 💡 Overview & Problem Solved

Running a high-volume restaurant requires balancing speed, consistency, and cost. Many kitchens rely on tribal knowledge and menus that unintentionally lead to:
* **Station Overload:** E.g., the Curry station buckling under peak demand.
* **Ingredient Redundancy:** Duplication of prep work across different menu items.
* **Avoidable Bottlenecks:** Delays caused by shared equipment or preparation steps (e.g., Tandoor oven capacity).

**Mise No Mess** uses **Gemini 2.5 Flash** to parse raw menu text and generate actionable reports, turning menu data into operational intelligence.

---

## ✨ Key Features

* **Menu Parsing:** Converts raw menu text/PDFs into structured JSON data (items, ingredients, prep times, station assignments).
* **Operational Analysis:** Detects bottlenecks, cross-utilization problems, and prep redundancy during simulated peak hours.
* **Actionable Reports:** Generates short, owner-friendly narratives and structured findings on *why* problems occur and *how* to fix them.
* **Interactive UI:** Deployed with the ADK's built-in web interface for easy testing and tracing.

---

## ⚙️ Architecture

The system is deployed as a serverless microservice using the **Google Cloud** ecosystem, ensuring scalability and low latency.



| Component | Role | Technology |
| :--- | :--- | :--- |
| **ADK Agent** | Orchestrates tool-calling (parsing, analysis, reporting). | AI Development Kit (ADK) |
| **LLM Core** | Handles NLP, pattern recognition, and report writing. | Gemini 2.5 Flash |
| **Backend API** | Exposes core tools (`/parse_menu`, `/analyze_conflicts`). | FastAPI on Google Cloud Run |
| **Database** | Stores raw menus, analysis runs, and final reports. | Google Cloud Firestore |

---

## 🚀 Getting Started (Local Setup)

To run **Mise No Mess** locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR_REPO_URL]
    cd misenomess
    ```
2.  **Setup Environment:** Create and activate a Python virtual environment.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install Dependencies:** Ensure you have a `requirements.txt` file ready.
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set API Key:** Set your Gemini API key as an environment variable.
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```
5.  **Run Local Server:** Use the ADK CLI to start the web server with the UI.
    ```bash
    python -m google.adk.cli web --port 8000
    ```
    Access the UI at `http://127.0.0.1:8000`.

---

## ☁️ Deployment to Cloud Run

The recommended method for production deployment is using the `adk deploy cloud_run` command.

1.  Ensure you have the **gcloud CLI** configured and necessary APIs enabled (Cloud Run, Artifact Registry, etc.).
2.  Run the deployment command from the project root:
    ```bash
    adk deploy cloud_run \
      --project="YOUR_PROJECT_ID" \
      --region="YOUR_GCP_REGION" \
      --service_name="mise-no-mess-agent" \
      --with_ui \
      --trace_to_cloud \
      ./mise_no_mess # Path to the agent code folder
    ```
3.  The final output will provide the public HTTPS Service URL for your deployed agent and UI.

---

## 🤝 Contribution

We welcome contributions! If you have suggestions for new analysis tools (e.g., plating time analysis) or improvements to the menu parsing, please feel free to submit a Pull Request.

---
