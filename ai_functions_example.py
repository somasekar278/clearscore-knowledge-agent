"""
Example: Integrating Databricks AI Functions into ClearScore Chatbot

This demonstrates how to use Databricks AI functions like:
- ai_summarize() - Summarize conversations
- ai_classify() - Classify customer sentiment
- ai_extract() - Extract structured information
- ai_query() - Query knowledge bases

These functions can be called via the Databricks SQL Execution API.
"""

from databricks import sql
import os


class DatabricksAIFunctions:
    """Wrapper for Databricks AI Functions using SQL Execution API"""
    
    def __init__(self):
        """Initialize connection parameters from environment"""
        self.server_hostname = os.getenv('DATABRICKS_SERVER_HOSTNAME', 
                                         'e2-demo-field-eng.cloud.databricks.com')
        self.http_path = os.getenv('DATABRICKS_HTTP_PATH', 
                                   '/sql/1.0/warehouses/xxxxx')  # Update with your SQL warehouse
        self.access_token = os.getenv('DATABRICKS_TOKEN')
        
    def _get_connection(self):
        """Create a SQL connection to Databricks"""
        return sql.connect(
            server_hostname=self.server_hostname,
            http_path=self.http_path,
            access_token=self.access_token
        )
    
    def summarize_conversation(self, chat_history: list, max_length: int = 150) -> str:
        """
        Summarize a conversation using ai_summarize()
        
        Args:
            chat_history: List of message dicts with 'role' and 'content'
            max_length: Maximum length of summary
            
        Returns:
            Summary string
        """
        # Combine all messages into one text
        full_conversation = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in chat_history
        ])
        
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT ai_summarize(
                        '{full_conversation}',
                        'max_length' => {max_length}
                    )
                """)
                result = cursor.fetchone()
                return result[0] if result else "Unable to summarize"
    
    def classify_sentiment(self, message: str) -> str:
        """
        Classify customer sentiment using ai_classify()
        
        Args:
            message: Customer message text
            
        Returns:
            Sentiment: 'positive', 'neutral', or 'negative'
        """
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT ai_classify(
                        '{message}',
                        ARRAY('positive', 'neutral', 'negative')
                    )
                """)
                result = cursor.fetchone()
                return result[0] if result else "neutral"
    
    def classify_intent(self, message: str) -> str:
        """
        Classify customer intent using ai_classify()
        
        Args:
            message: Customer message text
            
        Returns:
            Intent category
        """
        intents = [
            'check_credit_score',
            'improve_credit_score',
            'score_change_inquiry',
            'update_personal_details',
            'product_inquiry',
            'account_closure',
            'dispute_error',
            'general_inquiry'
        ]
        
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                intents_str = ", ".join([f"'{intent}'" for intent in intents])
                cursor.execute(f"""
                    SELECT ai_classify(
                        '{message}',
                        ARRAY({intents_str})
                    )
                """)
                result = cursor.fetchone()
                return result[0] if result else "general_inquiry"
    
    def extract_customer_info(self, message: str) -> dict:
        """
        Extract structured information from customer message using ai_extract()
        
        Args:
            message: Customer message text
            
        Returns:
            Dict with extracted information
        """
        schema = {
            "customer_name": "string",
            "email": "string",
            "phone": "string",
            "account_number": "string"
        }
        
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT ai_extract(
                        '{message}',
                        '{schema}'
                    )
                """)
                result = cursor.fetchone()
                return result[0] if result else {}
    
    def query_knowledge_base(self, question: str, context: str) -> str:
        """
        Query knowledge base using ai_query()
        
        Args:
            question: Customer's question
            context: Knowledge base context or documentation
            
        Returns:
            Answer from knowledge base
        """
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT ai_query(
                        '{question}',
                        '{context}'
                    )
                """)
                result = cursor.fetchone()
                return result[0] if result else "No answer found"
    
    def detect_language(self, message: str) -> str:
        """
        Detect language of customer message
        
        Args:
            message: Customer message text
            
        Returns:
            Language code (e.g., 'en', 'es', 'fr')
        """
        languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'pl', 'zh', 'ja']
        
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                langs_str = ", ".join([f"'{lang}'" for lang in languages])
                cursor.execute(f"""
                    SELECT ai_classify(
                        '{message}',
                        ARRAY({langs_str})
                    )
                """)
                result = cursor.fetchone()
                return result[0] if result else 'en'


# Example usage in your chatbot
def enhance_chatbot_with_ai_functions():
    """
    Example of how to integrate AI functions into the chatbot
    
    Add these features to ClearScoreChatbot.py:
    """
    
    ai_functions = DatabricksAIFunctions()
    
    # 1. Classify intent when user sends a message
    def on_user_message(message):
        intent = ai_functions.classify_intent(message)
        sentiment = ai_functions.classify_sentiment(message)
        
        print(f"Intent: {intent}")
        print(f"Sentiment: {sentiment}")
        
        # Route to specialized handlers based on intent
        if intent == 'check_credit_score':
            return handle_credit_score_check()
        elif intent == 'account_closure':
            return handle_account_closure()
        # ... etc
    
    # 2. Summarize conversation when user clicks "Clear Chat"
    def on_clear_chat(chat_history):
        if len(chat_history) > 3:
            summary = ai_functions.summarize_conversation(chat_history)
            # Save summary to database
            save_conversation_summary(summary)
    
    # 3. Extract customer information automatically
    def on_extract_info(message):
        info = ai_functions.extract_customer_info(message)
        if info.get('email'):
            # Auto-fill customer profile
            update_customer_profile(info)
    
    # 4. Multi-language support
    def on_detect_language(message):
        language = ai_functions.detect_language(message)
        if language != 'en':
            # Translate or route to language-specific agent
            handle_non_english(message, language)


# Integration Example: Enhanced Chatbot Component
class EnhancedClearScoreChatbot:
    """
    Example of ClearScoreChatbot enhanced with AI functions
    
    To use this, update ClearScoreChatbot.py with these additions:
    """
    
    def __init__(self, app, endpoint_name, height='700px'):
        # ... existing initialization ...
        self.ai_functions = DatabricksAIFunctions()
        self.conversation_analytics = []
    
    def process_user_message(self, message):
        """Enhanced message processing with AI functions"""
        
        # 1. Classify sentiment and intent
        sentiment = self.ai_functions.classify_sentiment(message)
        intent = self.ai_functions.classify_intent(message)
        
        # 2. Track analytics
        self.conversation_analytics.append({
            'message': message,
            'sentiment': sentiment,
            'intent': intent,
            'timestamp': datetime.now()
        })
        
        # 3. Show intent indicator to customer service rep
        # (if this is being monitored)
        print(f"📊 Analytics: Intent={intent}, Sentiment={sentiment}")
        
        # 4. If negative sentiment, escalate or add empathy
        if sentiment == 'negative':
            return self.handle_negative_sentiment(message)
        
        # 5. Call the agent endpoint normally
        return self.call_agent_endpoint(message)
    
    def summarize_conversation_history(self, chat_history):
        """Summarize long conversations"""
        if len(chat_history) > 10:
            summary = self.ai_functions.summarize_conversation(
                chat_history, 
                max_length=200
            )
            return summary
        return None
    
    def generate_analytics_dashboard(self):
        """Generate insights from conversation analytics"""
        if not self.conversation_analytics:
            return None
        
        # Calculate metrics
        sentiments = [a['sentiment'] for a in self.conversation_analytics]
        intents = [a['intent'] for a in self.conversation_analytics]
        
        return {
            'total_messages': len(self.conversation_analytics),
            'positive_sentiment': sentiments.count('positive'),
            'neutral_sentiment': sentiments.count('neutral'),
            'negative_sentiment': sentiments.count('negative'),
            'top_intent': max(set(intents), key=intents.count),
            'all_intents': list(set(intents))
        }


# Configuration example for app.yaml
"""
To enable AI functions, update your app.yaml:

command: ["python", "app.py"]

env:
  - name: "SERVING_ENDPOINT"
    value: "mas-691e9159-endpoint"
  
  # Add SQL warehouse connection for AI functions
  - name: "DATABRICKS_SERVER_HOSTNAME"
    value: "e2-demo-field-eng.cloud.databricks.com"
  
  - name: "DATABRICKS_HTTP_PATH"
    value: "/sql/1.0/warehouses/YOUR_WAREHOUSE_ID"
  
  - name: "DATABRICKS_TOKEN"
    valueFrom:
      secretKeyRef:
        scope: customer-service
        key: sql-token

resources:
  # Bind to SQL warehouse for AI functions
  sql-warehouses:
    - name: sql-warehouse
      warehouse_id: YOUR_WAREHOUSE_ID
      permission: CAN_USE
"""


if __name__ == '__main__':
    # Test AI functions
    print("Testing Databricks AI Functions...")
    
    ai = DatabricksAIFunctions()
    
    # Test message
    test_message = "I'm really frustrated that my credit score dropped by 50 points!"
    
    try:
        sentiment = ai.classify_sentiment(test_message)
        print(f"✅ Sentiment: {sentiment}")
        
        intent = ai.classify_intent(test_message)
        print(f"✅ Intent: {intent}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure to set DATABRICKS_TOKEN and DATABRICKS_HTTP_PATH environment variables")

