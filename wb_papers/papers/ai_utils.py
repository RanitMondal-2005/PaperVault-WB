import openai
from django.conf import settings
import PyPDF2  # Library to read, manipulate, and process PDF files

# Prompts defined for our AI according to diff tasks
PROMPTS = {
    'topics': (
        "You are an academic expert for West Bengal universities. Analyze these papers and identify top recurring topics.\n\n"
        "Output strictly in this format, exactly as shown:\n\n"
        "### Topic Extraction on [subject(subject code)]\n"
        "Topic: [Name]\n"
        "  - Priority: [High/Medium/Low]\n"
        "  - Subtopics: [List of subtopics]\n\n"
        "After listing all topics, conclude with this exact header:\n\n"
        "### Important Related Topics\n"
        "[List Other Core Important Topics related to this.]\n\n"
        "### Exam Strategy\n"
        "[Your 2-sentence strategy note]"
    ),

    'summary': (
        "STRICT INSTRUCTION: DO NOT OUTPUT PARAGRAPHS. USE MARKDOWN HEADERS AND BULLET POINTS ONLY. DOUBLE NEWLINE BETWEEN SECTIONS.\n\n"
        "You are a tutor. Summarize these papers as follows:\n\n"
        "### Executive Summary\n- [Brief Summary]\n\n"
        "### Key Concepts Covered\n- [Item 1]\n- [Item 2]\n\n"
        "### Common Probable Questions\n- [Question 1]\n- [Question 2]\n\n"
        "### Suggested Study Resources\n- [Resource 1]"
    ),

    'pdf_upload': (
        "STRICT INSTRUCTION: DO NOT OUTPUT DENSE PARAGRAPHS. USE MARKDOWN HEADERS AND BULLET POINTS ONLY.\n\n"
        "You are a Senior Academic Analyst. Analyze the provided documents:\n\n"
        "### 1. Context Assessment\n"
        "- [One sentence identifying the relationship between the documents]\n\n"
        "### 2. Conceptual Pillars & Weightage\n"
        "- [Identify the 'High-Value' knowledge areas. Focus on topic clusters, module weightage, and difficulty tiers. Do not write questions here; focus solely on the 'What to study' aspect.]\n\n"
        "### 3. Practical Exam Simulation (Practice Set)\n"
        "- [Translate the concepts from Point 2 into a comprehensive list of specific, exam-style questions. Focus on the 'How it is tested' aspect. Provide enough questions to cover the full breadth of the topics.]\n  - Answer Expectation: [Brief explanation of what the answer requires, e.g., 'Diagram', 'Derivation', 'Case Study']\n\n"
        "### 4. Required Answer Complexity\n"
        "- [Brief bulleted summary of the depth, technical vocabulary, and structure required to score high marks.]\n\n"
        "### 5. Future Trend Projection (Next Year's Probable Q)\n"
        "- [Predict evolutionary trends. Identify related, more complex, or peripheral concepts that are logically next in the learning progression. Do not repeat current questions.]"
    ),

    'mock_test': (
        "STRICT INSTRUCTION: FORMAT AS A CLEAN LIST. NO INTRODUCTIONS. NO PARAGRAPHS.\n\n"
        "Create 25 high-priority MCQs. Follow this exact template for every question and use double-spacing:\n\n"
        "### 25 high-priority MCQs \n\n"
        "Q[Number]: [Question Text]\n\n"
        "A) [Option]\n"
        "B) [Option]\n"
        "C) [Option]\n"
        "D) [Option]\n\n"
        "Correct Answer: [Option]\n"
        "Explanation: [Brief reason]\n\n"
        "---"  # Visual separator for the AI
    )
}


def get_gemini_analysis(combined_text, task_type):

    # Guard: Stop execution if text is too short to save API calls
    if not combined_text or len(combined_text.strip()) < 30:
        return "Not enough data to analyze. Please upload valid PDF."

    # Validate key existence before initializing the client
    api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
    if not api_key:
        return "Configuration Error: API_KEY is not set/found in settings.py."

    # Create OpenAI client pointing to OpenRouter Server, so we can send request to OpenRouter Server
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    try:
        # Send the analysis prompt and PDF content to the selected AI model
        completion = client.chat.completions.create(
            model="poolside/laguna-xs-2.1:free",
            messages=[
                {
                    "role": "user",
                    # Combine the selected task prompt with the first 10,000 characters of the PDF text
                    "content": f"{PROMPTS.get(task_type, 'Analyze:')}\n\n{combined_text[:10000]}"
                }
            ],
        )
        # Extract and return the generated text response from the first choice
        return completion.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return "AI Rate Limit: The server is busy. Please wait 60 seconds and Try again later."
        return f"AI Error: {error_msg}"


def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        # Read up to the first 8 pages of the pdf
        for page in reader.pages[:8]:
            content = page.extract_text()
            if content:
                text += content

    except Exception as e:
        print(f"Error reading PDF: {e}")

    return text
