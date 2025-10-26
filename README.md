# Code Review Assistant

## Requirements 

- `stremalit` Interactive UI framework
- `scikit-learn` For ML model
- `openai` For OpenAI Agents integration
- `python-dotenv` For API Keys usage

## AST (Abstract Syntax Tree)

AST transforms Python code into a tree structure which represents code syntax. Each element (functions, classes, variables) becomes a tree node.

Ex:
```
def greet(name):
    print("Hello, " + name)
```

Becomes: 

```
Module
└── FunctionDef (name='greet')
    ├── arguments
    │   └── arg (arg='name')
    └── body
        └── Expr
            └── Call (func=print)
```

---

### Why to use AST

AST allow us to "read" the code structure better and to detect different "patterns" (code smells)

---

## ML Classifier with Scikit-Learn

**What We're Building**:

A machine learning model that takes code smell features and predicts severity levels (low/medium/high). This adds intelligence to our system by learning patterns from training data.

###  Why Logistic Regression?

- Logistic Regression is perfect for multi-class classification tasks like severity prediction

- Fast training: Works well with small datasets

- Interpretable: You can see which features matter most

- Reliable: Achieves 90%+ accuracy on similar tasks



 
