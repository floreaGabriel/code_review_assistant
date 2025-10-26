import streamlit as st
from streamlit_ace import st_ace
from src.ast_analyzer import CodeSmellDetector
from src.ml_classifier import SeverityClassifier
from src.ai_agent import CodeReviewAgent
import os

# Page configuration
st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .smell-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid;
    }
    .severity-high {
        border-left-color: #ff4b4b;
    }
    .severity-medium {
        border-left-color: #ffa500;
    }
    .severity-low {
        border-left-color: #00cc00;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">🔍 AI Code Review Assistant</div>', unsafe_allow_html=True)
st.markdown("""
Welcome to the **AI Code Review Assistant**! This tool combines:
- 🔬 **AST Analysis** - Detects code smells using Abstract Syntax Trees
- 🤖 **Machine Learning** - Classifies severity using Scikit-Learn
- 💡 **AI Suggestions** - Provides intelligent refactoring advice via OpenAI

Upload your Python code and get instant, actionable feedback!
""")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # AST Analyzer settings
    st.subheader("Code Smell Detection")
    max_function_length = st.slider(
        "Max Function Length (lines)",
        min_value=10,
        max_value=50,
        value=20,
        help="Functions longer than this will be flagged"
    )

    max_parameters = st.slider(
        "Max Function Parameters",
        min_value=3,
        max_value=10,
        value=5,
        help="Functions with more parameters will be flagged"
    )

    # AI Agent settings
    st.subheader("AI Analysis")
    enable_ai = st.checkbox(
        "Enable AI Suggestions",
        value=True,
        help="Generate AI-powered refactoring suggestions"
    )

    if enable_ai and not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ OpenAI API key not found in .env file")

    st.divider()
    st.markdown("### 📊 About")
    st.info("""
    This tool uses:
    - Python AST parsing
    - Logistic Regression
    - OpenAI Agents SDK
    """)

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["📝 Code Analysis", "📚 Examples", "ℹ️ Help"])

with tab1:
    # Two columns: code input and results
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🖊️ Enter Your Code")

        # Default example code
        default_code = """def process_user_data(user_id, username, email, phone, address, city, country, postal_code, birth_date):
    \"\"\"Function with too many parameters\"\"\"
    print(f"Processing {username}")
    # More processing...
    pass

class UserManager:
    \"\"\"Example class\"\"\"

    def create_user(self):
        pass

    def update_user(self):
        # Very long function
        statement_1 = "line"
        statement_2 = "line"
        statement_3 = "line"
        statement_4 = "line"
        statement_5 = "line"
        statement_6 = "line"
        statement_7 = "line"
        statement_8 = "line"
        statement_9 = "line"
        statement_10 = "line"
        statement_11 = "line"
        statement_12 = "line"
        statement_13 = "line"
        statement_14 = "line"
        statement_15 = "line"
        statement_16 = "line"
        statement_17 = "line"
        statement_18 = "line"
        statement_19 = "line"
        statement_20 = "line"
        statement_21 = "line"
"""

        # Code editor with syntax highlighting
        code = st_ace(
            value=default_code,
            language="python",
            theme="monokai",
            height=400,
            font_size=14,
            tab_size=4,
            key="code_editor"
        )

        # Analyze button
        analyze_button = st.button("🔍 Analyze Code", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 Analysis Results")

        # Initialize session state for results
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None

        # Perform analysis when button is clicked
        if analyze_button and code:
            # Initialize components
            detector = CodeSmellDetector(
                max_function_length=max_function_length,
                max_parameters=max_parameters
            )

            with st.spinner("🔬 Analyzing code structure..."):
                # Detect code smells
                smells = detector.analyze_code(code)

            if not smells:
                st.session_state.analysis_results = {'smells': [], 'message': 'success'}
            else:
                # Load ML classifier
                classifier = SeverityClassifier()
                try:
                    classifier.load_model('severity_model.pkl')
                except FileNotFoundError:
                    pass

                # Predict severities
                for smell in smells:
                    predicted_severity = classifier.predict_severity(smell)
                    smell['predicted_severity'] = predicted_severity

                # Store in session state
                st.session_state.analysis_results = {'smells': smells, 'message': 'analyzed'}

        # Display results from session state
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results

            if results['message'] == 'success':
                st.success("✅ No code smells detected! Your code looks great!")
            elif results['message'] == 'analyzed':
                smells = results['smells']
                st.warning(f"⚠️ Detected {len(smells)} code smell(s)")

                # Display each smell
                for i, smell in enumerate(smells, 1):
                    severity = smell.get('predicted_severity', smell.get('severity', 'unknown'))
                    severity_color = {
                        'high': '🔴',
                        'medium': '🟡',
                        'low': '🟢'
                    }.get(severity, '⚪')

                    # Create a card for each smell
                    st.markdown("---")
                    st.markdown(f"### {severity_color} {smell['type']} - Line {smell['line']} [{severity.upper()}]")

                    # Initialize button variable
                    btn_clicked = False

                    col_info, col_action = st.columns([3, 1])

                    with col_info:
                        st.markdown(f"**Location:** `{smell.get('name', 'N/A')}` (Line {smell['line']})")
                        st.markdown(f"**Issue:** {smell['message']}")

                    with col_action:
                        if enable_ai and os.getenv("OPENAI_API_KEY"):
                            btn_clicked = st.button(
                                "💡 Get AI Fix",
                                key=f"ai_btn_{i}",
                                type="primary",
                                use_container_width=True
                            )

                    # Check button state AFTER columns
                    if enable_ai and os.getenv("OPENAI_API_KEY") and btn_clicked:
                        st.info("🤖 Generating AI suggestion... Please wait 10-15 seconds")

                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        try:
                            # Step 1
                            status_text.text("🔍 Analyzing code smell...")
                            progress_bar.progress(33)

                            agent = CodeReviewAgent()

                            # Step 2
                            status_text.text("📝 Generating suggestions...")
                            progress_bar.progress(66)

                            suggestion = agent.generate_suggestion(smell)

                            # Step 3
                            status_text.text("✨ Formatting response...")
                            progress_bar.progress(100)

                            # Clear progress
                            progress_bar.empty()
                            status_text.empty()

                            # Show success and suggestion
                            st.success("✅ AI Suggestion Generated!")
                            st.markdown("### 💡 AI-Powered Refactoring Suggestion")
                            st.markdown(suggestion)

                        except Exception as e:
                            progress_bar.empty()
                            status_text.empty()
                            st.error(f"❌ Error: {str(e)}")

                            with st.expander("🐛 Debug Info"):
                                st.code(f"""
Error Type: {type(e).__name__}
Error Message: {str(e)}

Troubleshooting:
1. Check OpenAI API key is valid
2. Ensure internet connection is working
3. Verify openai-agents package is installed: pip list | grep openai
                                """)

                    elif enable_ai and not os.getenv("OPENAI_API_KEY"):
                        st.warning("⚠️ API Key missing - Add it to .env file")

        else:
            st.info("👈 Enter some Python code and click 'Analyze Code' to get started!")

with tab2:
    st.subheader("📚 Example Code Smells")

    examples = {
        "Long Function": """def calculate_statistics(data):
    # Too many responsibilities in one function
    total = sum(data)
    average = total / len(data)
    sorted_data = sorted(data)
    median = sorted_data[len(data) // 2]
    variance = sum((x - average) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5
    minimum = min(data)
    maximum = max(data)
    range_val = maximum - minimum
    # ... 20+ more lines
    return {
        'total': total,
        'average': average,
        'median': median,
        'variance': variance,
        'std_dev': std_dev,
        'min': minimum,
        'max': maximum,
        'range': range_val
    }""",

        "Too Many Parameters": """def create_user_profile(user_id, first_name, last_name, email, 
                         phone, address, city, state, zip_code, 
                         country, birth_date, join_date):
    # Too many parameters - should use a data class
    pass""",

        "God Class": """class UserManager:
    # Class with too many responsibilities
    def create_user(self): pass
    def update_user(self): pass
    def delete_user(self): pass
    def authenticate(self): pass
    def send_email(self): pass
    def generate_report(self): pass
    def export_data(self): pass
    def import_data(self): pass
    # ... 20+ more methods
"""
    }

    for name, example_code in examples.items():
        with st.expander(f"🔍 {name}"):
            st.code(example_code, language="python")

with tab3:
    st.subheader("ℹ️ How It Works")

    st.markdown("""
    ### 🔬 AST Analysis
    The tool parses your Python code into an **Abstract Syntax Tree** and detects common code smells:
    - Long functions
    - Too many parameters
    - Complex classes
    - Deep nesting

    ### 🤖 ML Classification
    A **Logistic Regression** model trained on code examples predicts the severity of each issue:
    - 🔴 **High**: Critical issues affecting maintainability
    - 🟡 **Medium**: Important issues to address soon
    - 🟢 **Low**: Minor improvements

    ### 💡 AI Suggestions
    **OpenAI Agents** analyze each code smell and provide:
    - Explanation of why it's problematic
    - Specific refactoring steps
    - Before/after code examples
    - Best practices to prevent future issues

    ### 🚀 Getting Started
    1. Enter or paste Python code in the editor
    2. Adjust detection thresholds in the sidebar
    3. Click "Analyze Code"
    4. Review detected issues and AI suggestions
    """)

    st.markdown("---")
    st.markdown("**Built with:** Streamlit • OpenAI • Scikit-Learn • AST")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Made with ❤️ for the NEXXT AI Hackathon 2025
    </div>
    """,
    unsafe_allow_html=True
)
