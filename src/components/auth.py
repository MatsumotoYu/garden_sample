# src/components/auth.py
from supabase import Client


from supabase import create_client


def signup(supabase: Client, email: str, password: str):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return response.user
    except Exception as e:
        st.error(f"サインアップエラー: {str(e)}")
        return None

def login(supabase: Client, email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return response.user
    except Exception as e:
        st.error(f"ログインエラー: {str(e)}")
        return None

def logout(supabase: Client):
    supabase.auth.sign_out()