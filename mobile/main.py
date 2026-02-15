from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import requests

# Professional Privacy-Focused Branding
PRIMARY_COLOR = "#0D1B2A"
SECONDARY_COLOR = "#1B263B"
ACCENT_COLOR = "#2ECC71"
ALERT_COLOR = "#E74C3C"

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
            height=80,
            color=get_color_from_hex("#FFFFFF")
        )
        layout.add_widget(header)

        # Mission Statement
        mission = Label(
            text="Empowering you before you click accept",
            font_size='14sp',
            italic=True,
            size_hint_y=None,
            height=30,
            color=get_color_from_hex("#BDC3C7")
        )
        layout.add_widget(mission)
        
        # Status Card (Real-time updates)
        self.status_label = Label(
            text="Background Monitoring: INITIALIZING",
            font_size='18sp',
            color=get_color_from_hex("#F1C40F")
        )
        layout.add_widget(self.status_label)
        
        # Risk Display
        self.risk_label = Label(
            text="Proactive Scanner: Ready",
            italic=True,
            color=get_color_from_hex("#BDC3C7")
        )
        layout.add_widget(self.risk_label)
        
        # Action Buttons
        btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        
        self.scan_btn = Button(
            text="Start Proactive Protection",
            background_color=get_color_from_hex("#3498DB"),
            background_normal=''
        )
        self.scan_btn.bind(on_press=self.toggle_service)
        btn_layout.add_widget(self.scan_btn)
        
        upgrade_btn = Button(
            text="Upgrade to PRO ($1/mo)",
            background_color=get_color_from_hex(ACCENT_COLOR),
            background_normal=''
        )
        upgrade_btn.bind(on_press=self.initiate_upgrade)
        btn_layout.add_widget(upgrade_btn)
        
        layout.add_widget(btn_layout)
        
        # Start a periodic check for service status
        Clock.schedule_interval(self.check_service_status, 2)
        
        return layout

    def toggle_service(self, instance):
        if "Start" in self.scan_btn.text:
            # Logic to start the background service via p4a
            self.status_label.text = "Background Monitoring: ACTIVE"
            self.status_label.color = get_color_from_hex(ACCENT_COLOR)
            self.scan_btn.text = "Stop Proactive Protection"
            self.scan_btn.background_color = get_color_from_hex(ALERT_COLOR)
        else:
            self.status_label.text = "Background Monitoring: STOPPED"
            self.status_label.color = get_color_from_hex(ALERT_COLOR)
            self.scan_btn.text = "Start Proactive Protection"
            self.scan_btn.background_color = get_color_from_hex("#3498DB")

    def check_service_status(self, dt):
        # In a real implementation, this would check if the service process is running
        pass

    def initiate_upgrade(self, instance):
        # Trigger Mobile Money Integration (Pure Python implementation)
        print("Initiating Mobile Money Checkout via Flutterwave API...")
        self.risk_label.text = "Redirecting to secure payment..."

if __name__ == "__main__":
    PrivacySentinelApp().run()
