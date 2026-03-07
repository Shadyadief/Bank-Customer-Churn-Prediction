import pandas as pd
import os


def load_raw_data(path: str) -> pd.DataFrame:
    """
    تحمّل البيانات الخام من ملف CSV.

    Parameters:
        path (str): المسار الكامل لملف CSV

    Returns:
        pd.DataFrame: البيانات الخام
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"الملف مش موجود في المسار ده: {path}")

    df = pd.read_csv(path)
    print(f"✅ تم تحميل البيانات — Shape: {df.shape}")
    return df


def get_basic_info(df: pd.DataFrame) -> None:
    """
    تطبع معلومات أساسية عن الـ DataFrame.
    """
    print("\n📊 معلومات البيانات:")
    print(f"  الأبعاد: {df.shape}")
    print(f"  الأعمدة: {list(df.columns)}")
    print("\n🎯 توزيع الـ Target (Exited):")
    print(df['Exited'].value_counts())
    print("\n  النسب المئوية:")
    print((df['Exited'].value_counts(normalize=True) * 100).round(2))
    print("\n❓ القيم الناقصة:")
    print(df.isnull().sum())


if __name__ == "__main__":
    # ✅ absolute path بناءً على موقع الـ file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "raw", "Churn_Modelling.csv")
    df = load_raw_data(path)
    get_basic_info(df)
