"""
Smart Tracker Configuration
Contains planning blueprints and shared configuration constants.
"""

__version__ = "0.1.0"

PLANNING_BLUEPRINT = {
    "🌐 Core Full-Stack Development": {
        "subsections": [
            {
                "name": "🖥️ Front-End",
                "tools": [
                    {"name": "HTML", "min_hours": 20, "max_hours": 30},
                    {"name": "CSS", "min_hours": 20, "max_hours": 30},
                    {"name": "JavaScript (ES6+)", "min_hours": 60, "max_hours": 80},
                    {"name": "React", "min_hours": 70, "max_hours": 90},
                    {"name": "Tailwind CSS", "min_hours": 15, "max_hours": 25}
                ]
            },
            {
                "name": "⚙️ Back-End",
                "tools": [
                    {"name": "Django", "min_hours": 80, "max_hours": 100},
                    {"name": "PostgreSQL", "min_hours": 40, "max_hours": 50}
                ]
            },
            {
                "name": "🔗 Lightweight APIs / Model Serving",
                "tools": [
                    {"name": "FastAPI", "min_hours": 40, "max_hours": 60}
                ]
            },
            {
                "name": "🌉 Integration (optional)",
                "tools": [
                    {"name": "Next.js", "min_hours": 40, "max_hours": 60}
                ]
            },
            {
                "name": "☁️ Deployment",
                "tools": [
                    {"name": "AWS (S3 + EC2 + Lambda)", "min_hours": 80, "max_hours": 100},
                    {"name": "GitHub Actions", "min_hours": 25, "max_hours": 40}
                ]
            }
        ]
    },
    "📊 Data Science & Machine Learning": {
        "subsections": [
            {
                "name": "🧮 Core Libraries",
                "tools": [
                    {"name": "Pandas", "min_hours": 80, "max_hours": 100},
                    {"name": "NumPy", "min_hours": 25, "max_hours": 35},
                    {"name": "SciPy", "min_hours": 15, "max_hours": 20}
                ]
            },
            {
                "name": "📈 Visualization",
                "tools": [
                    {"name": "Matplotlib", "min_hours": 25, "max_hours": 35},
                    {"name": "Seaborn", "min_hours": 20, "max_hours": 25},
                    {"name": "Streamlit", "min_hours": 50, "max_hours": 70}
                ]
            },
            {
                "name": "🤖 Machine Learning",
                "tools": [
                    {"name": "scikit-learn", "min_hours": 60, "max_hours": 80},
                    {"name": "PyTorch", "min_hours": 60, "max_hours": 80},
                    {"name": "TensorFlow", "min_hours": 60, "max_hours": 80},
                    {"name": "CUDA (optional)", "min_hours": 20, "max_hours": 30}
                ]
            },
            {
                "name": "🔄 Pipelines",
                "tools": [
                    {"name": "Apache Airflow", "min_hours": 50, "max_hours": 70}
                ]
            },
            {
                "name": "🗄️ Databases (for data work)",
                "tools": [
                    {"name": "PostgreSQL", "min_hours": 40, "max_hours": 60}
                ]
            }
        ]
    },
    "📑 Excel Automation & Data Handling": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "OpenPyXL", "min_hours": 20, "max_hours": 30},
                    {"name": "xlwings", "min_hours": 25, "max_hours": 40}
                ]
            }
        ]
    },
    "⚙️ Core Automation (Support Layer)": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "Python (automation scripting)", "min_hours": 50, "max_hours": 70},
                    {"name": "Cron Jobs + Airflow", "min_hours": 20, "max_hours": 30},
                    {"name": "Selenium / Playwright", "min_hours": 40, "max_hours": 60},
                    {"name": "Requests + aiohttp", "min_hours": 25, "max_hours": 40},
                    {"name": "GitHub Actions (CI/CD automation)", "min_hours": 20, "max_hours": 30}
                ]
            }
        ]
    },
    "🔒 Reliability & Security": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "pytest (testing)", "min_hours": 30, "max_hours": 50},
                    {"name": "OAuth 2.0 + Web App Security", "min_hours": 40, "max_hours": 60}
                ]
            }
        ]
    },
    "🧰 Supporting Skills": {
        "subsections": [
            {
                "name": "",
                "tools": [
                    {"name": "Git (version control)", "min_hours": 25, "max_hours": 40},
                    {"name": "REST + GraphQL APIs", "min_hours": 40, "max_hours": 60},
                    {"name": "Jira + Agile Collaboration", "min_hours": 20, "max_hours": 30}
                ]
            }
        ]
    }
}
