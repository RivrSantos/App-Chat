import time
import flet as ft

# classe remetente das mensagens
class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

# classe chat para configuraçoes e controles
class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown" 

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
            ft.colors.BLACK,
            ft.colors.WHITE,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "WORKCHAT"
    page.theme_mode = (ft.ThemeMode.LIGHT)
        # if page.theme_mode == ft.ThemeMode.LIGHT
        # else ft.ThemeMode.LIGHT)
        # c.label = ("Light theme" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme")
        # page.update()

        # page.theme_mode = ft.ThemeMode.LIGHT
        # c = ft.Switch(label="Light theme", on_change=theme_changed)
        # page.add(c)

    # ft.app(target=main)
    
    def set_android(e):
        page.platform = ft.PagePlatform.ANDROID
        page.update()

    def set_ios(e):
        page.platform = "ios"
        page.update()

    page.add(
        ft.Image(
            src=f"Black.png",
            width=220,
            height=90,
            expand= True,
            fit=ft.ImageFit.CONTAIN,
        ),
        # ft.Text('Escolha o dispositivo', color= 'PURPLE', expand= True),
        ft.ElevatedButton("Android", on_click=set_android, icon= ft.icons.ANDROID, color= 'WHITE',  bgcolor= 'PURPLE', width= 10, height= 30, expand= 0),
        ft.ElevatedButton("iOS", on_click=set_ios, icon= ft.icons.APPLE, color= 'WHITE', bgcolor= 'PURPLE', width= 10, height= 30, expand= 0),
        ft.Switch(label="ATIVAR SO", adaptive=True, width= 20, height= 20, label_position= 'LEFT'),
    )
    page.theme = ft.Theme(color_scheme_seed='BLUE')
    page.update()
    bg_container = ft.Ref[ft.Container]()

    def handle_color_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    def handle_on_hover(e):
        # print(f"{e.control.content.value}.on_hover")
        ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("BgColors"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Blue"),
                        leading=ft.Icon(ft.icons.COLORIZE),
                        style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.colors.BLUE}),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Green"),
                        leading=ft.Icon(ft.icons.COLORIZE),
                        style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.colors.GREEN}),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Red"),
                        leading=ft.Icon(ft.icons.COLORIZE),
                        style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.colors.RED}),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    )
                ]
            ),
        ]
    )

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} entrou no chat.",
                    message_type="login_message",
                )
            )
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    
    join_user_name = ft.TextField(
        label="Entre com seu nome ou apelido",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Bem vindo!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Entrar no chat", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Escreva sua mensagem...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        border_radius= 20,
        on_submit=send_message_click,
    )

    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius= 20,
            padding=15,
            expand=True,
            margin= 10,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Enviar messagem",
                    on_click=send_message_click,
                ),
            ]
        ),
    )


ft.app(target=main)
  