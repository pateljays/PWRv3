import pandas as pd
import sqlite3
import csv

dbfile = 'db.sqlite3'
con = sqlite3.connect(dbfile)

cur = con.cursor()
cur.execute("""ALTER TABLE main_patientinfo DROP Intermediate_Complexity; """)
con.commit()

cur.execute("""ALTER TABLE main_patientinfo DROP Cash_or_No_Insurance; """)
con.commit()

cur.execute("""ALTER TABLE main_patientinfo DROP Private_Insurance; """)
con.commit()
con.close()

#cur.execute("DROP TABLE main_patientinfo")
#con.commit()
#cur.execute("""CREATE TABLE main_patientinfo (ids,Oral_Health_Index,Bitewing_Series,
#                                                Tobacco_Counsel,Age,Completed_Tx,Recall_Exams,
#                                                Fluoride,Nutritional_Counsel,Class_II_Restorations,
#                                                Other_Composite_restorations,
#                                                Fixed_Pros_Natural_Teeth,Fixed_Pros_Implant_or_Other,
#                                                Removable_Prosthesis,Periodontal_Tx,
#                                                Gender,RyanWhite_Insurance,Basic_Complexity,
#                                                Complex_Complexity);""") 
#                                                # use your column names here
#data = pd.read_csv('encoded_X_after.csv')
#data.to_sql('main_patientinfo', con, if_exists='append', index = False)
#con.commit()
#con.close()