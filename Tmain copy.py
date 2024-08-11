from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.clock import Clock
from kivy.animation import Animation
import requests
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle


#♣Main_url = "http://localhost:5000/"
Main_url = "http://151.71.87.181/"


class FluorescentToggleButton(Button):
    is_active = BooleanProperty(False)
    active_color = ListProperty([0, 1, 1, 1])
    inactive_color = ListProperty([0.3, 0.3, 0.3, 1])
    circle_position = NumericProperty(0)  # Position of the circle, between 0 and 1
    button_label_color = ListProperty([1, 1, 1, 1])  # Default color for button label
    posX = NumericProperty(defaultvalue=0.2)  # Horizontal position using pos_hint

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 0, 1)  # Set the text color to yellow
        self.size_hint = (None, None)
        self.size = (400, 100)  # Increase width of the button
        self.pos_hint = {'center_x': self.posX, 'center_y': 0.5}
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bind(on_press=self.toggle)

        # Properties for animation
        self.fluorescent_effect = False
        self.fluorescent_animation = None
        self.fluorescent_color = [0, 1, 1, 0.5]
        self.circle_animation = None
        self.circle_position = 0

        # Button label widget
        self.label = Label(text=self.text, color=self.button_label_color, font_size='18sp')
        self.bind(text=self.update_label_text)

    def update_label_text(self, instance, value):
        self.label.text = value

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_active:
                Color(*self.active_color)
                print("66")
            else:
                Color(*self.inactive_color)
                print("69")
            RoundedRectangle(size=self.size, pos=self.pos, radius=[50])
            if self.fluorescent_effect:
                print("70")
                Color(*self.fluorescent_color)
                RoundedRectangle(size=(self.width * 1.2, self.height * 1.2),
                                pos=(self.x - self.width * 0.1, self.y - self.height * 0.1), radius=[50])
            Color(1, 1, 1, 1)
            print("75")
            Ellipse(size=(self.height * 0.8, self.height * 0.8),
                    pos=(self.x + self.circle_position * (self.width - self.height * 0.8),
                         self.y + self.height * 0.1))
            self.label.color = self.button_label_color  # Set button label color
            self.label.pos = (self.center_x - self.label.texture_size[0] / 2,
                            self.center_y - self.label.texture_size[1] / 2)
            print("82")
            self.canvas.ask_update()  # Force canvas update

    def toggle(self, *args):
        self.is_active = not self.is_active
        print("84     toggling   ")
        # Toggle fluorescent effect
        self.fluorescent_effect = True
        print("92 self.fluorescent_animation  prima ", self.fluorescent_animation)
        if self.fluorescent_animation:
            self.fluorescent_animation.cancel()
            print("89 prima ")
        print("90 prima ")
        self.fluorescent_animation = Clock.schedule_once(self.reset_fluorescent_effect, 0.5)
        print(" 97 self.fluorescent_animation  dopo ", self.fluorescent_animation)

        # Move the circle animation
        if self.circle_animation:
            print("94 prima ")
            self.circle_animation.cancel(self)
        target_position = 1 if self.is_active else 0
        self.circle_animation = Animation(circle_position=target_position, duration=0.2)
        self.circle_animation.start(self)

    def reset_fluorescent_effect(self, dt):
        print(" 102 ")
        self.fluorescent_effect = False
        self.update_canvas()


class AddScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.label = MDLabel(text="Aggiungi un nuovo Toggle", halign="center", theme_text_color="Primary")
        self.layout.add_widget(self.label)
        self.text_input = MDTextField(hint_text="Nome del Toggle", size_hint=(0.8, None), height="30dp", pos_hint={"center_x": 0.5})
        self.layout.add_widget(self.text_input)
        self.submit_button = MDRaisedButton(text="Submit", size_hint=(0.8, None), height="50dp", pos_hint={"center_x": 0.5})
        self.submit_button.bind(on_press=self.submit_data)
        self.layout.add_widget(self.submit_button)
        self.back_button = MDRaisedButton(text="Back to Toggle", size_hint=(0.8, None), height="50dp", pos_hint={"center_x": 0.5})
        self.back_buttonH = MDRaisedButton(text="Back to Home", size_hint=(0.8, None), height="50dp", pos_hint={"center_x": 0.5})
        self.back_button.bind(on_press=self.goto_main_screen)
        self.back_buttonH.bind(on_press= lambda instance: setattr(self.manager,  'current', 'main'))
                            
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.back_buttonH)
        self.add_widget(self.layout)

    def submit_data(self, instance):
        toggle_name = self.text_input.text
        print(" 285 toggle_name " ,toggle_name)
        #url = "http://localhost:5000/add"
        url =Main_url+"add"
        print(" 123 url= ",url)
        
        
        
        data = {"buttonLabel": toggle_name}
        headers = {'User-Agent': 'MyKivyApp'}
        print("290 kivy ")
        login_screen = self.manager.get_screen('login')
        response = login_screen.session.post(url, json=data, headers=headers)
        print("290 kivy ")
        if response.status_code == 200:
            print("Toggle 295  aggiunto con successo.")
        else:
            print("Errore nell'aggiungere il Toggle.")
############################################
    def submit_form(self, instance):
        print(" 416    submit_form  collegato al  Toggle ")
        url = Main_url+"toggle"
        print(" 147 Main_url+'toggle' ",url)
        url = Main_url+"toggle"
        print(" 152 Main_url+'toggle' ",url)        
        headers = {'User-Agent': 'MyKivyApp'}
        # Utilizza la sessione creata durante il login
        login_screen = self.manager.get_screen('login')
        response = login_screen.session.get(url, headers=headers)
        print("536  submit response ",response)
        print(response.json()['button_labels'])
        if response.status_code == 200:
            print(response.json()['num_buttons'])
            # Richiesta GET riuscita
            self.manager.get_screen('toggle').update_buttons( response.json()['num_buttons'],response.json()['button_labels'],response.json()['button_states'])
            self.manager.current = 'toggle'
        else:
            # Gestisci errore nella richiesta GET
            print("Failed to toggle.")
# #################################################

    def goto_main_screen(self, instance):
        print("line 166")
        url = Main_url+"toggle"
        headers = {'User-Agent': 'MyKivyApp'}
        # Utilizza la sessione creata durante il login
        login_screen = self.manager.get_screen('login')
        response = login_screen.session.get(url, headers=headers)
        print("536  submit response ",response)
        print(response.json()['button_labels'])
        if response.status_code == 200:
            print(response.json()['num_buttons'])
            # Richiesta GET riuscita
            self.manager.get_screen('toggle').update_buttons( response.json()['num_buttons'],response.json()['button_labels'],response.json()['button_states'])
            self.manager.current = 'toggle'
        else:
            # Gestisci errore nella richiesta GET
            print("Failed to toggle.")
class ColoredBoxLayout(FloatLayout):
    def __init__(self, background_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
class pColoredBoxLayout(BoxLayout):
    def __init__(self, background_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
#################################
class WWColoredBoxLayout(BoxLayout):
    background_color = ListProperty([1, 1, 1, 1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class WWToggleScreen(Screen):
    def __init__(self, **kwargs):
        print(" line 177 WWToggleScreen")
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')
        # Create ScrollView
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.button_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        self.button_layout.bind(minimum_height=self.button_layout.setter('height'))
        # Add button_layout to ScrollView
        self.scroll_view.add_widget(self.button_layout)
        float_layout = ColoredBoxLayout(size_hint_y=None, height=150, background_color=(1, 1, 1, 1))
        logout_button = Button(
            text="Logout", size_hint=(None, None),size=(dp(150), dp(60)),
            pos_hint={"center_x": 0.1, "center_y": 0.3},
            font_size = '40dp',
            background_color=(0.4, 0.2, 12 / 255, 1),
            color=(1, 0, 1, 1)
        )
        logout_button.bind(on_press=self.logout)
        float_layout.add_widget(logout_button)
        submit_label = Label(
            text="Aggiorna Toggle", size_hint=(None, None),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            color=(1, 0, 75, 1), font_size='40sp'
        )
        float_layout.add_widget(submit_label)
        submit_button = Button(
            text='Aggiorna', size_hint=(None, None),
            pos_hint={"center_x": 0.85, "center_y": 0.3},
            width=200, height=60,font_size = '40dp',
            background_color=(2 / 255, 5, 12 / 255, 1), color=(0, 0, 1, 1)
        )
        submit_button.bind(on_press=self.submit_form)
        float_layout.add_widget(submit_button)
        add_button = Button(
            text='Aggiungi', size_hint=(None, None),
            pos_hint={"center_x": 0.4, "center_y": 0.3},
            width=150, height=60,font_size = '40dp',
            size=(dp(150), dp(60)),
            background_color=(0.8,0.4, 0, 0.8), color=(0,1,0.4, 1)
        )
        add_button.bind(on_press=self.goto_add_screen)
        float_layout.add_widget(add_button)
        Back_button = Button(
            text='BackTo Home', size_hint=(None, None),
            pos_hint={"center_x": 0.15, "center_y": 0.7},
            font_size = '35dp',
            size=(dp(220), dp(60)),
            background_color=(.3, 1,.4,0.6), color=(0, 0, 0, 1)
        )
        Back_button.bind(on_press=self.goto_home)
        float_layout.add_widget(Back_button)
        self.main_layout.add_widget(float_layout)
        
        ##  il Main screen 
        self.add_widget(self.main_layout)
    def goto_home(self,instance):
        self.manager.current = 'main'
    def update_buttons(self, num_buttons, button_labels, button_states):
        self.num_buttons = num_buttons
        self.button_labels = button_labels
        self.button_states = button_states
        print("  558  linee ")
        self.update_layout()

    def Aupdate_buttons(self, num_buttons, button_labels, button_states):
        self.num_buttons = num_buttons
        self.button_labels = button_labels
        self.button_states = button_states
        self.update_layout()
        
    def submit_form(self, instance):       
        print("642  linee ")        
        url = Main_url+"toggle"
        headers = {'User-Agent': 'MyKivyApp'}
        login_screen = self.manager.get_screen('login')
        response = login_screen.session.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            num_buttons = data['num_buttons']
            button_labels = data['button_labels']
            button_states = data.get('button_states', ['off'] * num_buttons)            
            print(" line 654 num_buttons ", num_buttons )
            print(" line 655 button_labels ", button_labels)
            print(" line 656 ")
            self.Aupdate_buttons(num_buttons, button_labels, button_states)
        else:
            print("Failed to fetch toggle data.")

    def update_layout(self):
        self.button_layout.clear_widgets()
        print("  577  linee ")
        
        if self.scroll_view.parent:
            self.scroll_view.parent.remove_widget(self.scroll_view)
        predefined_colors = [
            (1, 0, 0, 1),  # Red
            (0, 1, 0, 1),  # Green
            (0, 0, 1, 1)   # Blue
        ]
        print( " line  586 self.num_buttons =  ",self.num_buttons )
        #print( len(button_labels))
        for i in range(self.num_buttons):
            # Capture the current index in a variable
            current_index = i
            # Set background color
            if i < len(predefined_colors):
                background_color = predefined_colors[i]
            else:
                background_color = (0, 1 / (i + 2), 1 / (i + 1), 1)
            horizontal_layout = ColoredBoxLayout(size_hint_y=None, height=dp(150), background_color=background_color)
            posX = "0.2"
            # Configure the button
            button = FluorescentToggleButton(
                text=f"{self.button_labels[i]} - {'ON' if self.button_states[i] == 'on' else 'OFF'}",
                button_label_color=(1, 1, 0, 1),font_size = '35dp',
                pos_hint={'center_y': 0.5, 'x': posX}  # Set horizontal position using posX
            )
            button.size_hint = (None, None)
            button.size = (dp(300), dp(100))
            button.is_active = self.button_states[i] == 'on'
            button.circle_position = 1 if button.is_active else 0
            # Use 'current_index' to avoid late binding issues
            button.bind(on_press=lambda btn, idx=current_index: self.toggle_state(btn, idx))
            # Configure the label
            label = Label(
                text=f"Button {i+1}  hello from label",
                size_hint_x=None,
                width=dp(200),
                height=dp(100),
                color=(1,0,1, 1),
                font_size = '40dp',
                halign='center',
                valign='middle',
                pos_hint={'center_y': 0.4, 'x': 0.55} 
            )
            label.size_hint = (None, None)  # Set size_hint to ensure it's not ignored
            label.width = dp(200)  # Set fixed width
            label.height = dp(100)  # Set fixed height
            data_label = Label(text=f"{self.button_labels[i]}", size_hint_y=None, height=dp(50))
            # Add the button and label to the horizontal layout
            horizontal_layout.add_widget(button)
            horizontal_layout.add_widget(label)
            # , size_hint=(None, None),size=(dp(150), dp(60)),
            submiton = Button(
                text='Elimina', size_hint=(None, None),
                pos_hint={"center_x": 0.6, "center_y": 0.7},
                width=200, height=50,font_size = '40dp',
                background_color=(1,1,0,1), color=(1, 0, 0, 1)
            )
            submiton.bind(on_press=lambda instance, hl=horizontal_layout, btn=button, lbl=label, dl=data_label, sbm=submiton: self.delete_button(hl, btn, lbl, dl, sbm))
            horizontal_layout.add_widget(submiton)
            # Add the horizontal layout to the main layout
            self.button_layout.add_widget(horizontal_layout)
        self.main_layout.add_widget(self.scroll_view)
    def delete_button(self, horizontal_layout, button, label, data_label, submiton):
        toggle_name = data_label.text  # Use the passed label argument
        login_screen = self.manager.get_screen('login')
        url = Main_url+"remove"
        data = {"buttonLabel": toggle_name}
        headers = {'User-Agent': 'MyKivyApp'}
        response = login_screen.session.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Toggle removed successfully.")
            ### Optionally, you can remove the button from the UI here
            horizontal_layout.remove_widget(button)
            horizontal_layout.remove_widget(label)
            horizontal_layout.remove_widget(data_label)
            horizontal_layout.remove_widget(submiton)
            self.button_layout.remove_widget(horizontal_layout) # Rimuove il box di bottone 
        
        ###### self.button_layout.remove_widget(horizontal_layout) # Rimuove il box di bottone 
        else:
            print("Error removing the toggle.")
        print(" 7 62 Toggle removed successfully.")
        ###### self.button_layout.remove_widget(horizontal_layout) # Rimuove il box di bottone 
    
    def toggle_state(self, btn, idx):
        current_state = self.button_states[idx]
        new_state = 'off' if current_state == 'on' else 'on'
        self.button_states[idx] = new_state
        btn.text = f"{self.button_labels[idx]} - {'ON' if new_state == 'on' else 'OFF'}"
        url = Main_url+"state"
        data = {
            "buttonId": idx,
            "state": new_state,
            "buttonLabel": self.button_labels[idx]
        }
        headers = {'User-Agent': 'MyKivyApp'}
        login_screen = self.manager.get_screen('login')
        response = login_screen.session.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("State updated successfully.")
        else:
            print("Failed to update state.")

    def logout(self, instance):
        url = Main_url+"logout"
        headers = {'User-Agent': 'MyKivyApp'}
        login_screen = self.manager.get_screen('login')
        response = login_screen.session.get(url, headers=headers)
        if response.status_code == 200:
            print("Logged out successfully.")
            login_screen.session.cookies.clear()
            self.manager.current = 'login'
        else:
            print("Logout failed.")
    def goto_add_screen(self, instance):
        self.manager.current = 'add'
class KColoredBoxLayout(BoxLayout):
    def __init__(self, background_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
class MainScreen(Screen):
    num_buttons_input = ObjectProperty(None)
    button_labels_container = ObjectProperty(None)
    welcome_label = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.labels = []  # Inizializza l'attributo labels
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        # Num buttons input section
        num_buttons_box = KColoredBoxLayout(orientation='horizontal', size_hint_y=None, height=80, background_color=(.2, 0.8, 0, 1))  # green
        float_layout = FloatLayout()
        num_buttons_label = Label(text="Number of Buttons:", color=(0, 1, 1, 1), font_size=54, size_hint=(None, None), size=(150, 250), pos_hint={'center_x': 0.2, 'center_y': 0.5})
        float_layout.add_widget(num_buttons_label)
        self.num_buttons_input = TextInput(hint_text="Enter number (1-10)", input_filter='int', size_hint=(None, None), size=(200, 30), pos_hint={'center_x': 0.6, 'center_y': 0.5})
        self.num_buttons_input.bind(text=self.update_button_labels)
        float_layout.add_widget(self.num_buttons_input)
        num_buttons_box.add_widget(float_layout)
        layout.add_widget(num_buttons_box)
        # Welcome label section
        welcome_box = BoxLayout(size_hint_y=None, height=dp(50))
        self.welcome_label = Label(text="Welcome, User", halign="center", font_size=44, color=(1, 0, 0, 1), size_hint_y=None, height=dp(120))
        welcome_box.add_widget(self.welcome_label)
        layout.add_widget(welcome_box)
        # Scroll view for button labels
        scroll_view_box = BoxLayout(orientation='horizontal')
        colored_box = ColoredBoxLayout(size=(10, 100), background_color=(0.4, 0.8, 0.3, 1))
        scroll_view = ScrollView(size_hint=(1, 1))
        self.button_labels_container = GridLayout(cols=2, spacing=10, size_hint_y=None, size_hint_x=None, width=dp(600))
        self.button_labels_container.bind(minimum_height=self.button_labels_container.setter('height'))
        scroll_view.add_widget(self.button_labels_container)
        colored_box.add_widget(scroll_view)
        scroll_view_box.add_widget(colored_box)
        scroll_view_box.add_widget(Widget(size_hint_x=None, width=dp(0)))
        layout.add_widget(scroll_view_box)
        # Submit button section
        submit_box = KColoredBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(100), background_color=(0, .3, .2, 1))  # Adjust height if needed
        submit_label = Label(text="Toggle", color=(36/255, 1, 0, 1), font_size='20sp')  # Increase font size
        submit_button = Button(text='Toggle', size_hint=(None, None),pos_hint={"right":0.1,"top":1} , width=200, height=50, background_color=(0, 1, 102/255, 1), color=(1, 1, 1, 1))
        submit_button.bind(on_press=self.submit_form)
        submit_box.add_widget(submit_label)
        submit_box.add_widget(submit_button)
        #layout.add_widget(submit_box)
        submit_label = Label(text="Add new", color=(55, 55, 7/255, 1), font_size='20sp')  # Increase font size
        submit_button = Button(text='Add botton', size_hint=(None, None),pos_hint={"right":0.1,"top":1} , width=200, height=50, background_color=(5, 7/255, 12/255, 1), color=(1, 1, 1, 1))
        
        #submit_button.bind(on_press=self.submit_form)
        submit_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'add'))

        
        submit_box.add_widget(submit_label)
        submit_box.add_widget(submit_button)
        toggle_label = Label(text=" Submit ", color=(1, 0, 7/255, 1), font_size='20sp')  # Increase font size
        #toggle_button = FluorescentToggleButton(text='Toggle')
        toggle_button = Button(text=' Submit ', size_hint=(None, None), width=200, height=50, background_color=(1, .2, 0.4, 1), color=(0, 1, 1, 1))
        toggle_button.bind(on_press=self.goto_toggle)
        submit_box.add_widget(toggle_label)
        submit_box.add_widget(toggle_button)
        layout.add_widget(submit_box)
        

        self.add_widget(layout)
    def goto_toggle(self, instance):
        button_labels = [label.text for label in self.labels]
        num_buttons = len(button_labels)
        url = Main_url+"toggle"
        data = {
            'num_buttons': num_buttons,
            'button_labels': button_labels
        }
        
        print(" 518 url ",url)
        print(" 520  data  = ",data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # Utilizza la sessione creata durante il login
        response = self.manager.get_screen('login').session.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Dati inviati con successo
            print("response.json()['num_buttons']      358 ")
        else:
            # Gestisci errore nell'invio dei dati
            print("Failed to send data.")
        button_states = num_buttons*["on"]
        print(" 391  ", button_states)
        self.manager.get_screen('toggle').update_buttons(self.num_buttons, button_labels,button_states)
        #self.manager.get_screen('toggle').update_buttons(self.num_buttons)
        self.manager.current = 'toggle'

    def update_button_labels(self, instance, value):
        self.button_labels_container.clear_widgets()
        self.labels = []  # Assicurati di reimpostare self.labels
        if value.isdigit():
            num_buttons = int(value)
            self.button_labels_container.height = dp(40) * num_buttons
            for i in range(1, num_buttons + 1):
                label = Label(text=f"Button {i} Label:", size_hint_y=None, height=30)
                input_field = TextInput(hint_text=f"Button {i} Label", size_hint_y=None, height=30)
                self.button_labels_container.add_widget(label)
                self.button_labels_container.add_widget(input_field)
                self.labels.append(input_field)
            self.num_buttons = num_buttons

    def submit_form(self, instance):
        print(" 416    submit_form  collegato al  Toggle ")
        url = Main_url+"toggle"
        headers = {'User-Agent': 'MyKivyApp'}
        # Utilizza la sessione creata durante il login
        login_screen = self.manager.get_screen('login')    
        response = login_screen.session.get(url, headers=headers)
        print("536  submit response ",response)
        print(response.json()['button_labels'])
        if response.status_code == 200:
            print(response.json()['num_buttons'])
            # Richiesta GET riuscita
            self.manager.get_screen('toggle').update_buttons( response.json()['num_buttons'],response.json()['button_labels'],response.json()['button_states'])
            self.manager.current = 'toggle'
        else:
            # Gestisci errore nella richiesta GET
            print("Failed to toggle.")


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=dp(50), spacing=dp(10))
        layout.add_widget(MDLabel(text="Login", halign="center", theme_text_color="Primary", font_style="H2"))
        self.email = MDTextField(hint_text="Email", size_hint=(None, None), size=(Window.width * 0.8, dp(50)))
        layout.add_widget(self.email)
        self.password = MDTextField(hint_text="Password", password=True, size_hint=(None, None), size=(Window.width * 0.8, dp(50)))
        layout.add_widget(self.password)
        self.login_btn = MDRaisedButton(text="Login", size_hint=(None, None), size=(Window.width * 0.4, dp(50)), on_press=self.login)
        layout.add_widget(self.login_btn)
        self.message = MDLabel(halign="center", theme_text_color="Error")
        layout.add_widget(self.message)
        self.add_widget(layout)
        
    def wlogin(self, instance):
        email = self.email.text
        password = self.password.text        
        data = {'email': email, 'password': password}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # Crea una sessione per gestire i cookie
        self.session = requests.Session()
        # Effettua la richiesta POST per il login
        print("/***************  588 ******")
        response = self.session.post(Main_url+'loginPg', json=data, headers=headers)
        if response.status_code == 200:
            # Login riuscito, cambia schermata
            self.manager.current = 'main'
        else:
            # Login fallito, gestisci l'errore
            print("Login failed. Invalid credentials.")
    def login(self, instance):
        data = {'email':"sharifleeon@yahoo.com", 'password': "leeon1234"}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.session = requests.Session()
        print("/***************  600 ******")
        response = self.session.post(Main_url+'loginPg', json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                self.manager.current = 'main'
            else:
                self.message.text = result['message']
        else:
            self.message.text = "Server error, please try again later."
class ToggleApp(MDApp):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(WWToggleScreen(name='toggle'))
        sm.add_widget(AddScreen(name='add'))
        return sm

if __name__ == '__main__':
    ToggleApp().run()
