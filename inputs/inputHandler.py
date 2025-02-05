from inputs.command import Command

class InputHandler:
    def __init__(self) -> None:
        self._commands: dict[int,Command] = {}

    def bind_command(self,command: Command,key: int):
        self._commands[key] = command

    def input_start(self,key):
        command = self._commands.get(key,None)

        if command:
            command.on_start()

    def input_triggered(self,key):
        command = self._commands.get(key,None)

        if command:
            command.on_triggered()