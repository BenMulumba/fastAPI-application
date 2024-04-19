from fastapi import FastAPI, Body
app = FastAPI()

students = [
    {'ID':'001','name':'Ben Mulumba', 'course': 'Computer science' },    
    {'ID':'002','name':'Elysee Lompegnu','course': 'Business admistration' },
    {'ID':'003','name':'Jhon', 'course': 'Epidemology' },
    {'ID':'004','name':'Maurice', 'course': 'Math' }
]

@app.get('/students')
async def al_stundets ():
    return students

@app.get ("/students/{course}")
async def students_name (name: str):
    for i in students:
        if i.get('name').casefold() == name.casefold():
            return i
        

@app.post ("/students/add_a_student")
async def add_student (new_student = Body()):
    students.append (new_student)

    




