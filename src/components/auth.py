# src/components/auth.py
from supabase import Client
import streamlit as st

def signup(supabase: Client, email: str, password: str):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.session is None:
            # メール確認が必要な場合
            st.info("サインアップが完了しました。メールに送信されたリンクからアカウントを有効化してください。")
            return None  # セッションがないため、ログイン状態にはしない
        else:
            # セッションがある場合（メール確認が不要な場合）
            supabase.auth.set_session(response.session.access_token, response.session.refresh_token)
            return response.user
    except Exception as e:
        st.error(f"サインアップエラー: {str(e)}")
        return None

def login(supabase: Client, email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        supabase.auth.set_session(response.session.access_token, response.session.refresh_token)
        return response.user
    except Exception as e:
        st.error(f"ログインエラー: {str(e)}")
        return None

def logout(supabase: Client):
    supabase.auth.sign_out()