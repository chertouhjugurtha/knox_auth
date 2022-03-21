import json
import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest

# set window size
Window.size=(300,450)
HOST_URL='localhost:8000/'
class LoginApp(MDApp):
    dialog = None
    def build(self):
        # define theme colors
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Blue"
        # load and return kv string
        return Builder.load_file('login.kv')
    
    def user_home_welcome(self, result, req):
        result = req['token']
        if os.stat("token.json").st_size == 0:
            with open('token.json', 'w') as outfile:
                json.dump(result, outfile)
        self.root.ids.spinner_verify.active = False
        self.root.ids.spinner_login.active = False
        self.root.ids.scr_mngr.current = 'user_home'
    
    def login(self):
        # check entered username and password
        params = json.dumps({'email': self.root.ids.user.text, 'password': self.root.ids.password.text})
        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json'}
        req = UrlRequest(HOST_URL+'api/accounts/signup/', method='POST', on_success=self.user_verify_email,
                         on_failure=self.user_register_error, req_body=params,
                         req_headers=headers)
        print(self.root.ids.user.text)
        if self.root.ids.user.text=='admin' and self.root.ids.password.text=='admin123':
            if not self.dialog:
                # create dialog
                self.dialog = MDDialog(
                    title="Log In",
                    text=f"Welcome {self.root.ids.user.text}!",
                    buttons=[
                        MDFlatButton(
                            text="Ok", text_color=self.theme_cls.primary_color,
                            on_release=self.close
                        ),
                    ],
                )
            # open and display dialog
            self.dialog.open()
    def close(self, instance):
        # close dialog
        self.dialog.dismiss()
# run app    
LoginApp().run()