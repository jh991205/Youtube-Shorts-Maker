import openai
import os

def check_openai_token(token):
    openai.api_key = token
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "This is a test message to check the API token."},
                {"role": "user", "content": "Can you confirm if this API token is working?"}
            ],
            max_tokens=5
        )
        
        if response:
            print(response)
            return True
    except openai.error.AuthenticationError:
        print("The OpenAI token is invalid.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

token = os.getenv('OPENAI_API')
check_openai_token(token)
