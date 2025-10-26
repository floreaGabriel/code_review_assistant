from src.ml_classifier import SeverityClassifier

# Create synthetic training data with labeled severities
training_data = [
    # High severity examples
    {'type': 'GodClass', 'line': 50, 'message': 'Class has 25 methods', 'severity': 'high'},
    {'type': 'GodClass', 'line': 120, 'message': 'Class has 30 methods', 'severity': 'high'},
    {'type': 'ComplexCondition', 'line': 80, 'message': 'Cyclomatic complexity 15', 'severity': 'high'},
    {'type': 'GodClass', 'line': 200, 'message': 'Class has 20 methods', 'severity': 'high'},
    {'type': 'ComplexCondition', 'line': 45, 'message': 'Cyclomatic complexity 12', 'severity': 'high'},

    # Medium severity examples
    {'type': 'LongFunction', 'line': 30, 'message': 'Function has 25 statements', 'severity': 'medium'},
    {'type': 'LongFunction', 'line': 100, 'message': 'Function has 30 statements', 'severity': 'medium'},
    {'type': 'DeepNesting', 'line': 65, 'message': 'Nesting level 6', 'severity': 'medium'},
    {'type': 'LongFunction', 'line': 150, 'message': 'Function has 22 statements', 'severity': 'medium'},
    {'type': 'DeepNesting', 'line': 90, 'message': 'Nesting level 5', 'severity': 'medium'},

    # Low severity examples
    {'type': 'TooManyParameters', 'line': 10, 'message': 'Function has 6 parameters', 'severity': 'low'},
    {'type': 'TooManyParameters', 'line': 40, 'message': 'Function has 7 parameters', 'severity': 'low'},
    {'type': 'TooManyParameters', 'line': 70, 'message': 'Function has 8 parameters', 'severity': 'low'},
    {'type': 'TooManyParameters', 'line': 110, 'message': 'Function has 9 parameters', 'severity': 'low'},
    {'type': 'TooManyParameters', 'line': 140, 'message': 'Function has 10 parameters', 'severity': 'low'},
]

# Train the classifier
classifier = SeverityClassifier()
classifier.train(training_data)

# Save the trained model
classifier.save_model('severity_model.pkl')

print("\n✅ Training complete! Model saved.")
