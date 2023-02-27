from samplebase import SampleBase
from RGBMatrixEmulator import graphics
import time


def getBetaStatement():  # this is a rigged beta test. used it during the ship showcase.
    choice = input(
        "Which beta would you like to see?\n1. Weather\n2. News\n3. Now Playing\n4. Minecraft\n5. Hack Club line\n6. Custom Input\n")

    if choice == "1":
        return "The weather in Coopersville, MI is 28 degrees, clear sky"
    elif choice == "2":
        return "Mardi Gras: Australia's PM Anthony Albanese first to join march"
    elif choice == "3":
        return "Now Playing: Never Gonna Give You Up by Rick Astley"
    elif choice == "4":
        return "MCEarth is online, player count of 1"
    elif choice == "5":
        return "Hello, Hack Club!"
    elif choice == "6":
        return input("Enter your custom input: ")
    else:
        print("Invalid choice")
        return getBetaStatement()


class RunText(SampleBase):  # tbh no clue what's going on here, stole this from hzeller
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel",
                                 default="Hello, Hack Club!")

    def run(self, newOut=True):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("7x13.bdf")
        textColor = graphics.Color(163, 171, 212)
        pos = offscreen_canvas.width

        while True:
            if newOut:  # is there something new?
                my_text = getBetaStatement()
                newOut = False

            offscreen_canvas.Clear()
            length = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            pos -= 1
            if pos + length < 0:
                newOut = True  # this one's over, get something new
                pos = offscreen_canvas.width
            time.sleep(0.03)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":  # wtf is __name__ and __main__ anyway?
    run_text = RunText()
    if not run_text.process:
        run_text.print_help()
