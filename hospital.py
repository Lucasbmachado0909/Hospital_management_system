import pickle
import tkinter as tk
from tkinter import messagebox
from tkinter import *

class Person:
    def __init__(self, first_name, last_name, email, contact, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.password = password

    def display(self):
        return f"Name: {self.first_name} {self.last_name}\nContact: {self.contact}\nEmail: {self.email}"

class Patient(Person):
    def __init__(self, first_name, last_name, email, contact, password, patient_id, age, gender, medical_history):
        super().__init__(first_name, last_name, email, contact, password)
        self.patient_id = patient_id
        self.age = age
        self.gender = gender
        self.medical_history = medical_history

    def display(self):
        base_info = super().display()
        return (f"{base_info}\nPatient ID: {self.patient_id}\nAge: {self.age}\nGender: {self.gender}\n"
                f"Medical History: {self.medical_history}")

class Doctor(Person):
    def __init__(self, first_name, last_name, email, contact, password, doctor_id, specialization, availability):
        super().__init__(first_name, last_name, email, contact, password)
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.availability = availability

    def display(self):
        base_info = super().display()
        return (f"{base_info}\nDoctor ID: {self.doctor_id}\nSpecialization: {self.specialization}\n"
                f"Availability: {self.availability}")
class Appointment:
    def __init__(self, doctor, patient, date, time, notes=""):
        self.doctor = doctor
        self.patient = patient
        self.date = date
        self.time = time
        self.notes = notes

    def display(self):
        return (f"Doctor: {self.doctor.first_name} {self.doctor.last_name}\n"
                f"Patient: {self.patient.first_name} {self.patient.last_name}\n"
                f"Date: {self.date}\nTime: {self.time}\nNotes: {self.notes}")

myDoctorsList = []
myPatientsList = []
appointments = []


def load_patients(): #David
    try:
        with open("patient_info.dat", "rb") as f:
            while True:
                try:
                    patient = pickle.load(f)
                    myPatientsList.append(patient)
                except EOFError:
                    break
    except FileNotFoundError:
        with open("patient_info.dat", "wb") as f:
            pass


def load_doctors(): #David
    try:
        with open("doctor_info.dat", "rb") as f:
            while True:
                try:
                    doctor = pickle.load(f)
                    myDoctorsList.append(doctor)
                except EOFError:
                    break
    except FileNotFoundError:
        with open("doctor_info.dat", "wb") as f:
            pass

def create_account(): #David
    def toggle_fields():
        if account_type.get() == "patients":
            patient_fields_frame.pack()
            doctor_fields_frame.pack_forget()
        elif account_type.get() == "doctors":
            doctor_fields_frame.pack()
            patient_fields_frame.pack_forget()

    def submit_account():
        user_type = account_type.get()
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        email = entry_email.get()
        contact = entry_contact.get()
        user_id = entry_id.get()
        password = entry_password.get()
        reenter_password = entry_reenter_password.get()

        if not all([first_name, last_name, email, contact, user_id, password, reenter_password]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != reenter_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if user_type == "patients":
            age = entry_age.get()
            gender = gender_type_label.get()
            medical_history = entry_medical_history.get()

            if not all([age, gender, medical_history]):
                messagebox.showerror("Error", "All patient fields are required.")
                return

            new_patient = Patient(first_name, last_name, email, contact, password, user_id, age, gender, medical_history)
            myPatientsList.append(new_patient)
            with open("patient_info.dat", "ab") as f:
                pickle.dump(new_patient, f)

            messagebox.showinfo("Success", "Patient account created successfully!")

        elif user_type == "doctors":
            specialization = entry_specialization.get()
            availability = entry_availability.get()

            if not all([specialization, availability]):
                messagebox.showerror("Error", "All doctor fields are required.")
                return

            new_doctor = Doctor(first_name, last_name, email, contact, password, user_id, specialization, availability)
            myDoctorsList.append(new_doctor)
            with open("doctor_info.dat", "ab") as f:
                pickle.dump(new_doctor, f)

            messagebox.showinfo("Success", "Doctor account created successfully!")

        create_account_window.destroy()



    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create Account")
    create_account_window.geometry("1920x1080")

    tk.Label(create_account_window, text="Account Type: ").pack()
    account_type = tk.StringVar(value="patients")
    tk.Radiobutton(create_account_window, text="Patient", variable=account_type, value="patients",
                   command=toggle_fields).pack()
    tk.Radiobutton(create_account_window, text="Doctor", variable=account_type, value="doctors",
                   command=toggle_fields).pack()

    tk.Label(create_account_window, text="First Name: ").pack()
    entry_first_name = tk.Entry(create_account_window)
    entry_first_name.pack()

    tk.Label(create_account_window, text="Last Name: ").pack()
    entry_last_name = tk.Entry(create_account_window)
    entry_last_name.pack()

    tk.Label(create_account_window, text="Email: ").pack()
    entry_email = tk.Entry(create_account_window)
    entry_email.pack()

    tk.Label(create_account_window, text="Contact: ").pack()
    entry_contact = tk.Entry(create_account_window)
    entry_contact.pack()

    tk.Label(create_account_window, text="ID: ").pack()
    entry_id = tk.Entry(create_account_window)
    entry_id.pack()

    tk.Label(create_account_window, text="Password: ").pack()
    entry_password = tk.Entry(create_account_window, show="*")
    entry_password.pack()

    tk.Label(create_account_window, text="Re-enter Password: ").pack()
    entry_reenter_password = tk.Entry(create_account_window, show="*")
    entry_reenter_password.pack()

    patient_fields_frame = tk.Frame(create_account_window)
    tk.Label(patient_fields_frame, text="Age: ").pack()
    entry_age = tk.Entry(patient_fields_frame)
    entry_age.pack()

    tk.Label(patient_fields_frame, text="Gender: ").pack()
    gender_type_label = tk.StringVar(value="")
    tk.Radiobutton(patient_fields_frame, text="Male", variable=gender_type_label, value="male").pack()
    tk.Radiobutton(patient_fields_frame, text="Female", variable=gender_type_label, value="female").pack()
    tk.Radiobutton(patient_fields_frame, text="None", variable=gender_type_label, value="none").pack()

    tk.Label(patient_fields_frame, text="Medical History: ").pack()
    entry_medical_history = tk.Entry(patient_fields_frame)
    entry_medical_history.pack()

    doctor_fields_frame = tk.Frame(create_account_window)
    tk.Label(doctor_fields_frame, text="Specialization: ").pack()
    entry_specialization = tk.Entry(doctor_fields_frame)
    entry_specialization.pack()

    tk.Label(doctor_fields_frame, text="Availability: ").pack()
    entry_availability = tk.Entry(doctor_fields_frame)
    entry_availability.pack()

    toggle_fields()

    tk.Button(create_account_window, text="Submit", command=submit_account).pack()

def load_appointments(): #Layth
    try:
        with open("appointments.dat", "rb") as f:
            while True:
                try:
                    appointment = pickle.load(f)
                    appointments.append(appointment)
                except EOFError:
                    break
    except FileNotFoundError:
        with open("appointments.dat", "wb") as f:
            pass

def reschedule_appointment(index): #David
    reschedule_window = tk.Toplevel(root)
    reschedule_window.title("Reschedule Appointment")
    reschedule_window.geometry("400x300")

    tk.Label(reschedule_window, text="New Date (YYYY-MM-DD): ").pack(pady=5)
    entry_new_date = tk.Entry(reschedule_window)
    entry_new_date.pack(pady=5)

    tk.Label(reschedule_window, text="New Time (HH:MM): ").pack(pady=5)
    entry_new_time = tk.Entry(reschedule_window)
    entry_new_time.pack(pady=5)

    def save_reschedule():
        new_date = entry_new_date.get()
        new_time = entry_new_time.get()

        if not new_date or not new_time:
            messagebox.showerror("Error", "Both Date and Time are required.")
            return

        appointments[index].date = new_date
        appointments[index].time = new_time

        with open("appointments.dat", "wb") as f:
            for appt in appointments:
                pickle.dump(appt, f)

        messagebox.showinfo("Success", "Appointment rescheduled successfully!")
        reschedule_window.destroy()

    tk.Button(reschedule_window, text="Save", command=save_reschedule).pack(pady=10)

def open_user_window(user): #Layth
    user_window = tk.Toplevel(root)
    user_window.title(f"Welcome, {user.first_name}")
    user_window.geometry("1920x1080")

    tk.Label(user_window, text=user.display(), justify=tk.LEFT, anchor="w").pack(fill=tk.BOTH, padx=10, pady=10)

    if isinstance(user, Patient):
        tk.Label(user_window, text="Your Appointments", font=("Arial", 14)).pack(pady=10)

        appointments_frame = tk.Frame(user_window)
        appointments_frame.pack(fill=tk.BOTH, expand=True)

        for appt in appointments:
            if appt.patient == user:
                appointment_text = appt.display()
                tk.Label(appointments_frame, text=appointment_text, justify=tk.LEFT, anchor="w",
                         relief=tk.SUNKEN, pady=5).pack(fill=tk.BOTH, padx=5, pady=5)

        tk.Label(user_window, text="Schedule a New Appointment", font=("Arial", 14)).pack(pady=10)

        tk.Label(user_window, text="Doctor Name: ").pack()
        entry_doctor_name = tk.Entry(user_window)
        entry_doctor_name.pack()

        tk.Label(user_window, text="Date (YYYY-MM-DD): ").pack()
        entry_date = tk.Entry(user_window)
        entry_date.pack()

        tk.Label(user_window, text="Time (HH:MM): ").pack()
        entry_time = tk.Entry(user_window)
        entry_time.pack()

        tk.Label(user_window, text="Notes: ").pack()
        entry_notes = tk.Entry(user_window)
        entry_notes.pack()

        def schedule_appointment():
            doctor_name = entry_doctor_name.get()
            date = entry_date.get()
            time = entry_time.get()
            notes = entry_notes.get()

            if not all([doctor_name, date, time]):
                messagebox.showerror("Error", "All fields are required.")
                return

            doctor = next((doc for doc in myDoctorsList if f"{doc.first_name} {doc.last_name}" == doctor_name), None)
            if not doctor:
                messagebox.showerror("Error", "Doctor not found.")
                return

            new_appointment = Appointment(doctor, user, date, time, notes)
            appointments.append(new_appointment)
            with open("appointments.dat", "ab") as f:
                pickle.dump(new_appointment, f)

            messagebox.showinfo("Success", "Appointment scheduled successfully!")
            user_window.destroy()

        tk.Button(user_window, text="Schedule", command=schedule_appointment).pack(pady=10)

    elif isinstance(user, Doctor):
        tk.Label(user_window, text="Your Appointments", font=("Arial", 14)).pack(pady=10)
        appointments_frame = tk.Frame(user_window)
        appointments_frame.pack(fill=tk.BOTH, expand=True)

        for index, appt in enumerate(appointments):
            if appt.doctor == user:
                appointment_text = appt.display()
                tk.Label(appointments_frame, text=appointment_text, justify=tk.LEFT, anchor="w",
                         relief=tk.SUNKEN, pady=5).pack(fill=tk.BOTH, padx=5, pady=5)

                reschedule_button = tk.Button(appointments_frame, text="Reschedule",
                                              command=lambda idx=index: reschedule_appointment(idx))
                reschedule_button.pack(pady=5)

def login(): #Lucas
    def submit_login():
        user_id = entry_user_id.get()
        password = entry_password.get()
        for patient in myPatientsList:
            if patient.patient_id == user_id and patient.password == password:
                login_window.destroy()
                open_user_window(patient)
                return

        for doctor in myDoctorsList:
            if doctor.doctor_id == user_id and doctor.password == password:
                login_window.destroy()
                open_user_window(doctor)
                return

        messagebox.showerror("Login Error", "Invalid ID or password.")

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x300")

    tk.Label(login_window, text="User ID: ").pack(pady=5)
    entry_user_id = tk.Entry(login_window)
    entry_user_id.pack(pady=5)

    tk.Label(login_window, text="Password: ").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=submit_login)
    login_button.pack(pady=20)
load_patients()
load_doctors()
load_appointments()

#Lucas
root = tk.Tk()
root.config(bg="lightblue")
root.geometry("1000x800")
welcome_label = tk.Label(root, text="Welcome to Hospital Management System", font=("Times New Roman", 20),
                         bg="lightblue")
welcome_label.pack(pady=20)
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)
create_account_button = tk.Button(root,text="Create Account", command=create_account)
create_account_button.pack(pady=10)
root = Canvas(root, width= 1920, height=1080)
root.pack()
image = PhotoImage(file="C:\\Users\\borge\\OneDrive\\Imagens\\health-care-.png")
root.create_image(0, 0, anchor= NW, image=image)
root.mainloop()