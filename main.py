import json
from lib2to3.pgen2 import token
import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest

# set window size
Window.size=(300,450)
HOST_URL='http://127.0.0.1:8000/'
class LoginApp(MDApp):
    dialog = None
    def build(self):
        # define theme colors
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Blue"
        
        if os.stat("token.json").st_size != 0:
            with open('token.json') as f:
                data = json.load(f)
                result = data['token']
                print(result,'----------------------')
                token =  result
                headers = {'Content-type': 'application/json',
                           'Accept': 'application/json',
                           'x-auth-token': token}
                req = UrlRequest(HOST_URL+'api/user', method='GET',
                                 on_success=self.user_home_welcome,
                                 on_failure=self.login(),  on_error=self.error_response,req_headers=headers)
        else:
            self.login()
        # load and return kv string
        return Builder.load_file('login.kv')
    
    
    
   
    def user_home_welcome(self, result, req):
        

        result = req
        
        if os.stat("token.json").st_size == 0:
            with open('token.json', 'w') as outfile:
                # result={"token":req}
                json.dump(result, outfile)
        else:
            with open("token.json", "r+") as jsonFile:
                data = json.load(jsonFile)

                data["token"] = req
            result.update(data)

        
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
            
            
        print('home')
        # self.root.ids.spinner_verify.active = False
        # self.root.ids.spinner_login.active = False
        # self.root.ids.scr_mngr.current = 'user_home'
    
    def login(self):
        # check entered username and password
        params = json.dumps({'email': self.root.ids.user.text, 'password': self.root.ids.password.text})
        headers = {'Content-type': 'application/json',
                   'Accept': 'application/json'}
        req = UrlRequest(HOST_URL+'api/login', method='POST',on_failure=self.error_response , on_error=self.error_response, on_success=self.user_home_welcome, req_body=params,
                         req_headers=headers)
        print(req )
       
        
        
        # if self.root.ids.user.text=='admin' and self.root.ids.password.text=='admin123':
        #     if not self.dialog:
        #         # create dialog
        #         self.dialog = MDDialog(
        #             title="Log In",
        #             text=f"Welcome {self.root.ids.user.text}!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Ok", text_color=self.theme_cls.primary_color,
        #                     on_release=self.close
        #                 ),
        #             ],
        #         )
        #     # open and display dialog
        #     self.dialog.open()
            
    
        # self.root.ids.spinner_verify.active = False
        # self.root.ids.spinner_login.active = False
        # self.root.ids.scr_mngr.current = 'user_home'
    
    
    def close(self, instance):
        # f = open('token.json', 'r+')
        # f.truncate(0)
        self.root.ids.scr_mngr.current = 'user_login'
        # close dialog
        self.dialog.dismiss()
        
    def error_response(self, req, response_obj):
        print(req)
        print(response_obj)   
         
    def user_logout(self):
        f = open('token.json', 'r+')
        f.truncate(0)
        self.root.ids.scr_mngr.current = 'user_login'


# run app    
LoginApp().run()