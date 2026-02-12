from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import requests

# Professional Privacy-Focused Branding
# Colors: Navy (#0D1B2A), Safe Green (#2ECC71), Alert Red (#E74C3C)
PRIMARY_COLOR = "#0D1B2A"
SECONDARY_COLOR = "#1B263B"
ACCENT_COLOR = "#2ECC71"

class PrivacySentinelApp(App):
    def build(self):
        self.title = "Privacy Sentinel AI"
        Window.clearcolor = get_color_from_hex(PRIMARY_COLOR)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        header = Label(
            text="🛡️ Privacy Sentinel",
            font_size='32sp',
            bold=True,
            size_hint_y=None,
            height=100,
            color=get_color_from_hex("#FFFFFF")
        )
        layout.add_widget(header)
        
        # Status Card
        self.status_label = Label(
            text="Background Monitoring: ACTIVE",
            font_size='18sp',
            color=get_color_from_hex(ACCENT_COLOR)
        )
        layout.add_widget(self.status_label)
        
        # Risk Display
        self.risk_label = Label(
            text="Latest Scan: No risks detected",
            italic=True,
            color=get_color_from_hex("#BDC3C7")
        )
        layout.add_widget(self.risk_label)
        
        # Action Buttons
        btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        
        scan_btn = Button(
            text="Manual Policy Scan",
            background_color=get_color_from_hex("#3498DB"),
            background_normal=''
        )
        scan_btn.bind(on_press=self.manual_scan)
        btn_layout.add_widget(scan_btn)
        
        upgrade_btn = Button(
            text="Upgrade to PRO ($1/mo)",
            background_color=get_color_from_hex(ACCENT_COLOR),
            background_normal=''
        )
        upgrade_btn.bind(on_press=self.initiate_upgrade)
        btn_layout.add_widget(upgrade_btn)
        
        layout.add_widget(btn_layout)
        
        return layout

    def manual_scan(self, instance):
        self.risk_label.text = "Scanning clipboard content..."
        # Logic to send clipboard content to API

    def initiate_upgrade(self, instance):
        # Trigger Mobile Money Integration
        print("Initiating Mobile Money Checkout...")

if __name__ == "__main__":
    PrivacySentinelApp().run()
