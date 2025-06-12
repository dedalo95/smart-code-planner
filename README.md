# Smart Code Planner 🤖

A sophisticated code organization agent built with LangGraph that helps developers break down complex tasks into manageable subtasks and provides intelligent code organization advice.

## ✨ Features

- **🧠 Intelligent Task Decomposition**: Uses LangGraph workflows to recursively break down complex tasks
- **🤖 Multi-LLM Support**: Supports both OpenAI (GPT) and Google (Gemini) models
  - OpenAI: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`
  - Google: `gemini-2.0-flash-lite`, `gemini-2.0-flash`, `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-pro`
- **📊 Visual Workflow**: Terminal graph visualization showing LangGraph structure on startup
- **🎯 Recursive Analysis**: Automatically identifies when subtasks need further breakdown
- **🏗️ Code Organization Advice**: Provides expert recommendations for project structure
- **🌐 Modern Web UI**: Clean Streamlit interface with model selection and configuration
- **🐳 Docker Support**: Fully containerized for easy deployment
- **🧪 Comprehensive Testing**: Unit tests, integration tests, and validation scripts
- **📖 Rich Documentation**: Detailed setup guides and examples

## 🏗️ Architecture

The project follows a clean architecture pattern:

```
smart-code-planner/
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── graph.py          # LangGraph workflow definition
│   │   ├── nodes.py          # Graph node implementations
│   │   └── state.py          # State management
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py         # Pydantic models
│   │   └── config.py         # Configuration management
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_analyzer.py  # Task analysis logic
│   │   └── code_advisor.py   # Code organization advisor
│   └── ui/
│       ├── __init__.py
│       └── streamlit_app.py  # Streamlit interface
├── prompts/
│   ├── task_decomposition.txt
│   ├── subtask_analysis.txt
│   └── code_organization.txt
├── tests/
├── Dockerfile              # Docker configuration
├── pyproject.toml
├── README.md
└── docker-compose.yml      # Optional Docker Compose setup
```

## 🚀 Quick Start

### Using Poetry (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd smart-code-planner
   poetry install
   ```

2. **Set environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the application**:
   ```bash
   poetry run streamlit run src/ui/streamlit_app.py
   ```

### Using Docker

1. **Build the Docker image**:
   ```bash
   docker build -t smart-code-planner .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8501:8501 smart-code-planner
   ```

3. **Access the application**:
   Open http://localhost:8501 in your browser

**Alternative with Docker Compose (if available)**:
```bash
docker-compose up --build
```

**Useful Docker commands**:
```bash
# Run in background
docker run -d -p 8501:8501 --name smart-code-planner-app smart-code-planner

# View logs
docker logs smart-code-planner-app

# Stop container
docker stop smart-code-planner-app

# Remove container
docker rm smart-code-planner-app
```

## 🔧 Configuration

Create a `.env` file with your API keys:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google API Configuration (for Gemini models)
GOOGLE_API_KEY=your_google_api_key_here

# LangChain Configuration (Optional)
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=smart-code-planner

# Model Configuration
MODEL_NAME=gpt-4o
MODEL_PROVIDER=openai
TEMPERATURE=0.3
MAX_TOKENS=2000
```

### Supported Models

**OpenAI Models:**
- `gpt-4o` (recommended)
- `gpt-4o-mini`
- `gpt-4-turbo`
- `gpt-4`
- `gpt-3.5-turbo`

**Google Gemini Models:**
- `gemini-2.0-flash-lite` (fast and efficient)
- `gemini-2.0-flash` (recommended)
- `gemini-1.5-pro`
- `gemini-1.5-flash`
- `gemini-pro`

## 📖 Usage

1. **Launch the Streamlit interface** - The app will display the LangGraph workflow visualization in the terminal
2. **Select your preferred AI model** from the sidebar (OpenAI or Google Gemini)
3. **Configure analysis parameters** (depth, temperature, etc.)
4. **Enter your coding task** in the text area or choose from examples
5. **Click "Analyze Task"** to start the decomposition process
6. **Review the comprehensive results**:
   - Task breakdown with complexity analysis
   - Recursive subtask decomposition
   - Code organization recommendations
   - Implementation roadmap
7. **Export results** to JSON or Markdown for further use

## 🧪 Testing

Run the test suite:

```bash
poetry run pytest
```

Run with coverage:

```bash
poetry run pytest --cov=src tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for the graph-based workflow engine
- [Streamlit](https://streamlit.io/) for the beautiful web interface
- [Poetry](https://python-poetry.org/) for dependency management

---

**Built with ❤️ by Federico Antosiano**
