import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import pandas as pd
from datetime import datetime
import threading


class SerialMonitorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Serial Monitor")

        self.serial_instance = None
        self.is_running = False

        self.init_ui()

    def init_ui(self):
        # COM Port Selection
        self.port_label = ttk.Label(self.master, text="COM Port:")
        self.port_label.grid(column=0, row=0)

        self.port_combobox = ttk.Combobox(self.master)
        self.port_combobox['values'] = self.get_serial_ports()
        self.port_combobox.grid(column=1, row=0)

        # Baud Rate Selection
        self.baud_label = ttk.Label(self.master, text="Baud Rate:")
        self.baud_label.grid(column=2, row=0)

        self.baud_entry = ttk.Entry(self.master)
        self.baud_entry.insert(0, "9600")  # default value
        self.baud_entry.grid(column=3, row=0)

        # Control Buttons
        self.start_button = ttk.Button(self.master, text="Start", command=self.start_serial)
        self.start_button.grid(column=4, row=0)

        self.stop_button = ttk.Button(self.master, text="Stop", command=self.stop_serial)
        self.stop_button.grid(column=5, row=0)

        self.save_button = ttk.Button(self.master, text="Save", command=self.save_data)
        self.save_button.grid(column=6, row=0)

        # Serial Data Display
        self.serial_data_text = tk.Text(self.master, height=10, width=50)
        self.serial_data_text.grid(column=0, row=1, columnspan=7)

        # Made by Label
        self.made_by_label = ttk.Label(self.master, text="Made by Vedant K. Naik")
        self.made_by_label.grid(column=0, row=2, columnspan=7, sticky=tk.W)

        # Data Storage
        self.data = []

    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def read_serial(self):
        while self.is_running:
            if self.serial_instance.isOpen():
                try:
                    line = self.serial_instance.readline().decode('utf-8').rstrip()
                    self.data.append({'timestamp': datetime.now(), 'data': line})
                    self.serial_data_text.insert(tk.END, line + '\n')
                except Exception as e:
                    print("Error reading serial data:", e)

    def start_serial(self):
        try:
            self.serial_instance = serial.Serial(self.port_combobox.get(), self.baud_entry.get(), timeout=1)
            self.is_running = True
            self.thread = threading.Thread(target=self.read_serial)
            self.thread.start()
        except Exception as e:
            print("Error starting serial communication:", e)

    def stop_serial(self):
        if self.serial_instance and self.serial_instance.isOpen():
            self.is_running = False
            self.serial_instance.close()

    def save_data(self):
        if self.data:
            df = pd.DataFrame(self.data)
            filename = datetime.now().strftime('Session_%Y%m%d_%H%M%S.csv')
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("C:/Users/vnaik/PycharmProjects/pythonProject1/my_serial_icon.ico")
    app = SerialMonitorApp(root)
    root.mainloop()
