import openai 
from django.conf import settings
import PyPDF2 # Library to extract text from PDF files

def get_gemini_analysis(combined_text, task_type): # combined_text is the text extracted from the PDF and task_type is the type of analysis requested, both parameters coming from the user input via papers/views.py
    #  Validate key existence before doing anything else
    api_key = getattr(settings, 'OPENROUTER_API_KEY', None) # Get API key from settings.py ; getattr()  safely retrieves the API key from settings, providing a default value of None if not found.
    # Use of getattr() -> used to dynamically access model fields, settings, or properties using their string names
    # GUARD: Stop execution if there is no content/less content to save API costs and prevent empty payloads
    if not combined_text or len(combined_text) < 30:
        return "Not enough data to analyze. Please upload valid PDF."

    # Create a new instance of the OpenAI client redirected to point at OpenRouter's servers
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1", # Base URL for the OpenRouter API
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
        # We use the Free AI model via OpenRouter's gateway
        completion = client.chat.completions.create( # send request to OpenRouter API through OpenAI client. This line Fires the request to the API, navigating: Connection -> Chat Dept -> Text Tool -> Execute
            # this above line :navigates down the chain from the client connection, to the chat department, to the completions tool, and uses .create() to package and send our prompt payload over the network.
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "user", "content": f"{prompts.get(task_type, 'Analyze:')}\n\n{combined_text[:10000]}"} # # Combines the matching task prompt with the first 10,000 text characters of the PDF because AI can only process a limited amount of text at once.
            ],
        )
        return completion.choices[0].message.content # Returns the AI's response content by accessing the first choice's message given by the AI. It basically extracts and pass the generated Markdown text response back to the calling view.

    except Exception as e:
        error_msg = str(e)
        # OpenRouter uses similar error codes, so this catch remains useful
        if "429" in error_msg:   # if too many requests send, so RATE LIMIT EXCEPTION handled cleanly.
            return "AI Rate Limit: The server is busy. Please wait 60 seconds."
        return f"AI Error: {error_msg}"

def extract_text_from_pdf(pdf_file): # This pdf_file is the uploaded PDF file coming from the user via papers/views.py 
    """Kept identical so you don't need to change other files."""
    text = "" # Initialize text variable to store extracted content
    try:
        reader = PyPDF2.PdfReader(pdf_file) # Create a PDF reader object which will read the PDF file
        # Then, Loop through pages, restricting processing exclusively to the first 8 pages
        for page in reader.pages[:8]:   # For now only read the first 8 pages of the pdf
            content = page.extract_text() # Extract text from the page, .extract_text() is an inbuilt method provided by PyPDF2 that processes the page's content and returns it as a plain string and returns None for empty pages.
            # this extracted text from a page is put to content variable; since we will read only the first 8 pages,so basic structure : read pg one by one and extract that page's content and store it.
            if content: # If content is not None or empty
                text += content # Append the extracted content to the text variable
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text # Return the final extracted text
