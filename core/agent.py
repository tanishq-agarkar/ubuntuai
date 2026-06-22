
import sys

import os



sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from core import llm, executor, logger, os_metrics





def main():

    print("\nUbuntu AI Assistant\n")



    history = []

    cwd = os.path.expanduser("~")



    while True:

        try:

            inp = input(f"[{os.path.basename(cwd) or cwd}] $ ").strip()

        except (EOFError, KeyboardInterrupt):

            print()

            break



        if inp.lower() in ("exit", "quit"):

            break



        if not inp:

            continue



        snap = str(os_metrics.fast_snapshot())



        data, raw = llm.interpret(

            f"{inp}\n[cwd:{cwd}][{snap}]",

            history

        )



        cmd = data.get("command", "").strip()



        if not cmd:

            continue



        res = executor.run(cmd, cwd=cwd)



        logger.log(

            inp,

            cmd,

            data.get("risk", "low"),

            res

        )



        # Handle directory changes

        if cmd.startswith("cd "):

            target = cmd[3:].strip("'\"")

            candidate = os.path.normpath(

                os.path.join(cwd, os.path.expanduser(target))

            )



            if os.path.isdir(candidate):

                cwd = candidate



        # Show command output only

        if res["stdout"]:

            print(res["stdout"], end="")



        if res["stderr"]:

            print(res["stderr"], end="")



        history = (

            history

            + [{"role": "user", "content": inp}]

            + [{"role": "assistant", "content": raw}]

        )[-10:]





if __name__ == "__main__":

    main()

