from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox

class AppException(ABC, Exception):

    @abstractmethod
    def show(self):
        pass

class AppWarning(AppException):

    def show(self):
        messagebox.showwarning("Advertencia", str(self))

class AppError(AppException):

    def show(self):
        messagebox.showerror("Error", str(self))
        