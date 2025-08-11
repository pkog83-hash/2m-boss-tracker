import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd

# 頁面配置
st.set_page_config(
    page_title="🐉 天堂2M - BOSS重生追蹤器",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 樣式 (手機版適配 + 修正顏色問題)
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #2c3e50, #34495e);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .boss-table {
        border-radius: 8px;
        overflow: hidden;
    }
    
    .boss-info-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    .click-hint {
        text-align: center;
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        border: 1px solid #bbdefb;
    }
    
    /* 修正表格顏色對比問題 */
    div[data-testid="stDataFrame"] div[data-testid="stDataFrame"] > div {
        background-color: white;
    }
    
    /* 手機版適配 */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        
        .stButton > button {
            width: 100%;
            margin: 0.2rem 0;
        }
        
        div[data-testid="stDataFrame"] {
            font-size: 0.8rem;
        }
        
        .stSelectbox > div > div {
            font-size: 0.9rem;
        }
    }
    
    /* 隱藏Streamlit元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 表格行點擊效果 */
    .clickable-row {
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .clickable-row:hover {
        background-color: #f5f5f5 !important;
    }
</style>
""", unsafe_allow_html=True)

class BossTracker:
    def __init__(self):
        self.data_file = "boss_data.json"
        self.bosses = self.load_boss_data()
    
    def load_boss_data(self):
        """載入BOSS數據"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_bosses()
        else:
            return self.get_default_bosses()
    
    def get_default_bosses(self):
        """獲取默認BOSS列表"""
        return {
            "佩爾利斯": {"respawn_minutes": 120, "last_killed": None},
            "巴實那": {"respawn_minutes": 150, "last_killed": None},
            "采爾圖巴": {"respawn_minutes": 180, "last_killed": None},
            "潘納洛德": {"respawn_minutes": 180, "last_killed": None},
            "安庫拉": {"respawn_minutes": 210, "last_killed": None},
            "坦佛斯特": {"respawn_minutes": 210, "last_killed": None},
            "史坦": {"respawn_minutes": 240, "last_killed": None},
            "布賴卡": {"respawn_minutes": 240, "last_killed": None},
            "魔圖拉": {"respawn_minutes": 240, "last_killed": None},
            "特倫巴": {"respawn_minutes": 270, "last_killed": None},
            "提米特利斯": {"respawn_minutes": 300, "last_killed": None},
            "塔金": {"respawn_minutes": 300, "last_killed": None},
            "雷比魯": {"respawn_minutes": 300, "last_killed": None},
            "凱索思": {"respawn_minutes": 360, "last_killed": None},
            "巨蟻女王": {"respawn_minutes": 360, "last_killed": None},
            "卡雷斯": {"respawn_minutes": 360, "last_killed": None},
            "貝希莫斯": {"respawn_minutes": 360, "last_killed": None},
            "希瑟雷蒙": {"respawn_minutes": 360, "last_killed": None},
            "塔拉金": {"respawn_minutes": 420, "last_killed": None},
            "沙勒卡": {"respawn_minutes": 420, "last_killed": None},
            "梅杜莎": {"respawn_minutes": 420, "last_killed": None},
            "賽魯": {"respawn_minutes": 450, "last_killed": None},
            "潘柴特": {"respawn_minutes": 480, "last_killed": None},
            "突變克魯瑪": {"respawn_minutes": 480, "last_killed": None},
            "被汙染的克魯瑪": {"respawn_minutes": 480, "last_killed": None},
            "卡坦": {"respawn_minutes": 480, "last_killed": None},
            "提米妮爾": {"respawn_minutes": 480, "last_killed": None},
            "瓦柏": {"respawn_minutes": 480, "last_killed": None},
            "克拉奇": {"respawn_minutes": 480, "last_killed": None},
            "弗林特": {"respawn_minutes": 480, "last_killed": None},
            "蘭多勒": {"respawn_minutes": 480, "last_killed": None},
            "費德": {"respawn_minutes": 540, "last_killed": None},
            "寇倫": {"respawn_minutes": 600, "last_killed": None},
            "瑪杜克": {"respawn_minutes": 600, "last_killed": None},
            "薩班": {"respawn_minutes": 720, "last_killed": None},
            "核心基座": {"respawn_minutes": 720, "last_killed": None},
            "猛龍獸": {"respawn_minutes": 720, "last_killed": None},
            "黑色蕾爾莉": {"respawn_minutes": 720, "last_killed": None},
            "司穆艾爾": {"respawn_minutes": 720, "last_killed": None},
            "卡布里歐": {"respawn_minutes": 720, "last_killed": None},
            "安德拉斯": {"respawn_minutes": 720, "last_killed": None},
            "忘卻之鏡": {"respawn_minutes": 720, "last_killed": None},
            "納伊阿斯": {"respawn_minutes": 720, "last_killed": None},
            "希拉": {"respawn_minutes": 720, "last_killed": None},
            "姆夫": {"respawn_minutes": 720, "last_killed": None},
            "諾勒姆斯": {"respawn_minutes": 1080, "last_killed": None},
            "烏坎巴": {"respawn_minutes": 1080, "last_killed": None},
            "伊波斯": {"respawn_minutes": 1080, "last_killed": None},
            "凱都都": {"respawn_minutes": 1080, "last_killed": None},
            "伊格尼思": {"respawn_minutes": 1080, "last_killed": None},
            "奧爾芬": {"respawn_minutes": 1440, "last_killed": None},
            "哈普": {"respawn_minutes": 1440, "last_killed": None},
            "歐克斯": {"respawn_minutes": 1440, "last_killed": None},
            "塔那透斯": {"respawn_minutes": 1440, "last_killed": None},
            "鳳凰": {"respawn_minutes": 1440, "last_killed": None},
            "摩德烏斯": {"respawn_minutes": 1440, "last_killed": None},
            "霸拉克": {"respawn_minutes": 1440, "last_killed": None},
            "薩拉克斯": {"respawn_minutes": 1440, "last_killed": None},
            "巴倫": {"respawn_minutes": 1440, "last_killed": None},
            "黑卡頓": {"respawn_minutes": 1440, "last_killed": None},
            "拉何": {"respawn_minutes": 1980, "last_killed": None}
        }
    
    def save_boss_data(self):
        """保存BOSS數據"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.bosses, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            st.error(f"保存失敗: {e}")
            return False
    
    def calculate_respawn_info(self, boss_name, boss_data):
        """計算重生資訊"""
        if boss_data['last_killed'] is None:
            return "未擊殺", "等待擊殺", "⚪ 未記錄", "normal"
        
        try:
            last_killed = datetime.fromisoformat(boss_data['last_killed'])
            respawn_time = last_killed + timedelta(minutes=boss_data['respawn_minutes'])
            current_time = datetime.now()
            
            last_killed_str = last_killed.strftime('%m/%d %H:%M')
            respawn_time_str = respawn_time.strftime('%m/%d %H:%M')
            
            if current_time >= respawn_time:
                return last_killed_str, respawn_time_str, "✅ 已重生", "ready"
            else:
                time_left = respawn_time - current_time
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                if hours > 0:
                    status = f"⏳ {hours}h{minutes}m"
                else:
                    status = f"⏳ {minutes}m"
                return last_killed_str, respawn_time_str, status, "waiting"
                
        except Exception as e:
            return "錯誤", "錯誤", "❌ 錯誤", "error"
    
    def get_boss_dataframe(self):
        """獲取BOSS數據框"""
        # 按重生時間排序
        sorted_bosses = sorted(self.bosses.items(), key=lambda x: x[1]['respawn_minutes'])
        
        data = []
        for index, (boss_name, boss_data) in enumerate(sorted_bosses, 1):
            respawn_minutes = boss_data['respawn_minutes']
            hours = respawn_minutes // 60
            minutes = respawn_minutes % 60
            
            if hours > 0:
                respawn_time_str = f"{hours}h{minutes}m" if minutes > 0 else f"{hours}h"
            else:
                respawn_time_str = f"{minutes}m"
            
            last_killed_str, respawn_time_str_full, status, status_type = self.calculate_respawn_info(boss_name, boss_data)
            
            data.append({
                '編號': f"{index:02d}",
                'BOSS名稱': boss_name,
                '重生時間': respawn_time_str,
                '上次擊殺': last_killed_str,
                '下次重生': respawn_time_str_full,
                '狀態': status,
                '_status_type': status_type  # 用於樣式
            })
        
        return pd.DataFrame(data)
    
    def parse_time_string(self, time_str):
        """解析時間字串"""
        try:
            time_str = time_str.strip()
            formats = [
                "%Y/%m/%d %H:%M",
                "%m/%d %H:%M",
                "%Y-%m-%d %H:%M",
                "%m-%d %H:%M",
                "%Y/%m/%d %H:%M:%S",
                "%m/%d %H:%M:%S",
            ]
            
            for fmt in formats:
                try:
                    if fmt.startswith("%m/") or fmt.startswith("%m-"):
                        current_year = datetime.now().year
                        if "/" in time_str:
                            full_time_str = f"{current_year}/{time_str}"
                            parsed = datetime.strptime(full_time_str, fmt.replace("%m/", "%Y/%m/"))
                        else:
                            full_time_str = f"{current_year}-{time_str}"
                            parsed = datetime.strptime(full_time_str, fmt.replace("%m-", "%Y-%m-"))
                    else:
                        parsed = datetime.strptime(time_str, fmt)
                    
                    return parsed
                except ValueError:
                    continue
            
            return None
        except:
            return None

# 初始化
if 'boss_tracker' not in st.session_state:
    st.session_state.boss_tracker = BossTracker()

tracker = st.session_state.boss_tracker

# 主標題
st.markdown("""
<div class="main-header">
    <h1>🐉 天堂2M - BOSS重生追蹤器</h1>
    <p>📱 Web版 | 多人共享數據 | 手機版適配</p>
</div>
""", unsafe_allow_html=True)

# 當前時間顯示
current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
st.markdown(f"<div style='text-align: center; margin: 1rem 0; font-size: 1.1rem;'>⏰ 現在時間: {current_time}</div>", unsafe_allow_html=True)

# 獲取BOSS數據
df = tracker.get_boss_dataframe()

# 統計信息
total_bosses = len(df)
ready_bosses = len(df[df['狀態'].str.contains('✅')])
waiting_bosses = len(df[df['狀態'].str.contains('⏳')])

# 響應式佈局
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.metric("總BOSS數", total_bosses)

with col2:
    st.metric("已重生", ready_bosses)

with col3:
    st.metric("等待中", waiting_bosses)

with col4:
    st.metric("未記錄", total_bosses - ready_bosses - waiting_bosses)

# BOSS表格顯示
st.markdown("### 📊 BOSS狀態一覽")

# 使用原生顏色樣式，不額外設定避免衝突
display_df = df.drop('_status_type', axis=1)

# 使用 Streamlit 的原生表格顯示，避免樣式衝突
st.dataframe(
    display_df,
    use_container_width=True,
    height=400,
    column_config={
        "編號": st.column_config.TextColumn("編號", width="small"),
        "BOSS名稱": st.column_config.TextColumn("BOSS名稱", width="medium"), 
        "重生時間": st.column_config.TextColumn("重生時間", width="small"),
        "上次擊殺": st.column_config.TextColumn("上次擊殺", width="medium"),
        "下次重生": st.column_config.TextColumn("下次重生", width="medium"),
        "狀態": st.column_config.TextColumn("狀態", width="medium")
    }
)

# 點擊提示
st.markdown("""
<div class="click-hint">
    💡 <strong>操作說明</strong>：請使用下方選擇器選擇BOSS，然後點擊按鈕更新擊殺時間
</div>
""", unsafe_allow_html=True)

# 分隔線
st.markdown("---")

# 手動更新區域
st.markdown("### 📝 更新BOSS擊殺時間")

# 響應式佈局
col1, col2 = st.columns([2, 1])

with col1:
    # BOSS選擇
    boss_names = list(tracker.bosses.keys())
    
    # 根據重生時間排序BOSS名稱顯示
    sorted_boss_items = sorted(tracker.bosses.items(), key=lambda x: x[1]['respawn_minutes'])
    sorted_boss_names = [name for name, _ in sorted_boss_items]
    
    selected_boss = st.selectbox(
        "🎯 選擇要更新的BOSS",
        sorted_boss_names,
        index=0,
        key="boss_selector"
    )
    
    # 顯示選中BOSS信息
    if selected_boss:
        boss_data = tracker.bosses[selected_boss]
        current_record = "無記錄"
        if boss_data['last_killed']:
            try:
                dt = datetime.fromisoformat(boss_data['last_killed'])
                current_record = dt.strftime('%Y/%m/%d %H:%M')
            except:
                current_record = "格式錯誤"
        
        respawn_minutes = boss_data['respawn_minutes']
        hours = respawn_minutes // 60
        minutes = respawn_minutes % 60
        respawn_str = f"{hours}h{minutes}m" if minutes > 0 else f"{hours}h" if hours > 0 else f"{minutes}m"
        
        st.markdown(f"""
        <div class="boss-info-card">
            <strong>🎯 {selected_boss}</strong><br>
            <small>重生時間: {respawn_str} | 當前記錄: {current_record}</small>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # 快速操作按鈕
    st.markdown("#### ⚡ 快速操作")
    
    if st.button("🕐 記錄現在時間", use_container_width=True, type="primary"):
        if selected_boss:
            tracker.bosses[selected_boss]['last_killed'] = datetime.now().isoformat()
            if tracker.save_boss_data():
                st.success(f"✅ 已記錄 {selected_boss} 擊殺於 {datetime.now().strftime('%H:%M:%S')}")
                st.rerun()
    
    if st.button("🗑️ 清除此BOSS記錄", use_container_width=True):
        if selected_boss:
            tracker.bosses[selected_boss]['last_killed'] = None
            if tracker.save_boss_data():
                st.success(f"✅ 已清除 {selected_boss} 的記錄")
                st.rerun()

# 手動輸入時間
st.markdown("#### ⏰ 手動輸入擊殺時間")

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    time_input = st.text_input(
        "擊殺時間",
        placeholder="格式: 2025/08/11 16:30 或 08/11 16:30",
        help="支援多種格式：YYYY/MM/DD HH:MM 或 MM/DD HH:MM",
        key="time_input"
    )

with col2:
    if st.button("📅 填入現在", use_container_width=True):
        current_time_str = datetime.now().strftime("%Y/%m/%d %H:%M")
        st.session_state.time_input = current_time_str
        st.rerun()

with col3:
    if st.button("🧹 清空", use_container_width=True):
        st.session_state.time_input = ""
        st.rerun()

# 更新按鈕
if st.button("🎯 更新擊殺時間", use_container_width=True, type="secondary"):
    if not selected_boss:
        st.error("⚠️ 請選擇一個BOSS")
    elif not time_input.strip():
        # 清除記錄
        tracker.bosses[selected_boss]['last_killed'] = None
        if tracker.save_boss_data():
            st.success(f"✅ 已清除 {selected_boss} 的擊殺記錄")
            st.rerun()
    else:
        # 解析時間
        parsed_time = tracker.parse_time_string(time_input)
        if parsed_time is None:
            st.error("⚠️ 時間格式不正確！請使用：YYYY/MM/DD HH:MM 或 MM/DD HH:MM")
        else:
            tracker.bosses[selected_boss]['last_killed'] = parsed_time.isoformat()
            if tracker.save_boss_data():
                st.success(f"✅ 已更新 {selected_boss} 的擊殺時間為 {parsed_time.strftime('%Y/%m/%d %H:%M')}")
                # 清空輸入框
                st.session_state.time_input = ""
                st.rerun()

# 分隔線
st.markdown("---")

# 批量操作
st.markdown("### 🛠️ 系統功能")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 重新載入數據", use_container_width=True):
        st.session_state.boss_tracker = BossTracker()
        st.success("✅ 數據已重新載入")
        st.rerun()

with col2:
    if st.button("🗑️ 清除所有記錄", use_container_width=True, type="secondary"):
        # 二次確認
        if st.session_state.get('confirm_clear_all', False):
            for boss_name in tracker.bosses:
                tracker.bosses[boss_name]['last_killed'] = None
            if tracker.save_boss_data():
                st.success("✅ 已清除所有BOSS記錄")
                st.session_state.confirm_clear_all = False
                st.rerun()
        else:
            st.session_state.confirm_clear_all = True
            st.warning("⚠️ 請再次點擊確認清除所有記錄")

with col3:
    # 下載數據備份
    backup_data = json.dumps(tracker.bosses, ensure_ascii=False, indent=2)
    st.download_button(
        "💾 下載備份",
        backup_data,
        file_name=f"boss_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )

# 底部信息
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin: 2rem 0;'>
    <p>🎮 天堂2M BOSS重生追蹤器 - Web版 (修正版)</p>
    <p>📱 支援手機、平板、電腦 | 🌐 多人共享數據 | ⚡ 即時更新</p>
    <small>✅ 修正點擊問題 ✅ 修正顏色對比 ✅ 優化操作體驗</small>
</div>
""", unsafe_allow_html=True)