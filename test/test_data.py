import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data.load_data import load_raw_data
from src.data.preprocess import (
    drop_unnecessary_columns,
    encode_categoricals,
    split_features_target,
    split_train_test,
)


# ─── Fixtures ──────────────────────────────────────────────────
@pytest.fixture
def sample_df():
    """بيانات تجريبية صغيرة للاختبار"""
    return pd.DataFrame({
        'RowNumber': [1, 2, 3, 4, 5],
        'CustomerId': [101, 102, 103, 104, 105],
        'Surname': ['A', 'B', 'C', 'D', 'E'],
        'CreditScore': [600, 700, 500, 800, 650],
        'Geography': ['France', 'Germany', 'Spain', 'France', 'Germany'],
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'Age': [35, 45, 28, 55, 40],
        'Tenure': [3, 7, 1, 10, 5],
        'Balance': [50000, 0, 80000, 120000, 30000],
        'NumOfProducts': [1, 2, 1, 3, 2],
        'HasCrCard': [1, 0, 1, 1, 0],
        'IsActiveMember': [1, 1, 0, 1, 0],
        'EstimatedSalary': [70000, 90000, 50000, 110000, 60000],
        'Exited': [0, 1, 0, 1, 0],
    })


# ─── Tests: Load Data ──────────────────────────────────────────
class TestLoadData:

    def test_load_returns_dataframe(self, sample_df, tmp_path):
        """تأكد إن الـ function بترجع DataFrame"""
        path = tmp_path / "test.csv"
        sample_df.to_csv(path, index=False)
        df = load_raw_data(str(path))
        assert isinstance(df, pd.DataFrame)

    def test_load_correct_shape(self, sample_df, tmp_path):
        """تأكد إن الـ shape صح"""
        path = tmp_path / "test.csv"
        sample_df.to_csv(path, index=False)
        df = load_raw_data(str(path))
        assert df.shape == (5, 14)

    def test_load_file_not_found(self):
        """تأكد إن FileNotFoundError بتتعمل لو المسار غلط"""
        with pytest.raises(FileNotFoundError):
            load_raw_data("path/does/not/exist.csv")

    def test_target_column_exists(self, sample_df, tmp_path):
        """تأكد إن عمود Exited موجود"""
        path = tmp_path / "test.csv"
        sample_df.to_csv(path, index=False)
        df = load_raw_data(str(path))
        assert 'Exited' in df.columns

    def test_no_missing_values_in_target(self, sample_df, tmp_path):
        """تأكد مفيش null في الـ target"""
        path = tmp_path / "test.csv"
        sample_df.to_csv(path, index=False)
        df = load_raw_data(str(path))
        assert df['Exited'].isnull().sum() == 0


# ─── Tests: Preprocessing ──────────────────────────────────────
class TestPreprocessing:

    def test_drop_unnecessary_columns(self, sample_df):
        """تأكد إن الأعمدة الزيادة اتشالت"""
        df = drop_unnecessary_columns(sample_df.copy())
        assert 'RowNumber' not in df.columns
        assert 'CustomerId' not in df.columns
        assert 'Surname' not in df.columns

    def test_drop_keeps_important_columns(self, sample_df):
        """تأكد إن الأعمدة المهمة لسه موجودة"""
        df = drop_unnecessary_columns(sample_df.copy())
        assert 'CreditScore' in df.columns
        assert 'Exited' in df.columns
        assert 'Age' in df.columns

    def test_encode_categoricals(self, sample_df):
        """تأكد إن الـ Encoding اتعمل صح"""
        df = drop_unnecessary_columns(sample_df.copy())
        df = encode_categoricals(df)
        assert 'Gender' not in df.columns
        assert 'Geography' not in df.columns
        assert 'Gender_Male' in df.columns

    def test_no_object_columns_after_encoding(self, sample_df):
        """تأكد مفيش object columns بعد الـ Encoding"""
        df = drop_unnecessary_columns(sample_df.copy())
        df = encode_categoricals(df)
        object_cols = df.select_dtypes(include='object').columns.tolist()
        assert len(object_cols) == 0

    def test_split_features_target(self, sample_df):
        """تأكد إن الـ split صح"""
        df = drop_unnecessary_columns(sample_df.copy())
        df = encode_categoricals(df)
        X, y = split_features_target(df)
        assert 'Exited' not in X.columns
        assert len(y) == len(X)
        assert set(y.unique()).issubset({0, 1})

    def test_train_test_split_sizes(self, sample_df):
        """تأكد إن نسب الـ split صح"""
        df = drop_unnecessary_columns(sample_df.copy())
        df = encode_categoricals(df)
        X, y = split_features_target(df)

        # نعمل DataFrame أكبر عشان الـ split يشتغل
        X_big = pd.concat([X] * 20, ignore_index=True)
        y_big = pd.concat([y] * 20, ignore_index=True)

        X_train, X_test, y_train, y_test = split_train_test(X_big, y_big, test_size=0.2)
        total = len(X_big)
        assert len(X_test) == pytest.approx(total * 0.2, abs=2)

    def test_no_data_leakage(self, sample_df):
        """تأكد مفيش data leakage بين train و test"""
        df = drop_unnecessary_columns(sample_df.copy())
        df = encode_categoricals(df)
        X, y = split_features_target(df)

        X_big = pd.concat([X] * 20, ignore_index=True)
        y_big = pd.concat([y] * 20, ignore_index=True)

        X_train, X_test, _, _ = split_train_test(X_big, y_big)
        train_indices = set(X_train.index)
        test_indices = set(X_test.index)
        assert len(train_indices & test_indices) == 0
