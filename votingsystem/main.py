# Email Varification Using OTP in Flask

from flask import Flask, render_template, request, url_for, redirect
from flask_mail import Mail, Message
from random import randint
from io import StringIO
from flask import session
from datetime import datetime, timedelta
import time
from bson.objectid import ObjectId
import threading
import Signup_verification
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
from pymongo import MongoClient, message
import Areas
import Parties
import candidates
import Create_Election
import Create_Provincial_Election
import Create_NA
import Create_PA
import Voter
import City
import Province
import CheckandViewVote
import PA_CheckandViewVote
import NA_Vote_Count

import PA_Vote_Count
import States_PR
from PIL import Image

import Create_Presidential_Election
import Presidential_Voter
import Presidential_candidates
import presidential_Parties
import Create_PR
# import Counting_Presidential_Vote
import PR_Vote_Count
import PR_CheckandViewVote
# import PR_B_chain
import Credentials
mydatabase = Credentials.db

# Access collection of the database
signups_block = mydatabase['signups']
cand = mydatabase['candidates']
db_area = mydatabase['Areas']
db_parties = mydatabase['Parties']
db_NA = mydatabase['NA']
db_PA = mydatabase['PA']
db_PR = mydatabase['PR']
db_candid = mydatabase['Candidates']
db_Voter = mydatabase['Voter']
db_City = mydatabase['Cities']
db_province = mydatabase['Province']
db_election = mydatabase['Create_election']
db_PA_election = mydatabase['Create_PA_Elections']
db_Presidential_election = mydatabase['Create_Presidential_Election']
db_States = mydatabase['States']
db_Presidential_Voter = mydatabase['Presidential_Voter']
db_Presidential_candid = mydatabase['Presidential_Candidates']
db_Presidential_parties = mydatabase['Presidential_Parties']


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
mail = Mail(app)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'saadabbaszulfiqar@gmail.com'
# you have to give your password of gmail account
app.config['MAIL_PASSWORD'] = '3132590051'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)
local_party_image_path = 'static/images'
expire_time = 0
# session['username']
# session['username'] = ''
session_voter_id = ''


@app.route('/')
def index():
    return render_template('register.html')


@app.route('/signup', methods=['GET', 'POST'])
def checksignup():
    try:

        if request.method == 'POST':
            # lOCAL = PAKISTAN/ INTERNATIONAL = US AMERICA
            admin_Type = request.form['type']
            admin_username = request.form['uname']
            admin_cnic = request.form['cnic']
            admin_fname = request.form['fname']
            admin_lname = request.form['lname']
            admin_email = request.form['email']
            admin_gender = request.form['gender']
            admin_phone = request.form['phone']
            admin_pass = request.form['pass']
            admin_repass = request.form['cpass']
            if admin_pass == admin_repass:
                if admin_Type == "Local":
                    check = Signup_verification.Local_signup_verify(
                        admin_username, admin_cnic, admin_fname, admin_lname, admin_email, admin_gender, admin_phone, admin_pass, admin_repass)
                    if check == 0:
                        return " Local Account Successfully Created..."
                    elif check == 1:
                        message = " Something went wrong..."
                    return render_template('register.html', value=message)
                elif admin_Type == "International":

                    check = Signup_verification.International_signup_verify(
                        admin_username, admin_cnic, admin_fname, admin_lname, admin_email, admin_gender, admin_phone, admin_pass, admin_repass)
                    if check == 0:
                        return " International Account Successfully Created..."
                    elif check == 1:
                        message = " Something went wrong..."
                    return render_template('register.html', value=message)
            else:
                message = 'Password and Confirm Password are not same...'
                return render_template('register.html',value = message)
    except:
        message = 'Please Signup again..'
        return render_template('register.html', value=message)


@app.route('/signin', methods=['GET', 'POST'])
def registration():
    try:
        if request.method == 'POST':
            signin_Type = request.form['Type']
            signin_cnic = request.form['cnic']
            signin_pass = request.form['password']
            # global session['username']
            global session_voter_id
            global expire_time
            print(signin_Type)

            ####################### Local Admin SignIn      ##################
            if signin_Type == 'LocalAdmin':
                print('LocalAdmin')
                check_signing = Signup_verification.Local_admin_signin(
                    signin_cnic, signin_pass)
                if check_signing['admin_cnic'] == signin_cnic and check_signing['admin_pass'] == signin_pass:

                    session['username'] = str(check_signing['_id'])
                    message = 'Admin SignIn Successfull'
                    return render_template('dashboard.html', value=message)

                else:
                    message = 'Wrong Try Again'
                    return render_template('register.html', value=message)

                # message = 'Please SignIn Again'
                # return render_template('register.html', value=message)

                ####################### International Admin SignIn      ##################

            elif signin_Type == 'InternationalAdmin':
                print('InternationalAdmin')
                check_signing = Signup_verification.International_admin_signin(
                    signin_cnic, signin_pass)
                if check_signing['admin_cnic'] == signin_cnic and check_signing['admin_pass'] == signin_pass:

                    session['username'] = str(check_signing['_id'])
                    message = 'Presidential Admin SignIn Successfull'
                    return render_template('Presidential/International_dashboard.html', value=message)

                else:
                    message = 'Wrong Try Again'
                    return render_template('register.html', value=message)

               

              ####################### Local Voter SignIn      ##################

            elif signin_Type == 'LocalVoter':
                print('LocalVoter')

                voter_record = Signup_verification.search_cnic(signin_cnic)
                print("Current Voter ", voter_record)
                if voter_record['Voter_Father_CNIC'] == signin_pass and voter_record['Voter_CNIC'] == signin_cnic:
                    msg = Message(subject='OTP', sender='saadabbaszulfiqar@gmail.com',
                                  recipients=[voter_record['Voter_Email']])
                    msg.body = str(otp)  # edit code here
                    print(voter_record)
                    # global session_voter_id
                    session['username'] = str(voter_record['Admin_ID'])
                    session_voter_id = voter_record['_id']
                    # if not equals to 0 then it means we get email of that user other wise 0 means user not exist...
                    if voter_record['Voter_Email'] != 0:
                        print(msg)
                        # mail.send(msg)
                        global expire_time
                        # time expires after 20 seconds....
                        expire_time = datetime.now() + timedelta(seconds=40)
                        # message = " User"
                        return render_template('verify.html')
                    else:
                        message = "Invalid User"
                        return render_template('register.html', value=message)
                else:
                    message = 'Invalid Voter Please Try Again...'
                    return render_template('register.html', value=message)

    ###################################################### International Voter Signin ##########################################################

            elif signin_Type == 'InternationalVoter':
                print('InternationalVoter')

                voter_record = Signup_verification.Internationa_Voter_Signin(
                    signin_cnic)
                if voter_record['Voter_Father_CNIC'] == signin_pass and voter_record['Voter_CNIC'] == signin_cnic:
                    msg = Message(subject='OTP', sender='saadabbaszulfiqar@gmail.com',
                                  recipients=[voter_record['Voter_Email']])
                    msg.body = str(otp)  # edit code here
                    print(voter_record)
                    # global session_voter_id
                    session['username'] = str(voter_record['Admin_ID'])
                    session_voter_id = voter_record['_id']
                    # if not equals to 0 then it means we get email of that user other wise 0 means user not exist...
                    if voter_record['Voter_Email'] != 0:
                        print(msg)
                        # mail.send(msg)
                        # global expire_time
                        # time expires after 20 seconds....
                        expire_time = datetime.now() + timedelta(seconds=40)
                        # message = " User"
                        return render_template('Presidential/verify_International_Voter.html')
                    else:
                        message = "Invalid User"
                        return render_template('register.html', value=message)
                else:
                    message = 'Invalid Voter Please Try Again...'
                    return render_template('register.html', value=message)

        return render_template('register.html')
    except:
        message = 'Invalid User Please Try Again...'
        return render_template('register.html', value=message)


################### /validate is used for Local Voter Verification ########


@app.route('/validate', methods=['POST'])
def validate():
    try:
        user_otp = request.form['otp']
        current_time = datetime.now()
        if current_time < expire_time:
            if otp == int(user_otp):
                print(session['username'])            # global variable voter CNIC
                print(session_voter_id)             # global variable Admin CNIC
                message = " Email varification Successfull "
                # return render_template('View_Vote.html',value = message)
                return redirect(url_for('Voter_dashboard'))
        elif current_time > expire_time:
            message = "Time Expires "
            return render_template('register.html', value=message)

        message = "Invalid Voter \n Please Try Again "
        return render_template('register.html', value=message)
    except:
        message = "Invalid Voter \n Please Try Again "
        return render_template('register.html', value=message)


####################### /validate_International_Voter is used for International Voter Verification ########


@app.route('/validate_International_Voter', methods=['POST'])
def validate_International_Voter():
    try:
        user_otp = request.form['otp']
        current_time = datetime.now()
        if current_time < expire_time:
            if otp == int(user_otp):
                print(session['username'])            # global variable Admin ID
                print(session_voter_id)             # global variable Voter ID
                message = " Email varification Successfull "
                # return render_template('View_Vote.html',value = message)
                return redirect(url_for('International_Voter_dashboard'))
        elif current_time > expire_time:
            message = "Time Expires "
            return render_template('register.html', value=message)

        message = "Invalid Voter \n Please Try Again "
        return render_template('register.html', value=message)
    except:
        message = "Invalid Voter \n Please Try Again "
        return render_template('register.html', value=message)

@app.route('/Add_Area', methods=['GET', 'POST'])
def addarea():
    try:
        if request.method == 'POST':
            Area_name = request.form['area']
            Area_city = request.form['city']
            Province   = request.form['Province']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = Areas.Add_area(Area_name, Area_city,Province, ObjectId(Admin_ID))
                if result == 0:
                    message = 'Area Added Successfully...'
                    return render_template('Add_Area.html', value=message)
                elif result == 1:
                    message = 'This Area is already exist...'
                    return render_template('Add_Area.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax Name'
                    return render_template('Add_Area.html', value=message)
                elif result == 3:
                    message = 'Area is not Added..'
                    return render_template('Add_Area.html', value=message)
                message = 'Signin Again..'
                return render_template('dashboard.html', value=message)

        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            city_record = []
            province_record = []
            for x in db_City.find({'Admin_ID': ObjectId(Admin_ID)}):
                city_record.append(x)
            for x in db_province.find({'Admin_ID': ObjectId(Admin_ID)}):
                province_record.append(x)
            return render_template('Add_Area.html', city=city_record,Province= province_record)
    except:
        message = 'Something Went Wrong.'
        return render_template('Add_Area.html', value=message)


@app.route('/Delete_Area', methods=['GET', 'POST'])
def delete_area():
    try:
        if request.method == 'POST':
            Area_id = request.form['Area_id']  # search area to edit area
            deleted_area = Areas.delete_area(Area_id)
            if deleted_area == 0:
                message = 'Successfully deleted..'
                return redirect(url_for('viewarea'))
            elif deleted_area == 1:
                message = 'Not Deleted Try Again..'
                return render_template('Add_Area.html', value=message)

        return render_template('Add_Area.html', value='')
    except:
        message = 'Please Fill Complete Information.'
        return render_template('Add_Area.html', value=message)


@app.route('/Search_Area', methods=['GET', 'POST'])
def search_area():
    try:
        if request.method == 'POST':
            Area_id = request.form['Area_id']  # search area to edit area
            search_area = Areas.search_area(Area_id)
            if search_area == 0:
                message = 'Select Again..'
                return render_template('Edit_Area.html', value=message)
            else:
                Admin_ID = session['username']
                city_record = []
                province_record = []
                for x in db_City.find({'Admin_ID': ObjectId(Admin_ID)}):
                    city_record.append(x)
                for x in db_province.find({'Admin_ID': ObjectId(Admin_ID)}):
                    province_record.append(x)
                return render_template('Edit_Area.html', edit_area=search_area, city=city_record,Province= province_record)

        return render_template('Edit_Area.html', edit_area=search_area)

    except:
        return render_template('Add_Area.html')


@app.route('/Edit_Area', methods=['GET', 'POST'])
def Edit_area():
    try:
        if request.method == 'POST':
            Area_id = request.form['Area_id']
            Area_name = request.form['area']
            Area_city = request.form['city']
            Province   = request.form['Province']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                updated_area = Areas.update_area(Area_name, Area_city, Area_id,Province,ObjectId(Admin_ID))
                if updated_area == 0:
                    message = 'Area Successfully Updated..'
                    return redirect(url_for('viewarea'))
                elif updated_area == 1:
                    message = 'Area is Already Exist..'
                    return render_template('Add_Area.html', value=message)
                elif updated_area == 2:
                    message = 'Incorrect Syntax..'
                    return render_template('Add_Area.html', value=message)
                elif updated_area == 3:
                    message = 'Area is not Updated'
                    return render_template('Add_Area.html', value=message)        

        return render_template('Edit_Area.html')

    except:
        message = 'Please Complete Information.'
        return render_template('Edit_Area.html', edit_area=search_area)


@app.route('/View_Area', methods=['GET', 'POST'])
def viewarea():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            City_record = []
            # view all those records whose Admin_Id login adminID
            c = db_area.count_documents({'Admin_Id': ObjectId(Admin_ID)})
            print(c)
            # view all those records whose Admin_Id login adminID
            for x in db_area.find({'Admin_Id': ObjectId(Admin_ID)}):
                City_record.append(x)

        return render_template('View_Area.html', results=City_record)
    except:
        return render_template('register.html')


@app.route('/Add_Candidates', methods=['GET', 'POST'])
def addcandidates():
    try:
        if request.method == 'POST':
            cand_fname = request.form['fname']
            cand_lname = request.form['lname']
            cand_cnic = request.form['cnic']
            cand_email = request.form['email']
            cand_Dob = request.form['Dob']
            cand_number = request.form['number']
            cand_party = request.form['cand_party']
            cand_constituency = request.form['cand_constituency']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            result = candidates.Add_candidates(
                cand_fname, cand_lname, cand_cnic, cand_email, cand_Dob, cand_number, cand_party, cand_constituency, ObjectId(Admin_ID))
            if result == 0:
                message = 'Candidate Added Successfully...'
                return render_template('Add_candidates.html', value=message)
            elif result == 1:
                message = 'This Candidate is already exist...'
                return render_template('Add_candidates.html', value=message)
            elif result == 2:
                message = 'Incorrect Syntax Name'
                return render_template('Add_candidates.html', value=message)
            elif result == 3:
                message = 'Candidate is not Added..'
                return render_template('Add_candidates.html', value=message)
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            party_record = []
            for x in db_parties.find({'Admin_Id': ObjectId(Admin_ID)}):
                party_record.append(x)

            return render_template('Add_candidates.html', party=party_record)

    except:
        return render_template('Add_candidates.html')


@app.route('/Delete_Candidate', methods=['GET', 'POST'])
def Delete_Candidate():
    try:
        if request.method == 'POST':
            # search area to edit area
            candidate_id = request.form['candidate_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_cand = candidates.delete_candidate(
                    candidate_id, ObjectId(Admin_ID))
                if deleted_cand == 0:
                    message = 'Successfully deleted..'
                    return redirect(url_for('View_Candidates'))
                elif deleted_cand == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('dashboard.html', value=message)

        return render_template('dashboard.html', value='')
    except:
        message = 'Candidate is not deleted'
        return render_template('Add_candidates.html', value=message)


@app.route('/Search_Candidate', methods=['GET', 'POST'])
def Search_Candidate():
    try:
        if request.method == 'POST':
            # search party to edit area
            candidate_id = request.form['candidate_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_candidate = candidates.search_candidate(candidate_id)
                if search_candidate == 0:
                    message = 'Select Again..'
                    return render_template('Edit_candidates.html', value=message)
                else:
                    party_record = []
                    for x in db_parties.find({'Admin_Id': ObjectId(Admin_ID)}):
                        party_record.append(x)
                    return render_template('Edit_candidates.html', edit_candidate=search_candidate, party=party_record)

        return render_template('Edit_candidates.html', edit_candidate=search_candidate)
    except:
        return render_template('Add_candidates.html')


@app.route('/Edit_Candidates', methods=['GET', 'POST'])
def Edit_Candidates():
    try:
        if request.method == 'POST':
            cand_id = request.form['cand_id']
            cand_fname = request.form['fname']
            cand_lname = request.form['lname']
            cand_cnic = request.form['cnic']
            cand_email = request.form['email']
            cand_Dob = request.form['Dob']
            cand_number = request.form['number']
            cand_party = request.form['cand_party']
            cand_constituency = request.form['cand_constituency']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = candidates.update_candidate(
                    cand_id, cand_fname, cand_lname, cand_cnic, cand_email, cand_Dob, cand_number, cand_party, cand_constituency, ObjectId(Admin_ID))
                if result == 1:
                    message = 'Candidate Updated Successfully...'
                    return redirect(url_for('View_Candidates'))
                elif result == 0:
                    message = 'This Candidates Not Updated'
                    return render_template('Add_candidates.html', value=message)

    except:

        return render_template('dashboard.html')


@app.route('/View_Candidates')
def View_Candidates():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            p = db_candid.count_documents({'Admin_Id': ObjectId(Admin_ID)})
            print(p)
            candidates_record = []
            for x in db_candid.find({'Admin_Id': ObjectId(Admin_ID)}):
                candidates_record.append(x)
        return render_template('View_Candidates.html', results=candidates_record)
    except:
        return render_template('register.html')


@app.route('/Add_National_Elections', methods=['GET', 'POST'])
def Add_National_Election():
    try:

        if request.method == 'POST':
            NA_election_name = request.form['Election_Name']
            NA_seat_start = request.form['NA_Start']
            NA_seat_end = request.form['NA_End']
            NA_date_start = request.form['Election_Start_Date']
            NA_Election_Time = request.form['Election_Time']
            NA_Election_Hours = request.form['Election_Hours']
            print(NA_election_name, NA_seat_start, NA_seat_end,
                  NA_date_start, NA_Election_Time, NA_Election_Hours)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)

            else:
                # TOTAL PARTIES OF THIS ADMIN
                p = db_parties.count_documents({'Admin_Id': ObjectId(Admin_ID)})
                result = Create_Election.create_elec(
                    ObjectId(Admin_ID), NA_election_name, NA_seat_start, NA_seat_end, NA_date_start, NA_Election_Time, NA_Election_Hours, int(p))
                if result == 0:
                    message = 'Election Create Successfully...'
                    return render_template('Add_National_Elections.html', value=message)
                elif result == 1:
                    message = 'This Election Name Already Exits...'
                    return render_template('Add_National_Elections.html', value=message)
                elif result == 2:
                    message = 'Election is not Created..'
                    return render_template('Add_National_Elections.html', value=message)
        return render_template('Add_National_Elections.html')
    except:
        message = 'Election is not Created'
        return render_template('Add_National_Elections.html', value=message)


@app.route('/National_Election_List')
def National_Election_List():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            NA_lst = searchinelection(ObjectId(Admin_ID))
            # election_record =[]
            # c = db_NA.count_documents({'Admin_ID' : Admin_ID})          # view all those records whose Admin_Id login adminID
            # print(c)
            # for x in db_NA.find({'Admin_ID' : Admin_ID}):                             # view all those records whose Admin_Id login adminID
            #     election_record.append(x)

            return render_template('National_Election_List.html', results=NA_lst)
    except:
        message = 'Something went worng'
        return render_template('dashboard.html', results=message)
    # return render_template('National_Election_List.html')


def searchinelection(Admin_ID):
    election_record = []
    NA_record = []
    # view all those records whose Admin_Id login adminID
    for x in db_election.find({'Admin_ID': ObjectId(Admin_ID), 'Status': 'Constructing'}):
        election_record.append(x['_id'])
    for elction in election_record:
        # view all those records whose Admin_Id login adminID
        for x in db_NA.find({'Admin_ID': ObjectId(Admin_ID), 'Election_ID': elction}):
            NA_record.append(x)
            print(x)

    return NA_record


################################ Provincial Election ############################


@app.route('/Add_Provincial_Elections', methods=['GET', 'POST'])
def Add_Provincial_Elections():
    try:
        if request.method == 'POST':
            PA_election_name = request.form['Election_Name']
            PA_seat_start = request.form['PA_Start']
            PA_seat_end = request.form['PA_End']
            PA_date_start = request.form['Election_Start_Date']
            PA_Election_Time = request.form['Election_Time']
            PA_Election_Hours = request.form['Election_Hours']
            print(PA_election_name, PA_seat_start, PA_seat_end,
                PA_date_start, PA_Election_Time, PA_Election_Hours)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                # TOTAL PARTIES OF THIS ADMIN
                p = db_parties.count_documents({'Admin_Id': ObjectId(Admin_ID)})
                result = Create_Provincial_Election.create_elec(ObjectId(Admin_ID), PA_election_name, PA_seat_start, PA_seat_end, PA_date_start, PA_Election_Time, PA_Election_Hours, int(p))
                if result == 0:
                    message = 'Election Create Successfully...'
                    return render_template('Add_Provincial_Elections.html', value=message)
                elif result == 1:
                    message = 'This Election Name Already Exits...'
                    return render_template('Add_Provincial_Elections.html', value=message)
                elif result == 2:
                    message = 'Election is not Created..'
                    return render_template('Add_Provincial_Elections.html', value=message)
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        return render_template('Add_Provincial_Elections.html')
    except:
        message = 'Election is not Created'
        return render_template('Add_Provincial_Elections.html',value = message)


@app.route('/Provincial_Election_List')
def Provincial_Election_List():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            PA_lst = searchinPAelection(ObjectId(Admin_ID))
            # election_record =[]
            # c = db_PA.count_documents({'Admin_ID' : Admin_ID})          # view all those records whose Admin_Id login adminID
            # print(c)
            # for x in db_PA.find({'Admin_ID' : Admin_ID}):                             # view all those records whose Admin_Id login adminID
            #     election_record.append(x)
            return render_template('Provincial_Election_List.html', results=PA_lst)
    except:
        message = 'Something went worng'
        return render_template('dashboard.html', results=message)
  

def searchinPAelection(Admin_ID):
    election_record = []
    PA_record = []
    # view all those records whose Admin_Id login adminID
    for x in db_PA_election.find({'Admin_ID': ObjectId(Admin_ID), 'Status': 'Constructing'}):
        election_record.append(x['_id'])
    for elction in election_record:
        # view all those records whose Admin_Id login adminID
        for x in db_PA.find({'Admin_ID': ObjectId(Admin_ID), 'Election_ID': elction}):
            PA_record.append(x)
            print(x)

    return PA_record


# @app.route('/sampleInitiate_N_Election', methods=['GET', 'POST'])
# def sampleInitiate_N_Election():
#     try:
#         if request.method == 'POST':
#             NA_id = request.form['NA_id']  # search SEAT to edit
#             cnics = []
#             Admin_ID = session['username']
#             if Admin_ID == '':
#                 message = 'Please SignIn Again..'
#                 return render_template('register.html', value=message)
#             elif NA_id == 'submit':        # post function calling from initiate button and fill na so check type here
#                 # placed this line here only for the loop iterations
#                 data = Create_NA.Party_Candidates(Admin_ID)
#                 Election_Name = request.form['Election_Name']
#                 NA_No = request.form['NA_No']
#                 Area_Name = request.form['Area_Name']

#                 COUNTRY = request.form.getlist("country")
#                 for i in range(0, len(data)):
#                     if cnics != '':
#                         cnics.append(COUNTRY[i])
#                 print(Election_Name, NA_No, Area_Name)
#                 print(cnics)

#                 message = 'SUCCESSFULL'
#                 updated_NA = Create_NA.fill_NA(
#                     Election_Name, NA_No, Area_Name, cnics)
#                 if updated_NA == 1:
#                     message = 'Save NA Seat..'
#                     return render_template('dashboard.html', value=message)
#                 elif updated_NA == 0:
#                     message = 'Connot Save NA here'
#                     return render_template('dashboard.html', value=message)
#                 else:
#                     message = 'Connot Save NA'
#                     return render_template('dashboard.html', value=message)
              
#             else:
#                 search_elec_seat = Create_NA.search_elec_seat_number(
#                     NA_id, Admin_ID)
#                 print(search_elec_seat)
#                 if search_elec_seat == 0:
#                     message = 'Select Again..'
#                     return render_template('dashboard.html', value=message)
#                 else:
#                     p = db_candid.count_documents(
#                         {'Admin_Id': Admin_ID, 'cand_constituency': 'National'})
#                     print(p)
#                     data = Create_NA.Party_Candidates(Admin_ID)
#                     area_record = []
#                     for x in db_area.find({'Admin_Id': Admin_ID}):
#                         area_record.append(x)
#                     print("OKAY...")
#                     return render_template('Initiate_N_Election.html', edit_seat=search_elec_seat, areas=area_record, loop_iteration=len(data), data=data)

         
#     except:
#         message = 'Select Again..'
#         return render_template('National_Election_List.html', value=message)
#     return render_template('Initiate_N_Election.html')


@app.route('/Initiate_P_Election', methods=['GET', 'POST'])
def Initiate_P_Election():
    try:
        if request.method == 'POST':
            PA_id = request.form['PA_id']  # search SEAT to edit

            cnics = []
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            elif PA_id == 'submit':
                # placed this line here List of Candidates
                data = Create_PA.Party_Candidates(ObjectId(Admin_ID))
                Election_Name = request.form['Election_Name']
                PA_No = request.form['PA_No']
                Area_Name = request.form['Area_Name']
                Province_Name = request.form['Province_Name']
                COUNTRY = request.form.getlist("country")
                for i in range(0, len(data)):
                    if cnics != '':
                        cnics.append(COUNTRY[i])
                print(Election_Name, PA_No, Area_Name)
                print(cnics)

                message = 'SUCCESSFULL'
                updated_PA = Create_PA.fill_PA(
                    Election_Name, PA_No, Area_Name, Province_Name, cnics)
                if updated_PA == 1:
                    message = 'Save PA Seat..'
                    return redirect(url_for('Provincial_Election_List'))
                elif updated_PA == 0:
                    message = 'Connot Save PA-Seat'
                    return render_template('dashboard.html', value=message)
                else:
                    message = 'Connot Save PA'
                    return render_template('dashboard.html', value=message)

               
            else:
                search_elec_seat = Create_PA.search_elec_seat_number(
                    PA_id, ObjectId(Admin_ID))
                print(search_elec_seat)
                if search_elec_seat == 0:
                    message = 'Select Again..'
                    return render_template('dashboard.html', value=message)
                else:
                    p = db_candid.count_documents(
                        {'Admin_Id': ObjectId(Admin_ID), 'cand_constituency': 'Provincial'})
                    print(p)
                    data = Create_PA.Party_Candidates(ObjectId(Admin_ID))                   
                    area_record = Areas.check_for_PA_area(PA_id,ObjectId(Admin_ID))
                    province_record = Province.check_province(PA_id,ObjectId(Admin_ID))
                  
                    print("OKAY...")
                    return render_template('Initiate_P_Election.html', edit_seat=search_elec_seat, areas=area_record, province=province_record, loop_iteration=len(data), data=data)

            # return render_template('Initiate_P_Election.html', edit_seat=search_elec_seat)
    except:
        message = 'Select Again..'
        return render_template('Provincial_Election_List.html', value=message)
    # return render_template('Initiate_P_Election.html')


@app.route('/Delete_P_ELECTION', methods=['GET', 'POST'])
def delete_P_election():
    try:
        if request.method == 'POST':
            PA_id = request.form['PA_id']  # search Election to Delete Election
            Admin_ID = session['username']

            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_seat = Create_PA.delete_seat(PA_id)
                if deleted_seat == 0:
                    message = 'Successfully deleted..'
                    return render_template('dashboard.html', value=message)
                elif deleted_seat == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('dashboard.html', value=message)
        message = 'Not Deleted Due to some technical issues...'       
        return render_template('dashboard.html', value=message)
    except:
        message = 'Please Fill Complete Information.'
        return render_template('dashboard.html', value=message)


@app.route('/Start_PA_Election')
def Start_PA_Election():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            # p = db_election.count_documents({'Admin_ID' : Admin_ID})
            election_record = []
            for x in db_PA_election.find({'Admin_ID': ObjectId(Admin_ID)}):
                if x['Election_End_Time'] < datetime.now():

                    myquery = {"_id": x['_id']}
                    newvalues = {"$set": {"Status": 'Ended'}}
                    db_PA_election.update_one(myquery, newvalues)
                    election_record.append(x)

                else:
                    election_record.append(x)

        return render_template('Start_Pa_Election.html', results=election_record)
    except:
        return render_template('dashboard.html')


@app.route('/Check_and_Start_PA', methods=['GET', 'POST'])
def Check_and_Start_PA():
    try:
        if request.method == 'POST':
            election_id = request.form['election_id']
            print(election_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                Election_Start_Date_time = Create_Provincial_Election.check_election_status_and_date(
                    election_id, ObjectId(Admin_ID))
                if Election_Start_Date_time == 0:
                    message = 'Already Another Election is Running...'
                    return render_template('dashboard.html', value=message)
                else:
                    check_date_and_Start_election = Create_Provincial_Election.check_election_date_with_currentdate_and_time(
                        Election_Start_Date_time, election_id)
                    if check_date_and_Start_election == 1:

                        message = 'Election Starts date and time is match...'
                        return redirect(url_for('Start_PA_Election'))

                    elif check_date_and_Start_election == 2:
                        message = 'Election Cannot Started date and time is not match...'
                        return render_template('dashboard.html', value=message)
                    elif check_date_and_Start_election == 3:
                        message = 'Something wrong with this Election...'
                        return render_template('dashboard.html', value=message)
                    elif check_date_and_Start_election == 4:
                        message = 'Election is finished'
                        return render_template('dashboard.html', value=message)

        return render_template('dashboard.html')
    except:
        message = 'Please Complete Information.'
        return render_template('dashboard.html')


# end PA here


@app.route('/Add_Parties', methods=['GET', 'POST'])
def Add_Parties():
    try:
        if request.method == 'POST':
            party_name = request.form['party_name']
            Party_Img = request.files['image']
            Party_Image = local_party_image_path+'/local_parties/'+ \
                str(secure_filename(Party_Img.filename))
            print(Party_Image)

            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = Parties.Add_Party(party_name, Party_Image, ObjectId(Admin_ID))

                if result == 0:
                    Party_Img.save(Party_Image)
                    message = 'Party Added Successfully...'
                    return render_template('Add_Parties.html', value=message)
                elif result == 1:
                    message = 'This Party is already exist...'
                    return render_template('Add_Parties.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax Name'
                    return render_template('Add_Parties.html', value=message)
                elif result == 3:
                    message = 'Party is not Added..'
                    return render_template('Add_Parties.html', value=message)

        return render_template('Add_Parties.html')
    except:
        message = 'Party is not Added... Please Enter Again'
        return render_template('Add_Parties.html', value=message)


@app.route('/Delete_Party', methods=['GET', 'POST'])
def delete_Party():
    try:
        if request.method == 'POST':
            Party_id = request.form['Party_id']  # search area to edit area
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_Party = Parties.delete_party(Party_id)
                if deleted_Party == 0:
                    message = 'Successfully deleted..'
                    return redirect(url_for('View_Parties'))
                elif deleted_Party == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('Add_Parties.html', value=message)

        return render_template('Add_Parties.html', value=message)
    except:
        message = 'Party is not deleted'
        return render_template('Add_Parties.html', value=message)


@app.route('/Search_Party', methods=['GET', 'POST'])
def Search_Party():
    try:
        if request.method == 'POST':
            Party_id = request.form['Party_id']  # search party to edit area
            print(Party_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_Party = Parties.search_party(Party_id)
                print(search_Party)
                if search_Party == 0:
                    message = 'Select Again..'
                    return render_template('Edit_Parties.html', value=message)
                else:
                    return render_template('Edit_Parties.html', edit_party=search_Party)
                
        return render_template('Edit_Parties.html', edit_party=search_Party)
    except:
        return render_template('Add_Parties.html')


@app.route('/Edit_Parties', methods=['GET', 'POST'])
def Edit_party():
    try:
        if request.method == 'POST':
            Party_name = request.form['Party_name']
            party_id = request.form['party_id']
            Party_Img = request.files['image']
            Party_Image =local_party_image_path+'/local_parties/' + \
                str(secure_filename(Party_Img.filename))
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                updated_party = Parties.update_party(Party_name, Party_Image, party_id,ObjectId(Admin_ID))
                if updated_party == 0:
                    Party_Img.save(Party_Image)
                    message = 'Party Successfully Updated..'
                    return redirect(url_for('View_Parties'))
                elif updated_party == 1:
                    message = 'This Party is already exist...'
                    return render_template('Add_Parties.html', value=message)
                elif updated_party == 2:
                    message = 'Incorrect Syntax Name'
                    return render_template('Add_Parties.html', value=message)
                elif updated_party == 3:
                    message = 'Party is not Added..'
                    return render_template('Add_Parties.html', value=message)

        return render_template('Edit_Parties.html')
    except:
        message = 'Please Complete Information.'
        return render_template('Edit_Area.html', edit_party=updated_party)


@app.route('/View_Parties')
def View_Parties():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        # signups_block.insert(data)
        else:
            p = db_parties.count_documents({'Admin_Id': ObjectId(Admin_ID)})
            print(p)
            party_record = []
            for x in db_parties.find({'Admin_Id': ObjectId(Admin_ID)}):
                party_record.append(x)
        return render_template('View_Parties.html', results=party_record)
    except:
        return render_template('register.html')


@app.route('/Add_City', methods=['GET', 'POST'])
def Add_City():
    try:
        if request.method == 'POST':
            Province = request.form['Province']
            City_name = request.form['City_name']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = City.Add_city(City_name,Province, ObjectId(Admin_ID))
                if result == 0:
                    message = 'City Added Successfully...'
                    return render_template('Add_City.html', value=message)
                elif result == 1:
                    message = 'This City is already exist...'
                    return render_template('Add_City.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax Name'
                    return render_template('Add_City.html', value=message)
                elif result == 3:
                    message = 'City is not Added..'
                    return render_template('Add_City.html', value=message)
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:          
            province_record = []
            for x in db_province.find({'Admin_ID': ObjectId(Admin_ID)}):
                province_record.append(x)
        return render_template('Add_City.html',Province = province_record)
    except:
        message = 'Party is not Added... Please Enter Again'
        return render_template('Add_City.html', value=message)


@app.route('/Delete_City', methods=['GET', 'POST'])
def Delete_City():
    try:
        if request.method == 'POST':
            City_id = request.form['City_id']  # search area to edit area
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_city = City.delete_city(City_id)
                if deleted_city == 0:
                    message = 'Successfully deleted..'
                    return redirect(url_for('View_Cities'))
                elif deleted_city == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('Add_City.html', value=message)
        message = 'Not Deleted Due to some technical issues...'
        return render_template('Add_City.html', value=message)
    except:
        message = 'City is not deleted'
        return render_template('Add_City.html', value=message)


@app.route('/Search_City', methods=['GET', 'POST'])
def Search_City():
    # try:
        if request.method == 'POST':
            City_id = request.form['City_id']  # search party to edit area
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_City = City.search_city(City_id)
                if search_City == 0:
                    message = 'Select Again..'
                    return render_template('dashboard.html', value=message)
                else:
                    province_record = []
                    for x in db_province.find({'Admin_ID': ObjectId(Admin_ID)}):
                        province_record.append(x)
                    return render_template('Edit_City.html', edit_city=search_City,Province = province_record )
        
        return render_template('Edit_City.html', edit_city=search_City)
    # except:
    #     return render_template('Add_Parties.html')


@app.route('/Edit_City', methods=['GET', 'POST'])
def Edit_City():
    try:
        if request.method == 'POST':
            City_id = request.form['City_id']
            City_name = request.form['City_Name']
            Province = request.form['Province']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                updated_City = City.update_city(City_id, City_name,Province,ObjectId(Admin_ID))
                if updated_City == 0:
                    message = 'City Successfully Updated..'
                    return redirect(url_for('View_Cities'))
                elif updated_City == 1:
                    message = 'City is already exist..'
                    return render_template('dashboard.html', value=message)
                elif updated_City == 2:
                    message = 'Incorrect Syntax..'
                    return render_template('dashboard.html', value=message)
                elif updated_City == 3:
                    message = 'City is not Updated'
                    return render_template('dashboard.html', value=message)        

        return render_template('Edit_Parties.html')
    except:
        message = 'Please Complete Information.'
        return render_template('dashboard.html', value=message)


@app.route('/View_Cities', methods=['GET', 'POST'])
def View_Cities():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        # signups_block.insert(data)
        else:
            p = db_City.count_documents({'Admin_ID': ObjectId(Admin_ID)})
            print(p)
            city_record = []
            for x in db_City.find({'Admin_ID': ObjectId(Admin_ID)}):
                city_record.append(x)
        return render_template('View_Cities.html', results=city_record)
    except:
        return render_template('register.html')


@app.route('/Add_Province', methods=['GET', 'POST'])
def Add_Province():
    try:
        if request.method == 'POST':
            Province_name = request.form['Province_name']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = Province.Add_province(Province_name, ObjectId(Admin_ID))
                if result == 0:
                    message = 'Province Added Successfully...'
                    return render_template('Add_Province.html', value=message)
                elif result == 1:
                    message = 'This Province is already exist...'
                    return render_template('Add_Province.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax Name'
                    return render_template('Add_Province.html', value=message)
                elif result == 3:
                    message = 'Province is not Added..'
                    return render_template('Add_Province.html', value=message)

        return render_template('Add_Province.html')
    except:
        message = 'Party is not Added... Please Enter Again'
        return render_template('Add_Province.html', value=message)


@app.route('/Delete_Province', methods=['GET', 'POST'])
def Delete_Province():
    try:
        if request.method == 'POST':
            # search area to edit area
            Province_id = request.form['Province_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_province = Province.delete_province(Province_id)
                if deleted_province == 0:
                    message = 'Successfully deleted..'
                    return redirect(url_for('View_Province'))
                elif deleted_province == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('Add_Province.html', value=message)

        return render_template('Add_City.html', value=message)
    except:
        message = 'Province is not deleted'
        return render_template('Add_City.html', value=message)


@app.route('/Search_Province', methods=['GET', 'POST'])
def Search_Province():
    try:
        if request.method == 'POST':
            # search party to edit area
            Province_id = request.form['Province_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_province = Province.search_province(Province_id)
                if search_province == 0:
                    message = 'Select Again..'
                    return render_template('dashboard.html', value=message)
                else:
                    return render_template('Edit_Province.html', edit_province=search_province)

        return render_template('Add_Province.html', edit_city=search_province)
    except:
        return render_template('Add_Province.html')


@app.route('/Edit_Province', methods=['GET', 'POST'])
def Edit_Province():
    try:
        if request.method == 'POST':
            Province_id = request.form['Province_id']
            Province_Name = request.form['Province_Name']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                updated_province = Province.update_province(Province_id, Province_Name,ObjectId(Admin_ID))
                if updated_province == 0:
                    message = 'Province Successfully Updated..'
                    return redirect(url_for('View_Province'))
                elif updated_province == 1:
                    message = 'This Province is already exist...'
                    return render_template('Add_Province.html', value=message)
                elif updated_province == 2:
                    message = 'Incorrect Syntax Name'
                    return render_template('Add_Province.html', value=message)
                elif updated_province == 3:
                    message = 'Province is not Added..'
                    return render_template('Add_Province.html', value=message)


        return render_template('Add_Province.html')
    except:
        message = 'Please Complete Information.'
        return render_template('dashboard.html', value=message)


@app.route('/View_Province', methods=['GET', 'POST'])
def View_Province():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        # signups_block.insert(data)
        else:
            p = db_province.count_documents({'Admin_ID': ObjectId(Admin_ID)})
            province_record = []
            for x in db_province.find({'Admin_ID': ObjectId(Admin_ID)}):
                province_record.append(x)
        return render_template('View_Province.html', results=province_record)
    except:
        return render_template('register.html')


@app.route('/Add_voters', methods=['GET', 'POST'])
def Add_voters():
    try:
        if request.method == 'POST':
            voter_fname = request.form['fname']
            voter_lname = request.form['lname']
            voter_cnic = request.form['cnic']
            voter_Father_cnic = request.form['Father_cnic']
            voter_email = request.form['email']
            voter_Dob = request.form['Dob']
            voter_number = request.form['number']
            voter_province = request.form['province']
            voter_Area = request.form['Area']
            voter_city = request.form['city']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = Voter.Add_voter(voter_fname, voter_lname, voter_cnic, voter_Father_cnic,
                                         voter_email, voter_Area, voter_Dob, voter_number, voter_city, voter_province, ObjectId(Admin_ID))
                if result == 0:
                    message = 'Voter Added Successfully...'
                    return render_template('Add_voters.html', value=message)
                elif result == 1:
                    message = 'This Voter is already exist...'
                    return render_template('Add_voters.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax'
                    return render_template('Add_voters.html', value=message)
                elif result == 3:
                    message = 'Voter is not Added..'
                    return render_template('Add_voters.html', value=message)
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            area_record = []
            province_record = []
            city_record = []
            for x in db_area.find({'Admin_Id': ObjectId(Admin_ID)}):
                area_record.append(x)
            for x in db_province.find({'Admin_ID': ObjectId(Admin_ID)}):
                province_record.append(x)
            for x in db_City.find({'Admin_ID': ObjectId(Admin_ID)}):
                city_record.append(x)
            return render_template('Add_voters.html', results=area_record, province=province_record, city=city_record)
    except:

        return render_template('Add_voters.html', results=area_record)


@app.route('/Delete_Voter', methods=['GET', 'POST'])
def delete_Voter():
    try:
        if request.method == 'POST':
            Voter_id = request.form['Voter_id']  # search area to edit area
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_voter = Voter.delete_voter(Voter_id, ObjectId(Admin_ID))
                if deleted_voter == 0:
                    message = 'Successfully deleted..'
                    print(message)
                    return redirect(url_for('View_Voters'))
                elif deleted_voter == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('dashboard.html', value=message)
        message = 'Not Deleted Due to some technical issues...'
        return render_template('dashboard.html', value=message)
    except:
        message = 'Voter is not deleted'
        return render_template('Add_Parties.html', value=message)


@app.route('/Search_Voter', methods=['GET', 'POST'])
def Search_Voter():
    # try:
        if request.method == 'POST':
            voter_id = request.form['voter_id']  # search party to edit area
            print(voter_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_voter = Voter.search_voter(voter_id)
                if search_voter == 0:
                    message = 'Select Again..'
                    return redirect(url_for('View_Voters'))
                else:
                   
                    province_record = []
                    city_record = []
                    area_record = []
                    for x in db_province.find({'Admin_ID': ObjectId(Admin_ID)}):
                        province_record.append(x)

                    for x in db_City.find({'Admin_ID': ObjectId(Admin_ID)}):
                        city_record.append(x)
                   
                    for x in db_area.find({'Admin_Id': ObjectId(Admin_ID)}):
                        area_record.append(x)
                    # return render_template('Add_voters.html',results=area_record)
                    return render_template('Edit_voters.html', edit_voter=search_voter,city=city_record,province = province_record, area=area_record)
                print(search_voter)
        return render_template('dashboard.html',  value=message)
    # except:
    #     return redirect(url_for('View_Voters'))


@app.route('/Edit_voters', methods=['GET', 'POST'])
def Edit_voters():
    try:
        if request.method == 'POST':
            voter_fname = request.form['fname']
            voter_lname = request.form['lname']
            voter_cnic = request.form['cnic']
            voter_Father_cnic = request.form['Father_cnic']
            voter_email = request.form['email']
            voter_Dob = request.form['Dob']
            voter_number = request.form['number']
            voter_province = request.form['province']
            voter_Area = request.form['Area']
            voter_city = request.form['city']
            voter_id = request.form['voter_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = Voter.update_voter(voter_fname, voter_lname, voter_cnic, voter_Father_cnic, voter_email,
                                            voter_Area, voter_Dob, voter_number, voter_city, voter_province, ObjectId(Admin_ID), voter_id)
                if result == 0:
                    message = 'Voter Updated Successfully...'
                    return redirect(url_for('View_Voters'))
                elif result == 1:
                    message = 'This Voter Information is already exist...'
                    return render_template('Add_voters.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax'
                    return render_template('Add_voters.html', value=message)
                elif result == 3:
                    message = 'Voter is not Added..'
                    return render_template('Add_voters.html', value=message)

        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            party_record = []
            province_record = []
            Area_record = []
            city_record = []
            for x in db_parties.find({'Admin_Id': ObjectId(Admin_ID)}):
                party_record.append(x)

            for x in db_area.find({'Admin_Id': ObjectId(Admin_ID)}):
                Area_record.append(x)

            for x in db_province.find({'Admin_ID': ObjectId(Admin_ID)}):
                province_record.append(x)

            for x in city_record.find({'Admin_ID': ObjectId(Admin_ID)}):
                city_record.append(x)

        return render_template('Edit_voters.html', results=party_record,province = province_record,Area = Area_record)
    except:

        return render_template('Add_voters.html', results=party_record)


@app.route('/View_Voters')
def View_Voters():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            p = db_Voter.count_documents({'Admin_ID': ObjectId(Admin_ID)})
            print(p)
            voter_record = []
            for x in db_Voter.find({'Admin_ID': ObjectId(Admin_ID)}):
                voter_record.append(x)
        return render_template('View_Voters.html', results=voter_record)
    except:
        return render_template('register.html')


@app.route('/icons')
def icons():
    return render_template('icons.html')


@app.route('/dashboard')
def dashboard():
    Admin_ID = session['username']
    if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
    return render_template('/dashboard.html')


###################################      National Election ##########################

@app.route('/Initiate_N_Election', methods=['GET', 'POST'])
def Initiate_N_Election():
    try:
        if request.method == 'POST':
            NA_id = request.form['NA_id']  # search SEAT to edit
            cnics = []
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            elif NA_id == 'submit':        # post function calling from initiate button and fill na so check type here SUBMIT MEANS FILL seat
                # placed this line here only for the loop iterations
                data = Create_NA.Party_Candidates(ObjectId(Admin_ID))
                Election_Name = request.form['Election_Name']
                NA_No = request.form['NA_No']
                Area_Name = request.form['Area_Name']

                COUNTRY = request.form.getlist("country")
                for i in range(0, len(data)):
                    if cnics != '':
                        cnics.append(COUNTRY[i])
                print(Election_Name, NA_No, Area_Name)
                print(cnics)

                message = 'SUCCESSFULL'
                updated_NA = Create_NA.fill_NA(
                    Election_Name, NA_No, Area_Name, cnics)
                if updated_NA == 1:
                    message = 'Save NA Seat..'
                    return redirect(url_for('National_Election_List'))
                elif updated_NA == 0:
                    message = 'Connot Save NA here'
                    return render_template('dashboard.html', value=message)
                else:
                    message = 'Connot Save NA'
                    return render_template('dashboard.html', value=message)

            else:
                search_elec_seat = Create_NA.search_elec_seat_number(
                    NA_id, ObjectId(Admin_ID))
                print(search_elec_seat)
                if search_elec_seat == 0:
                    message = 'Select Again..'
                    return render_template('dashboard.html', value=message)
                else:
                    p = db_candid.count_documents(
                        {'Admin_Id': ObjectId(Admin_ID), 'cand_constituency': 'National'})
                    print(p)
                    data = Create_NA.Party_Candidates(ObjectId(Admin_ID))

                    area = Areas.check_for_NA_area(NA_id, ObjectId(Admin_ID))

                    return render_template('Initiate_N_Election.html', edit_seat=search_elec_seat, areas=area, loop_iteration=len(data), data=data)

    except:
        message = 'Select Again..'
        return render_template('National_Election_List.html', value=message)
    return render_template('Initiate_N_Election.html')


@app.route('/Delete_N_ELECTION', methods=['GET', 'POST'])
def delete_N_election():
    try:
        if request.method == 'POST':
            # Election_Name=request.form['E_Name']
            NA_id = request.form['NA_id']  # search Election to Delete Election
            Admin_ID = session['username']
            # print('dhfjdfjls',NA_No,Admin_ID,Election_Name)
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_seat = Create_NA.delete_seat(NA_id)
                if deleted_seat == 0:
                    message = 'Successfully deleted..'
                    return redirect(url_for('National_Election_List'))
                elif deleted_seat == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('dashboard.html', value=message)
        message = 'Election is not deleted due to some Tecnical Issues'
        return render_template('Add_Area.html', value=message)
    except:
        message = 'Please Fill Complete Information.'
        return render_template('Add_Area.html', value=message)


@app.route('/Start_NA_Election')
def Start_NA_Election():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            # p = db_election.count_documents({'Admin_ID' : Admin_ID})
            election_record = []
            for x in db_election.find({'Admin_ID': ObjectId(Admin_ID)}):
                if x['Election_End_Time'] < datetime.now():
                  
                    myquery = {"_id": x['_id']}
                    newvalues = {"$set": {"Status": 'Ended'}}
                    db_election.update_one(myquery, newvalues)
                    election_record.append(x)

                else:
                    election_record.append(x)

        return render_template('Start_Na_Election.html', results=election_record)
    except:
        return render_template('dashboard.html')


@app.route('/Check_and_Start', methods=['GET', 'POST'])
def Check_and_Start():
    try:
        if request.method == 'POST':
            election_id = request.form['election_id']
            print(election_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                Election_Start_Date_time = Create_Election.check_election_status_and_date(
                    election_id, ObjectId(Admin_ID))
                if Election_Start_Date_time == 0:
                    message = 'Already Another Election is Running...'
                    return render_template('dashboard.html', value=message)
                else:
                    check_date_and_Start_election = Create_Election.check_election_date_with_currentdate_and_time(
                        Election_Start_Date_time, election_id)
                    if check_date_and_Start_election == 1:

                        message = 'Election Starts date and time is match...'
                        return redirect(url_for('Start_NA_Election'))

                    elif check_date_and_Start_election == 2:
                        message = 'Election Cannot Started date and time is not match...'
                        return render_template('dashboard.html', value=message)
                    elif check_date_and_Start_election == 3:
                        message = 'Something wrong with this Election...'
                        return render_template('dashboard.html', value=message)
                    elif check_date_and_Start_election == 4:
                        message = 'Election is finished'
                        return render_template('dashboard.html', value=message)

        return render_template('dashboard.html')
    except:
        message = 'Please Complete Information.'
        return render_template('dashboard.html')


@app.route('/register')
def register():
    global adminID,session_voter_id 
    # session['username'] = ''
    session.pop('username', None)
    adminID = ''
    session_voter_id = ''
    return render_template('register.html')


@app.route('/View_PA_Vote')
def PA_Vote():
    try:
        Admin_ID = session['username']
        Voter_ID = session_voter_id
        print(ObjectId(Admin_ID), Voter_ID)
        if Admin_ID == '' and Voter_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            electiondata = PA_CheckandViewVote.check_election(
                ObjectId(Admin_ID), Voter_ID)
            if electiondata == None:
                print("No Election is in Running State")
                message = 'No Election is in Running State'
                return render_template('Voter_dashboard.html', value=message)
            else:
                # PA-Seat number get from this method
                Search_PA = PA_CheckandViewVote.elect(
                    electiondata, Voter_ID, ObjectId(Admin_ID))
                if Search_PA == 0:
                    message = "No Candidate is Elected from this Area..."
                    return render_template('Voter_dashboard.html', value=message)
                elif Search_PA == 1:
                    message = "You are Already Voted..."
                    return render_template('Voter_dashboard.html', value=message)
                else:

                    candidates_rec, party_logo_path,datetime_end_of_election = PA_CheckandViewVote.Search_each_candidate_record(
                        Search_PA)    # send PA seat to search_each_candidate_record to find each candidate record
                    print(candidates_rec)
                    return render_template('PA_Ballot_Vote.html', PA_seat=Search_PA, candidates_list=candidates_rec, party_logo_path=party_logo_path,datetime_end_of_election = datetime_end_of_election)

          
    except:
        message = "Something went wrong...."
        return render_template('Voter_dashboard.html', value=message)


@app.route('/PA_Ballot_Vote', methods=['GET', 'POST'])
def PA_Ballot_Vote():
    if session['username'] == '':
        message = 'Please SignIn Again..'
        return render_template('register.html', value=message)

    if request.method == 'POST':
        PA_cand_cnic = request.form['radio']
        Admin_ID = session['username']
        Voter_ID = session_voter_id
        if Admin_ID == '' and Voter_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        elif PA_cand_cnic != '':
            create_block = PA_CheckandViewVote.generate_vote_record(
                ObjectId(Admin_ID), Voter_ID, PA_cand_cnic)
            print('Specific Vote : ', create_block)
            message = 'Successfully Voted..'
            return render_template('Voter_dashboard.html', value=message)
        else:
            message = 'Please Select a party which you want to vote for...'
            return render_template('Voter_dashboard.html', value=message)
    return render_template('Voter_dashboard.html')

                    ########################### for Provincial Election Results


@app.route('/Search_PA_election_result', methods=['GET', 'POST'])
def Search_election_result():
    try:
        if request.method == 'POST':
            election_id = request.form['election_id']  # search party to edit area
            print(election_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:

                election_votes = PA_Vote_Count.vote_Count(election_id, ObjectId(Admin_ID))
                province_wise_votes = PA_Vote_Count.Total_party_vote_Count(
                    ObjectId(Admin_ID), election_id)
                if election_votes == 0:
                    message = 'Select Again..'
                    return redirect(url_for('View_Voters'))
                else:
                    print('ye asal cirand he', province_wise_votes)
                    return render_template('View_PA_Results.html', votes=election_votes, party_votes=province_wise_votes)
                # print(search_voter)
        return render_template('dashboard.html')
    except:
        return redirect(url_for('View_Voters'))


@app.route('/Voter_dashboard')
def Voter_dashboard():
    return render_template('Voter_dashboard.html')


@app.route('/View_NA_Vote')
def Vote():
    try:
        Admin_ID = session['username']
        Voter_ID = session_voter_id
        print(Admin_ID, Voter_ID)
        if Admin_ID == '' and Voter_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            electiondata = CheckandViewVote.check_election(ObjectId(Admin_ID), Voter_ID)
            if electiondata == None:
                print("No Election is in Running State")
                message = 'No Election is in Running State'
                return render_template('Voter_dashboard.html', value=message)
            else:
                # NA-Seat number get from this method
                Search_NA = CheckandViewVote.elect(
                    electiondata, Voter_ID, Admin_ID)
                if Search_NA == 0:
                    message = "No Candidate is Elected from this Area..."
                    return render_template('Voter_dashboard.html', value=message)
                elif Search_NA == 1:
                    message = "You are Already Voted..."
                    return render_template('Voter_dashboard.html', value=message)

                else:
                    # send NA seat to search_each_candidate_record to find each candidate record
                    candidates_rec, party_logo_path,datetime_end_of_election = CheckandViewVote.Search_each_candidate_record(
                        Search_NA)
                    print(candidates_rec)
                    length = len(candidates_rec)
                    print(length)
                    print(Search_NA)
                    return render_template('NA_Ballot_Vote.html', Na_seat=Search_NA, candidates_list=candidates_rec, party_logo_path=party_logo_path,datetime_end_of_election = datetime_end_of_election)
         
    except:
        message ="Error in Election "
        return render_template('Voter_dashboard.html', value=message)



@app.route('/NA_Ballot_Vote', methods=['GET', 'POST'])
def Ballot_Vote():
    if session['username'] == '':
        message = 'Please SignIn Again..'
        return render_template('register.html', value=message)

    if request.method == 'POST':
        cand_cnic = request.form['radio']
        Admin_ID = session['username']
        Voter_ID = session_voter_id
        if Admin_ID == '' and Voter_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        elif cand_cnic != '':
            create_block = CheckandViewVote.generate_vote_record(
                ObjectId(Admin_ID), Voter_ID, cand_cnic)
            print('Specific Vote : ', create_block)
            message = 'Successfully Voted..'
            return render_template('Voter_dashboard.html', value=message)
        else:
            message = 'Please Select a party which you want to vote for...'
            return render_template('Voter_dashboard.html', value=message)
    return render_template('Voter_dashboard.html')


@app.route('/Search_election_result', methods=['GET', 'POST'])
def Search_NA_election_result():
    try:
        if request.method == 'POST':
            election_id = request.form['election_id']  # search party to edit area
            print(election_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:

                election_votes = NA_Vote_Count.vote_Count(election_id, ObjectId(Admin_ID))
                party_wise_votes = NA_Vote_Count.Total_party_vote_Count(ObjectId(Admin_ID))
                if election_votes == 0:
                    message = 'Select Again..'
                    return redirect(url_for('View_Voters'))
                else:
                    print('ye asal cirand he', election_votes)
                    return render_template('View_Results.html', votes=election_votes, party_votes=party_wise_votes)
                # print(search_voter)
        return render_template('dashboard.html')
    except:
        return redirect(url_for('View_Voters'))


# all those elections results are shown whose status is ended
@app.route('/Voter_NA_Results_List')
def Voter_NA_Results_List():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            # p = db_election.count_documents({'Admin_ID' : Admin_ID})
            election_record = []
            for x in db_election.find({'Admin_ID': ObjectId(Admin_ID), "Status": 'Ended'}):
                election_record.append(x)

        return render_template('Voter_NA_Results_List.html', results=election_record)
    except:
        return render_template('dashboard.html')


@app.route('/Voter_Search_NA_election_result', methods=['GET', 'POST'])
def Voter_Search_NA_election_result():
    # try:
    if request.method == 'POST':
        election_id = request.form['election_id']  # search party to edit area
        print(election_id)
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:

            election_votes = NA_Vote_Count.vote_Count(election_id, ObjectId(Admin_ID))
            party_wise_votes = NA_Vote_Count.Total_party_vote_Count(ObjectId(Admin_ID))
            if election_votes == 0:
                message = 'Select Again..'
                return redirect(url_for('View_Voters'))
            else:
                print('ye asal cirand he', election_votes)
                return render_template('Voter_NA_Vote_Result.html', votes=election_votes, party_votes=party_wise_votes)
            # print(search_voter)
    return render_template('dashboard.html')
    # except:
    #     return redirect(url_for('View_Voters'))


# all those elections results are shown whose status are ended
@app.route('/Voter_PA_Results_List')
def Voter_PA_Results_List():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            # p = db_election.count_documents({'Admin_ID' : Admin_ID})
            election_record = []
            for x in db_PA_election.find({'Admin_ID': ObjectId(Admin_ID), "Status": 'Ended'}):
                election_record.append(x)

        return render_template('Voter_PA_Results_List.html', results=election_record)
    except:
        return render_template('dashboard.html')


@app.route('/Voter_Search_PA_election_result', methods=['GET', 'POST'])
def Voter_Search_PA_election_result():
    try:
        if request.method == 'POST':
            election_id = request.form['election_id']  # search party to edit area
            print(election_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:

                election_votes = PA_Vote_Count.vote_Count(election_id, ObjectId(Admin_ID))
                province_wise_votes = PA_Vote_Count.Total_party_vote_Count(
                    ObjectId(Admin_ID), election_id)
                if election_votes == 0:
                    message = 'Select Again..'
                    return redirect(url_for('View_Voters'))
                else:
                    print('OK --------------', province_wise_votes)
                    return render_template('Voter_PA_Vote_Result.html', votes=election_votes, party_votes=province_wise_votes)
                # print(search_voter)
        return render_template('dashboard.html')
    except:
        return redirect(url_for('View_Voters'))


# @app.route('/prac', methods=['GET', 'POST'])
# def View_Results():
#     length = 50
#     if request.method == 'POST':
#         Election_Name = request.form['Election_Name']
#         NA_No = request.form['NA_No']
#         Area_Name = request.form['Area_Name']

#         COUNTRY = request.form.getlist("country")
#         for i in range(0, 6):
#             print(COUNTRY[i])
#         print(Election_Name, NA_No, Area_Name)
#     return render_template('practice.html', length=length)


################################### Presidential Election Controller code Start from Here  ###############################


@app.route('/International_dashboard')
def International_dashboard():
    return render_template('/Presidential/International_dashboard.html')

    ################# States insertion code ##########################


@app.route('/Add_State', methods=['GET', 'POST'])
def Add_State():
    try:
        if request.method == 'POST':
            State_name = request.form['State_name']
            Electoral_Votes = request.form['Electoral_Votes']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = States_PR.Add_States(State_name, Electoral_Votes)
                if result == 0:
                    message = 'State Added Successfully...'
                    return render_template('Presidential/Add_States.html', value=message)
                elif result == 1:
                    message = 'This State is already exist...'
                    return render_template('Presidential/Add_States.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax Name'
                    return render_template('Presidential/Add_States.html', value=message)
                elif result == 3:
                    message = 'Party is not Added..'
                    return render_template('Presidential/Add_States.html', value=message)

        return render_template('Presidential/Add_States.html')
    except:
        message = 'State is not Added... Please Enter Again'
        return render_template('Presidential/Add_States.html', value=message)


@app.route('/Delete_State', methods=['GET', 'POST'])
def Delete_State():
    try:
        if request.method == 'POST':
            State_id = request.form['State_id']  # search area to edit area
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_State = States_PR.delete_state(State_id)
                if deleted_State == 0:
                    message = 'Successfully deleted..'
                    return redirect(url_for('View_States'))
                elif deleted_State == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('Presidential/International_dashboard.html', value=message)

        message = 'Not Deleted Try Again..'
        return render_template('Presidential/International_dashboard.html', value=message)
    except:
        message = 'Party is not deleted'
        return render_template('Presidential/International_dashboard.html', value=message)


@app.route('/Search_state', methods=['GET', 'POST'])
def Search_State():
    try:
        if request.method == 'POST':
            state_id = request.form['State_id']  # search party to edit area
            print(state_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_state = States_PR.search_state(state_id)
                if search_state == 0:
                    message = 'Select Again..'
                    return render_template('Presidential/Edit_States.html', value=message)
                else:
                    return render_template('Presidential/Edit_States.html', edit_state=search_state)
        search_state =  "Please Select Again...."   
        return render_template('Presidential/Edit_States.html', edit_state=search_state)
    except:
        return render_template('Presidential/Edit_States.html.html')


@app.route('/Edit_States', methods=['GET', 'POST'])
def Edit_States():
    try:
        if request.method == 'POST':
            State_name = request.form['State_name']
            Electoral_Votes = request.form['Electoral_Votes']
            State_id = request.form['State_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                updated_state = States_PR.update_state(
                    State_name, Electoral_Votes, State_id)
                if updated_state == 1:
                    message = 'State Successfully Updated..'
                    return redirect(url_for('View_States'))
                elif updated_state == 0:
                    message = 'State is not Updated'
                    return render_template('Presidential/International_dashboard.html', value=message)

        return render_template('Presidential/International_dashboard.html')
    except:
        message = 'Please Complete Information.'
        return render_template('Presidential/International_dashboard.html', value=message)


@app.route('/View_States')
def View_States():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        # signups_block.insert(data)
        else:
            p = db_States.count_documents({'Admin_Id': ObjectId(Admin_ID)})
            print(p)
            states_record = []
            for x in db_States.find():
                states_record.append(x)
        return render_template('Presidential/View_States.html', results=states_record)
    except:
        return render_template('register.html')


######################################## Presidential States Ended #################################################

########################################## Presidential   Voter Started ###############################################


@app.route('/Add_Presidential_voters', methods=['GET', 'POST'])
def Add_Presidential_voters():
    try:
        if request.method == 'POST':
            voter_fname = request.form['fname']
            voter_lname = request.form['lname']
            voter_cnic = request.form['cnic']
            voter_Father_cnic = request.form['Father_cnic']
            voter_email = request.form['email']
            voter_Dob = request.form['Dob']
            voter_number = request.form['number']
            voter_state = request.form['state']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = Presidential_Voter.Add_voter(
                    voter_fname, voter_lname, voter_cnic, voter_Father_cnic, voter_email, voter_Dob, voter_number, voter_state, ObjectId(Admin_ID))
                if result == 0:
                    message = 'Voter Added Successfully...'
                    return render_template('Presidential/Add_voters.html', value=message)
                elif result == 1:
                    message = 'This Voter is already exist...'
                    return render_template('Presidential/Add_voters.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax'
                    return render_template('Presidential/Add_voters.html', value=message)
                elif result == 3:
                    message = 'Voter is not Added..'
                    return render_template('Presidential/Add_voters.html', value=message)
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:

            state_record = []

            for x in db_States.find():
                state_record.append(x)
            return render_template('Presidential/Add_voters.html', city=state_record)
        # return render_template('Presidential/Add_voters.html', city=state_record)
    except:

        return render_template('Presidential/Add_voters.html', city=state_record)


@app.route('/Delete_Presidential_Voter', methods=['GET', 'POST'])
def Delete_Presidential_Voter():
    try:
        if request.method == 'POST':
            Voter_id = request.form['Voter_id']  # search area to edit area
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_voter = Presidential_Voter.delete_voter(
                    Voter_id, ObjectId(Admin_ID))
                if deleted_voter == 0:
                    message = 'Successfully deleted..'
                    print(message)
                    return redirect(url_for('View_Presidential_Voters'))
                elif deleted_voter == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('Presidential/International_dashboard.html', value=message)

        return render_template('Presidential/International_dashboard.html', value=message)
    except:
        message = 'Voter is not deleted'
        return render_template('Presidential/International_dashboard.html', value=message)


@app.route('/Search_Presidential_Voter', methods=['GET', 'POST'])
def Search_Presidential_Voter():
    try:
        if request.method == 'POST':
            voter_id = request.form['voter_id']  # search cnic to voters table
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_voter = Presidential_Voter.search_voter(voter_id)
                if search_voter == 0:
                    message = 'Select Again..'
                    return redirect(url_for('View_Presidential_Voters'))
                else:
                    state_record = []
                    for x in db_States.find():
                        state_record.append(x)
                    # return render_template('Add_voters.html',results=area_record)
                    return render_template('Presidential/Edit_voters.html', edit_voter=search_voter, results=state_record)
                # print(search_voter)
        return render_template('Presidential/International_dashboard.html.html', edit_party=search_voter, results=state_record)
    except:
        return redirect(url_for('View_Presidential_Voters'))


@app.route('/Edit_Presidential_voters', methods=['GET', 'POST'])
def Edit_Presidential_voters():
    try:
        if request.method == 'POST':
            voter_fname = request.form['fname']
            voter_lname = request.form['lname']
            voter_cnic = request.form['cnic']
            voter_Father_cnic = request.form['Father_cnic']
            voter_email = request.form['email']
            voter_Dob = request.form['Dob']
            voter_number = request.form['number']
            Voter_State = request.form['state']
            voter_id = request.form['voter_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = Presidential_Voter.update_voter(
                    voter_fname, voter_lname, voter_cnic, voter_Father_cnic, voter_email, voter_Dob, voter_number, Voter_State, ObjectId(Admin_ID), voter_id)
                if result == 1:
                    message = 'Voter Updated Successfully...'
                    return redirect(url_for('View_Presidential_Voters'))
                elif result == 0:
                    message = 'This Voter Not Updated'
                    return render_template('Add_voters.html', value=message)

        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            state_record = []
            for x in db_States.find():
                state_record.append(x)

        return render_template('Presidential/Edit_voters.html', results=state_record)
    except:

        return render_template('Presidential/Edit_voters.html', results=state_record)


@app.route('/View_Presidential_Voters')
def View_Presidential_Voters():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:

            voter_record = []
            for x in db_Presidential_Voter.find({'Admin_ID': ObjectId(Admin_ID)}):
                voter_record.append(x)
        return render_template('Presidential/View_Voters.html', results=voter_record)
    except:
        return render_template('dashboard.html')


##########################################    End Voter Section     #################################################

        ###################################  Presidential Parties #####################################


@app.route('/Add_Presidential_Parties', methods=['GET', 'POST'])
def Add_Presidential_Parties():
    try:
        if request.method == 'POST':
            party_name = request.form['party_name']
            Party_Img = request.files['image']
            Party_Image = local_party_image_path+'/Presidential_parties/' + \
                str(secure_filename(Party_Img.filename))
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = presidential_Parties.Add_Party(
                    party_name, Party_Image, ObjectId(Admin_ID))
                if result == 0:
                    Party_Img.save(Party_Image)
                    message = 'Party Added Successfully...'
                    return render_template('Presidential/Add_Parties.html', value=message)
                elif result == 1:
                    message = 'This Party is already exist...'
                    return render_template('Presidential/Add_Parties.html', value=message)
                elif result == 2:
                    message = 'Incorrect Syntax Name'
                    return render_template('Presidential/Add_Parties.html', value=message)
                elif result == 3:
                    message = 'Party is not Added..'
                    return render_template('Presidential/Add_Parties.html', value=message)

        return render_template('Presidential/Add_Parties.html')
    except:
        message = 'Party is not Added... Please Enter Again'
        return render_template('Add_Parties.html', value=message)


@app.route('/Delete_Presidential_Party', methods=['GET', 'POST'])
def Delete_Presidential_Party():
    try:
        if request.method == 'POST':
            Party_id = request.form['Party_id']  # search area to edit area
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_Party = presidential_Parties.delete_party(Party_id)
                if deleted_Party == 0:
                    message = 'Successfully deleted..'
                    return redirect(url_for('View_Presidential_Parties'))
                elif deleted_Party == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('Presidential/Add_Parties.html', value=message)
        message = "Please Select Again...."   
        return render_template('Presidential/Add_Parties.html', value=message)
    except:
        message = 'Party is not deleted'
        return render_template('Presidential/Add_Parties.html', value=message)


@app.route('/Search_Presidential_Party', methods=['GET', 'POST'])
def Search_Presidential_Party():
    try:
        if request.method == 'POST':
            Party_id = request.form['Party_id']  # search party to edit area
            print(Party_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_Party = presidential_Parties.search_party(Party_id)
                if search_Party == 0:
                    message = 'Select Again..'
                    return render_template('Presidential/Edit_Parties.html', value=message)
                else:
                    return render_template('Presidential/Edit_Parties.html', edit_party=search_Party)
                
        search_Party= "Please Select Again...."        
        return render_template('Presidential/Edit_Parties.html', edit_party=search_Party)
    except:
        return render_template('Presidential/Add_Parties.html')


@app.route('/Edit_Presidential_Parties', methods=['GET', 'POST'])
def Edit_Presidential_Parties():
    try:
        if request.method == 'POST':
            Party_name = request.form['Party_name']
            party_id = request.form['party_id']
            Party_Img = request.files['image']
            Party_Image = local_party_image_path+'/Presidential_parties/' + \
                str(secure_filename(Party_Img.filename))
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                updated_party = presidential_Parties.update_party(
                    Party_name, Party_Image, party_id)
                if updated_party == 1:
                    Party_Img.save(Party_Image)
                    message = 'Party Successfully Updated..'
                    return redirect(url_for('View_Presidential_Parties'))
                elif updated_party == 0:
                    message = 'Party is not Updated'
                    return render_template('Presidential/International_dashboard.html', value=message)

        return render_template('Presidential/Edit_Parties.html')
    except:
        message = 'Please Complete Information.'
        return render_template('Presidential/International_dashboard.html',value = message)


@app.route('/View_Presidential_Parties')
def View_Presidential_Parties():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        # signups_block.insert(data)
        else:
            p = db_Presidential_parties.count_documents({'Admin_Id': ObjectId(Admin_ID)})
            print(p)
            party_record = []
            for x in db_Presidential_parties.find({'Admin_Id': ObjectId(Admin_ID)}):
                party_record.append(x)
        return render_template('Presidential/View_Parties.html', results=party_record)
    except:
        return render_template('register.html')


##########################################    End Presidential Party Section     #################################################

        ################################### Start Candidate Section ####################################


@app.route('/Add_Presidential_Candidates', methods=['GET', 'POST'])
def Add_Presidential_Candidates():
    try:
        if request.method == 'POST':
            cand_fname = request.form['fname']
            cand_lname = request.form['lname']
            cand_cnic = request.form['cnic']
            cand_email = request.form['email']
            cand_Dob = request.form['Dob']
            cand_number = request.form['number']
            cand_party = request.form['cand_party']
            cand_constituency = request.form['cand_constituency']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            result = Presidential_candidates.Add_candidates(
                cand_fname, cand_lname, cand_cnic, cand_email, cand_Dob, cand_number, cand_party, cand_constituency, ObjectId(Admin_ID))
            if result == 0:
                message = 'Candidate Added Successfully...'
                return render_template('Presidential/Add_candidates.html', value=message)
            elif result == 1:
                message = 'This Candidate is already exist...'
                return render_template('Presidential/Add_candidates.html', value=message)
            elif result == 2:
                message = 'Incorrect Syntax Name'
                return render_template('Presidential/Add_candidates.html', value=message)
            elif result == 3:
                message = 'Candidate is not Added..'
                return render_template('Presidential/Add_candidates.html', value=message)
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            party_record = []
            for x in db_Presidential_parties.find({'Admin_Id': ObjectId(Admin_ID)}):
                party_record.append(x)

            return render_template('Presidential/Add_candidates.html', party=party_record)

    except:
        return render_template('Presidential/Add_candidates.html')


@app.route('/Delete_Presidential_Candidate', methods=['GET', 'POST'])
def Delete_Presidential_Candidate():
    try:
        if request.method == 'POST':
            # search area to edit area
            candidate_id = request.form['candidate_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                deleted_cand = Presidential_candidates.delete_candidate(
                    candidate_id, ObjectId(Admin_ID))
                if deleted_cand == 0:
                    message = 'Successfully deleted..'
                    return redirect(url_for('View_Presidential_Candidates'))
                elif deleted_cand == 1:
                    message = 'Not Deleted Try Again..'
                    return render_template('dashboard.html', value=message)

        return render_template('dashboard.html', value=message)
    except:
        message = 'Candidate is not deleted'
        return render_template('Presidential/International_dashboard.html', value=message)


@app.route('/Search_Presidential_Candidate', methods=['GET', 'POST'])
def Search_Presidential_Candidate():
    try:
        if request.method == 'POST':
            # search party to edit area
            candidate_id = request.form['candidate_id']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                search_candidate = Presidential_candidates.search_candidate(
                    candidate_id)
                if search_candidate == 0:
                    message = 'Select Again..'
                    return render_template('Presidential/Edit_candidates.html', value=message)
                else:
                    party_record = []
                    for x in db_Presidential_parties.find({'Admin_Id': ObjectId(Admin_ID)}):
                        party_record.append(x)
                    return render_template('Presidential/Edit_candidates.html', edit_candidate=search_candidate, party=party_record)

        return render_template('Presidential/Edit_candidates.html', edit_candidate=search_candidate)
    except:
        return render_template('Presidential/Add_candidates.html')


@app.route('/Edit_Presidential_Candidates', methods=['GET', 'POST'])
def Edit_Presidential_Candidates():
    try:
        if request.method == 'POST':
            cand_id = request.form['cand_id']
            cand_fname = request.form['fname']
            cand_lname = request.form['lname']
            cand_cnic = request.form['cnic']
            cand_email = request.form['email']
            cand_Dob = request.form['Dob']
            cand_number = request.form['number']
            cand_party = request.form['cand_party']
            cand_constituency = request.form['cand_constituency']
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                result = Presidential_candidates.update_candidate(
                    cand_id, cand_fname, cand_lname, cand_cnic, cand_email, cand_Dob, cand_number, cand_party, cand_constituency, ObjectId(Admin_ID))
                if result == 1:
                    message = 'Candidate Updated Successfully...'
                    print(message)
                    return redirect(url_for('View_Presidential_Candidates'))
                elif result == 0:
                    message = 'This Candidates Not Updated'
                    return render_template('Presidential/Add_candidates.html', value=message)

    except:
        message = 'This Candidates Not Updated'
        return render_template('Presidential/International_dashboard.html', value=message)


@app.route('/View_Presidential_Candidates')
def View_Presidential_Candidates():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            # p = db_Presidential_candid.count_documents({'Admin_Id' : Admin_ID})
            # print(p)
            candidates_record = []
            for x in db_Presidential_candid.find({'Admin_Id': ObjectId(Admin_ID)}):
                candidates_record.append(x)
        return render_template('Presidential/View_Candidates.html', results=candidates_record)
    except:
        return render_template('register.html')


@app.route('/Add_Presindential_Elections', methods=['GET', 'POST'])
def Add_Presindential_Elections():
    try:
        if request.method == 'POST':
            PR_election_name = request.form['Election_Name']
            PR_date_start = request.form['Election_Start_Date']
            PR_Election_Time = request.form['Election_Time']
            PR_Election_Hours = request.form['Election_Hours']
            print(PR_election_name, PR_date_start,
                PR_Election_Time, PR_Election_Hours)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)

            else:
                states_count = db_States.count_documents(
                    {'Admin_Id': ObjectId(Admin_ID)})  # TOTAL States OF Presidential
                result = Create_Presidential_Election.create_elec(
                    ObjectId(Admin_ID), PR_election_name, PR_date_start, PR_Election_Time, PR_Election_Hours, int(states_count))
                if result == 0:
                    message = 'Election Create Successfully...'
                    return render_template('Presidential/Add_Presindential_Elections.html', value=message)
                elif result == 1:
                    message = 'This Election Name Already Exits...'
                    return render_template('Presidential/Add_Presindential_Elections.html', value=message)
                elif result == 2:
                    # print("akkar bakkar")
                    message = 'Election is not Created..'
                    return render_template('Presidential/Add_Presindential_Elections.html', value=message)
        else:
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                states = []
                for x in db_States.find():                             # view all those records whose Admin_Id login adminID
                    states.append(x)

                return render_template('Presidential/Add_Presindential_Elections.html', Presidential_states=states)
    except:
        message = 'Election is not Created'
        return render_template('Presidential/Add_Presindential_Elections.html', value=message)


@app.route('/Presindential_Election_List')
def Presindential_Election_List():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            PR_lst = search_in_Presindential_election(ObjectId(Admin_ID))
            print(PR_lst)

            return render_template('Presidential/Presindential_Election_List.html', results=PR_lst)
    except:
        message = 'Something went worng'
        return render_template('Presidential/International_dashboard.html', value=message)
    # return render_template('Presindential_Election_List.html')


def search_in_Presindential_election(Admin_ID):
    election_record = []
    PR_record = []
    # view all those records whose Admin_Id login adminID
    for x in db_Presidential_election.find({'Admin_ID': ObjectId(Admin_ID), 'Status': 'Constructing'}):

        election_record.append(x['_id'])

    for elction in election_record:
        # view all those records whose Admin_Id login adminID
        for x in db_PR.find({'Admin_ID': ObjectId(Admin_ID), 'Election_ID': elction}):
            PR_record.append(x)

    return PR_record


@app.route('/Initiate_PR_Election', methods=['GET', 'POST'])
def Initiate_PR_Election():
    try:
        if request.method == 'POST':
            PR_id = request.form['PR_id']  # search SEAT to edit
            cnics = []
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            elif PR_id == 'submit':        # post function calling from initiate button and fill na so check type here
                # placed this line here only for the loop iterations
                data = Create_PR.Party_Candidates(ObjectId(Admin_ID))
                Election_Name = request.form['Election_Name']
                State_Name = request.form['State_Name']
                Cand_cnic = request.form.getlist("cand_cnic")
                for i in range(0, len(data)):
                    if cnics != '':
                        cnics.append(Cand_cnic[i])
                print(Election_Name, State_Name)
                print(cnics)

                message = 'SUCCESSFULL'
                updated_PR = Create_PR.fill_PR(
                    Election_Name, State_Name, cnics)
                if updated_PR == 1:
                    message = 'Save Presidential Seat..'
                    return render_template('Presidential/International_dashboard.html', value=message)
                elif updated_PR == 0:
                    message = 'Connot Save Presidential here'
                    return render_template('Presidential/International_dashboard.html', value=message)
                else:
                    message = 'Connot Save Presidential'
                    return render_template('Presidential/International_dashboard.html', value=message)
                # return render_template('Presidential/International_dashboard.html', value=message)

            else:
                search_elec_seat = Create_PR.search_elec_seat_number(
                    PR_id, ObjectId(Admin_ID))
                print(search_elec_seat)
                if search_elec_seat == 0:
                    message = 'Select Again..'
                    return render_template('Presidential/International_dashboard.html', value=message)
                else:
                    p = db_candid.count_documents(
                        {'Admin_Id': ObjectId(Admin_ID), 'cand_constituency': 'Presidential'})
                    print(p)
                    # all Party candidates dictionary
                    data = Create_PR.Party_Candidates(ObjectId(Admin_ID))

                    print("OKAY...")
                    return render_template('Presidential/Initiate_Presidential_Election.html', edit_seat=search_elec_seat, loop_iteration=len(data), data=data)
            #         # print(search_elec_seat)
            # return render_template('Presidential/Initiate_Presidential_Election.html', edit_seat=search_elec_seat)
    except:
        message = 'Select Again..'
        return render_template('Presidential/Initiate_Presidential_Election.html', value=message)


@app.route('/Start_PR_Election')
def Start_PR_Election():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            # p = db_election.count_documents({'Admin_ID' : Admin_ID})
            election_record = []
            for x in db_Presidential_election.find({'Admin_ID': ObjectId(Admin_ID)}):
                if x['Election_End_Time'] < datetime.now():
                    # print(x['Election_End_Time'])
                    # print(x['Status'])
                    myquery = {"_id": x['_id']}
                    newvalues = {"$set": {"Status": 'Ended'}}
                    db_Presidential_election.update_one(myquery, newvalues)
                    election_record.append(x)

                else:
                    election_record.append(x)

        return render_template('Presidential/Start_PR_Election.html', results=election_record)
    except:
        message = 'Error...'
        return render_template('Presidential/International_dashboard.html', value=message)


@app.route('/Check_and_Start_PR_Election', methods=['GET', 'POST'])
def Check_and_Start_PR_Election():
    try:
        if request.method == 'POST':
            election_id = request.form['election_id']
            print(election_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:
                Election_Start_Date_time = Create_Presidential_Election.check_election_status_and_date(
                    election_id, ObjectId(Admin_ID))
                if Election_Start_Date_time == 0:
                    message = 'Already Another Election is Running...'
                    return render_template('Presidential/International_dashboard.html', value=message)
                elif Election_Start_Date_time == 1:
                    message = 'Error with the date that stores in this election'
                    return render_template('Presidential/International_dashboard.html', value=message)

                else:
                    check_date_and_Start_election = Create_Presidential_Election.check_election_date_with_currentdate_and_time(
                        Election_Start_Date_time, election_id)
                    if check_date_and_Start_election == 1:

                        message = 'Election Starts date and time is match...'
                        return redirect(url_for('Start_PR_Election'))

                    elif check_date_and_Start_election == 2:
                        message = 'Election Cannot Started date and time is not match...'
                        return render_template('Presidential/International_dashboard.html', value=message)
                    elif check_date_and_Start_election == 3:
                        message = 'Something wrong with this Election...'
                        return render_template('Presidential/International_dashboard.html', value=message)
                    elif check_date_and_Start_election == 4:
                        message = 'Election is finished'
                        return render_template('Presidential/International_dashboard.html', value=message)

        return render_template('Presidential/International_dashboard.html', value=message)
    except:
        message = 'Please Complete Information.'
        return render_template('Presidential/International_dashboard.html',value = message)



                                    ### Fot Presidential Election Results ####


@app.route('/Search_PR_election_result', methods=['GET', 'POST'])
def Search_PR_election_result():
    try:
        if request.method == 'POST':
            election_id = request.form['election_id']  # search party to edit area
            print(election_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:

                election_votes = PR_Vote_Count.vote_Count(election_id, ObjectId(Admin_ID))
                print('wsssssssssssssssssssssd', election_votes)
                party_wise_votes, Wining_Party = PR_Vote_Count.Total_party_vote_Count(
                    ObjectId(Admin_ID), election_id)
                if election_votes == 0:
                    message = 'There is no States in this Election'
                    return render_template('Presidential/International_dashboard.html', value=message)
                    # return redirect(url_for('View_Voters'))
                elif election_votes == 1:
                    message = 'Election Are not Exist'
                    return render_template('Presidential/International_dashboard.html', value=message)
                    # return redirect(url_for('View_Voters'))
                else:
                    states_list = []
                    # view all states whose Admin_Id login adminID
                    for states in db_States.find({}):
                        states_list.append(states)

                    return render_template('Presidential/View_Presidential_Results.html', votes=election_votes, party_votes=party_wise_votes, Wining_Party=Wining_Party, states_list=states_list)

        return render_template('Presidential/International_dashboard.html')
    except:
        return render_template('Presidential/International_dashboard.html')
 


@app.route('/View_Presidential_State_Result', methods=['GET', 'POST'])
def View_Presidential_State_Result():
    if request.method == 'POST':
        state_name = request.form['State_name']  # search party to edit area
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            generating_result = dict()
            generating_result = PR_Vote_Count.Vote_Count(state_name, ObjectId(Admin_ID))
            return render_template('Presidential/View_Presidential_State_Results.html', generating_resultsss=generating_result)

       
    return render_template('dashboard.html')

################################################## End Presidential Election   #########################################

    ############################## Ballot and Vote Portion For Voter   ###################################


@app.route('/International_Voter_dashboard')
def International_Voter_dashboard():
    
    return render_template('Presidential/International_Voter_dashboard.html')


@app.route('/View_PR_Vote')
def View_PR_Vote():
    try: 
        Admin_ID = session['username']
        Voter_ID = session_voter_id
        print(Admin_ID, Voter_ID)
        if Admin_ID == '' and Voter_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            electiondata = PR_CheckandViewVote.check_election(
                ObjectId(Admin_ID), Voter_ID)        # For Voter
            if electiondata == None:
                print("No Election is in Running State")
                message = 'No Election is in Running State'
                return render_template('Presidential/International_Voter_dashboard.html', value=message)
            else:
                # PR-State number get from this method
                Search_PR = PR_CheckandViewVote.elect(
                    electiondata, Voter_ID, ObjectId(Admin_ID))
                if Search_PR == 0:
                    message = "No Candidate is Elected from this State..."
                    return render_template('Presidential/International_Voter_dashboard.html', value=message)
                elif Search_PR == 1:
                    message = "You are Already Voted..."
                    return render_template('Presidential/International_Voter_dashboard.html', value=message)

                else:

                    candidates_rec, party_logo_path,datetime_end_of_election = PR_CheckandViewVote.Search_each_candidate_record(
                        Search_PR)    # send pr seat to search_each_candidate_record to find each candidate record
                    print(candidates_rec)
                    print(datetime_end_of_election)
                    return render_template('Presidential/PR_Ballot_Vote.html', Na_seat=Search_PR, candidates_list=candidates_rec, party_logo_path=party_logo_path,datetime_end_of_election=datetime_end_of_election)
            # return render_template('Presidential/International_Voter_dashboard.html', value=message)

        # return render_template('NA_Ballot_Vote.html')
    except: 
        message = "You are Already Voted..."
        return render_template('Presidential/International_Voter_dashboard.html', value=message)

@app.route('/PR_Ballot_Vote', methods=['GET', 'POST'])
def PR_Ballot_Vote():
    if session['username'] == '':
        message = 'Please SignIn Again..'
        return render_template('register.html', value=message)

    if request.method == 'POST':
        cand_cnic = request.form['radio']
        Admin_ID = session['username']
        Voter_ID = session_voter_id
        if Admin_ID == '' and Voter_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        elif cand_cnic != '':

            create_block = PR_CheckandViewVote.generate_vote_record(
                ObjectId(Admin_ID), Voter_ID, cand_cnic)
            print('Specific Vote : ', create_block)
            message = 'Successfully Voted..'
            return render_template('Presidential/International_Voter_dashboard.html', value=message)
        else:
            message = 'Please Select a party which you want to vote for...'
            return render_template('Presidential/International_Voter_dashboard.html', value=message)
    else:
        message = 'Voter Dashboard'
        return render_template('Presidential/International_Voter_dashboard.html', value=message)


# all those Presidential Elections results are shown whose status is ended
@app.route('/Voter_PR_Results_List')
def Voter_PR_Results_List():
    try:
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            # p = db_election.count_documents({'Admin_ID' : Admin_ID})
            election_record = []
            for x in db_Presidential_election.find({'Admin_ID': ObjectId(Admin_ID), "Status": 'Ended'}):
                election_record.append(x)

        return render_template('Presidential/Voter_PR_Results_List.html', results=election_record)
    except:
        return render_template('Presidential/International_Voter_dashboard.html')


# Result for specific Election Selected by Voter
@app.route('/Voter_Search_PR_election_result', methods=['GET', 'POST'])
def Voter_Search_PR_election_result():
    try:
        if request.method == 'POST':
            election_id = request.form['election_id']  # search party to edit area
            print(election_id)
            Admin_ID = session['username']
            if Admin_ID == '':
                message = 'Please SignIn Again..'
                return render_template('register.html', value=message)
            else:

                election_votes = PR_Vote_Count.vote_Count(election_id, ObjectId(Admin_ID))
                party_wise_votes, Wining_Party = PR_Vote_Count.Total_party_vote_Count(
                    ObjectId(Admin_ID), election_id)
                if election_votes == 0:
                    message = 'There is no States in this Election'
                    return render_template('Presidential/International_Voter_dashboard.html', value=message)
                elif election_votes == 1:
                    message = 'Election Are not Exist'
                    return render_template('Presidential/International_Voter_dashboard.html', value=message)
                       
                else:
                    states_list = []
                    # view all states whose Admin_Id login adminID
                    for states in db_States.find({}):
                        states_list.append(states)

                    return render_template('Presidential/Voter_PR_Vote_Result.html', votes=election_votes, party_votes=party_wise_votes, Wining_Party=Wining_Party, states_list=states_list)
                
        return render_template('Presidential/International_Voter_dashboard.html')
    except:
        return render_template('Presidential/International_Voter_dashboard.html')
             
@app.route('/View_Voter_Presidential_State_Result', methods=['GET', 'POST'])
def View_Voter_Presidential_State_Result():
    if request.method == 'POST':
        state_name = request.form['State_name']  # search party to edit area
        Admin_ID = session['username']
        if Admin_ID == '':
            message = 'Please SignIn Again..'
            return render_template('register.html', value=message)
        else:
            generating_result = dict()
            generating_result = PR_Vote_Count.Vote_Count(state_name, ObjectId(Admin_ID))
            return render_template('Presidential/View_Voter_Presidential_State_Results.html', generating_resultsss=generating_result)

   

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    dict = {"Republican": 50, "Democratic": 30, "Green": 20, "Libertarian": 15}
    keys = dict.keys()
    val = dict.values()
    print(list(val))

    return render_template('Insert_Image.html', keysss=list(keys), valll=list(val))



@app.route('/counter', methods=['GET', 'POST'])
def grccaph():
    id = '609a0a9edabd90b2665e29df'
    election_votes = db_election.find_one({'_id':ObjectId(id)})
    datetime  = election_votes['Election_End_Time'] 
    # Date("May 21, 2021 16:37:52")         
    print(datetime)
    return render_template('counter.html', data =datetime )







# 2021-05-11T12:39:55.000+00:00








# @app.route('/set', methods=['GET', 'POST'])
# def set_session():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return f'The value you set is: { session.get("username") }'
#     return render_template('session.html') 

# @app.route('/get')
# def get_session():
#     return f'The value in the session is: { session.get("username") }'
# # © 2021 GitHub, Inc.


# @app.route('/login', methods=['GET', 'POST]')
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['session_name']
#         # session_pass = request.form['session_pass'] 
#         print(session)
#         # message =  " successfull"
#     return render_template('session.html',value = message)
   

# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index1'))
#     return '''      
#     <form action = "" method = "post">
#         <p><input type = text name = username/></p>
#         <p<<input type = submit value = Login/></p>
#     </form>
        
#     '''

   
      
# @app.route('/logout')
# def logout():
#    # remove the username from the session if it is there
#    session.pop('username', None)
#    return redirect(url_for('index1'))

# @app.route('/')
# def index1():
#     if 'username' in session:
#         username = session['username']
#         return 'Logged in as ' + username + '<br>' + \
#             "<b><a href = '/logout'>click here to log out</a></b>"
#     return "You are not logged in <br><a href = '/login'></b>" + \
#         "click here to log in</b></a>"

if __name__ == '__main__':
    app.run(debug=True)
