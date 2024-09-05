import PySimpleGUI as sg
import command_parser.command_parser as parser


# this is for the theme of the window (Dark blue 2) https://pysimplegui.readthedocs.io/en/latest/call%20reference/#theme
# the size image box(600 is the width and 800 is the height)  https://pysimplegui.readthedocs.io/en/latest/call%20reference/#image-element
#  key of the image box source : https://docs.pysimplegui.com/en/latest/documentation/module/keys/
def create_game_window():
    sg.theme("Dark blue 2")
    layout = [
        [
            sg.Image(
                parser.location[parser.current_location]["Image"],
                size=(
                    600,
                    700,
                ),
                key="-IMG-",
            ),
            sg.Column(
                [
                    [
                        sg.Text(
                            parser.get_current_story()
                            + "\n"
                            + parser.get_available_commands(),
                            size=(
                                50,  # size of the text box(50 is the width and 12 is the height)
                                12,
                            ),
                            font="Any 14",
                            key="-OUTPUT-",
                        ),
                    ],
                    # font of the text box(Any is the font style and 14 is the size) https://pysimplegui.readthedocs.io/en/latest/call%20reference/#text-element
                    # this is for the key of the text box meaning it is the output of the text box.
                    [
                        sg.Text("Enter command", font="Any 14"),
                        sg.Input(key="-IN-", size=(20, 1), font="Any 14"),
                    ],
                    [sg.Button("Enter", bind_return_key=True), sg.Button("Quit")],
                ],
                element_justification="center",  # https://pysimplegui.readthedocs.io/en/latest/call%20reference/#column-element
                vertical_alignment="center",  #  https://pysimplegui.readthedocs.io/en/latest/call%20reference/#column-element
            ),
        ]
    ]

    return sg.Window("Jeu Mario Bros", layout, size=(1200, 700))


if __name__ == "__main__":
    window = create_game_window()
    while True:
        event, values = window.read()
        if event == "Enter":
            current_story = parser.game_play(values["-IN-"].lower())
            window["-OUTPUT-"].update(
                current_story + "\n\n" + parser.get_available_commands()
            )
            # source on how to update the text box on: https://pysimplegui.readthedocs.io/en/latest/call%20reference/#text-element
            # source on how to change img size in create_game_window() on: https://pysimplegui.readthedocs.io/en/latest/call%20reference/#image-element
            window["-IN-"].update("")
            window["-IMG-"].update(
                parser.location[parser.current_location]["Image"],
                size=(
                    600,
                    800,
                ),
            )

        elif event == "Quit" or event is None or event == sg.WIN_CLOSED:
            break

    window.close()
