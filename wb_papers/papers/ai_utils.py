import openai 
from django.conf import settings
import PyPDF2

def get_gemini_analysis(combined_text, task_type):
    #  Validate key existence before doing anything else
    api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
    # GUARD: Stop execution if there is no content/less content
    if not combined_text or len(combined_text) < 30:
        return "Not enough data to analyze. Please upload valid PDF."

    # Initialize the OpenRouter client
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key, # Key is  in settings.py and loaded from .env, so it won't be hardcoded here.
    )
    
    prompts = {
        'topics': (
            "You are an academic expert for West Bengal universities. Analyze these papers and identify top recurring topics.\n\n"
            "Output strictly in this format, exactly as shown:\n\n"
            "### Topic Extraction on [subject(subject code)]\n"
            "Topic: [Name]\n"
            "  - Priority: [High/Medium/Low]\n"
            "  - Subtopics: [List of subtopics]\n\n"
            "After listing all topics, conclude with this exact header:\n"
            "### Important Related Topics \n"
            "[List Other Core Important Topics related to this.]"
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
                "STRICT INSTRUCTION: DO NOT OUTPUT DENSE PARAGRAPHS. USE MARKDOWN HEADERS AND BULLET POINTS ONLY.\n"
                
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
            "### 25 high-priority MCQs \n"
            "Q[Number]: [Question Text]\n\n"
            "A) [Option]\n"
            "B) [Option]\n"
            "C) [Option]\n"
            "D) [Option]\n\n"
            "Correct Answer: [Option]\n"
            "Explanation: [Brief reason]\n\n"
            "---" # Visual separator for the AI
        )
    }

    try:
        # We use the Gemini Flash 2.0 model via OpenRouter's gateway
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "user", "content": f"{prompts.get(task_type, 'Analyze:')}\n\n{combined_text[:10000]}"}
            ],
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        # OpenRouter uses similar error codes, so this catch remains useful
        if "429" in error_msg:   # if too many requests send
            return "AI Rate Limit: The server is busy. Please wait 60 seconds."
        return f"AI Error: {error_msg}"

def extract_text_from_pdf(pdf_file):
    """Kept identical so you don't need to change other files."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages[:8]:   # For now only read the first 8 pages of the pdf
            content = page.extract_text()
            if content:
                text += content
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text