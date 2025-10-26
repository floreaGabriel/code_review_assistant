import os
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class CodeReviewAgent:
    """
    AI Agent that provides intelligent code improvement suggestions
    using OpenAI's Chat Completions API.
    """

    def __init__(self):
        """Initialize the AI agent with OpenAI client."""
        # Verify API key is set
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please create a .env file with your OpenAI API key."
            )

        # Create OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # System prompt for the agent
        self.system_prompt = """You are an expert code reviewer specializing in Python best practices.

Your role is to:
1. Analyze code smells and their severity
2. Explain WHY the code smell is problematic
3. Provide SPECIFIC refactoring suggestions with code examples
4. Reference relevant design patterns or principles (SOLID, DRY, etc.)
5. Keep suggestions practical and actionable

When providing suggestions:
- Show concrete code examples (before/after)
- Explain the benefits of the refactoring
- Consider readability, maintainability, and performance
- Be constructive and educational, not critical

Format your response with clear sections:
## Issue Analysis
## Why This Matters
## Suggested Refactoring
## Code Example
## Additional Best Practices
"""

    def generate_suggestion(self, smell: Dict) -> str:
        """
        Generate an AI-powered suggestion for fixing a code smell.

        Args:
            smell: Dictionary containing code smell information

        Returns:
            Detailed suggestion with code examples
        """
        # Create a detailed prompt for the agent
        prompt = self._create_prompt(smell)

        try:
            # Call OpenAI Chat Completions API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cost-effective
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating suggestion: {str(e)}"

    def _create_prompt(self, smell: Dict) -> str:
        """
        Create a detailed prompt for the AI agent.
        """
        smell_type = smell.get('type', 'Unknown')
        smell_name = smell.get('name', 'unknown')
        line = smell.get('line', 0)
        message = smell.get('message', '')
        severity = smell.get('severity', 'unknown')

        prompt = f"""Analyze this code smell and provide refactoring suggestions:

**Code Smell Type:** {smell_type}
**Location:** {smell_name} (line {line})
**Severity:** {severity}
**Details:** {message}

Please provide:
1. A clear explanation of why this is a problem
2. Specific refactoring steps
3. Before/After code examples
4. Best practices to prevent this in the future
"""

        return prompt

    def batch_analyze(self, smells: List[Dict]) -> List[Dict]:
        """
        Generate suggestions for multiple code smells.

        Args:
            smells: List of code smell dictionaries

        Returns:
            List of smells with added 'ai_suggestion' field
        """
        results = []

        for i, smell in enumerate(smells, 1):
            print(f"\n🤖 Generating AI suggestion {i}/{len(smells)}...")

            suggestion = self.generate_suggestion(smell)
            smell_with_suggestion = smell.copy()
            smell_with_suggestion['ai_suggestion'] = suggestion
            results.append(smell_with_suggestion)

        return results
