import pyrebase

config = {
    "apiKey": "AIzaSyB-vDYih44gd38rklsIesGsGkCOCOqZ42A",
    "authDomain": "auth-development-dbbc1.firebaseapp.com",
    "databaseURL": "https://auth-development-dbbc1-default-rtdb.firebaseio.com",
    "projectId": "auth-development-dbbc1",
    "storageBucket": "auth-development-dbbc1.appspot.com",
    "messagingSenderId": "906326561427",
    "appId": "1:906326561427:web:1e50d12b2ed3acde327366"

}

firebase = pyrebase.initialize_app(config)
storage  = firebase.storage()

#path_on_cloud = "images/Students/Mukesh"
#path_local = "ImagesAttendance/Mukesh Ambani.jpg"
#storage.child(path_on_cloud).put(path_local)

file = input("Enter the name of the file you want to upload")
cloudfilename = input("Enter the name for the file in the storage")
storage.child(cloudfilename).put(file)

