"""Streamlit web interface for the Coder Assistant."""

import asyncio
import streamlit as st
import json
from typing import Optional

# Add src to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import after page config
from src.agent.graph import CoderAssistantGraph
from src.core.models import TaskAnalysisResult, SubTask
from src.core.config import settings
from src.services.llm_service import LLMService


class StreamlitUI:
    """Streamlit user interface for the coder assistant."""

    def __init__(self):
        """Initialize the UI."""
        self.graph = CoderAssistantGraph()

    def run(self):
        """Run the Streamlit application."""
        self._render_header()
        self._render_sidebar()
        self._render_main_content()

    def _render_header(self):
        """Render the application header."""
        st.title("🤖 Smart Code Planner")
        st.markdown("""
        **Transform complex coding tasks into organized, actionable plans**

        This intelligent agent uses LangGraph to:
        - 📝 Break down complex tasks into manageable subtasks
        - 🔄 Recursively analyze subtasks for optimal granularity
        - 🏗️ Provide expert code organization advice
        - ⚡ Generate implementation roadmaps
        """)
        st.divider()

    def _render_sidebar(self):
        """Render the sidebar with configuration options."""
        with st.sidebar:
            st.header("⚙️ Configuration")

            # Analysis depth setting
            max_depth = st.slider(
                "Maximum Analysis Depth",
                min_value=1,
                max_value=5,
                value=3,
                help="How deep should the agent analyze subtasks?"
            )

            # Model settings
            st.subheader("🤖 Model Settings")

            # Provider selection
            available_models = LLMService.list_available_models()

            provider = st.selectbox(
                "Provider",
                options=["openai", "google"],
                index=0,
                help="Choose the LLM provider"
            )

            # Model selection based on provider
            if provider in available_models and available_models[provider]:
                model_options = available_models[provider]
                default_model = model_options[0] if model_options else "gpt-4o"

                model_name = st.selectbox(
                    "Model",
                    options=model_options,
                    index=0 if default_model in model_options else 0,
                    help=f"Available models for {provider}"
                )
            else:
                st.warning(f"No models available for {provider}")
                model_name = "gpt-4o"
                provider = "openai"

            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.1,
                help="Higher values make output more creative"
            )

            # Store settings in session state
            st.session_state.max_depth = max_depth
            st.session_state.model_name = model_name
            st.session_state.model_provider = provider
            st.session_state.temperature = temperature

            st.divider()

            # API Key status
            st.subheader("🔑 API Status")
            try:
                # Check OpenAI API key
                if settings.openai_api_key and settings.openai_api_key.startswith('sk-'):
                    st.success("✅ OpenAI API Key configured")
                else:
                    st.warning("⚠️ OpenAI API Key not found")

                # Check Google API key
                if settings.google_api_key:
                    st.success("✅ Google API Key configured")
                else:
                    st.warning("⚠️ Google API Key not found")

                # Validate current configuration
                is_valid, message = LLMService.validate_configuration(
                    st.session_state.get('model_name', 'gpt-4o'),
                    st.session_state.get('model_provider', 'openai')
                )

                if is_valid:
                    st.success(f"✅ Current configuration: {message}")
                else:
                    st.error(f"❌ Configuration issue: {message}")

            except Exception as e:
                st.error("❌ Configuration error")
                st.info("Please check your .env file configuration")

            # About section
            st.subheader("ℹ️ About")
            st.markdown("""
            **Smart Code Planner** v0.1.0

            Built with:
            - 🦜 LangChain & LangGraph
            - 🎈 Streamlit
            - 🐍 Python
            - 🔧 Poetry

            Created by Federico Antosiano
            """)

    def _render_main_content(self):
        """Render the main content area."""
        # Task input section
        st.header("📝 Task Input")

        # Example tasks for quick testing
        example_tasks = {
            "None": "",
            "Web App": "Build a full-stack web application for task management with user authentication, real-time updates, and mobile responsiveness",
            "API Service": "Create a RESTful API service for an e-commerce platform with inventory management, order processing, and payment integration",
            "Data Pipeline": "Design and implement a data processing pipeline that ingests data from multiple sources, transforms it, and loads it into a data warehouse",
            "ML Model": "Develop a machine learning model for predicting customer churn with feature engineering, model training, and deployment pipeline"
        }

        selected_example = st.selectbox(
            "Choose an example task or write your own:",
            options=list(example_tasks.keys())
        )

        # Task input text area
        default_task = example_tasks.get(selected_example, "")
        task_description = st.text_area(
            "Describe your coding task:",
            value=default_task,
            height=120,
            placeholder="Enter a detailed description of what you want to build..."
        )

        # Analysis button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button(
                "🚀 Analyze Task",
                type="primary",
                use_container_width=True,
                disabled=not task_description.strip()
            )

        # Process analysis
        if analyze_button and task_description.strip():
            with st.spinner("🤖 Analyzing your task... This may take a few moments."):
                try:
                    # Run the analysis
                    result = asyncio.run(self._run_analysis(task_description))

                    # Check if there was an error
                    if hasattr(result, 'error_message') and result.error_message:
                        st.error(f"❌ Analysis failed: {result.error_message}")
                    elif 'error_message' in result and result.get('error_message'):
                        st.error(f"❌ Analysis failed: {result['error_message']}")
                    else:
                        # Store result in session state
                        st.session_state.analysis_result = result
                        st.success("✅ Analysis complete!")
                        st.rerun()

                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())

        # Display results if available
        if hasattr(st.session_state, 'analysis_result') and st.session_state.analysis_result:
            self._render_results(st.session_state.analysis_result)

    async def _run_analysis(self, task: str):
        """Run the task analysis."""
        max_depth = getattr(st.session_state, 'max_depth', 3)

        # Create a new graph instance with the selected model configuration
        from src.services.task_analyzer import TaskAnalyzer
        from src.services.code_advisor import CodeAdvisor
        from src.services.llm_service import LLMService

        # Override the default LLM settings for this analysis
        model_name = getattr(st.session_state, 'model_name', settings.model_name)
        provider = getattr(st.session_state, 'model_provider', settings.model_provider)
        temperature = getattr(st.session_state, 'temperature', settings.temperature)

        # Temporarily update the services with the selected model
        original_settings = (settings.model_name, settings.model_provider, settings.temperature)
        try:
            settings.model_name = model_name
            settings.model_provider = provider
            settings.temperature = temperature

            # Create a fresh graph instance
            graph = CoderAssistantGraph()
            result = await graph.run(task, max_depth)

            return result

        finally:
            # Restore original settings
            settings.model_name, settings.model_provider, settings.temperature = original_settings

    def _render_results(self, state):
        """Render the analysis results."""
        # Handle both AgentState and AddableValuesDict from LangGraph
        if hasattr(state, 'final_result'):
            final_result = state.final_result
        elif 'final_result' in state:
            final_result = state.get('final_result')
        else:
            st.warning("⚠️ No final result available yet. The analysis may still be processing.")
            return

        if not final_result:
            st.warning("⚠️ Analysis incomplete. Please try again.")
            return

        result: TaskAnalysisResult = final_result

        st.divider()
        st.header("📊 Analysis Results")

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Main Subtasks",
                len(result.main_subtasks)
            )

        with col2:
            st.metric(
                "Complexity Score",
                f"{result.complexity_score:.2f}",
                help="Scale: 0.0 (Simple) to 1.0 (Very Complex)"
            )

        with col3:
            total_subtasks = self._count_all_subtasks(result.main_subtasks)
            st.metric(
                "Total Subtasks",
                total_subtasks
            )

        with col4:
            st.metric(
                "Estimated Time",
                result.total_estimated_time or "Not estimated"
            )

        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Task Breakdown", "🏗️ Code Organization", "💡 Recommendations", "📁 Export"])

        with tab1:
            self._render_task_breakdown(result.main_subtasks)

        with tab2:
            self._render_code_organization(result.code_organization)

        with tab3:
            self._render_recommendations(result.recommendations)

        with tab4:
            self._render_export_options(result)

    def _render_task_breakdown(self, subtasks):
        """Render the task breakdown section."""
        st.subheader("📋 Task Breakdown")

        for i, subtask in enumerate(subtasks, 1):
            with st.expander(f"**{i}. {subtask.title}**", expanded=True):

                # Subtask details
                col1, col2, col3 = st.columns(3)
                with col1:
                    priority_color = {
                        "low": "🟢",
                        "medium": "🟡",
                        "high": "🟠",
                        "critical": "🔴"
                    }
                    st.write(f"**Priority:** {priority_color.get(subtask.priority, '⚪')} {subtask.priority.title()}")

                with col2:
                    complexity_emoji = {
                        "simple": "🟢",
                        "moderate": "🟡",
                        "complex": "🟠",
                        "very_complex": "🔴"
                    }
                    st.write(f"**Complexity:** {complexity_emoji.get(subtask.complexity, '⚪')} {subtask.complexity.replace('_', ' ').title()}")

                with col3:
                    if subtask.estimated_time:
                        st.write(f"**Time:** ⏱️ {subtask.estimated_time}")

                # Description
                st.write(f"**Description:** {subtask.description}")

                # Dependencies
                if subtask.dependencies:
                    st.write(f"**Dependencies:** {', '.join(subtask.dependencies)}")

                # Sub-subtasks
                if subtask.sub_subtasks:
                    st.write("**Sub-subtasks:**")
                    for j, sub_subtask in enumerate(subtask.sub_subtasks, 1):
                        st.write(f"  {j}. **{sub_subtask.title}**")
                        st.write(f"     {sub_subtask.description}")
                        if sub_subtask.estimated_time:
                            st.write(f"     ⏱️ {sub_subtask.estimated_time}")

    def _render_code_organization(self, code_org):
        """Render the code organization section."""
        st.subheader("🏗️ Code Organization Advice")

        # File structure
        if code_org.file_structure:
            st.write("### 📁 Recommended File Structure")
            for path, description in code_org.file_structure.items():
                st.write(f"**{path}** - {description}")

        # Classes
        if code_org.classes:
            st.write("### 🏛️ Recommended Classes")
            for class_info in code_org.classes:
                with st.expander(f"**{class_info.get('name', 'Unknown Class')}**"):
                    st.write(f"**Description:** {class_info.get('description', 'No description')}")
                    if class_info.get('file_location'):
                        st.write(f"**Location:** {class_info['file_location']}")
                    if class_info.get('key_methods'):
                        st.write(f"**Key Methods:** {', '.join(class_info['key_methods'])}")
                    if class_info.get('relationships'):
                        st.write(f"**Relationships:** {', '.join(class_info['relationships'])}")

        # Functions
        if code_org.functions:
            st.write("### ⚙️ Recommended Functions")
            for func_info in code_org.functions:
                with st.expander(f"**{func_info.get('name', 'Unknown Function')}**"):
                    st.write(f"**Description:** {func_info.get('description', 'No description')}")
                    if func_info.get('file_location'):
                        st.write(f"**Location:** {func_info['file_location']}")
                    if func_info.get('parameters'):
                        st.write(f"**Parameters:** {', '.join(func_info['parameters'])}")
                    if func_info.get('return_type'):
                        st.write(f"**Returns:** {func_info['return_type']}")

        # Design patterns
        if code_org.design_patterns:
            st.write("### 🎯 Suggested Design Patterns")
            for pattern in code_org.design_patterns:
                st.write(f"• {pattern}")

        # Best practices
        if code_org.best_practices:
            st.write("### ✨ Best Practices")
            for practice in code_org.best_practices:
                st.write(f"• {practice}")

    def _render_recommendations(self, recommendations):
        """Render the recommendations section."""
        st.subheader("💡 General Recommendations")

        if recommendations:
            for i, recommendation in enumerate(recommendations, 1):
                st.write(f"{i}. {recommendation}")
        else:
            st.info("No specific recommendations generated.")

    def _render_export_options(self, result: TaskAnalysisResult):
        """Render export options."""
        st.subheader("📁 Export Results")

        # JSON export
        json_data = result.dict()
        json_str = json.dumps(json_data, indent=2, default=str)

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📄 Download JSON",
                data=json_str,
                file_name="task_analysis.json",
                mime="application/json"
            )

        with col2:
            # Markdown export
            markdown_content = self._generate_markdown_report(result)
            st.download_button(
                label="📝 Download Markdown",
                data=markdown_content,
                file_name="task_analysis.md",
                mime="text/markdown"
            )

    def _generate_markdown_report(self, result: TaskAnalysisResult) -> str:
        """Generate a markdown report of the analysis."""
        md = f"""# Task Analysis Report

## Original Task
{result.original_task}

## Overview
- **Complexity Score:** {result.complexity_score:.2f}/1.0
- **Total Estimated Time:** {result.total_estimated_time or 'Not estimated'}
- **Main Subtasks:** {len(result.main_subtasks)}

## Task Breakdown
"""

        for i, subtask in enumerate(result.main_subtasks, 1):
            md += f"""
### {i}. {subtask.title}
- **Description:** {subtask.description}
- **Priority:** {subtask.priority}
- **Complexity:** {subtask.complexity}
- **Estimated Time:** {subtask.estimated_time or 'Not estimated'}
"""

            if subtask.dependencies:
                md += f"- **Dependencies:** {', '.join(subtask.dependencies)}\n"

            if subtask.sub_subtasks:
                md += "\n**Sub-subtasks:**\n"
                for j, sub_subtask in enumerate(subtask.sub_subtasks, 1):
                    md += f"  {j}. {sub_subtask.title} - {sub_subtask.description}\n"

        # Add recommendations
        if result.recommendations:
            md += "\n## Recommendations\n"
            for rec in result.recommendations:
                md += f"- {rec}\n"

        return md

    def _count_all_subtasks(self, subtasks) -> int:
        """Count total number of subtasks including nested ones."""
        total = len(subtasks)
        for subtask in subtasks:
            if subtask.sub_subtasks:
                total += self._count_all_subtasks(subtask.sub_subtasks)
        return total


def main():
    """Main entry point for the Streamlit app."""
    try:
        ui = StreamlitUI()
        ui.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please check your configuration and API keys.")


if __name__ == "__main__":
    main()
