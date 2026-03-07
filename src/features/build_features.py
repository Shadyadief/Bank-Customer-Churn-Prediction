import pandas as pd
import numpy as np # noqa: F401


def add_balance_salary_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """
    نسبة الـ Balance للـ EstimatedSalary —
    بتعبّر عن مدى اعتماد العميل على رصيده.
    """
    df['Balance_Salary_Ratio'] = df['Balance'] / (df['EstimatedSalary'] + 1)
    return df


def add_products_per_tenure(df: pd.DataFrame) -> pd.DataFrame:
    """
    عدد المنتجات لكل سنة — بتعبّر عن مدى engagement العميل.
    """
    df['Products_Per_Tenure'] = df['NumOfProducts'] / (df['Tenure'] + 1)
    return df


def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
    """
    تقسيم العمر لمجموعات — عشان نعبّر عن العلاقة غير الخطية بين العمر والـ Churn.
    """
    df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[0, 30, 45, 60, 100],
        labels=['Young', 'Mid', 'Senior', 'Elder']
    )
    df = pd.get_dummies(df, columns=['Age_Group'], drop_first=True)
    return df


def add_is_zero_balance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag للعملاء اللي رصيدهم صفر.
    """
    df['Is_Zero_Balance'] = (df['Balance'] == 0).astype(int)
    return df


def build_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    تطبّق كل الـ Feature Engineering دفعة واحدة.
    """
    print("🔧 بدء Feature Engineering...")
    df = add_balance_salary_ratio(df)
    df = add_products_per_tenure(df)
    df = add_age_group(df)
    df = add_is_zero_balance(df)
    print(f"✅ انتهى — Shape بعد Feature Engineering: {df.shape}")
    return df


if __name__ == "__main__":
    import sys
    sys.path.append("../data")
    from load_data import load_raw_data
    from preprocess import drop_unnecessary_columns, encode_categoricals

    df = load_raw_data("data/raw/Churn_Modelling.csv")
    df = drop_unnecessary_columns(df)
    df = build_all_features(df)
    df = encode_categoricals(df)
    print(df.head())
