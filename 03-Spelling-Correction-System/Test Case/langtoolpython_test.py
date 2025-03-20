import language_tool_python

# Initialize LanguageToolPublicAPI with English
lt_tool = language_tool_python.LanguageToolPublicAPI('en-US')

# Test case input
text = """
The central bank decided to lower intrest rates to stimulate borrowing and investment. Analysts say that banking regulations require better risk mangment to ensure stability. New policies are affecting loan approvals and impacting mortgage rates. Meanwhile, the government allocated additional funds to the capital for infrastructure projects.
"""

# Function to detect spelling & grammar errors using LanguageToolPublicAPI
def detect_errors(text, top_n=3):
    matches = lt_tool.check(text)
    detected_errors = {}

    for match in matches:
        # Extract the incorrect word using match.offset and match.errorLength
        error_word = text[match.offset : match.offset + match.errorLength].strip()

        # **Filter by relevant LanguageTool rule categories**
        is_spelling_error = match.ruleId.startswith("MORFOLOGIK_RULE")
        is_confused_word = "CONFUSED_WORDS" in match.ruleId.upper()

        # Store errors only if they have valid replacement suggestions
        if error_word and match.replacements:
            if is_spelling_error or is_confused_word:
                detected_errors[error_word] = match.replacements[:top_n]  # Store top N suggestions

    return detected_errors

# Run error detection
errors = detect_errors(text)

# Print results
print("\n**Detected Errors**:")
for word, suggestions in errors.items():
    print(f"**{word}** Suggestions: {suggestions}")
