import pickle
from typing import Dict, List
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import numpy as np


class SeverityClassifier:
    """
    ML model to classify code smell severity using Logistic Regression.
    """

    def __init__(self):
        """Initialize the classifier and label encoder."""
        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            multi_class='multinomial',  # For multi-class classification
            solver='lbfgs'  # Efficient solver for small datasets
        )
        self.label_encoder = LabelEncoder()
        self.is_trained = False

    def extract_features(self, smell: Dict) -> List[float]:
        """
        Extract numerical features from a code smell dictionary.

        Features extracted:
        - Code smell type (encoded as number)
        - Line number
        - Length metrics (if available in message)

        Args:
            smell: Dictionary with code smell information

        Returns:
            List of numerical features
        """
        features = []

        # Feature 1: Code smell type encoded as number
        smell_types = {
            'LongFunction': 1,
            'TooManyParameters': 2,
            'GodClass': 3,
            'ComplexCondition': 4,
            'DeepNesting': 5
        }
        features.append(smell_types.get(smell['type'], 0))

        # Feature 2: Line number (normalized to 0-1 range)
        features.append(smell.get('line', 0) / 1000.0)

        # Feature 3: Extract numeric value from message (e.g., "20 parameters")
        message = smell.get('message', '')
        numbers = [int(s) for s in message.split() if s.isdigit()]
        features.append(numbers[0] if numbers else 0)

        return features

    def train(self, training_data: List[Dict]):
        """
        Train the classifier on labeled code smells.

        Args:
            training_data: List of code smell dictionaries with 'severity' labels
        """
        if len(training_data) < 5:
            print("Warning: Need at least 5 training examples. Using default rules.")
            return

        # Extract features and labels
        X = [self.extract_features(smell) for smell in training_data]
        y = [smell['severity'] for smell in training_data]

        # Encode labels (low=0, medium=1, high=2)
        y_encoded = self.label_encoder.fit_transform(y)

        # Split data into train/test sets (80/20 split)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded  # Maintain class distribution
        )

        # Train the model
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Evaluate on test set
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\n✅ Model trained successfully!")
        print(f"Accuracy: {accuracy * 100:.2f}%")
        print("\nClassification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=self.label_encoder.classes_,
            zero_division=0
        ))

    def predict_severity(self, smell: Dict) -> str:
        """
        Predict severity for a single code smell.

        Args:
            smell: Dictionary with code smell information

        Returns:
            Predicted severity ('low', 'medium', or 'high')
        """
        if not self.is_trained:
            # Fallback to rule-based classification
            return self._rule_based_classification(smell)

        features = self.extract_features(smell)
        features_array = np.array([features])

        prediction_encoded = self.model.predict(features_array)[0]
        severity = self.label_encoder.inverse_transform([prediction_encoded])[0]

        return severity

    def _rule_based_classification(self, smell: Dict) -> str:
        """
        Fallback rule-based severity classification.
        Used when model isn't trained.
        """
        # Simple rules based on smell type
        high_severity_types = ['GodClass', 'ComplexCondition']
        medium_severity_types = ['LongFunction', 'DeepNesting']

        smell_type = smell.get('type', '')

        if smell_type in high_severity_types:
            return 'high'
        elif smell_type in medium_severity_types:
            return 'medium'
        else:
            return 'low'

    def save_model(self, filepath: str):
        """Save trained model to disk."""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'label_encoder': self.label_encoder,
                'is_trained': self.is_trained
            }, f)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """Load trained model from disk."""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.label_encoder = data['label_encoder']
            self.is_trained = data['is_trained']
        print(f"Model loaded from {filepath}")
