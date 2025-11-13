<<<<<<< HEAD
# Member-QA-System
=======
# Member QA System

A natural language question-answering system for member data, built with FastAPI and OpenAI GPT.

## 🌟 Features

- Natural language question processing
- Real-time data fetching from member API
- RESTful API endpoint for questions
- Fast and accurate answers using GPT-4o-mini

## 🚀 Live Demo

**API Endpoint:** `[Your deployed URL here]/ask`

## 📋 Example Questions

- "When is Layla planning her trip to London?"
- "How many cars does Vikram Desai have?"
- "What are Amira's favorite restaurants?"

## 🛠️ Technology Stack

- **Framework:** FastAPI
- **AI/ML:** OpenAI GPT-4o-mini
- **HTTP Client:** httpx
- **Deployment:** Docker-ready

## 📦 Installation

### Prerequisites

- Python 3.11+
- OpenAI API key

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/member-qa-system.git
cd member-qa-system
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```bash
cp .env.example .env
```

5. Add your OpenAI API key to `.env`:

```
OPENAI_API_KEY=your_actual_api_key_here
MEMBER_API_URL=https://november7-730026606190.europe-west1.run.app
```

6. Run the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. Build the Docker image:

```bash
docker build -t member-qa-system .
```

2. Run the container:

```bash
docker run -p 8000:8000 --env-file .env member-qa-system
```

## 🔌 API Usage

### Ask a Question

**Endpoint:** `POST /ask`

**Request Body:**

```json
{
	"question": "When is Layla planning her trip to London?"
}
```

**Response:**

```json
{
	"answer": "Layla Kawaguchi is planning to book a trip to London..."
}
```

### Example with cURL

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "When is Layla planning her trip to London?"}'
```

### Example with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "When is Layla planning her trip to London?"}
)
print(response.json())
```

## 🏗️ Architecture & Design Notes (Bonus 1)

### Approach Chosen: **LLM-based QA with OpenAI GPT**

I selected this approach for its superior natural language understanding and flexibility.

### Alternative Approaches Considered:

#### 1. **Keyword/Pattern Matching**

- **Pros:**
  - Fast and lightweight
  - No external API dependencies
  - Deterministic results
- **Cons:**
  - Limited to predefined patterns
  - Poor handling of paraphrased questions
  - Requires extensive manual pattern engineering
  - Cannot handle complex queries

#### 2. **Local NLP with spaCy + Named Entity Recognition**

- **Pros:**
  - No API costs
  - Privacy-friendly (all processing local)
  - Good for entity extraction
- **Cons:**
  - Requires training data
  - Limited reasoning capabilities
  - Struggles with complex queries
  - Requires more development time

#### 3. **RAG (Retrieval-Augmented Generation) with Vector Database**

- **Pros:**
  - Scalable for large datasets
  - Efficient semantic search
  - Good for similar question matching
- **Cons:**
  - Overkill for current dataset size (3,349 messages)
  - Additional infrastructure (vector DB)
  - More complex deployment
  - Higher operational costs

#### 4. **Fine-tuned Small Language Model**

- **Pros:**
  - Custom-tailored to domain
  - Potentially lower inference costs
  - No external dependencies
- **Cons:**
  - Requires labeled training data
  - Time-intensive fine-tuning process
  - Model maintenance overhead
  - May underperform GPT-4 on edge cases

### Why GPT-4o-mini Was Selected:

1. **Superior NLU:** Handles diverse question phrasings naturally
2. **Zero Training:** Works out-of-box without training data
3. **Reasoning:** Can infer answers from context effectively
4. **Development Speed:** Fastest to production-ready state
5. **Cost-Effective:** GPT-4o-mini is affordable for this use case
6. **Reliability:** Proven performance on QA tasks

### System Design:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│  FastAPI     │────▶│  Data       │
│             │     │  /ask        │     │  Service    │
└─────────────┘     └──────────────┘     └─────────────┘
                           │                     │
                           │                     ▼
                           │              ┌─────────────┐
                           │              │  Member API │
                           │              └─────────────┘
                           ▼
                    ┌──────────────┐
                    │  QA Service  │
                    │  (OpenAI)    │
                    └──────────────┘
```

## 📊 Data Insights & Anomalies (Bonus 2)

After analyzing the member messages dataset, here are the key findings:

### Dataset Overview:

- **Total Messages:** 3,349
- **Unique Members:** Multiple high-value members
- **Time Range:** 2024-11-14 to 2025-11-04

### Anomalies & Inconsistencies:

#### 1. **Outdated Communication Methods**

- **Finding:** Fax numbers mentioned in messages (e.g., "My new fax number is 431-555-2363")
- **Impact:** Unusual for modern luxury concierge service
- **Example:** Lily O'Sullivan - Message ID: 32c3ee64-0e65-44c8-a1c6-5ec134043e75

#### 2. **Inconsistent Date Handling**

- **Finding:** Some requests reference future dates that may have passed
- **Impact:** System needs to handle temporal context
- **Example:** Requests for "next month" or "next Friday" without absolute dates

#### 3. **Data Quality Issues**

- **Missing Context:** Some messages lack crucial details (specific dates, locations)
- **Ambiguous References:** "Next weekend," "tomorrow" without timestamp context
- **No Structured Data:** All preferences stored as free-text messages

#### 4. **Member Behavior Patterns**

- **High-Frequency Users:** Some members (Sophia Al-Farsi, Vikram Desai) have significantly more messages
- **Request Types:** Mix of bookings, preferences, complaints, and profile updates
- **Luxury Services:** Frequent requests for private jets, yachts, exclusive restaurants

#### 5. **Inconsistent Information**

- **Contact Updates:** Multiple phone number updates for same members
- **Address Changes:** Members updating addresses frequently
- **Billing Issues:** Recurring complaints about charges and invoices

#### 6. **Temporal Inconsistencies**

- **Finding:** Timestamps show messages dated in future (2025)
- **Impact:** May indicate test data or timezone issues
- **Example:** Messages dated up to November 2025

### Recommendations:

1. **Structured Data:** Store preferences and profile data separately from messages
2. **Entity Extraction:** Parse and extract structured information (dates, locations, numbers)
3. **Deduplication:** Handle multiple messages about the same topic
4. **Temporal Awareness:** Better handling of relative dates and time references
5. **Validation:** Add data validation for phone numbers, dates, and other structured fields

## 🧪 Testing

Test the system with the provided example questions:

```bash
# Question 1: Layla's London trip
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "When is Layla planning her trip to London?"}'

# Question 2: Vikram's cars
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How many cars does Vikram Desai have?"}'

# Question 3: Amira's restaurants
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are Amira'\''s favorite restaurants?"}'
```

## 🚀 Deployment

This application is Docker-ready and can be deployed to:

- **Render:** Connect GitHub repo, set environment variables
- **Railway:** Automatic deployment from GitHub
- **Fly.io:** `flyctl deploy`
- **Google Cloud Run:** Container-based deployment
- **AWS ECS/Fargate:** Docker container deployment

### Environment Variables Required:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MEMBER_API_URL`: The member API endpoint (default: https://november7-730026606190.europe-west1.run.app)

## 📝 License

MIT License

<!-- Intentionally concise; authored for the take-home submission. -->
>>>>>>> 24f6b47 (chore: initial commit for Member QA System)
