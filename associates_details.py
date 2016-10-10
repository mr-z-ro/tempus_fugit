import csv

inputfile = 'associates.csv'
def getEmployeeDetails(emailaddress):
    with open(inputfile,'rb') as f:
        header = f.next() # this takes in the header
        for row in f:
            # loop through all the rows
            employee, title, location, email = row.split(',')

            if email.strip() == emailaddress.strip():
                return employee, title, location
    # if the email is not found return None
    return None, None, None
