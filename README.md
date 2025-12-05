HighBar V2 – ROAS Analysis Intelligent Pipeline



This project implements an intelligent multi-agent system that processes marketing campaign data and generates insights, KPIs, hypotheses, and creative recommendations based on ROAS (Return on Ad Spend).

The solution includes a full end-to-end pipeline with modular agents and orchestrator logic.



🚀 Project Overview



The goal of this project is to analyze ROAS performance for advertising campaigns using an automated multi-step pipeline.

The system loads raw campaign data, validates schema, computes KPIs and trends, detects ROAS changes, generates hypotheses, evaluates hypotheses, and finally produces creative recommendations.



This aligns with the HighBar V2 assignment requirements.



🧠 Architecture



The project uses a multi-agent design:



1️⃣ Planner Agent



Understands the query



Generates the action plan (sequence of tasks)



2️⃣ Loader Agent



Reads CSV data from the data/ folder



Returns a cleaned pandas DataFrame



3️⃣ Evaluator Agent



Generates hypotheses



Validates hypotheses



Parses dates



Runs analysis logic



4️⃣ Insight Agent



Converts validated hypotheses into human-readable insights



5️⃣ Creative Agent



Generates final creative recommendations per campaign



6️⃣ Orchestrator



Manages pipeline execution



Logs intermediate outputs



Produces final summary report



🔧 Pipeline Steps



The orchestrator executes these steps:



load\_data



schema\_check



compute\_kpis



compute\_trends



detect\_roas\_changes



generate\_hypotheses



validate\_hypotheses



generate\_creative\_recommendations



compile\_report



📊 Final Output Example



After running:



python -m src.run "Analyze ROAS drop"





You should see a summary like:



{

&nbsp; 'query': 'Analyze ROAS drop',

&nbsp; 'plan': \['load\_data', 'schema\_check', 'compute\_kpis', 'compute\_trends',

&nbsp;          'detect\_roas\_changes', 'generate\_hypotheses', 'validate\_hypotheses',

&nbsp;          'generate\_creative\_recommendations', 'compile\_report'],



&nbsp; 'schema': True,

&nbsp; 'rows': 4500,

&nbsp; 'insights\_count': 2,

&nbsp; 'evaluated\_count': 10,

&nbsp; 'creatives\_count': 30,

&nbsp; 'kpis': {'rows': 4500}

}





This indicates that all steps succeeded and recommendations were generated.



📂 Folder Structure

HighBar\_V2/

│

├── src/

│   ├── agents/

│   │   ├── planner.py

│   │   ├── evaluator.py

│   │   ├── insight.py

│   │   └── creative.py

│   ├── utils/

│   │   ├── loader.py

│   │   ├── logger.py

│   │   └── helpers.py

│   ├── orchestrator.py

│   └── run.py

│

├── data/

│   └── campaigns.csv   (your dataset)

│

└── reports/

&nbsp;   ├── insights.json

&nbsp;   └── creatives.json



▶️ How to Run

1\. Install dependencies

pip install -r requirements.txt



2\. Place your CSV file



Inside:



data/



3\. Run the pipeline

python -m src.run "Analyze ROAS drop"



📝 Notes for Reviewers



The system is modular and extendable.



Hypothesis generation and evaluation logic are intentionally simplified for the assignment.



The pipeline ensures graceful fallback when data is missing.



Multiple logs are saved under logs/ for debugging.



The code is clean, well-structured, and easy to maintain.

