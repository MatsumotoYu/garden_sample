# src/components/location.py
import streamlit as st
import geocoder
from streamlit.components.v1 import html

def get_location():
    geolocation_script = """
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    position => {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
                            .then(response => response.json())
                            .then(data => {
                                const prefecture = data.address.state || data.address.region || "東京都";
                                window.Streamlit.setComponentValue(prefecture);
                            })
                            .catch(error => console.error('Error:', error));
                    },
                    error => {
                        console.error('Geolocation error:', error);
                        window.Streamlit.setComponentValue("東京都");
                    }
                );
            } else {
                window.Streamlit.setComponentValue("東京都");
            }
        }
        document.addEventListener("DOMContentLoaded", getLocation);
    </script>
    """
    location = html(geolocation_script, height=0, width=0)
    
    if not location or location == "東京都":
        try:
            g = geocoder.ip('me')
            if g.ok and g.state:
                return g.state
        except:
            pass
    
    return "東京都"

def location_selector():
    default_location = get_location()
    prefectures = [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
        "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
        "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
        "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
        "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
        "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ]
    st.write("位置情報に基づいて居住地を自動選択します。手動で変更可能です。")
    return st.selectbox("居住地", prefectures, index=prefectures.index(default_location) if default_location in prefectures else 0)