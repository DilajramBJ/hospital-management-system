# Hospital Management System

from datetime import datetime,timedelta,time
from collections import defaultdict
import json

specialist_ailments: dict[str, list[str]] = {
    "cardiologist": [
        "arrhythmia", "coronary artery disease", "heart attack", "high cholesterol", "hypertension"
    ],
    "dermatologist": [
        "acne", "eczema", "hair loss", "psoriasis", "rashes", "skin infections"
    ],
    "endocrinologist": [
        "diabetes", "hormonal imbalance", "metabolic disorders", "osteoporosis", "thyroid disorders"
    ],
    "ent specialist": [
        "ear infection", "hearing loss", "nasal polyps", "sinusitis", "sore throat", "tonsillitis"
    ],
    "gastroenterologist": [
        "acid reflux", "constipation", "gallstones", "gastritis", "hepatitis", "irritable bowel syndrome", "ulcers"
    ],
    "general physician": [
        "body aches", "cold", "cough", "fatigue", "fever", "headache", "nausea", "sore throat"
    ],
    "gynecologist": [
        "endometriosis", "fibroids", "infertility", "irregular bleeding", "menopause issues", "ovarian cysts",
        "pcos", "pid", "stis", "vaginal infections"
    ],
    "neurologist": [
        "alzheimer's disease", "epilepsy", "migraine", "multiple sclerosis", "parkinson's disease", "stroke"
    ],
    "oncologist": [
        "blood cancer", "cancer", "leukemia", "lymphoma", "melanoma", "sarcoma", "tumors"
    ],
    "ophthalmologist": [
        "cataracts", "dry eyes", "eye infections", "glaucoma", "macular degeneration", "vision problems"
    ],
    "orthopedic surgeon": [
        "arthritis", "back pain", "fractures", "joint pain", "scoliosis", "sports injuries"
    ],
    "pediatrician": [
        "childhood infections", "common cold", "ear infection", "growth disorders", "pediatric asthma", "vaccination"
    ],
    "psychiatrist": [
        "anxiety", "bipolar disorder", "depression", "insomnia", "ocd", "schizophrenia"
    ],
    "pulmonologist": [
        "asthma", "bronchitis", "copd", "lung cancer", "pneumonia", "sleep apnea", "tuberculosis"
    ],
    "urologist": [
        "bladder issues", "kidney infection", "kidney stones", "prostate problems", "urinary incontinence", "urinary tract infection"
    ]
}


class Doctor:
    def __init__(self,name:str,specialisation:str):
        self.name : str= name
        self.specialisation : str = specialisation
        self.appointments_schedule :dict[Patient,datetime] = {}
        self._patienttrackrecord : dict[Patient,list[datetime]] = defaultdict(list)
    
    def __eq__(self, other):
        return isinstance(other, Doctor) and self.name == other.name and self.specialisation == other.specialisation

    def __hash__(self):
        return hash((self.name, self.specialisation))

    def view_schedule(self) -> str:
        if not self.appointments_schedule:
            return "\nCurrently there are no appointments."
        appointmets = f"\n-----Dr.{self.name} appointments-----"

        for patient,date in self.appointments_schedule.items():
            appointmets += f"\nPatient name : {patient.name} | Date : {date.date()} | Time : {date.time()}"

        return appointmets
    
    def view_patient_record(self,patient_name : str) -> str:
        for patients in self._patienttrackrecord:
            if patients.name == patient_name:
                patient_account = patients
                break
        else:
            return f"\nNo records available for {patient_name}."
            
        record = f"\n------Patient : {patient_account.name}------"
        for appoint_date_time in self._patienttrackrecord[patient_account]:
            record += f"\n⁍ Date : {appoint_date_time.date()}, Time: {appoint_date_time.time()}"
        return record
    


class Patient:
    def __init__(self,name:str):
        self.name : str = name
        self.appointment : dict[Doctor,datetime] = {}
        self._appointmentrecord : dict[Doctor,list[datetime]]= defaultdict(list)

    def __eq__(self, other):
        return isinstance(other, Patient) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def view_record(self)-> str:
        if not self._appointmentrecord:
            return "\nNo data found."
        
        record = f"\n------Patient : {self.name}------"
        for doctor,app_date_list in self._appointmentrecord.items():
            record += f"\n\n⁍Doctor : Dr.{doctor.name}"
            for appointment_date in app_date_list:
                record += f"\n  Date : {appointment_date.date()} | Time: {appointment_date.time()}"
        
        return record

class Appointment:
    @staticmethod
    def book_appointment(patient_account:Patient,doctor_account : Doctor,app_date : datetime) -> str:

        patient_account.appointment[doctor_account] = app_date
        patient_account._appointmentrecord[doctor_account].append(app_date)
        
        doctor_account.appointments_schedule[patient_account] = app_date
        doctor_account._patienttrackrecord[patient_account].append(app_date)
        
        return f"\nAppointment booked to Dr.{doctor_account.name} on {app_date.date()} at {app_date.time()}."
        
class Hospital:
    def __init__(self,name):
        self.name : str = name
        self.patient_list : list[Patient]= []
        self.doctor_list : dict[str,list[Doctor]] = {} # Specialisation : list[Doctors]
      
    def vacancy(self) -> str:
        if specialist_ailments.keys() == self.doctor_list.keys() and all(len(doctors) == 3 for doctors in self.doctor_list.values()):
            return f"\nCurrently, no vacancies available at {self.name}."
        
        vacancies = f"\n-----Vacancies for specialist in {self.name}-----"
        for specialists in specialist_ailments:
            if (doc_available := len(self.doctor_list.get(specialists,[]))) <3:
                vacancies += f"\n➼  {specialists.title()} : {3-doc_available}"
        return vacancies

    def add_doctor(self,name:str,specialisation:str) -> str:
        if specialisation not in specialist_ailments or len(self.doctor_list.get(specialisation,[]))==3:
            return f"\nVacancy for {specialisation} is not available. Check vacancy list under join section."
        self.doctor_list.setdefault(specialisation,[]).append(Doctor(name,specialisation))
        return f"\nWelcome Dr.{name} to the family of {self.name}.\nYou can go back and access your account."


    def Book_appointment(self,name:str,ailment:str) -> str:
        for specialist in self.doctor_list:
            if ailment.lower() in specialist_ailments[specialist]:
                break
        else:
            return f"\nSorry, {ailment} is not treated here."
        
        app_date = input("\nEnter appointment date and time (DD-MM-YYYY hh:mm AM/PM): ").strip()
        try:
            app_date : datetime = datetime.strptime(app_date,"%d-%m-%Y %I:%M %p")
        except ValueError:
            return ("\n❌ Invalid format. Please use DD-MM-YYYY hh:mm AM/PM.")

        if app_date < datetime.now():
            return "\nInvalid appointment date and time."
        
        morning_start = time(9,0)
        morning_end = time(12,30)
        evening_start = time(15,0)
        evening_end = time(17,30)

        if not((morning_start <= app_date.time() <= morning_end) or (evening_start <= app_date.time() <= evening_end)):
            return f"\nAppointment is available between 9 AM to 12:30 PM morning and 3 PM to 5:30 PM evening only."
        
        for patient in self.patient_list:
            if name == patient.name:
                patient_acc = patient
                break
        else:
            patient_acc = Patient(name)
            self.patient_list.append(patient_acc)

        for app in patient_acc.appointment.values():
            if app <= app_date < app + timedelta(minutes = 30):
                return f"\nYou already have an appointment on {app_date.date()} at {app_date.time()}."

        for doctor in self.doctor_list[specialist]:
            for app_time in doctor.appointments_schedule.values():
                if app_time <= app_date < app_time + timedelta(minutes = 30):
                    break
            else:
                return Appointment.book_appointment(patient_acc,doctor,app_date)
            
        return f"\nSorry, there are other appointments at {app_date.time()}."
        
    def view_appointments_record_for_patient(self,pat_name : str) -> str:
        for patients in self.patient_list:
            if pat_name == patients.name:
                patient_acc = patients
                break
        else:
            return "\nNo records found. Please check your name."
        
        return patient_acc.view_record()
    
def check_name(input_name : str,prompt : str) -> str:
        while True:
            cross_check = input(f"Are you sure {input_name} is correct? (Yes/No): ").strip().lower()
            match cross_check:
                case "yes":
                    return input_name
                case "no":
                    input_name = input(prompt).strip().title()
                case _:
                    print ("Please enter Yes/No.")


if __name__ == '__main__':

    print (heading:="Welcome to Hospital Management System",'='*len(heading),sep='\n')
    hosp_name = input("\nEnter Hospital name : ").strip().title()
    hospital_acc = Hospital(hosp_name)
    

    while True:
        print (heading := f"\nWelcome to {hospital_acc.name}",'='*len(heading),sep='\n')
        user =  input("\nAre you\n1.A Doctor \n2.A Patient\n3.Exit\nSelect : ")
        match user:
            case "3":
                print ("\nThank you for using our service.")
                break

            case "1":
                while True:
                    print ("\nDoctor Dashboard\n================")
                    doc_type = input(f"\nAre you:\n1.Currently working with {hospital_acc.name}\n2.Here to join?\n3.Go back\nSelect option 1 or 2 or 3: ").strip()
                    match doc_type:
                        case "3":
                            break
                        case "1":
                            doc_name = input(prompt:="\nPlease enter your name: ").strip().title()
                            doc_name = check_name(doc_name,prompt)
                                
                            for doctors in hospital_acc.doctor_list.values():
                                for doctor in doctors:
                                    if doc_name == doctor.name:
                                        doc_acc = doctor
                                        break
                                else:
                                    continue
                                break    
                            else:
                                print("\nAccount not found, check your name once again.")
                                continue

                            while True:
                                print ("\nDoctor Dashboard\n================")
                                print (f"\nWelcome Dr.{doc_acc.name}")
                                print ("1.View appointments\n2.View patients records\n3.Go back")
                                opt = input("Select one of the above to proceed: ").strip()
                                match opt:
                                    case "3":
                                        print ("\nThank you for using our service.")
                                        break

                                    case "1":
                                        print (doc_acc.view_schedule())

                                    case "2":
                                        pat_name = input(prompt:="\nEnter patient name to view record: ").strip().title()
                                        pat_name = check_name(pat_name,prompt)
                                        print (doc_acc.view_patient_record(pat_name))

                                    case _:
                                        print("\nInvalid option, choose 1 or 2 or 3.")

                        case "2":
                            doc_name = input(prompt := "\nPlease enter your name: ").strip().title()
                            doc_name = check_name(doc_name,prompt)
                            while True:
                                print ("\nDoctor Dashboard\n================")
                                print (f"\nWelcome Dr.{doc_name}")
                                print (f"1.Check vacancies at {hospital_acc.name}\n2.Join to {hospital_acc.name}\n3.Go back")
                                opt = input("Select one of the above to proceed: ").strip()
                                match opt:
                                    case "3":
                                        break                                    
                                    case "1":
                                        print(hospital_acc.vacancy())
                                    case "2":
                                        spec = input("\nEnter your specialisation: ").strip().lower()
                                        print (hospital_acc.add_doctor(doc_name,spec))
                                        break
                                    case _:
                                        print("\nInvalid option, choose 1 or 2 or 3.")

                        case _:
                            print("\nInvalid option, choose 1 or 2 or 3.")

            case "2":
                patient_name = input(prompt:="\nEnter your name: ").strip().title()
                patient_name = check_name(patient_name,prompt)

                while True:
                    print ("\nPatient dashboard\n=================")
                    print (f"\nWelcome {patient_name}")
                    opt = input("1. Book appointment\n2. View your record with our hospital\n3. Go back\nSelect the service: ").strip()
                    match opt:
                        case "3":
                            print ("\nThank you for using our service.")
                            break

                        case "1":
                            ailment = input("\nEnter your ailment, we will give you a appointment of a specialist accordingly: ").strip()
                            print (hospital_acc.Book_appointment(patient_name,ailment))

                        case "2":
                            print (hospital_acc.view_appointments_record_for_patient(patient_name))

                        case _:
                            print ("\nInvalid option, choose 1 or 2 or 3.")

            case _:
                print ("\nSelect 1(Doctor) or 2(Patient) or 3(Exit).")
    
    # Data Storage

    # Doctor list storage
    with open(r"C:\Users\jp\Documents\Python_files\starter_projects\Hospital Management System\doctor_list.json","w") as file:
        json.dump({specialist : list(map(lambda x : x.name, doctor)) for specialist,doctor in hospital_acc.doctor_list.items()},file,indent=2,sort_keys=True)
    
    #Patient list storage
    with open(r"C:\Users\jp\Documents\Python_files\starter_projects\Hospital Management System\patient_list.json","w") as file:
        json.dump(list(map(lambda x: x.name, hospital_acc.patient_list)),file, indent=2)