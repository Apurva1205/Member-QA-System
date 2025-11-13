from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.models import QuestionRequest, AnswerResponse
from app.services.qa_service import QAService
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Member QA System",
    description="A question-answering system for member data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize QA service
qa_service = QAService()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - serves demo interface."""
    demo_path = Path(__file__).parent.parent / "demo.html"
    if demo_path.exists():
        return demo_path.read_text()
    return """
    <html>
        <body>
            <h1>Member QA System API</h1>
            <p>API is running. Use POST /ask to ask questions.</p>
            <p>Documentation: <a href="/docs">/docs</a></p>
        </body>
    </html>
    """


@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "message": "Member QA System API",
        "version": "1.0.0",
        "endpoints": {
            "/ask": "POST - Ask a question about member data",
            "/health": "GET - Health check endpoint",
            "/api": "GET - API information"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a natural language question about member data.
    
    Args:
        request: QuestionRequest containing the question
        
    Returns:
        AnswerResponse with the answer
        
    Example:
        POST /ask
        {
            "question": "When is Layla planning her trip to London?"
        }
        
        Response:
        {
            "answer": "Based on the messages, Layla Kawaguchi mentioned booking a trip to London on March 15, 2025."
        }
    """
    try:
        logger.info(f"Received question: {request.question}")
        answer = await qa_service.answer_question(request.question)
        logger.info(f"Generated answer: {answer}")
        return AnswerResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
