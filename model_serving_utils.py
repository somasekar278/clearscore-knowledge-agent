"""
Utilities for interacting with Databricks Model Serving endpoints
"""
from mlflow.deployments import get_deploy_client
from databricks.sdk import WorkspaceClient

def _get_endpoint_task_type(endpoint_name: str) -> str:
    """Get the task type of a serving endpoint."""
    try:
        w = WorkspaceClient()
        ep = w.serving_endpoints.get(endpoint_name)
        task = ep.task if hasattr(ep, 'task') and ep.task else "unknown"
        print(f"📋 Endpoint '{endpoint_name}' task type: {task}")
        return task
    except Exception as e:
        print(f"⚠️  Warning: Could not get endpoint task type: {e}")
        # Return a default that will pass validation - assume it's an agent endpoint
        return "agent/v1/chat"

def is_endpoint_supported(endpoint_name: str) -> bool:
    """Check if the endpoint has a supported task type."""
    task_type = _get_endpoint_task_type(endpoint_name)
    supported_task_types = [
        "agent/v1/chat", 
        "agent/v2/chat", 
        "llm/v1/chat", 
        "chat",
        "unknown"  # Allow unknown types - let the endpoint call fail gracefully if it doesn't work
    ]
    is_supported = task_type in supported_task_types
    
    if not is_supported:
        print(f"⚠️  Task type '{task_type}' not in supported list: {supported_task_types}")
    
    return is_supported

def _validate_endpoint_task_type(endpoint_name: str) -> None:
    """Validate that the endpoint has a supported task type."""
    if not is_endpoint_supported(endpoint_name):
        raise Exception(
            f"Detected unsupported endpoint type for this chatbot template. "
            f"This chatbot template only supports chat completions-compatible endpoints. "
            f"For more information, see https://docs.databricks.com/en/generative-ai/agent-framework/chat-app"
        )

def _query_endpoint(endpoint_name: str, messages: list[dict[str, str]], max_tokens: int) -> list[dict[str, str]]:
    """
    Calls a Databricks model serving endpoint.
    
    Args:
        endpoint_name: Name of the serving endpoint
        messages: List of chat messages with 'role' and 'content' keys
        max_tokens: Maximum tokens to generate
        
    Returns:
        List of message dictionaries with the assistant response
    """
    print(f"📤 Querying endpoint: {endpoint_name}")
    print(f"   Messages: {len(messages)} message(s)")
    print(f"   Max tokens: {max_tokens}")
    
    try:
        # Use MLflow deployment client to call the endpoint
        client = get_deploy_client('databricks')
        
        # Format the input for Databricks Agent API (responses.create format)
        # This matches: client.responses.create(model="...", input=[...])
        input_messages = [{'role': msg['role'], 'content': msg['content']} for msg in messages]
        
        print(f"   Using Databricks Agent API format (input=)")
        
        try:
            # Primary format: input= (for agent endpoints like ka-6859840b-endpoint)
            # Note: Some agent endpoints may not support max_tokens parameter
            res = client.predict(
                endpoint=endpoint_name,
                inputs={'input': input_messages, 'max_tokens': max_tokens},
            )
            print(f"   ✅ Success with 'input' format (with max_tokens={max_tokens})")
        except Exception as e1:
            print(f"   Format 1 (input=) failed: {str(e1)[:100]}")
            try:
                # Fallback format: messages= (for standard chat endpoints)
                res = client.predict(
                    endpoint=endpoint_name,
                    inputs={'messages': messages, "max_tokens": max_tokens},
                )
                print(f"   ✅ Success with 'messages' format")
            except Exception as e2:
                print(f"   Format 2 (messages=) failed: {str(e2)[:100]}")
                # Last try: just the messages array
                res = client.predict(
                    endpoint=endpoint_name,
                    inputs=messages,
                )
                print(f"   ✅ Success with direct messages array")
        
        print(f"📥 Response received: {type(res)}")
        print(f"   Response keys: {res.keys() if isinstance(res, dict) else 'not a dict'}")
        
        # Handle different response formats
        
        # Format 1: Direct messages array
        if "messages" in res:
            print("   Response format: messages array")
            return res["messages"]
        
        # Format 2: OpenAI-compatible format with choices
        elif "choices" in res:
            print("   Response format: choices array")
            choice_message = res["choices"][0]["message"]
            choice_content = choice_message.get("content")
            
            # Case 2a: Content is a list of structured objects
            if isinstance(choice_content, list):
                print("   Content type: structured list")
                combined_content = "".join([
                    part.get("text", "") 
                    for part in choice_content 
                    if part.get("type") == "text"
                ])
                reformatted_message = {
                    "role": choice_message.get("role"),
                    "content": combined_content
                }
                return [reformatted_message]
            
            # Case 2b: Content is a simple string
            elif isinstance(choice_content, str):
                print("   Content type: string")
                return [choice_message]
        
        # Format 3: Databricks agent format with output
        # This matches: response.output[0].content[0].text
        elif "output" in res:
            print("   Response format: Databricks agent output")
            output = res["output"]
            
            if isinstance(output, list) and len(output) > 0:
                # Extract content from output array
                first_output = output[0]
                print(f"   First output type: {type(first_output)}")
                
                if isinstance(first_output, dict):
                    # Check for content array (response.output[0].content[].text)
                    # IMPORTANT: content is a LIST of chunks, each with its own text!
                    if "content" in first_output and isinstance(first_output["content"], list):
                        content_list = first_output["content"]
                        print(f"   Content list length: {len(content_list)} chunks")
                        
                        # Concatenate ALL text chunks from all content items
                        all_text_chunks = []
                        for i, content_item in enumerate(content_list):
                            if isinstance(content_item, dict) and "text" in content_item:
                                chunk_text = content_item["text"]
                                all_text_chunks.append(chunk_text.strip())  # Strip whitespace
                                print(f"   Chunk {i}: {len(chunk_text)} chars")
                            elif isinstance(content_item, str):
                                all_text_chunks.append(content_item.strip())
                        
                        # Combine all chunks with blank lines between them for readability
                        full_text = "\n\n".join(all_text_chunks)
                        print(f"   ✅ Total extracted text length: {len(full_text)} chars")
                        
                        return [{
                            "role": "assistant",
                            "content": full_text
                        }]
                    # Check for direct content string
                    elif "content" in first_output and isinstance(first_output["content"], str):
                        return [{
                            "role": "assistant",
                            "content": first_output["content"]
                        }]
                    # Check if output itself has text field
                    elif "text" in first_output:
                        return [{
                            "role": "assistant",
                            "content": first_output["text"]
                        }]
        
        # Format 4: Direct text response (some simple endpoints)
        elif "text" in res:
            print("   Response format: direct text")
            return [{
                "role": "assistant",
                "content": res["text"]
            }]
        
        # Format 5: Direct content field
        elif "content" in res:
            print("   Response format: direct content")
            return [{
                "role": "assistant",
                "content": res["content"]
            }]
        
        # If we get here, log the response and try to extract any text
        print(f"⚠️  Unrecognized response format. Full response: {res}")
        
        # Last resort: try to find any text-like content
        if isinstance(res, dict):
            # Check if there's a predictions field
            if "predictions" in res:
                pred = res["predictions"]
                if isinstance(pred, list) and len(pred) > 0:
                    return [{
                        "role": "assistant",
                        "content": str(pred[0])
                    }]
            
            # Try to convert the whole response to string
            return [{
                "role": "assistant",
                "content": f"Response received (unexpected format): {str(res)[:500]}"
            }]
        
        raise Exception(
            f"Unable to parse response from endpoint. Response type: {type(res)}. "
            "Please check the endpoint output format."
        )
        
    except Exception as e:
        print(f"❌ Error querying endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

def query_endpoint(endpoint_name: str, messages: list[dict[str, str]], max_tokens: int = 2048) -> dict[str, str]:
    """
    Query a Databricks serving endpoint and return the last message.
    
    Args:
        endpoint_name: Name of the serving endpoint
        messages: List of chat messages
        max_tokens: Maximum tokens to generate (default: 512)
        
    Returns:
        The last message dictionary from the response
    """
    response_messages = _query_endpoint(endpoint_name, messages, max_tokens)
    return response_messages[-1]

