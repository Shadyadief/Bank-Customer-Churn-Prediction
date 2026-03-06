import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.train_model import train_model
from src.models.evaluate_model import evaluate_model, cross_validate_model
from src.models.predict_model import predict_single
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler


# ─── Fixtures ──────────────────────────────────────────────────
@pytest.fixture
def dummy_data():
    """بيانات عشوائية للاختبار"""
    np.random.seed(42)
    X = np.random.rand(200, 11)
    y = np.random.randint(0, 2, 200)
    return X, y


@pytest.fixture
def trained_rf(dummy_data, tmp_path):
    """Random Forest مدرّب على بيانات تجريبية"""
    X, y = dummy_data
    model = train_model(
        RandomForestClassifier(n_estimators=10, random_state=42),
        X, y,
        model_name="test_rf",
        models_dir=str(tmp_path)
    )
    return model


@pytest.fixture
def trained_xgb(dummy_data, tmp_path):
    """XGBoost مدرّب على بيانات تجريبية"""
    X, y = dummy_data
    model = train_model(
        XGBClassifier(n_estimators=10, random_state=42, eval_metric='logloss'),
        X, y,
        model_name="test_xgb",
        models_dir=str(tmp_path)
    )
    return model


# ─── Tests: Training ───────────────────────────────────────────
class TestTraining:

    def test_model_is_fitted(self, trained_rf):
        """تأكد إن الموديل اتدرب"""
        from sklearn.utils.validation import check_is_fitted
        check_is_fitted(trained_rf)

    def test_model_saved_to_disk(self, dummy_data, tmp_path):
        """تأكد إن الموديل اتحفظ على الـ disk"""
        X, y = dummy_data
        train_model(
            RandomForestClassifier(n_estimators=5, random_state=42),
            X, y,
            model_name="save_test",
            models_dir=str(tmp_path)
        )
        assert os.path.exists(os.path.join(str(tmp_path), "save_test.pkl"))

    def test_xgb_model_fitted(self, trained_xgb):
        """تأكد إن XGBoost اتدرب"""
        assert trained_xgb is not None
        assert hasattr(trained_xgb, 'feature_importances_')


# ─── Tests: Prediction ─────────────────────────────────────────
class TestPrediction:

    def test_predict_returns_0_or_1(self, trained_rf, dummy_data):
        """تأكد إن الـ prediction بترجع 0 أو 1 بس"""
        X, _ = dummy_data
        preds = trained_rf.predict(X)
        assert set(preds).issubset({0, 1})

    def test_predict_proba_between_0_and_1(self, trained_rf, dummy_data):
        """تأكد إن الـ probability بين 0 و 1"""
        X, _ = dummy_data
        proba = trained_rf.predict_proba(X)
        assert (proba >= 0).all()
        assert (proba <= 1).all()

    def test_predict_proba_sums_to_1(self, trained_rf, dummy_data):
        """تأكد إن مجموع الـ probabilities = 1"""
        X, _ = dummy_data
        proba = trained_rf.predict_proba(X)
        row_sums = proba.sum(axis=1)
        np.testing.assert_array_almost_equal(row_sums, np.ones(len(row_sums)))

    def test_predict_single_output_keys(self, trained_rf, dummy_data):
        """تأكد إن predict_single بترجع الـ keys الصح"""
        X, _ = dummy_data
        scaler = StandardScaler()
        scaler.fit(X)
        feature_names = [f'f{i}' for i in range(X.shape[1])]
        input_dict = {f: float(X[0][i]) for i, f in enumerate(feature_names)}

        result = predict_single(trained_rf, scaler, input_dict, feature_names)
        assert 'prediction' in result
        assert 'label' in result
        assert 'churn_probability' in result

    def test_predict_single_prediction_binary(self, trained_rf, dummy_data):
        """تأكد إن الـ prediction 0 أو 1"""
        X, _ = dummy_data
        scaler = StandardScaler()
        scaler.fit(X)
        feature_names = [f'f{i}' for i in range(X.shape[1])]
        input_dict = {f: float(X[0][i]) for i, f in enumerate(feature_names)}

        result = predict_single(trained_rf, scaler, input_dict, feature_names)
        assert result['prediction'] in [0, 1]

    def test_predict_correct_output_size(self, trained_rf, dummy_data):
        """تأكد إن عدد الـ predictions = عدد الـ samples"""
        X, _ = dummy_data
        preds = trained_rf.predict(X)
        assert len(preds) == len(X)


# ─── Tests: Evaluation ─────────────────────────────────────────
class TestEvaluation:

    def test_evaluate_returns_dict(self, trained_rf, dummy_data):
        """تأكد إن evaluate_model بترجع dict"""
        X, y = dummy_data
        result = evaluate_model(trained_rf, X, y, "test_rf")
        assert isinstance(result, dict)

    def test_evaluate_has_roc_auc(self, trained_rf, dummy_data):
        """تأكد إن النتيجة فيها ROC-AUC"""
        X, y = dummy_data
        result = evaluate_model(trained_rf, X, y, "test_rf")
        assert 'roc_auc' in result

    def test_roc_auc_between_0_and_1(self, trained_rf, dummy_data):
        """تأكد إن ROC-AUC بين 0 و 1"""
        X, y = dummy_data
        result = evaluate_model(trained_rf, X, y, "test_rf")
        assert 0.0 <= result['roc_auc'] <= 1.0

    def test_cross_val_returns_scores(self, dummy_data):
        """تأكد إن Cross Validation بترجع scores"""
        X, y = dummy_data
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X, y)
        result = cross_validate_model(model, X, y, cv=3)
        assert 'cv_scores' in result
        assert len(result['cv_scores']) == 3

    def test_cross_val_mean_reasonable(self, dummy_data):
        """تأكد إن متوسط الـ Cross Validation معقول"""
        X, y = dummy_data
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        result = cross_validate_model(model, X, y, cv=3)
        assert 0.0 <= result['mean'] <= 1.0
