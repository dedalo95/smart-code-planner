#!/bin/bash

# Project validation script
# Checks if all components are properly configured

echo "🔍 Smart Code Planner - Project Validation"
echo "============================================"

# Initialize counters
CHECKS_PASSED=0
TOTAL_CHECKS=0

# Helper function to check status
check_status() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ $1 -eq 0 ]; then
        echo "✅ $2"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "❌ $2"
    fi
}

# Check Python version
echo "📋 Checking Prerequisites..."
python3 --version > /dev/null 2>&1
check_status $? "Python 3 is installed"

# Check Poetry
poetry --version > /dev/null 2>&1
check_status $? "Poetry is installed"

# Check project structure
echo ""
echo "📁 Checking Project Structure..."

# Core directories
[ -d "src" ]
check_status $? "src/ directory exists"

[ -d "src/agent" ]
check_status $? "src/agent/ directory exists"

[ -d "src/core" ]
check_status $? "src/core/ directory exists"

[ -d "src/services" ]
check_status $? "src/services/ directory exists"

[ -d "src/ui" ]
check_status $? "src/ui/ directory exists"

[ -d "prompts" ]
check_status $? "prompts/ directory exists"

[ -d "tests" ]
check_status $? "tests/ directory exists"

# Core files
echo ""
echo "📄 Checking Core Files..."

[ -f "pyproject.toml" ]
check_status $? "pyproject.toml exists"

[ -f "README.md" ]
check_status $? "README.md exists"

[ -f "docker-compose.yml" ]
check_status $? "docker-compose.yml exists"

[ -f ".env.example" ]
check_status $? ".env.example exists"

# Source files
echo ""
echo "🐍 Checking Source Files..."

[ -f "src/core/models.py" ]
check_status $? "Core models exist"

[ -f "src/core/config.py" ]
check_status $? "Configuration module exists"

[ -f "src/agent/graph.py" ]
check_status $? "LangGraph workflow exists"

[ -f "src/services/task_analyzer.py" ]
check_status $? "Task analyzer service exists"

[ -f "src/services/code_advisor.py" ]
check_status $? "Code advisor service exists"

[ -f "src/ui/streamlit_app.py" ]
check_status $? "Streamlit app exists"

# Prompt files
echo ""
echo "📝 Checking Prompt Files..."

[ -f "prompts/task_decomposition.txt" ]
check_status $? "Task decomposition prompt exists"

[ -f "prompts/subtask_analysis.txt" ]
check_status $? "Subtask analysis prompt exists"

[ -f "prompts/code_organization.txt" ]
check_status $? "Code organization prompt exists"

# Test files
echo ""
echo "🧪 Checking Test Files..."

[ -f "tests/test_models.py" ]
check_status $? "Model tests exist"

[ -f "tests/test_task_analyzer.py" ]
check_status $? "Task analyzer tests exist"

[ -f "tests/test_agent.py" ]
check_status $? "Agent tests exist"

# Dependencies
echo ""
echo "📦 Checking Dependencies..."

if [ -f "poetry.lock" ]; then
    echo "✅ poetry.lock exists"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "❌ poetry.lock missing - run 'poetry lock'"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# Try to install dependencies (dry run)
poetry check > /dev/null 2>&1
check_status $? "Poetry configuration is valid"

# Check environment configuration
echo ""
echo "⚙️ Checking Environment Configuration..."

if [ -f ".env" ]; then
    if grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
        echo "✅ OpenAI API key is configured"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "⚠️  OpenAI API key not configured (add to .env file)"
    fi
else
    echo "⚠️  .env file not found (copy from .env.example)"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# Check executables
echo ""
echo "🔧 Checking Executable Scripts..."

[ -x "setup.sh" ]
check_status $? "setup.sh is executable"

[ -x "run.sh" ]
check_status $? "run.sh is executable"

[ -f "Makefile" ]
check_status $? "Makefile exists"

# Docker configuration
echo ""
echo "🐳 Checking Docker Configuration..."

[ -f "docker/Dockerfile" ]
check_status $? "Dockerfile exists"

[ -f "docker-compose.yml" ]
check_status $? "docker-compose.yml exists"

# Additional files
echo ""
echo "📋 Checking Additional Files..."

[ -f "LICENSE" ]
check_status $? "LICENSE file exists"

[ -f ".gitignore" ]
check_status $? ".gitignore exists"

[ -f ".pre-commit-config.yaml" ]
check_status $? "Pre-commit configuration exists"

# Final summary
echo ""
echo "============================================"
echo "📊 Validation Summary"
echo "============================================"
echo "Checks passed: $CHECKS_PASSED/$TOTAL_CHECKS"

PERCENTAGE=$((CHECKS_PASSED * 100 / TOTAL_CHECKS))
echo "Success rate: $PERCENTAGE%"

if [ $PERCENTAGE -ge 95 ]; then
    echo "🎉 Excellent! Project is ready for development"
    exit 0
elif [ $PERCENTAGE -ge 80 ]; then
    echo "✅ Good! Minor issues to address"
    exit 0
elif [ $PERCENTAGE -ge 60 ]; then
    echo "⚠️  Some issues found. Please review and fix"
    exit 1
else
    echo "❌ Major issues found. Please run setup again"
    exit 1
fi
