import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.login import LoginForm

if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()
