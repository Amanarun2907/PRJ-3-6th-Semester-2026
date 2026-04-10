system_context = "test"
user_input = "test"

enhanced_prompt = f"""{system_context}

User Question: {user_input}

Provide a helpful, detailed response with:
- Clear recommendations
- Specific examples where relevant
- Risk considerations
- Actionable next steps

Keep response under 300 words."""

print(enhanced_prompt)
