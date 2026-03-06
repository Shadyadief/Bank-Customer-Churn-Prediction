import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import joblib
import os


# الأعمدة اللي هنشيلها لأنها مش مفيدة
COLS_TO_DROP = ['RowNumber', 'CustomerId', 'Surname']

# الأعمدة اللي هنعمل لها One-Hot Encoding
CATEGORICAL_COLS = ['Gender', 'Geography']

TARGET = 'Exited'


def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """تشيل الأعمدة اللي مش محتاجها."""
    df = df.drop(columns=COLS_TO_DROP, errors='ignore')
    print(f"✅ تم حذف الأعمدة: {COLS_TO_DROP}")
    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """تعمل One-Hot Encoding للأعمدة الكاتيجوريكال."""
    df = pd.get_dummies(df, columns=CATEGORICAL_COLS, drop_first=True)
    print(f"✅ تم عمل Encoding — Shape بعد Encoding: {df.shape}")
    return df


def split_features_target(df: pd.DataFrame):
    """تفصل الـ Features عن الـ Target."""
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    print(f"✅ X shape: {X.shape} | y shape: {y.shape}")
    return X, y


def split_train_test(X, y, test_size: float = 0.2, random_state: int = 42):
    """تقسّم البيانات لـ Train و Test."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"✅ Train: {X_train.shape} | Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test, save_path: str = "models/scaler.pkl"):
    """
    تعمل StandardScaler على الـ Features وتحفظ الـ Scaler.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(scaler, save_path)
    print(f"✅ تم عمل Scaling وحفظ الـ Scaler في: {save_path}")

    return X_train_scaled, X_test_scaled


def apply_smote(X_train, y_train, random_state: int = 42):
    """
    تطبّق SMOTE على بيانات التدريب لحل مشكلة الـ Imbalance.
    """
    print(f"قبل SMOTE: {y_train.value_counts().to_dict()}")
    smote = SMOTE(random_state=random_state)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
    print(f"بعد SMOTE:  {pd.Series(y_resampled).value_counts().to_dict()}")
    return X_resampled, y_resampled


def run_full_preprocessing(df: pd.DataFrame):
    """
    تشغّل كل خطوات الـ Preprocessing من أول لآخر.

    Returns:
        X_train_sm, X_test, y_train_sm, y_test, feature_names
    """
    df = drop_unnecessary_columns(df)
    df = encode_categoricals(df)

    X, y = split_features_target(df)
    feature_names = X.columns.tolist()

    X_train, X_test, y_train, y_test = split_train_test(X, y)
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test)
    X_train_sm, y_train_sm = apply_smote(X_train_scaled, y_train)

    return X_train_sm, X_test_scaled, y_train_sm, y_test, feature_names


if __name__ == "__main__":
    from load_data import load_raw_data
    df = load_raw_data("data/raw/Churn_Modelling.csv")
    X_train_sm, X_test, y_train_sm, y_test, features = run_full_preprocessing(df)
    print(f"\n🎯 جاهز للتدريب! X_train shape: {X_train_sm.shape}")
