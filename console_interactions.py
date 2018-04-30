import interactions as session
import main_instances as mio

class ConsoleSession:
    current_user = None
    current_session = None

    @staticmethod
    def start():
        print("PYTHON TRACKER\n Hello! Please, introduce yourself")
        usename = input()
        ConsoleSession.current_user = mio.Author(usename)
        ConsoleSession.current_session = session.SessionManager(ConsoleSession.current_user)
        print("\n Great, nice to meet you, "+usename+"!")

    @staticmethod
    def console_create_task():
        print("!!!Task creation")
        name = input("Input the single_word unique name for your task:")
        message = input("Specify description:")
        str_path = input("Now carefully input the path, separate with /")
        path = str_path.split("/")
        t1 = mio.Task(name,message,ConsoleSession.current_user, None)
        ConsoleSession.current_session.add_task(t1, path)

    @staticmethod
    def console_print_w_shirinu():
        print("W SHIRINU!!!!")
        for i in ConsoleSession.current_session.main_task.poisk_w_shirinu():
            print(i)

    @staticmethod
    def console_command_listener():

        while(True):
            command = input("tracker>>> ")
            if(command.lower() == "add"):
                ConsoleSession.console_create_task()
            elif command.lower() == "print_all":
                ConsoleSession.console_print_w_shirinu()
