# src/components/posts.py
from supabase import Client

def create_post(supabase: Client, user_id: str, plant: str, image_url: str):
    supabase.table("posts").insert({
        "user_id": user_id,
        "plant": plant,
        "image_url": image_url,
        "likes": 0
    }).execute()

def get_posts(supabase: Client):
    response = supabase.table("posts").select("*").execute()
    return response.data

def like_post(supabase: Client, post_id: int, user_id: str):
    # 簡易的な実装：いいね数をインクリメント
    post = supabase.table("posts").select("likes").eq("id", post_id).execute().data[0]
    new_likes = post["likes"] + 1
    supabase.table("posts").update({"likes": new_likes}).eq("id", post_id).execute()