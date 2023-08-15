from PIL import Image
from flask import Flask, render_template,request,redirect,session,jsonify
import datetime
from pytesseract import pytesseract
from DBConnection import Db
import face_recognition
import scipy.misc

app = Flask(__name__)
app.secret_key="abc"

# @app.route('/')
# def abs():
#     return render_template("index.html")


path=r"C:\Adarsh\S8 CSE\CSD416 PROJECT PHASE 2\Eyemate\static\pic\\"
static_path=r"C:\Adarsh\S8 CSE\CSD416 PROJECT PHASE 2\Eyemate\static\\"
static_path1=r"C:\Adarsh\S8 CSE\CSD416 PROJECT PHASE 2\Eyemate\static\knownperson\\"

@app.route('/',methods=['get','post'])
def login():
    if request.method=="POST":
        name=request.form['textfield']
        password=request.form['textfield2']
        db=Db()
        res=db.selectOne("select * from login WHERE username='"+name+"'and password='"+password+"'")
        if res is not None:
            if res['usertype']=='admin':
                session['lg']="lo"
                return redirect('/view_adminhome')
            elif res['usertype'] == 'caretaker':
                session['lid']= res['login_id']
                session['lg'] = "lo"
                return redirect('/view_cthome')
            else:
                return '<script>alert("Invalid User")</script>'
        else:
            return '<script>alert("User not exist")</script>'
    else:
        return render_template("index.html")

@app.route('/view_review')
def view_review():
    if session['lg']=="lo":
        db=Db()
        res=db.select("select * from reviews,caretaker where reviews.ct_id=caretaker.ct_id")
        return render_template('Admin/review.html',data=res)
    return redirect('/')

@app.route('/view_blindlist')
def view_blindlist():
    if session['lg'] == "lo":
        db=Db()
        res=db.select("select * from blind,caretaker where blind.ct_id=caretaker.ct_id")
        return render_template('Admin/viewblindlist.html',data=res)
    return redirect('/')

@app.route('/view_caretaker')
def view_caretaker():
    if session['lg'] == "lo":
        db=Db()
        res=db.select("select * from caretaker, login WHERE login.usertype = 'caretaker' AND  login.username=caretaker.ct_mail or login.username=caretaker.ct_name")
        return render_template('Admin/viewcaretaker.html',data=res)
    return redirect('/')


@app.route('/verify_caretaker')
def verify_caretaker():
    if session['lg'] == "lo":
        db=Db()
        res=db.select("select * from caretaker,login where login.login_id=caretaker.ct_id and login.usertype='Pending'")
        return render_template('Admin/vnvcaretaker.html',data=res)
    return redirect('/')

@app.route('/approve_ct/<id>')
def approve(id):
    if session['lg'] == "lo":
        db=Db()
        res=db.update("update login set usertype='caretaker' where login_id='"+id+"'")
        return '<script>alert("Approved successfully");window.location="/verify_caretaker#abc"</script>'
    return redirect('/')

@app.route('/reject_ct/<id>')
def reject(id):
    if session['lg'] == "lo":
        db=Db()
        res=db.update("update login set usertype='rejected' where login_id='"+id+"'")
        return '<script>alert("Caretaker rejected");window.location="/verify_caretaker#abc"</script>'
    return redirect('/')

@app.route('/view_changepass',methods=['get','post'])
def view_changepass():
    if session['lg'] == "lo":
        if request.method=="POST":
            curpassword= request.form['textfield']
            newpassword = request.form['textfield2']
            conpassword= request.form['textfield3']
            db = Db()
            res = db.selectOne("select * from login WHERE password='"+curpassword+"'and usertype='admin'")
            if res is not None:
                if newpassword==conpassword:
                    db=Db()
                    db.update("update login set password='"+conpassword+"'where usertype='admin'")
                    return '<script>alert("Password changed Successfully");window.location="/"</script>'
                else:
                    return '<script>alert("Password mismatched");window.location="/view_changepass"</script>'
            else:
                return '<script>alert("Incorrect password");window.location="/view_changepass"</script>'
        else:
            return render_template('Admin/changepass.html')
    return redirect('/')

@app.route('/view_adminhome')
def view_adminhome():
    if session['lg'] == "lo":
        return render_template('Admin/adminindex.html')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    session['lg']=""
    return redirect('/')



# =============================================CARETAKER MODULE=====================================================

@app.route('/ctregister',methods=['get','post'])
def ctregister():

        if request.method=="POST":
            name=request.form['textfield']
            gender=request.form['gender']
            mobile=request.form['textfield2']
            pin=request.form['textfield3']
            mail=request.form['textfield4']
            place=request.form['textfield5']
            password=request.form['textfield6']
            con_password=request.form['textfield7']
            db=Db()
            if password==con_password:
                res=db.insert("insert into login(username,password,usertype) VALUES ('"+mail+"','"+con_password+"','pending')")
                db.insert("insert into caretaker VALUES ('"+str(res)+"','"+name+"','"+gender+"','"+mobile+"','"+pin+"','"+mail+"','"+place+"')")
                return '<script>alert("Registered successfully");window.location="/"</script>'
            else:
                return '<script>alert("Password mismatch");window.location="/ctregister"</script>'
        else:
            return render_template("ctregister.html")

@app.route('/view_cthome')
def view_cthome():
    if session['lg'] == "lo":
        db=Db()
        res2 = db.select("select ct_name from caretaker where ct_id='" + str(session['lid']) + "'")
        return render_template('Caretaker/caretakerindex.html',data=res2)
    return redirect('/')

@app.route('/view_blind')
def view_blind():
    if session['lg'] == "lo":
        db=Db()
        # res=db.select("select * from blind WHERE ct_id='"+str(session['lid'])+"'")
        res2=db.select("select * from blind,location where blind.blind_id=location.blind_id and blind.ct_id='"+str(session['lid'])+"'")
        return render_template('Caretaker/ctviewblind.html',data2=res2)
    return redirect('/')

@app.route('/add_blind',methods=['get','post'])
def add_blind():
    if session['lg'] == "lo":
        if request.method == "POST":
            name = request.form['textfield']
            age= request.form['textfield8']
            gender = request.form['radio']
            mobile = request.form['textfield2']
            pin = request.form['textfield3']
            mail = request.form['textfield5']
            place = request.form['textfield4']

            db = Db()
            db.insert("insert into blind(blind_name,blind_age,blind_gender,blind_mob,blind_pin,blind_place,blind_email,ct_id) VALUES ('" + name + "','"+age+"','" + gender + "','" + mobile + "','" + pin + "','" + place + "','" + mail + "','"+str(session['lid'])+"')")
            return '<script>alert("Entry added successfully");window.location="/view_cthome"</script>'

        else:
            return render_template("Caretaker/addblind.html")
    else:
        return redirect('/')

@app.route('/add_knownperson/<bid>',methods=['get','post'])
def add_knownperson(bid):
    if session['lg'] == "lo":
        if request.method == "POST":
            name = request.form['textfield']
            age= request.form['textfield6']
            gender = request.form['radio']
            mobile = request.form['textfield2']
            address = request.form['textfield3']
            image=request.files['filefield']
            date=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            image.save(r"C:\Adarsh\S8 CSE\CSD416 PROJECT PHASE 2\Eyemate\static\knownperson\\"+date+'.jpg')
            path="/static/knownperson/"+date+'.jpg'
            db = Db()
            try:
                b_img = face_recognition.load_image_file(r"C:\Adarsh\S8 CSE\CSD416 PROJECT PHASE 2\Eyemate\static\knownperson\\"+date+'.jpg')
                b_imgs = face_recognition.face_encodings(b_img)[0]
                db.insert("insert into knownperson (kp_name,kp_age,kp_gender,kp_mobile,kp_address,blind_id,kp_image)VALUES ('" + name + "','"+age+"','" + gender + "','" + mobile + "','" + address + "','"+str(bid)+"','"+str(path)+"')")
                return '<script>alert("Entry added successfully");window.location="/view_blind#abc"</script>'
            except Exception as e:
                return '<script>alert("Can not identify");window.location="/view_blind#abc"</script>'

        else:
            return render_template("Caretaker/addkp.html")
    else:
        return redirect('/')

@app.route('/view_knownperson/<bid>')
def view_knownperson(bid):
    if session['lg'] == "lo":
        db=Db()
        res=db.select("select * from knownperson WHERE blind_id='"+bid+"'")
        return render_template('Caretaker/viewkp.html',data=res)
    else:
        return redirect('/')

@app.route('/view_accident')
def view_accident():
    if session['lg'] == "lo":
        db=Db()
        # res=db.select("select * from accident,blind where accident.blind_id=blind.blind_id and blind.ct_id='"+str(session['lid'])+"'")
        res=db.select("select accident.accident_date,blind.blind_name,location.* from accident, blind,location where blind.blind_id=accident.blind_id and blind.blind_id=location.blind_id and blind.ct_id='"+str(session['lid'])+"'")
        return render_template('Caretaker/viewaccident.html',data=res)
    else:
        return redirect('/')

@app.route('/view_emergency')
def view_emergency():
    if session['lg'] == "lo":
        db=Db()
        res=db.select("select emergency.emergency_date,blind.blind_name,location.* from emergency, blind,location where blind.blind_id=emergency.blind_id and blind.blind_id=location.blind_id and blind.ct_id='"+str(session['lid'])+"'")
        return render_template('Caretaker/viewemergency.html',data=res)
    else:
        return redirect('/')

@app.route('/update_blind/<id>',methods=['get','post'])
def update_blind(id):
    if session['lg'] == "lo":
        if request.method=="POST":
            name = request.form['textfield']
            age= request.form['textfield8']
            gender = request.form['radio']
            mobile = request.form['textfield2']
            pin = request.form['textfield3']
            mail = request.form['textfield5']
            place = request.form['textfield4']
            db=Db()
            db.update("update blind set blind_name='"+name+"',blind_age='"+age+"',blind_gender='"+gender+"',blind_mob='"+mobile+"',blind_pin='"+pin+"',blind_email='"+mail+"',blind_place='"+place+"' where blind_id='"+id+"'")
            return '<script>alert("Blind details updated sucessfully");window.location="/view_blind"</script>'
        else:
            db=Db()
            res=db.selectOne("select * from blind where blind_id='"+id+"'")
            return render_template('Caretaker/update_blind.html',data=res)
    return redirect('/')

@app.route('/delete_blind/<id>')
def delete_blind(id):
    if session['lg'] == "lo":
        db=Db()
        db.delete("delete from blind where blind_id ='"+id+"'")
        return '<script>alert("Blind details Deleted sucessfully");window.location="/view_blind#abc"</script>'
    else:
        return redirect('/')

@app.route('/update_kp/<id>',methods=['get','post'])
def update_kp(id):
    if session['lg'] == "lo":
        if request.method=="POST":
            name = request.form['textfield']
            age = request.form['textfield6']
            gender = request.form['radio']
            mobile = request.form['textfield2']
            address = request.form['textfield3']
            image = request.files['filefield']
            date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            image.save(r"C:\Adarsh\S8 CSE\CSD416 PROJECT PHASE 2\Eyemate\static\knownperson\\" + date + '.jpg')
            path = "/static/knownperson/" + date + '.jpg'
            db=Db()

            if request.files !=None:
                if image.filename!="":
                    db.update("update knownperson set kp_name='" + name + "',kp_age='" + age + "',kp_gender='" + gender + "',kp_mobile='" + mobile + "',kp_address='" + address + "',kp_image='"+str(path)+"' where kp_id='" + id + "'")
                    return '<script>alert("Known person updated sucessfully");window.location="/view_blind#abc"</script>'
                else:
                    db.update("update knownperson set kp_name='"+name+"',kp_age='"+age+"',kp_gender='"+gender+"',kp_mobile='"+mobile+"',kp_address='"+address+"' where kp_id='"+id+"'")
                    return '<script>alert("Known person updated sucessfully");window.location="/view_blind#abc"</script>'
            else:
                db.update("update knownperson set kp_name='" + name + "',kp_age='" + age + "',kp_gender='" + gender + "',kp_mobile='" + mobile + "',kp_address='" + address + "' where kp_id='" + id + "'")
                return '<script>alert("Known person updated sucessfully");window.location="/view_blind#abc"</script>'
        else:
            db=Db()
            res=db.selectOne("select * from knownperson where kp_id='"+id+"'")
            return render_template('Caretaker/updatekp.html',data=res)
    return redirect('/')

@app.route('/delete_kp/<id>')
def delete_kp(id):
    if session['lg'] == "lo":
        db=Db()
        db.delete("delete from knownperson where kp_id ='"+id+"'")
        return '<script>alert("Known person details Deleted sucessfully");window.location="/view_blind#abc"</script>'
    else:
        return redirect('/')

@app.route('/add_review',methods=['get','post'])
def add_review():
    if session['lg'] == "lo":
        if request.method == "POST":
            review = request.form['textarea']
            rating= request.form['textfield']


            db = Db()
            db.insert("insert into reviews(review,rating,ct_id,review_date) VALUES ('" + review + "','"+rating+"','"+str(session['lid'])+"',curdate())")
            return '<script>alert("Review submitted");window.location="/view_cthome"</script>'

        else:
            return render_template("Caretaker/review.html")
    else:
        return redirect('/')

# @app.route('/rate')
# def rate():
#     return render_template("Caretaker/rate.html")

@app.route("/rate", methods=['get','post'])
def rate_post():
    if request.method=="POST":
        rt = request.form['star']
        revie=request.form['textfield5']
        # return "Rating = " + rt
        db=Db()
        db.insert("insert into reviews values('','"+str(session['lid'])+"','"+revie+"','"+rt+"',curdate())")
        return '<script>alert("Rating submitted");window.location="/view_cthome"</script>'
    else:
        return render_template("Caretaker/rate.html")



# =============================================BLIND MODULE=====================================================

@app.route('/updateloc',methods=['post'])
def location():
            latitude = request.form['lati']
            longitude = request.form['longi']
            id=request.form['bid']
            db = Db()
            res=db.selectOne("select *from location where blind_id='"+id+"'")
            if res is not None:
                db.update("update location set loc_latitude='"+latitude+"', loc_longitude='"+longitude+"' where  blind_id='"+id+"'")
            else:
                db.insert("insert into location(loc_latitude,loc_longitude,blind_id) VALUES ('" + latitude + "','"+longitude+"','"+ id +"')")
            return jsonify(status="ok")

@app.route('/verify_blind',methods=['post'])
def verify_blind():
        phone=request.form['u']
        db=Db()
        res=db.selectOne("select * from blind WHERE blind_mob='"+phone+"'")
        if res is not None:
                q=db.selectOne("select * from caretaker,blind where blind.ct_id=caretaker.ct_id and blind.blind_id='"+str(res['blind_id'])+"'")

                return jsonify(status="ok",lid=res['blind_id'],c=q['ct_mob'])
        else:
                return jsonify(status="no")

@app.route('/detect',methods=['post'])
def detect():
        command = request.form['command']
        id = request.form['id']
        lat=request.form['lat']
        long=request.form['lon']
        print("command :",command)

        db=Db()
        q = db.selectOne("select * from blind where blind_mob='"+str(id)+"'")
        id=str(q['blind_id'])

        if command=='look':
            photo = request.files["pic"]
            photo.save(r"C:\Adarsh\S8 CSE\CSD416 PROJECT PHASE 2\Eyemate\static\\" + "\\" + photo.filename)
            op = ""
            import cv2
            import numpy as np

            def get_output_layers(net):

                layer_names = net.getLayerNames()

                output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

                return output_layers

            # image = cv2.imread(args.image)
            image = cv2.imread(r"C:\Adarsh\S8 CSE\CSD416 PROJECT PHASE 2\Eyemate\static\\" + "\\" + photo.filename)

            Width = image.shape[1]
            Height = image.shape[0]
            scale = 0.00392

            classes = None

            with open('yolov3.txt', 'r') as f:
                classes = [line.strip() for line in f.readlines()]

            COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
            net = cv2.dnn.readNet('C:\\Adarsh\\S8 CSE\\CSD416 PROJECT PHASE 2\\Eyemate\\static\\yolov3.weights',
                                  'C:\\Adarsh\\S8 CSE\\CSD416 PROJECT PHASE 2\\Eyemate\\static\\yolov3.cfg')
            blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)

            outs = net.forward(get_output_layers(net))

            class_ids = []
            confidences = []
            boxes = []
            conf_threshold = 0.5
            nms_threshold = 0.4

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * Width)
                        center_y = int(detection[1] * Height)
                        w = int(detection[2] * Width)
                        h = int(detection[3] * Height)
                        x = center_x - w / 2
                        y = center_y - h / 2
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])

            indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
            objectss = ""
            for i in indices:
                i = i[0]
                objectss = objectss + classes[class_ids[i]] + ","
            print(objectss)
            return jsonify(status="ok", message=objectss)
        elif command == 'read':

            photo = request.files["pic"]
            photo.save(path + "a.jpg")
            config = ('-1 eng --oem 1 --psm 3')
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

            text = pytesseract.image_to_string(Image.open(path + "a.jpg"))
            # print(text)
            return jsonify(status="ok",message=text)
        elif command == 'capture':
            photo = request.files["pic"]
            photo.save(path+"ca.jpg")
            Original_Image = Image.open(path+"ca.jpg")

            rotated_image2 = Original_Image.transpose(Image.ROTATE_270)
            rotated_image2.save(path + "ca_270.jpg")

            qry = "select * from knownperson where blind_id='" + id + "'"
            print(qry)
            db = Db()
            res = db.select(qry)
            known_faces = []
            userids = []
            person_name = []

            identified = ""
            if res is not None:
                for result in res:
                    k = result["kp_image"]
                    k1 = k.split("/")
                    k1 = k1[len(k1) - 1]
                    img = static_path1  + k1
                    b_img = face_recognition.load_image_file(img)
                    b_imgs = face_recognition.face_encodings(b_img)[0]
                    known_faces.append(b_imgs)
                    userids.append(result["kp_id"])
                    person_name.append(result["kp_name"])
                    print(img + "done")

                unknown_image = face_recognition.load_image_file(path + "ca_270.jpg")
                unkonownpersons = face_recognition.face_encodings(unknown_image)

                if len(unkonownpersons) > 0:

                    for i in range(0, len(unkonownpersons)):
                        h = unkonownpersons[i]

                        red = face_recognition.compare_faces(known_faces, h, tolerance=0.45)  # true,false,false,false]

                        for i in range(0, len(red)):
                            if red[i] == True:
                                identified = identified + person_name[i]
                    return jsonify(status="ok", message=identified)
                else:
                    return jsonify(status="no", message="Person not found")



@app.route('/accident_detection',methods=['post'])
def accident_detection():
    lat=request.form['lati']
    log=request.form['longi']
    lid=request.form['did']
    print(lat)
    db=Db()
    qry=db.selectOne("select * from accident where blind_id='"+lid+"' and accident_date=now()")
    if qry is not None:
        aid=qry['accident_id']
        db.update("update accident set accident_latitude='"+lat+"' and accident_longitude='"+log+"' where accident_id='"+str(aid)+"'")
        return jsonify(status="ok")
    else:
        db.insert("insert into accident(accident_date,accident_latitude,accident_longitude,blind_id) VALUES (now(),'"+lat+"','"+log+"','"+lid+"')")
        # db.insert("insert into accident(accident_date,accident_latitude,accident_longitude,blind_id) VALUES (getdate(),'"+lat+"','"+log+"','"+lid+"')")
        return jsonify(status="ok")



# ----------emergency---

@app.route('/emergency_help',methods=['post'])
def emergency_help():
    lat = request.form['lati']
    log = request.form['longi']
    id = request.form['did']
    db=Db()
    print(lat)
    db.insert("insert into emergency(emergency_date,emergency_latitude,emergency_longitude,blind_id) VALUES (now(),'"+lat+"','"+log+"','" + id + "')")
    return jsonify(status="ok")





#######################################################################################################################

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000)

