# 🚀 How to Run Locally - Complete Guide

## ✅ **Current Status: WORKING WITH MULTI-LLM SUPPORT!**

The Smart Code Planner now supports both OpenAI and Google Gemini models, with beautiful terminal visualization. Here are all the ways to run it locally:

## 🎯 **Quick Start (Recommended)**

```bash
# 1. Make sure you're in the project directory
cd /Users/username/Desktop/smart-code-planner

# 2. Run the application
make run

# 3. Open your browser and go to:
# http://localhost:8501
```

## 📋 **All Available Methods**

### **Method 1: Using Make (Recommended)**

```bash
make run        # Run the application
make dev        # Run with auto-reload for development
make help       # See all available commands
```

### **Method 2: Using the Run Script**

```bash
./run.sh        # Simple shell script launcher
```

### **Method 3: Direct Poetry Command**

```bash
poetry run streamlit run app.py
```

### **Method 4: Using Docker**

```bash
# Option A: Docker Compose
docker-compose up --build

# Option B: Manual Docker
docker build -f docker/Dockerfile -t smart-code-planner .
docker run -p 8501:8501 --env-file .env smart-code-planner
```

### **Method 5: Development Mode**

```bash
make dev        # Runs with auto-reload when files change
```

## ⚙️ **Configuration**

Your configuration supports multiple LLM providers:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-... (✅ Configured)

# Google Gemini Configuration (Optional)
GOOGLE_API_KEY=AIxxx

# Model Settings
MODEL_NAME=gpt-4o
MODEL_PROVIDER=openai  # openai or google
TEMPERATURE=0.3
MAX_TOKENS=2000
MAX_ANALYSIS_DEPTH=3
STREAMLIT_PORT=8501
```

### **🤖 Supported Models**

**OpenAI Models:**

- `gpt-4o` (recommended)
- `gpt-4o-mini`
- `gpt-4-turbo`
- `gpt-4`
- `gpt-3.5-turbo`

**Google Gemini Models:**

- `gemini-2.0-flash-lite` (fast)
- `gemini-2.0-flash` (recommended)
- `gemini-1.5-pro`
- `gemini-1.5-flash`
- `gemini-pro`

## 🌐 **Access URLs**

- **Local:** http://localhost:8501
- **Network:** http://192.168.1.101:8501 (accessible from other devices on your network)

## 🎨 **Using the Application**

### **🚀 On Startup**

When you run `streamlit run app.py`, you'll see a beautiful LangGraph workflow visualization in your terminal!

### **🌐 In the Web Interface**

1. **Select your AI provider** (OpenAI or Google) in the sidebar
2. **Choose your preferred model** from the dropdown
3. **Configure analysis parameters** (depth, temperature)
4. **Enter a coding task** in the text area
5. **Choose from example tasks** or write your own
6. **Click "Analyze Task"** to start the AI analysis
7. **Review results** in the tabs:
   - 📋 Task Breakdown
   - 🏗️ Code Organization
   - 💡 Recommendations
   - 📁 Export (JSON/Markdown)

## 🧪 **Example Tasks to Try**

### **Web Application**

```
Build a full-stack web application for task management with user authentication, real-time updates, and mobile responsiveness
```

### **API Service**

```
Create a RESTful API service for an e-commerce platform with inventory management, order processing, and payment integration
```

### **Data Pipeline**

```
Design and implement a data processing pipeline that ingests data from multiple sources, transforms it, and loads it into a data warehouse
```

### **Machine Learning**

```
Develop a machine learning model for predicting customer churn with feature engineering, model training, and deployment pipeline
```

## 🔧 **Development Commands**

```bash
make help       # Show all available commands
make test       # Run the test suite
make lint       # Run code linting
make format     # Format code with black/isort
make clean      # Clean up cache files
make validate   # Validate project setup
```

## 🐛 **Troubleshooting**

### **If you get import errors:**

```bash
# Make sure you're in the project root
cd /Users/federico.antosiano/Desktop/smart-code-planner

# Run the app launcher directly
poetry run streamlit run app.py
```

### **If the port is busy:**

```bash
# Kill any process using port 8501
lsof -ti:8501 | xargs kill -9

# Then restart
make run
```

### **If you need to reinstall dependencies:**

```bash
poetry install --no-cache
```

## 🎉 **Success!**

Your Smart Code Planner is now running successfully at:
**http://localhost:8501**

The application features:

- ✅ Modern Streamlit UI
- ✅ LangGraph workflow orchestration
- ✅ OpenAI GPT integration
- ✅ Google Gemini integration
- ✅ Task decomposition and analysis
- ✅ Code organization recommendations
- ✅ Export functionality
- ✅ Clean architecture with Poetry and Docker

**Happy coding! 🚀**
