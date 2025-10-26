from src.ai_agent import CodeReviewAgent

# Sample code smell
smell = {
    'type': 'TooManyParameters',
    'name': 'process_user_data',
    'line': 3,
    'message': 'Function has 9 parameters (recommended: max 5)',
    'severity': 'low'
}

# Create agent and get suggestion
agent = CodeReviewAgent()
suggestion = agent.generate_suggestion(smell)

print("=" * 80)
print("AI-GENERATED SUGGESTION")
print("=" * 80)
print(suggestion)
