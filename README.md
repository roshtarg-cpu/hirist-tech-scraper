# 🚀 Hirist Tech Jobs Scraper — India's #1 Tech Job Data API

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-06f?style=flat&logo=apify)](https://apify.com)
[![Made with Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

Extract **60+ structured fields** from [Hirist.tech](https://hirist.tech) — India's leading tech job portal. Get AI/ML, DevOps, Backend, Frontend & Full-Stack jobs with salary data, company ratings, skills, and recruiter information.

**Perfect for:** AI agents (Claude, ChatGPT), MCP servers, recruitment analytics, salary research, market intelligence.

---

## 🎯 Features

✅ **60+ Job Fields** — Title, company, salary, skills, experience, locations, ratings  
✅ **Company Intelligence** — AmbitionBox ratings, reviews, founded year, employee count  
✅ **Recruiter Data** — Name, title, last active date  
✅ **Diversity Filters** — Female candidates, differently-abled, ex-defence flags  
✅ **No Login Required** — Direct API access, no cookies, no auth  
✅ **MCP Compatible** — Use in Claude Desktop, VS Code Cline, or any AI agent  
✅ **Multiple Categories** — AI/ML, Backend, Frontend, DevOps, Data Engineering +10 more  
✅ **Fast & Reliable** — Uses Hirist's REST API (not browser scraping)  

---

## 📊 Output Data Sample

```json
{
  "jobId": 1664303,
  "title": "eBay.com - Assistant Manager - Data Science",
  "url": "https://www.hirist.tech/j/-1664303",
  "company": {
    "name": "eBay",
    "logo": "https://...",
    "rating": 4.1,
    "reviews": 104,
    "about": "eBay Inc. is a global commerce leader...",
    "founded": "1995",
    "employees": "1001-5000",
    "headquarters": "San Jose, California",
    "industry": "Internet"
  },
  "experience": { "min": 3, "max": 6 },
  "salary": { "min": 0, "max": 0, "hidden": true, "currency": "INR" },
  "location": ["Bangalore"],
  "skills": [
    { "name": "Data Science", "mandatory": true },
    { "name": "Python", "mandatory": false }
  ],
  "description": {
    "html": "<p>...",
    "text": "Clean text version..."
  },
  "metadata": {
    "posted": "2026-08-18T12:30:00",
    "views": 409,
    "applications": 231,
    "premium": true,
    "workFromHome": false,
    "category": 14
  },
  "recruiter": {
    "name": "ANDREA D'SA",
    "title": "Senior Recruiter",
    "lastActive": "2026-08-20"
  }
}
```

---

## 🚀 Quick Start

### Input Configuration

```json
{
  "categories": ["ai-ml", "data-engineering", "devops-sre"],
  "maxResults": 50,
  "includeDescription": true
}
```

### Run via Apify Console

1. Open [this actor](https://console.apify.com/actors/)
2. Choose categories (ai-ml, backend-development, etc.)
3. Set `maxResults` (1-1000)
4. Enable `includeDescription` for full job details
5. Click **Start** ▶️

### Run via API

```bash
curl -X POST https://api.apify.com/v2/acts/YOUR_USERNAME~hirist-tech-scraper/runs \
  -H "Authorization: Bearer YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["ai-ml", "backend-development"],
    "maxResults": 100,
    "includeDescription": true
  }'
```

### Run via Python

```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_APIFY_TOKEN')

run = client.actor('YOUR_USERNAME/hirist-tech-scraper').call(
    run_input={
        'categories': ['ai-ml', 'devops-sre'],
        'maxResults': 50,
        'includeDescription': True
    }
)

# Fetch results
for item in client.dataset(run['defaultDatasetId']).iterate_items():
    print(f"{item['title']} at {item['company']['name']}")
```

---

## 📋 Available Job Categories

| Category | Code | Description |
|----------|------|-------------|
| 🤖 AI/ML | `ai-ml` | Machine Learning, Deep Learning, NLP, Computer Vision |
| 📊 Data Analytics | `data-analytics-bi` | Business Intelligence, Data Analysis, Tableau, Power BI |
| 🗄️ Data Engineering | `data-engineering` | Big Data, ETL, Hadoop, Spark, Data Pipelines |
| ⚙️ Backend Dev | `backend-development` | Python, Java, Node.js, Go, Spring, Django |
| 🎨 Frontend Dev | `frontend-development` | React, Angular, Vue.js, JavaScript, UI/UX |
| 🌐 Full Stack | `full-stack` | MEAN, MERN, LAMP, Full-stack engineering |
| 📱 Mobile Apps | `mobile-applications` | iOS, Android, React Native, Flutter |
| 🚀 DevOps/SRE | `devops-sre` | AWS, Kubernetes, Docker, CI/CD, Site Reliability |
| 🔐 Cybersecurity | `cybersecurity` | Security, Penetration Testing, IAM, Compliance |
| ✅ QA/Testing | `quality-assurance` | Automation Testing, Selenium, Performance Testing |
| 🔧 Platform Eng | `platform-engineering` | SAP, ERP, Pega, RPA, Cloud Architecture |
| 📦 Product Mgmt | `product-management` | Product Strategy, Roadmap, User Stories |

---

## 🤖 AI Integration (Claude, ChatGPT, MCP)

### Use in Claude Desktop (MCP)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hirist-jobs": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server-apify", "YOUR_USERNAME/hirist-tech-scraper"]
    }
  }
}
```

### Use in ChatGPT (via Zapier/Make)

1. Run actor via Apify API
2. Connect dataset to Zapier/Make
3. Send results to ChatGPT for analysis

### Use in Custom AI Agents

```python
# LangChain example
from langchain.tools import Tool
from apify_client import ApifyClient

def search_hirist_jobs(category: str, max_results: int = 20):
    client = ApifyClient('YOUR_TOKEN')
    run = client.actor('YOUR_USERNAME/hirist-tech-scraper').call({
        'categories': [category],
        'maxResults': max_results
    })
    return list(client.dataset(run['defaultDatasetId']).iterate_items())

hirist_tool = Tool(
    name="SearchHiristJobs",
    func=search_hirist_jobs,
    description="Search Indian tech jobs on Hirist.tech by category"
)
```

---

## 💡 Use Cases

### 🏢 Recruiters & HR
- Source AI/ML talent in India
- Analyze salary trends by role & location
- Identify active recruiters at target companies
- Track job posting frequency

### 📈 Market Research
- Monitor hiring trends in tech sectors
- Compare company ratings & reviews
- Identify emerging skills in demand
- Track work-from-home adoption

### 🤖 AI Agents & Automation
- Auto-apply to relevant jobs
- Send daily job alerts via email/Slack
- Match candidates to open positions
- Generate job market reports

### 💼 Job Seekers
- Track new postings in your skills
- Research company ratings before applying
- Identify recruiter contacts
- Monitor salary ranges

---

## ⚙️ Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `categories` | Array | `["ai-ml"]` | Job categories to scrape (see table above) |
| `maxResults` | Integer | `50` | Maximum jobs to scrape (1-1000) |
| `includeDescription` | Boolean | `true` | Fetch full job descriptions (slower but complete) |
| `searchQuery` | String | - | *Future:* Search by keywords |
| `location` | String | - | *Future:* Filter by city |
| `experienceMin` | Integer | - | *Future:* Minimum years of experience |

---

## 📦 Output Format

Export to **JSON**, **CSV**, **Excel**, **HTML**, or **RSS**.

### JSON
```bash
curl "https://api.apify.com/v2/datasets/DATASET_ID/items?format=json"
```

### CSV (Excel-compatible)
```bash
curl "https://api.apify.com/v2/datasets/DATASET_ID/items?format=csv"
```

### Flatten nested fields
```bash
curl "https://api.apify.com/v2/datasets/DATASET_ID/items?format=csv&flatten=company,experience,salary"
```

---

## ⚡ Performance

| Metric | Value |
|--------|-------|
| Speed | ~50 jobs/minute with descriptions |
| Memory | <512 MB |
| Proxy | Optional (API is scraper-friendly) |
| Cost | ~$0.005 per 50 jobs |

---

## 🛡️ Anti-Bot Protection

✅ **Hirist API is scraper-friendly** — no CAPTCHA, no Cloudflare challenges  
✅ **No browser required** — lightweight HTTP client  
✅ **Generous rate limits** — 160K requests per window  
✅ **No login needed** — anonymous access  

---

## 🐛 Troubleshooting

**Q: Some jobs have `salary.hidden: true`**  
A: Employers often hide salary ranges on Hirist. This is expected behavior.

**Q: No jobs returned**  
A: Check category name spelling. Use codes from the table above.

**Q: Missing company ratings**  
A: Not all companies have AmbitionBox profiles. Fields will be `null`.

**Q: Want to filter by skills/location?**  
A: API doesn't support direct filtering yet. Scrape broader category and filter results locally.

---

## 📞 Support & Feature Requests

- **Issues:** [GitHub Issues](#)
- **Feature Requests:** Comment on actor page
- **Custom Scraping:** Contact on Apify

---

## 📄 License

Apache 2.0 — Free for commercial use.

---

## 🙏 Credits

Built with ❤️ using [Apify SDK](https://docs.apify.com/sdk/python/).

Data source: [Hirist.tech](https://hirist.tech) — India's #1 tech job portal.

---

**Happy Scraping! 🚀**
