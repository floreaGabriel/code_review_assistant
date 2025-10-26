# 🔍 AI Code Review Assistant

An intelligent, automated code review tool that combines Abstract Syntax Tree (AST) analysis, Machine Learning classification, and Large Language Model-powered suggestions to detect code smells and provide actionable refactoring advice.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **🔬 AST-Based Detection** - Static code analysis using Python's Abstract Syntax Tree to identify anti-patterns
- **🤖 ML-Powered Classification** - Scikit-Learn Logistic Regression model classifies issue severity (Low/Medium/High)
- **💡 AI-Generated Suggestions** - OpenAI GPT-4 provides contextual, educational refactoring recommendations
- **🎨 Interactive UI** - Beautiful Streamlit interface with syntax highlighting and real-time feedback
- **⚡ Fast & Accurate** - Analyzes code in seconds with configurable detection thresholds


## Interface 

![1](./Screenshot%202025-10-26%20at%2014.21.09.png)

![2](./Screenshot%202025-10-26%20at%2014.21.25.png)

![3](./Screenshot%202025-10-26%20at%2014.27.14.png)

![4](./Screenshot%202025-10-26%20at%2014.27.35.png)
## 🎯 Detected Code Smells

- **Long Functions** - Functions exceeding recommended line counts
- **Too Many Parameters** - Functions with excessive parameter lists
- **God Classes** - Classes with too many responsibilities
- **Complex Conditions** - Overly nested or complex conditional logic
- **Deep Nesting** - Excessive indentation levels

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

## 📊 How It Works

1. **AST Parsing** - Code is parsed into an Abstract Syntax Tree
2. **Pattern Matching** - Tree traversal identifies anti-patterns
3. **Feature Extraction** - Metrics extracted for ML classification
4. **Severity Prediction** - Logistic Regression classifies issue severity
5. **AI Suggestion** - GPT-4 generates contextual refactoring advice

## 🎓 Educational Value

This tool not only identifies problems but **teaches best practices** by:
- Explaining WHY code smells are problematic
- Providing before/after code examples
- Referencing SOLID principles and design patterns
- Offering constructive, educational feedback
