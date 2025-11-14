from openai import OpenAI
from typing import List, Dict, Any
from app.config import settings
from app.services.data_service import MemberDataService
import logging

logger = logging.getLogger(__name__)


class QAService:
    """Question-answering service using OpenAI GPT."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.data_service = MemberDataService()
    
    async def answer_question(self, question: str) -> str:
        """
        Answer a natural language question about member data.
        
        Args:
            question: Natural language question about members
            
        Returns:
            Answer string
        """
        # Fetch member messages
        all_messages = await self.data_service.fetch_messages()
        logger.info(f"Total messages fetched: {len(all_messages)}")
        
        # Filter relevant messages based on the question
        relevant_messages = self._filter_relevant_messages(all_messages, question)
        logger.info(f"Relevant messages after filtering: {len(relevant_messages)}")
        
        # Prepare context for the LLM
        context = self._prepare_context(relevant_messages)
        
        # Create prompt
        system_prompt = """You are a helpful assistant that answers questions about member data.
You will be given a dataset of member messages and a question.
Answer the question based ONLY on the information provided in the messages.
If you cannot find the answer in the messages, say "I don't have enough information to answer that question."
Be concise and direct in your answers.
For questions about counts or numbers, provide the specific count.
For questions about dates or times, provide the specific date/time mentioned.
For questions about preferences or favorites, list the specific items mentioned."""

        user_prompt = f"""Member Messages:
{context}

Question: {question}

Answer:"""

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
    
    def _filter_relevant_messages(self, messages: List[Dict[str, Any]], question: str) -> List[Dict[str, Any]]:
        """
        Filter messages that are likely relevant to the question.
        
        Args:
            messages: All messages
            question: The user's question
            
        Returns:
            Filtered list of relevant messages (limited to fit in context)
        """
        question_lower = question.lower()
        
        # Extract keywords from the question (names, places, things)
        stop_words = {'when', 'what', 'where', 'who', 'how', 'many', 'does', 'have', 'the', 'are', 'is', 'planning', 'their', 'favorite', 'her', 'his', 'trip', 'to', 'for', 'in', 'at', 'on', 'a', 'an', 'and', 'or'}
        words = question_lower.split()
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        logger.info(f"Extracted keywords: {keywords}")
        
        # If we have keywords, filter by them
        if keywords:
            relevant = []
            for msg in messages:
                user_name = msg.get("user_name", "").lower()
                message_text = msg.get("message", "").lower()
                
                # Check if any keyword appears in user name or message
                for keyword in keywords:
                    if keyword in user_name or keyword in message_text:
                        relevant.append(msg)
                        break
            
            # If we found relevant messages, return limited set
            if relevant:
                logger.info(f"Found {len(relevant)} messages matching keywords")
                # Limit to 300 messages to stay well under token limit
                return relevant[:300]
        
        # If no keywords or no matches, return first 200 messages
        logger.info("No keyword matches, returning first 200 messages")
        return messages[:200]
    
    def _prepare_context(self, messages: List[Dict[str, Any]], max_messages: int = 1000) -> str:
        """
        Prepare context from messages for the LLM.
        
        Args:
            messages: List of message dictionaries
            max_messages: Maximum number of messages to include
            
        Returns:
            Formatted string context
        """
        # Format messages into a readable context
        context_parts = []
        for msg in messages[:max_messages]:
            user_name = msg.get("user_name", "Unknown")
            message = msg.get("message", "")
            timestamp = msg.get("timestamp", "")
            context_parts.append(f"[{timestamp}] {user_name}: {message}")
        
        return "\n".join(context_parts)
