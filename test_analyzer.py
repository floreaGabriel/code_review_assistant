from src.ast_analyzer import CodeSmellDetector
from src.ml_classifier import SeverityClassifier

# Load the trained model
classifier = SeverityClassifier()
try:
    classifier.load_model('severity_model.pkl')
except FileNotFoundError:
    print("⚠️  Model not found. Run generate_training_data.py first!")
    exit()

# Read and analyze code
with open('test_code.py', 'r') as f:
    code = f.read()

detector = CodeSmellDetector()
results = detector.analyze_code(code)

print(f"Detected {len(results)} code smells:\n")

# Predict severity with ML model
for smell in results:
    predicted_severity = classifier.predict_severity(smell)
    print(f"[{predicted_severity.upper()}] {smell['type']}")
    print(f"  Line {smell['line']}: {smell['message']}")
    print(f"  ML Predicted: {predicted_severity}\n")
