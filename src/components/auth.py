# src/components/auth.py
from supabase import Client
import streamlit as st

def signup(supabase: Client, email: str, password: str):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        supabase.auth.set_session(response.session.access_token, response.session.refresh_token)  # セッションを設定
        return response.user
    except Exception as e:
        st.error(f"サインアップエラー: {str(e)}")
        return None

def login(supabase: Client, email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        supabase.auth.set_session(response.session.access_token, response.session.refresh_token)  # セッションを設定
        return response.user
    except Exception as e:
        st.error(f"ログインエラー: {str(e)}")
        return None

def logout(supabase: Client):
    supabase.auth.sign_out()