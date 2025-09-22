# PsychPal: Your AI Companion for Mental Wellness

Mental health support systems play a critical role in providing accessible initial assistance to individuals seeking psychological help. This assignment tasks you with building a local LLM-based CUI for psychological pre-consultation. The system should provide empathetic listening, assess user needs, and appropriately refer users to professional resources when necessary.

PsychPal is a psychological pre-consultation support system designed to provide initial emotional support and guidance. It aims to offer a safe space for users to explore their feelings and concerns, while clearly communicating its limitations as an AI.

**Important**: This system is for educational purposes only and should NOT provide diagnoses or treatment recommendations.

## Repository Structure

```text
25s1-cs3249-assignment1/
├── README.md
├── Assignment 1.pdf
├── POLICY.md
├── INSTALL.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── model_provider.py
│   ├── moderation.py
│   ├── chat_engine.py
│   └── io_utils.py
├── scripts/
│   └── evaluate.py
├── tests/
│   ├── inputs.jsonl
│   └── expected_schema.json
├── app/
│   ├── __init__.py
│   ├── backend.py
│   └── frontend.py
├── .gitignore
└── LICENSE
```

## Installation Instructions

To set up and run PsychPal, we recommend using [Nix](https://nixos.org/download.html) for a reproducible development environment.

1.  **Install Nix:** Follow the official installation guide for your operating system: [Nix Installation Guide](https://nixos.org/download.html)

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YZTangent/cs3249-assignment1.git # Replace with your actual repo URL
    cd cs3249
    ```

## Running Instructions

After completing the installation steps, you can start the PsychPal application with a single command:
```bash
nix run
```
This command will:
1.  Start the Ollama server in the background (if not already running).
2.  Pull the LLM `phi3:mini`
3.  Start the FastAPI backend server (`app/backend.py`).
4.  Launch the Streamlit frontend application (`app/frontend.py`) in your web browser.

## Development Instructions
**Enter the Development Environment & Install Python Dependencies:**
```bash
nix develop
# This command will set up the environment and install all Python dependencies from requirements.txt
```

## Framework Choice Justification

This project leverages a combination of modern Python frameworks to deliver a robust and user-friendly experience:

*   **FastAPI (for Backend):**
    *   **High Performance:** FastAPI is known for its excellent performance, making it suitable for handling API requests efficiently.
    *   **Ease of Use & Development Speed:** Its modern Python type hints and automatic data validation significantly speed up API development.
    *   **Automatic Documentation:** FastAPI automatically generates interactive API documentation (OpenAPI/Swagger UI), which is invaluable for understanding and interacting with the backend.
    *   **Asynchronous Support:** Built on Starlette, it natively supports asynchronous programming, allowing for efficient handling of concurrent requests, crucial for a responsive chat application.

*   **Streamlit (for Frontend):**
    *   **Rapid Prototyping:** Streamlit enables the creation of beautiful, interactive web applications purely in Python with minimal code, accelerating the development of the user interface.
    *   **Simplicity:** Its component-based approach and intuitive API make it easy to build complex UIs without needing extensive web development knowledge (HTML, CSS, JavaScript).
    *   **Interactive Data Apps:** While PsychPal is a chat application, Streamlit's strength in interactive data applications translates well to creating a dynamic and responsive chat interface.

*   **Ollama (for Local LLM Serving):**
    *   **Privacy & Data Control:** Running the Large Language Model (LLM) locally via Ollama ensures that user data remains on the user's machine, addressing privacy concerns inherent in mental wellness applications.
    *   **Cost-Effective Development:** Eliminates the need for expensive API calls to cloud-based LLMs during development and testing.
    *   **Offline Capability:** The application can function without an internet connection once the model is downloaded, providing uninterrupted support.

## Additional Dependencies

Beyond the standard Python libraries, the project relies on the following packages, all listed in `requirements.txt`:

*   `fastapi`: The web framework for the backend API.
*   `uvicorn`: An ASGI server to run the FastAPI application.
*   `streamlit`: The framework for building the interactive web frontend.
*   `ollama`: The Python client for interacting with the local Ollama LLM server.
*   `requests`: For making HTTP requests from the frontend to the backend.
*   `pydantic`: For data validation and settings management (used by FastAPI).
*   `jsonschema`: For validating JSON data against schemas.
*   `python-dateutil`: Provides extensions to the standard `datetime` module.
*   `typing-extensions`: Backports and experimental types for Python's `typing` module.
*   `colorama`: For cross-platform colored terminal output.
*   `tqdm`: For displaying progress bars.

## UI Design Decisions

The UI design of PsychPal prioritizes safety, accessibility, user trust, and clear communication of system boundaries, especially given its sensitive domain.

### Safety-First Principles

*   **Prominent Disclaimer:** Upon first interaction, a clear and comprehensive disclaimer is presented, outlining the AI's capabilities and, more importantly, its limitations. This sets realistic expectations from the outset.
*   **Crisis Intervention:** If the user expresses thoughts of self-harm or other critical issues, the conversation is immediately blocked. A highly visible, full-width, red "Get Help" button appears, linking directly to the Samaritans of Singapore hotline. This ensures immediate access to professional help and prevents the AI from inadvertently providing harmful advice.
*   **Clear Blocking Mechanism:** When a conversation is blocked, a distinct error message is displayed, making it unambiguous why further interaction with the AI is halted.

### Accessibility Requirements

*   **Standard Streamlit Widgets:** The UI primarily uses Streamlit's built-in widgets, which are generally designed with accessibility in mind, supporting keyboard navigation and screen readers.
*   **High Contrast:** The default Streamlit theme provides good contrast for text and UI elements, ensuring readability for users with various visual needs.
*   **Responsive Layout:** The layout is designed to be responsive, adapting well to different screen sizes, from desktop to mobile, enhancing usability across devices.
*   **Full-Width Buttons:** Critical action buttons like "Clear Conversation" and "Get Help" utilize `use_container_width=True` to make them larger and easier to click, benefiting users with motor impairments or those using touch interfaces.

### User Trust and Comfort

*   **Friendly Introduction:** The bot's self-introduction uses a warm and personal tone ("Hello there! I'm PsychPal, your friendly AI companion"), aiming to build rapport and make the user feel comfortable.
*   **Transparency:** The disclaimer clearly states that PsychPal is an AI and not a human, fostering transparency and preventing misinterpretation of its role.
*   **Clear Conversation Reset:** A prominent "Clear Conversation" button is available in the sidebar, allowing users to easily reset the chat history. This provides a sense of control over their data and privacy, contributing to comfort and trust.
*   **Helpful Resources:** The sidebar prominently features links to reputable Singapore-based mental health helplines and resources, reinforcing that professional help is available and encouraging users to seek it when appropriate.

### Clear Communication of System Boundaries

*   **Explicit Limitations:** The disclaimer explicitly states what PsychPal *cannot* do: diagnose conditions, prescribe medication, provide treatment, or offer confidential therapy. This manages user expectations and prevents reliance on the AI for professional medical or psychological advice.
*   **Role Definition:** PsychPal is consistently presented as a "psychological pre-consultation support system" and an "AI companion," clearly defining its supportive, non-professional role.
*   **Crisis Redirection:** The immediate redirection to crisis hotlines for severe concerns reinforces that the AI is not a crisis service and that human intervention is necessary for such situations.
*   **No Confidentiality Claim:** The disclaimer clarifies that conversations are not confidential in the same way as with a doctor or therapist, setting a crucial boundary regarding privacy expectations.
