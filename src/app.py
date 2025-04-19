import sys
import os

# プロジェクトルートをモジュール検索パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from supabase import create_client
from src.components.auth import signup, login, logout
from src.components.advice import get_advice
from src.components.stores import get_stores
from src.components.posts import create_post, get_posts, like_post

# スタイルの読み込み
with open("src/style.css") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Supabase クライアントの初期化
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

# セッション状態の初期化
if "user" not in st.session_state:
    st.session_state.user = None

# タイトル
st.title("家庭菜園アプリ")

# サイドバー：ログイン/サインアップ/ログアウト
with st.sidebar:
    if st.session_state.user is None:
        st.subheader("ログイン / サインアップ")
        email = st.text_input("メールアドレス", key="email_input")
        password = st.text_input("パスワード", type="password", key="password_input")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("ログイン", key="login_button"):
                user = login(supabase, email, password)
                if user:
                    st.session_state.user = user
                    st.success("ログイン成功！")
                    st.rerun()
                else:
                    st.error("ログインに失敗しました。")
        with col2:
            if st.button("サインアップ", key="signup_button"):
                user = signup(supabase, email, password)
                if user:
                    st.session_state.user = user
                    st.success("サインアップ成功！")
                    st.rerun()
                else:
                    st.error("サインアップに失敗しました。")
    else:
        st.subheader(f"ようこそ、{st.session_state.user.email}！")
        if st.button("ログアウト", key="logout_button"):
            logout(supabase)
            st.session_state.user = None
            st.success("ログアウトしました。")
            st.rerun()

# メインコンテンツ
if st.session_state.user is None:
    st.write("ログインまたはサインアップしてください。")
else:
    # タブの設定
    tab1, tab2, tab3 = st.tabs(["ホーム", "投稿", "アドバイス"])

    # タブ1：ホーム
    with tab1:
        st.subheader("ようこそ！")
        st.write("投稿をシェアしたり、アドバイスをチェックしよう！")
        # 投稿フィードの表示
        posts = get_posts(supabase)
        if posts:
            st.markdown('<div class="grid">', unsafe_allow_html=True)
            for post in posts:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.image(post["image_url"], use_column_width=True)
                    st.markdown(f"<p>{post['plant']}</p>", unsafe_allow_html=True)
                    st.markdown('<div class="like-container">', unsafe_allow_html=True)
                    if st.button("♡", key=f"like_{post['id']}", help="いいね"):
                        like_post(supabase, post["id"], st.session_state.user.id)
                        st.rerun()
                    st.markdown(
                        f"<span class='like-count'>{post['likes']}</span>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.write("投稿がありません。")
        st.markdown("</div>", unsafe_allow_html=True)

    # タブ2：投稿
    with tab2:  # 94行目
        st.subheader("成長記録を投稿")  # 95行目：インデントを4スペース追加
        plant = st.selectbox(
            "植物",
            ["トマト", "キュウリ", "ナス", "ピーマン"],
            key="post_plant_selectbox",
        )
        image = st.file_uploader(
            "画像をアップロード", type=["jpg", "png", "jpeg"], key="post_image_uploader"
        )
        if st.button("投稿", key="submit_post_button"):
            if image:
                try:
                    # 画像を Supabase ストレージにアップロード
                    file_name = f"{st.session_state.user.id}_{image.name}"
                    supabase.storage.from_("images").upload(
                        file_name, image.read(), {"content-type": image.type}
                    )
                    image_url = supabase.storage.from_("images").get_public_url(
                        file_name
                    )
                    # 投稿をデータベースに保存
                    create_post(supabase, st.session_state.user.id, plant, image_url)
                    st.success("投稿しました！")
                    st.rerun()
                except Exception as e:
                    st.error(f"画像アップロードに失敗しました: {str(e)}")
            else:
                st.error("画像を選択してください。")

    # タブ3：アドバイス
    with tab3:
        st.subheader("栽培アドバイスと店舗情報")
        # 47都道府県リスト
        prefectures = [
            "北海道",
            "青森県",
            "岩手県",
            "宮城県",
            "秋田県",
            "山形県",
            "福島県",
            "茨城県",
            "栃木県",
            "群馬県",
            "埼玉県",
            "千葉県",
            "東京都",
            "神奈川県",
            "新潟県",
            "富山県",
            "石川県",
            "福井県",
            "山梨県",
            "長野県",
            "岐阜県",
            "静岡県",
            "愛知県",
            "三重県",
            "滋賀県",
            "京都府",
            "大阪府",
            "兵庫県",
            "奈良県",
            "和歌山県",
            "鳥取県",
            "島根県",
            "岡山県",
            "広島県",
            "山口県",
            "徳島県",
            "香川県",
            "愛媛県",
            "高知県",
            "福岡県",
            "佐賀県",
            "長崎県",
            "熊本県",
            "大分県",
            "宮崎県",
            "鹿児島県",
            "沖縄県",
        ]
        location = st.selectbox("居住地", prefectures, key="advice_location_selectbox")
        plant = st.selectbox(
            "植物",
            ["トマト", "キュウリ", "ナス", "ピーマン"],
            key="advice_plant_selectbox",
        )
        if st.button("アドバイスを取得", key="get_advice_button"):
            # 栽培アドバイスを取得
            advice = get_advice(location, plant)
            st.write("### 栽培アドバイス")
            st.write(advice)
            # 近隣店舗を取得
            stores = get_stores(location)
            if stores:
                st.write("### 近隣の園芸店")
                for store in stores:
                    st.write(f"- {store['store_name']} ({store['address']})")
                    st.write(f"  営業時間: {store['hours']}")
            else:
                st.write("近隣の店舗が見つかりませんでした。")
