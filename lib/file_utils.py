def save_csv(df, path, msg=""):
    df.to_csv(path, index=False)
    if msg:
        print(f"✅ {msg} salvato in: {path}")