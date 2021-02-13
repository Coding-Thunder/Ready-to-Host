from operator import pos, sub
from flask import Flask, request, session, redirect
from flask.templating import render_template
from flask_mail import Mail
from datetime import date, datetime
from werkzeug.utils import secure_filename
import os
import math
import json
from flask_sqlalchemy import SQLAlchemy

with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['UPLOAD_FOLDER_INVESTOR'] = params['upload_location_investor']
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params["gmail_password"]
)

mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20),  nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Job_application(db.Model):
    # table_name =  applicant_preference
    # columns name = sno, city_choice, job_keywords, job_type, date
    sno = db.Column(db.Integer, primary_key=True)
    JOBCODE = db.Column(db.String(50), nullable=False)
    DOB = db.Column(db.String(50),  nullable=False)
    SALUTATION = db.Column(db.String(20), nullable=False)
    F_NAME = db.Column(db.String(20), nullable=False)
    L_NAME = db.Column(db.String(20), nullable=False)
    CONTACT = db.Column(db.String(20), nullable=False)
    EMAIL = db.Column(db.String(20), nullable=False)
    CURRENT_STATUS = db.Column(db.String(20), nullable=True)
    EXP = db.Column(db.String(20), nullable=True)
    DEGREE = db.Column(db.String(50), nullable=False)
    COLLEGE = db.Column(db.String(50), nullable=False)
    REFRENCE = db.Column(db.String(50), nullable=True)
    POSSIBLE_DATE = db.Column(db.String(12), nullable=False)
    LAST_CTC = db.Column(db.String(20), nullable=True)
    CURRENT_CTC = db.Column(db.String(20), nullable=False)
    EXPECTED_CTC = db.Column(db.String(20), nullable=False)
    QUES1 = db.Column(db.String(120), nullable=False)
    QUES2 = db.Column(db.String(120), nullable=False)
    QUES3 = db.Column(db.String(120), nullable=False)
    CV = db.Column(db.String(20), nullable=True)
    WEBSITE_OF_WORK = db.Column(db.String(20), nullable=False)
    PORTFOLIO = db.Column(db.String(20), nullable=False)
    WORKSAMPLE = db.Column(db.String(20), nullable=False)
    SIGN = db.Column(db.String(20), nullable=True)
    PHOTO = db.Column(db.String(20), nullable=True)
    AADHAR_CARD = db.Column(db.String(20), nullable=True)
    PAN_CARD = db.Column(db.String(20), nullable=True)
    date = db.Column(db.String(12), nullable=True)


class Investor(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    DATE = db.Column(db.String(12), nullable=True)
    DAY = db.Column(db.String(80), nullable=False)
    NAME_OF_COMPANY = db.Column(db.String(20),  nullable=False)
    COMPANY_LOCATION = db.Column(db.String(80), nullable=False)
    COMPANY_REGISTRATION_NUMBER = db.Column(db.String(120), nullable=False)
    OWNER_OF_COMPANY = db.Column(db.String(80), nullable=False)
    WEBSITE_OF_COMPANY = db.Column(db.String(80), nullable=False)
    INTRESTED_IN = db.Column(db.String(80), nullable=False)
    APPROX_AMT_OF_INVESTMENT = db.Column(db.String(80), nullable=False)
    OTHER_CUSTOM_INTREST = db.Column(db.String(80), nullable=False)
    APPLICANTS_PHOTO = db.Column(db.String(80), nullable=False)
    APPLICANTS_SIGNATURE = db.Column(db.String(80), nullable=False)
    AADHAAR_CARD = db.Column(db.String(80), nullable=False)
    PAN_CARD = db.Column(db.String(80), nullable=False)
    INTERNATIONAL_ID = db.Column(db.String(80), nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    postedby = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    DATE = db.Column(db.String(12), nullable=False)


class Jobs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    jobcode = db.Column(db.String(50), nullable=False)
    jobdescription = db.Column(db.String(200), nullable=False)


@app.route("/")
def home():
    return render_template("index.html", params=params)


@ app.route("/about-us")
def aboutUs():
    return render_template("about.html", params=params)


@ app.route("/patent-publications")
def patentPublications():
    return render_template("patent.html", params=params)


@ app.route("/product")
def products():
    return render_template("product.html", params=params)


@ app.route("/product/visualization-based-product")
def laserSystems():
    return render_template("visualizationbasedsystems.html", params=params)


@ app.route("/product/laser-systems")
def visualizationBasedProduct():
    return render_template("lasersystems.html", params=params)


@ app.route("/product/software-and-driver")
def softwareAndDriver():
    return render_template("softwaresanddriver.html", params=params)


@ app.route("/product/android-based-systems")
def androidBasedSystems():
    return render_template("androidbasedproducts.html", params=params)


@ app.route("/career", methods=['GET', 'POST'])
def career():
    if(request.method == 'POST'):
        jobcode = request.form.get("jobcode")
        dob = request.form.get("dob")
        salutation = request.form.get("salutation")
        f_name = request.form.get("first-name")
        l_name = request.form.get("last-name")
        contact = request.form.get("contact")
        email = request.form.get("email")
        current_status = request.form.get("current_status")
        exp = request.form.get("exp")
        degree = request.form.get("degree")
        college = request.form.get("college")
        refrence = request.form.get("refrence")
        possibledate = request.form.get("possibledate")
        lastctc = request.form.get("lastctc")
        currentctc = request.form.get("current_ctc")
        expectedctc = request.form.get("expected_ctc")
        ques1 = request.form.get("ques1")
        ques2 = request.form.get("ques2")
        ques3 = request.form.get("ques3")
        cv = request.form.get("cv")
        website_of_work = request.form.get("website_of_work")
        portfolio = request.form.get("portfolio")
        worksample = request.form.get("worksample")
        sign = request.form.get("sign")
        photo = request.form.get("photo")
        adhar = request.form.get("adhar")
        pancard = request.form.get("pancard")

        sign = request.files["sign"]
        photo = request.files["photo"]
        adhar = request.files["adhar"]
        pancard = request.files["pancard"]
        cv = request.files["cv"]
        sign.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(sign.filename)))
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(photo.filename)))
        adhar.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(adhar.filename)))
        pancard.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(pancard.filename)))
        cv.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(cv.filename)))

        career_entry = Job_application(
            JOBCODE=jobcode,
            DOB=dob,
            SALUTATION=salutation,
            F_NAME=f_name,
            L_NAME=l_name,
            CONTACT=contact,
            EMAIL=email,
            CURRENT_STATUS=current_status,
            EXP=exp,
            DEGREE=degree,
            COLLEGE=college,
            REFRENCE=refrence,
            POSSIBLE_DATE=possibledate,
            LAST_CTC=lastctc,
            CURRENT_CTC=currentctc,
            EXPECTED_CTC=expectedctc,
            QUES1=ques1,
            QUES2=ques2,
            QUES3=ques3,
            CV=cv,
            WEBSITE_OF_WORK=website_of_work,
            PORTFOLIO=portfolio,
            WORKSAMPLE=worksample,
            SIGN=sign,
            PHOTO=photo,
            AADHAR_CARD=adhar,
            PAN_CARD=pancard,
            date=datetime.now()
        )

        db.session.add(career_entry)
        db.session.commit()
        mail.send_message(
            f"{f_name} {l_name} applied for a role",
            sender=email,
            recipients=[params["gmail_user"]],
            body=f"""HERE ARE THE DETAILS OF THE APPLICANT\n
    DATE : {datetime.now()}\n
    JOB CODE : {jobcode}\n
    DATE OF BIRTH : {dob}\n
    NAME : {salutation} {f_name} {l_name}\n
    CONTACT NUMBER : {contact}\n
    EMAIL : {email}\n
    CURRENT STATUS : {current_status}\n
    EXPERIENCE : {exp}\n
    DEGREE : {degree}\n
    COLLEGE : {college}\n
    REFERENCE : {refrence}\n
    POSSIBLE JOINING DATE : {possibledate}\n
    LAST CTC : {lastctc}\n
    EXPECTED CTC : {expectedctc}\n
    QUESTION 1 : WHY DO YOU WANT TO JOIN US...?\n
    ANSWER 1 : --{ques1}\n\n
    QUESTION 2 : WHAT ARE THE EXPECTATIONS FROM THE EMPLOYER\n
    ANSWER 2 : --{ques2}\n\n
    QUESTION 3 : DO YOU HAVE PREVIOUS SAMPLE OF RELATED WORK ? PROVIDE IF YES\n
    ANSWER 3 : --{ques3}\n
    CV : {cv}
    WEBSITE OF WORK : {website_of_work}\n
    PORTFOLIO : {portfolio}\n
    WORK SAMPLES : {worksample}\n
    SIGN : {sign} --this is a file name which is located in your server's directory--\n
    PHOTO : {photo} --this is a file name which is located in your server's directory--\n
    AADHAAR CARD : {adhar} --this is a file name which is located in your server's directory--\n
    PAN CAN : {pancard} --this is a file name which is located in your server's directory--\n
    LINK : TO ADMIN DASHBOARD : link will come here once developed
        """
        )
    # table_name =  applicant_preference
    # columns name = sno, city_choice, job_keywords, job_type, date
    jobs = Jobs.query.filter_by().all()[0:params["no_of_jobs"]]
    return render_template("career.html", params=params, jobs=jobs)


@ app.route("/contact-us", methods=['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        "ADD ENTRY TO THE DATABASE"
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        # Entry in the database
        contact_us_entry = Contacts(name=name, email=email,
                                    phone_num=phone, message=message, date=datetime.now())
        db.session.add(contact_us_entry)
        db.session.commit()
        mail.send_message(name + " tried to contact you",
                          sender=email,
                          recipients=[params["gmail_user"]],
                          body=message + "\n" + phone
                          )

    return render_template("contact.html", params=params)


@ app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')


@ app.route("/delete/<string:sno>")
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/')


@ app.route("/for-investors", methods=['GET', 'POST'])
def forInvestors():
    if(request.method == 'POST'):
        "ADD ENTRY TO THE DATABASE"
        date = request.form.get("date")
        day = request.form.get("day")
        nameofcompany = request.form.get("nameofcompany")
        location = request.form.get("location")
        reg_num = request.form.get("reg_num")
        owner = request.form.get("owner")
        website = request.form.get("website")
        invest = request.form.get("invest")
        funding = request.form.get("funding")
        customintrest = request.form.get("customintrest")
        photo = request.form.get("photo")
        sign = request.form.get("sign")
        adhar = request.form.get("adhar")
        pancard = request.form.get("pancard")
        Iid = request.form.get("Iid")

        sign = request.files["sign"]
        adhar = request.files["adhar"]
        pancard = request.files["pancard"]
        Iid = request.files["Iid"]
        photo = request.files["photo"]

        sign.save(os.path.join(
            app.config['UPLOAD_FOLDER_INVESTOR'], secure_filename(sign.filename)))
        adhar.save(os.path.join(
            app.config['UPLOAD_FOLDER_INVESTOR'], secure_filename(adhar.filename)))
        pancard.save(os.path.join(
            app.config['UPLOAD_FOLDER_INVESTOR'], secure_filename(pancard.filename)))
        Iid.save(os.path.join(
            app.config['UPLOAD_FOLDER_INVESTOR'], secure_filename(pancard.filename)))
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER_INVESTOR'], secure_filename(pancard.filename)))
        # Entry in the database
        investors_entry = Investor(
            DATE=date,
            DAY=day,
            NAME_OF_COMPANY=nameofcompany,
            COMPANY_LOCATION=location,
            COMPANY_REGISTRATION_NUMBER=reg_num,
            OWNER_OF_COMPANY=owner,
            WEBSITE_OF_COMPANY=website,
            INTRESTED_IN=invest,
            APPROX_AMT_OF_INVESTMENT=funding,
            OTHER_CUSTOM_INTREST=customintrest,
            APPLICANTS_PHOTO=photo,
            APPLICANTS_SIGNATURE=sign,
            AADHAAR_CARD=adhar,
            PAN_CARD=pancard,
            INTERNATIONAL_ID=Iid
        )
        db.session.add(investors_entry)
        db.session.commit()
        mail.send_message("Someone wants to invest",
                          sender=params["gmail_user"],
                          recipients=[params["gmail_user"]],
                          body=f"""
        DATE : {date}\n
        DAY : {day}\n
        NAME OF COMPANY : {nameofcompany}\n
        COMPANY LOCATION : {location}\n
        OWNER OF THE COMPANY : {owner}\n
        WEBSITE OF COMPANY : {website}\n
        INTRESTED IN : {invest}\n
        APPROX. AMT. OF INVESTMENT : {funding}\n
        OTHER CUSTOM INTREST : {customintrest}\n
        APPLICANTS PHOTO : {photo}\n
        SIGNATURE : {sign}\n
        AADHAAR CARD : {adhar}\n
        PAN CARD : {pancard}\n
        INTERNATIONAL ID : {Iid}\n

        """
                          )

    return render_template("investors.html", params=params)


@ app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html", params=params, post=post)


@ app.route("/blog", methods=['GET', 'POST'])
def blog():
    posts = Posts.query.filter_by().all()
    # [0:params['no_of_posts']]
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):(page-1) *
                  int(params['no_of_posts']) + int(params['no_of_posts'])]

    if(page == 1):
        prev = '#'
        next = '/blog?page='+str(page+1)
    elif(page == last):
        prev = '/blog?page='+str(page-1)
        next = "#"
    else:
        prev = '/blog?page='+str(page-1)
        next = '/blog?page='+str(page+1)
    return render_template("blog.html", params=params, posts=posts, prev=prev, next=next)


@ app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if ('user' in session and session['user'] == params["admin_user"]):
        posts = Posts.query.all()
        return render_template("admin.html", params=params, posts=posts)

    if(request.method == "POST"):
        recievedAdminUsername = request.form.get("admin-username")
        recievedAdminPassword = request.form.get("admin-password")

        if(recievedAdminUsername == params["admin_user"] and recievedAdminPassword == params["admin_pass"]):
            # set the session variable
            session['user'] = recievedAdminUsername
            posts = Posts.query.all()
            return render_template("admin.html", params=params, posts=posts)

    return render_template("login.html", params=params)


@ app.route("/admin/viewapplication", methods=['GET', 'POST'])
def viewjobapplications():
    applications = Job_application.query.filter_by().all()[
        0:params["no_of_jobapplications"]]
    return render_template("viewapplication.html", params=params, applications=applications)


@ app.route("/admin/addposts", methods=['GET', 'POST'])
def addpost():
    if(request.method == 'POST'):
        Posttitle = request.form.get("posttitle")
        Postsubtitle = request.form.get("postsubtitle")
        Postslug = request.form.get("postslug")
        Postcontent = request.form.get("postcontent")
        Postedby = request.form.get("postedby")
        postdate = request.form.get("postedate")

        post_entry = Posts(
            title=Posttitle,
            subtitle=Postsubtitle,
            slug=Postslug,
            content=Postcontent,
            postedby=Postedby,
            DATE=datetime.now()
        )
        db.session.add(post_entry)
        db.session.commit()

    posts = Posts.query.all()
    return render_template("addpost.html", params=params, posts=posts)


@ app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == "POST":
            title = request.form.get('edit_title')
            tagline = request.form.get('edit_tagline')
            postslug = request.form.get('edit_postslug')
            postedby = request.form.get('edit_postedby')
            postcontent = request.form.get('edit_postcontent')
            if sno == '0':
                post = Posts(title=title, subtitle=tagline, slug=postslug,
                             postedby=postedby, content=postcontent, DATE=datetime.now())
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = title
                post.subtitle = tagline
                post.slug = postslug
                post.postedby = postedby
                post.content = postcontent
                DATE = datetime.now()

                db.session.add(post)
                db.session.commit()
                return redirect('/edit/'+sno)

        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post)


@ app.route("/admin/addjob", methods=['GET', 'POST'])
def addjob():
    if(request.method == "POST"):
        form_jobcode = request.form.get("enterjobcode")
        form_jobdesc = request.form.get("jobdesc")

        add_job_entry = Jobs(
            date=datetime.now(),
            jobcode=form_jobcode,
            jobdescription=form_jobdesc
        )
        db.session.add(add_job_entry)
        db.session.commit()
    return render_template("addjob.html", params=params)


@ app.route("/admin/addproduct", methods=['GET', 'POST'])
def addproduct():
    return render_template("addproduct.html", params=params)


app.run(debug=True)
