from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.clock import Clock
import sqlite3
import datetime
import random
import string

# 适配手机竖屏尺寸
Window.size = (720, 1280)
DB_NAME = "points_system.db"

# ---------------------- 数据库类（完全复刻原逻辑） ----------------------
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_tables()
        self.init_config()

    def init_tables(self):
        # 会员表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS member (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, phone TEXT UNIQUE NOT NULL,
            points INTEGER DEFAULT 0, level TEXT, reg_date TEXT,
            birthday TEXT, total_consume REAL DEFAULT 0
        )''')
        # 积分变动日志
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS points_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL, change_amount INTEGER NOT NULL,
            reason TEXT, related_id INTEGER, create_time TEXT,
            FOREIGN KEY (member_id) REFERENCES member (id) ON DELETE CASCADE
        )''')
        # 消费记录
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS consume_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL, amount REAL NOT NULL,
            points_earned INTEGER, create_time TEXT, remark TEXT,
            coupon_id INTEGER DEFAULT NULL, saved_amount REAL DEFAULT 0,
            FOREIGN KEY (member_id) REFERENCES member (id) ON DELETE CASCADE
        )''')
        # 礼品表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS reward (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, points_cost INTEGER NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0, description TEXT, status TEXT DEFAULT '上架'
        )''')
        # 实物兑换记录
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS exchange_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL, reward_id INTEGER NOT NULL,
            points_cost INTEGER NOT NULL, exchange_time TEXT, status TEXT DEFAULT '已完成',
            FOREIGN KEY (member_id) REFERENCES member (id) ON DELETE CASCADE,
            FOREIGN KEY (reward_id) REFERENCES reward (id)
        )''')
        # 优惠券表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, points_cost INTEGER NOT NULL,
            condition_amount REAL DEFAULT 0, discount_amount REAL DEFAULT 0,
            description TEXT, status TEXT DEFAULT '上架'
        )''')
        # 优惠券兑换记录
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupon_exchange (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL, coupon_id INTEGER NOT NULL,
            points_cost INTEGER NOT NULL, exchange_time TEXT, code TEXT UNIQUE,
            used INTEGER DEFAULT 0, used_at TEXT,
            FOREIGN KEY (member_id) REFERENCES member (id) ON DELETE CASCADE,
            FOREIGN KEY (coupon_id) REFERENCES coupon (id)
        )''')
        # 系统配置表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sys_config (
            config_key TEXT PRIMARY KEY, config_value TEXT
        )''')
        self.conn.commit()
        self.init_default_coupons()

    def init_config(self):
        if not self.get_config("points_ratio"):
            self.set_config("points_ratio", "1")
        if not self.get_config("auto_refresh_interval"):
            self.set_config("auto_refresh_interval", "30")

    def init_default_coupons(self):
        default_coupons = [
            ("8元无门槛券", 200, 0, 8, "无门槛使用"),
            ("15元满150元减券", 350, 150, 15, "满150元减15元"),
            ("25元满200元减券", 500, 200, 25, "满200元减25元"),
            ("35元满300元减券", 700, 300, 35, "满300元减35元"),
            ("50元满400元减券", 900, 400, 50, "满400元减50元")
        ]
        for name, points, cond, disc, desc in default_coupons:
            self.cursor.execute("SELECT id FROM coupon WHERE name=?", (name,))
            if not self.cursor.fetchone():
                self.cursor.execute(
                    "INSERT INTO coupon (name, points_cost, condition_amount, discount_amount, description) VALUES (?,?,?,?,?)",
                    (name, points, cond, disc, desc)
                )
        self.conn.commit()

    def get_config(self, key, default=None):
        self.cursor.execute("SELECT config_value FROM sys_config WHERE config_key = ?", (key,))
        row = self.cursor.fetchone()
        return row[0] if row else default

    def set_config(self, key, value):
        self.cursor.execute("REPLACE INTO sys_config (config_key, config_value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    # 会员等级计算
    def calc_level(self, points):
        if points < 200:
            return "普通会员"
        elif points < 500:
            return "铜牌会员"
        elif points < 1000:
            return "银牌会员"
        else:
            return "金牌会员"

    # 会员操作
    def add_member(self, name, phone, birthday=""):
        try:
            reg_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            level = self.calc_level(0)
            self.cursor.execute(
                "INSERT INTO member (name, phone, points, level, reg_date, birthday, total_consume) VALUES (?, ?, 0, ?, ?, ?, 0)",
                (name, phone, level, reg_date, birthday))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_members(self):
        self.cursor.execute("SELECT id, name, phone, points, level, reg_date, birthday, total_consume FROM member ORDER BY id DESC")
        return self.cursor.fetchall()

    def search_member(self, keyword):
        self.cursor.execute("SELECT id, name, phone, points, level, reg_date, birthday, total_consume FROM member WHERE name LIKE ? OR phone LIKE ?",
                            (f"%{keyword}%", f"%{keyword}%"))
        return self.cursor.fetchall()

    def get_member_by_phone_or_id(self, text):
        if text.isdigit():
            self.cursor.execute("SELECT id, name, phone, points, level FROM member WHERE id=? OR phone=?", (text, text))
        else:
            self.cursor.execute("SELECT id, name, phone, points, level FROM member WHERE phone=?", (text,))
        return self.cursor.fetchone()

    def consume_and_add_points(self, member_id, amount, remark, coupon_exchange_id=None, discount_amount=0):
        actual_amount = amount - discount_amount
        if actual_amount < 0:
            actual_amount = 0
        ratio = float(self.get_config("points_ratio", "1"))
        points_earned = int(actual_amount * ratio)
        self.cursor.execute("SELECT points, total_consume FROM member WHERE id=?", (member_id,))
        current_points, total_consume = self.cursor.fetchone()
        new_points = current_points + points_earned
        new_total = total_consume + actual_amount
        self.cursor.execute("UPDATE member SET points=?, total_consume=? WHERE id=?", (new_points, new_total, member_id))
        new_level = self.calc_level(new_points)
        self.cursor.execute("UPDATE member SET level=? WHERE id=?", (new_level, member_id))
        
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO consume_record (member_id, amount, points_earned, create_time, remark, coupon_id, saved_amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (member_id, actual_amount, points_earned, create_time, remark, coupon_exchange_id, discount_amount))
        self.conn.commit()
        return points_earned

    def manual_adjust_points(self, member_id, change_amount, reason):
        """手动调整会员积分"""
        self.cursor.execute("SELECT points FROM member WHERE id=?", (member_id,))
        current_points = self.cursor.fetchone()[0]
        new_points = current_points + change_amount
        if new_points < 0:
            new_points = 0
        self.cursor.execute("UPDATE member SET points=? WHERE id=?", (new_points, member_id))
        new_level = self.calc_level(new_points)
        self.cursor.execute("UPDATE member SET level=? WHERE id=?", (new_level, member_id))
        
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO points_log (member_id, change_amount, reason, create_time) VALUES (?, ?, ?, ?)",
                            (member_id, change_amount, reason, create_time))
        self.conn.commit()

    def add_reward(self, name, points_cost, stock, description=""):
        """添加礼品"""
        self.cursor.execute("INSERT INTO reward (name, points_cost, stock, description) VALUES (?, ?, ?, ?)",
                            (name, points_cost, stock, description))
        self.conn.commit()

    def get_statistics(self):
        """获取统计数据"""
        self.cursor.execute("SELECT COUNT(*) FROM member")
        total_members = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT SUM(points) FROM member")
        total_points = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute("SELECT SUM(amount) FROM consume_record")
        total_consume = self.cursor.fetchone()[0] or 0.0
        
        self.cursor.execute("SELECT COUNT(*) FROM exchange_record")
        total_exchange = self.cursor.fetchone()[0]
        
        return total_members, total_points, total_consume, total_exchange

# ---------------------- 界面UI模块（手机适配） ----------------------
class MemberTab(BoxLayout):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.orientation = "vertical"
        self.padding = 15
        self.spacing = 10

        # 标题
        self.add_widget(Label(text="会员管理", font_size=22, size_hint_y=None, height=50, bold=True))

        # 新增会员输入区
        self.name_input = TextInput(hint_text="会员姓名", size_hint_y=None, height=45)
        self.phone_input = TextInput(hint_text="手机号", size_hint_y=None, height=45)
        self.birth_input = TextInput(hint_text="生日(例:2000-01-01)", size_hint_y=None, height=45)
        self.add_widget(self.name_input)
        self.add_widget(self.phone_input)
        self.add_widget(self.birth_input)

        self.add_btn = Button(text="添加会员", size_hint_y=None, height=45, background_color=(0.2, 0.7, 0.3, 1))
        self.add_btn.bind(on_press=self.add_member)
        self.add_widget(self.add_btn)

        # 搜索区
        self.search_input = TextInput(hint_text="搜索姓名/手机号", size_hint_y=None, height=45)
        self.search_input.bind(text=self.refresh_list)
        self.add_widget(self.search_input)

        # 会员列表
        scroll = ScrollView(size_hint_y=1)
        self.list_layout = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll.add_widget(self.list_layout)
        self.add_widget(scroll)

        self.refresh_list()

    def add_member(self, instance):
        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()
        birth = self.birth_input.text.strip()
        if not name or not phone:
            self.show_popup("提示", "姓名和手机号不能为空")
            return
        if self.db.add_member(name, phone, birth):
            self.show_popup("成功", "会员添加完成")
            self.refresh_list()
            self.name_input.text = ""
            self.phone_input.text = ""
            self.birth_input.text = ""
        else:
            self.show_popup("失败", "手机号已存在")

    def refresh_list(self, *args):
        self.list_layout.clear_widgets()
        keyword = self.search_input.text.strip()
        if keyword:
            members = self.db.search_member(keyword)
        else:
            members = self.db.get_all_members()
        for m in members:
            info = f"ID:{m[0]} | {m[1]} | {m[2]}\n积分:{m[3]} | {m[4]} | 消费:{m[7]:.2f}"
            item = Label(text=info, size_hint_y=None, height=70, halign="left", font_size=14)
            self.list_layout.add_widget(item)

    def show_popup(self, title, msg):
        Popup(title=title, content=Label(text=msg), size_hint=(0.7, 0.3)).open()

class CashierTab(BoxLayout):
    def __init__(self, db, member_tab, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.member_tab = member_tab
        self.orientation = "vertical"
        self.padding = 15
        self.spacing = 10
        self.current_member = None

        self.add_widget(Label(text="收银台", font_size=22, size_hint_y=None, height=50, bold=True))

        self.phone_input = TextInput(hint_text="会员手机号/ID", size_hint_y=None, height=45)
        self.add_widget(self.phone_input)

        self.query_btn = Button(text="查询会员", size_hint_y=None, height=45, background_color=(0.2, 0.6, 0.8, 1))
        self.query_btn.bind(on_press=self.query_member)
        self.add_widget(self.query_btn)

        self.member_info = Label(text="会员信息：未查询", size_hint_y=None, height=60, font_size=14)
        self.add_widget(self.member_info)

        self.amount_input = TextInput(hint_text="消费金额", input_filter="float", size_hint_y=None, height=45)
        self.add_widget(self.amount_input)

        self.remark_input = TextInput(hint_text="备注", size_hint_y=None, height=45)
        self.add_widget(self.remark_input)

        self.pay_btn = Button(text="确认消费", size_hint_y=None, height=50, background_color=(0.2, 0.7, 0.3, 1))
        self.pay_btn.bind(on_press=self.do_consume)
        self.add_widget(self.pay_btn)

        self.adjust_btn = Button(text="手动调整积分", size_hint_y=None, height=45, background_color=(0.8, 0.4, 0.2, 1))
        self.adjust_btn.bind(on_press=self.open_adjust_popup)
        self.add_widget(self.adjust_btn)

    def query_member(self, instance):
        text = self.phone_input.text.strip()
        self.current_member = self.db.get_member_by_phone_or_id(text)
        if self.current_member:
            self.member_info.text = f"会员：{self.current_member[1]}\n积分：{self.current_member[3]} | 等级：{self.current_member[4]}"
        else:
            self.member_info.text = "未找到会员"

    def do_consume(self, instance):
        if not self.current_member:
            self.show_popup("提示", "请先查询会员")
            return
        try:
            amount = float(self.amount_input.text)
            if amount <= 0:
                raise ValueError
        except:
            self.show_popup("错误", "请输入有效消费金额")
            return
        remark = self.remark_input.text.strip()
        earn = self.db.consume_and_add_points(self.current_member[0], amount, remark)
        self.show_popup("成功", f"消费完成，获得{earn}积分")
        self.amount_input.text = ""
        self.remark_input.text = ""
        self.query_member(None)
        self.member_tab.refresh_list()

    def open_adjust_popup(self, instance):
        if not self.current_member:
            self.show_popup("提示", "请先查询会员")
            return
        box = BoxLayout(orientation="vertical", padding=15, spacing=10)
        pts_input = TextInput(hint_text="积分变动(正加负减)", input_filter="int", size_hint_y=None, height=45)
        reason_input = TextInput(hint_text="变动原因", size_hint_y=None, height=45)
        box.add_widget(pts_input)
        box.add_widget(reason_input)
        popup = Popup(title="调整积分", content=box, size_hint=(0.8, 0.4))
        def confirm(_):
            try:
                change = int(pts_input.text)
            except:
                self.show_popup("错误", "请输入有效整数")
                return
            self.db.manual_adjust_points(self.current_member[0], change, reason_input.text)
            self.show_popup("成功", "积分调整完成")
            popup.dismiss()
            self.query_member(None)
            self.member_tab.refresh_list()
        confirm_btn = Button(text="确认", size_hint_y=None, height=45)
        confirm_btn.bind(on_press=confirm)
        box.add_widget(confirm_btn)
        popup.open()

    def show_popup(self, title, msg):
        Popup(title=title, content=Label(text=msg), size_hint=(0.7, 0.3)).open()

class RewardTab(BoxLayout):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.orientation = "vertical"
        self.padding = 15
        self.spacing = 10

        self.add_widget(Label(text="礼品&优惠券管理", font_size=22, size_hint_y=None, height=50, bold=True))
        # 礼品添加
        self.r_name = TextInput(hint_text="礼品名称", size_hint_y=None, height=45)
        self.r_points = TextInput(hint_text="所需积分", input_filter="int", size_hint_y=None, height=45)
        self.r_stock = TextInput(hint_text="库存", input_filter="int", size_hint_y=None, height=45)
        self.add_widget(self.r_name)
        self.add_widget(self.r_points)
        self.add_widget(self.r_stock)
        self.add_btn = Button(text="添加礼品", size_hint_y=None, height=45, background_color=(0.2, 0.7, 0.3, 1))
        self.add_btn.bind(on_press=self.add_reward)
        self.add_widget(self.add_btn)

    def add_reward(self, instance):
        try:
            name = self.r_name.text.strip()
            pts = int(self.r_points.text)
            stock = int(self.r_stock.text)
            self.db.add_reward(name, pts, stock)
            self.show_popup("成功", "礼品添加完成")
            self.r_name.text = ""
            self.r_points.text = ""
            self.r_stock.text = ""
        except:
            self.show_popup("错误", "输入格式错误")

    def show_popup(self, title, msg):
        Popup(title=title, content=Label(text=msg), size_hint=(0.7, 0.3)).open()

class StatsTab(BoxLayout):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.orientation = "vertical"
        self.padding = 15
        self.spacing = 10
        self.add_widget(Label(text="数据统计", font_size=22, size_hint_y=None, height=50, bold=True))
        self.stats_label = Label(text="加载中...", font_size=16, size_hint_y=None, height=100)
        self.add_widget(self.stats_label)
        self.refresh_btn = Button(text="刷新统计", size_hint_y=None, height=45)
        self.refresh_btn.bind(on_press=self.refresh)
        self.add_widget(self.refresh_btn)
        self.refresh()

    def refresh(self, *args):
        tm, tp, tc, te = self.db.get_statistics()
        self.stats_label.text = f"总会员：{tm}\n总积分：{tp}\n总消费：{tc:.2f}元\n实物兑换：{te}次"

class SettingsTab(BoxLayout):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.orientation = "vertical"
        self.padding = 15
        self.spacing = 10
        self.add_widget(Label(text="系统设置", font_size=22, size_hint_y=None, height=50, bold=True))
        self.ratio_input = TextInput(hint_text="1元=?积分", text=self.db.get_config("points_ratio"), size_hint_y=None, height=45)
        self.add_widget(self.ratio_input)
        self.save_btn = Button(text="保存积分比例", size_hint_y=None, height=45)
        self.save_btn.bind(on_press=self.save_ratio)
        self.add_widget(self.save_btn)

    def save_ratio(self, instance):
        try:
            val = float(self.ratio_input.text)
            if val <= 0:
                raise ValueError
            self.db.set_config("points_ratio", str(val))
            Popup(title="成功", content=Label(text="保存完成"), size_hint=(0.7, 0.3)).open()
        except:
            Popup(title="错误", content=Label(text="请输入正数"), size_hint=(0.7, 0.3)).open()

# ---------------------- 主界面与APP入口 ----------------------
class MainTabPanel(TabbedPanel):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.tab_pos = "top"
        self.do_default_tab = False

        # 初始化所有标签页
        self.member_tab = MemberTab(db)
        self.cashier_tab = CashierTab(db, self.member_tab)
        self.reward_tab = RewardTab(db)
        self.stats_tab = StatsTab(db)
        self.settings_tab = SettingsTab(db)

        t1 = TabbedPanelItem(text="会员")
        t1.add_widget(self.member_tab)
        self.add_widget(t1)

        t2 = TabbedPanelItem(text="收银")
        t2.add_widget(self.cashier_tab)
        self.add_widget(t2)

        t3 = TabbedPanelItem(text="礼品")
        t3.add_widget(self.reward_tab)
        self.add_widget(t3)

        t4 = TabbedPanelItem(text="统计")
        t4.add_widget(self.stats_tab)
        self.add_widget(t4)

        t5 = TabbedPanelItem(text="设置")
        t5.add_widget(self.settings_tab)
        self.add_widget(t5)

        self.default_tab = t1

class PointsShopApp(App):
    def build(self):
        self.db = Database()
        return MainTabPanel(self.db)

if __name__ == "__main__":
    PointsShopApp().run()
