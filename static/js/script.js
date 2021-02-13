// Drop down menu button functioning script in the resposnive mode
var date = new Date();
var latestYear = date.getFullYear();
document.getElementById("date-year").innerHTML = latestYear;


// Image Slider 

function showNavigation(){
    var responsiveNavbarItems = document.getElementById('responsive-nav');
    var hamBurgerMenu = document.getElementById("hamburgermenu");
    if (responsiveNavbarItems.className === "responsive-nav"){
        responsiveNavbarItems.className += " active";
        hamBurgerMenu.style.display = "none";
    }
}

function closeNavigation() {
    var responsiveNavbarItems = document.getElementById('responsive-nav');
    var hamBurgerMenu = document.getElementById("hamburgermenu");
    if (responsiveNavbarItems.className === "responsive-nav active"){
        responsiveNavbarItems.className = "responsive-nav";
        hamBurgerMenu.style.display = "block";
    }
}


// Form validation script

const form = document.getElementById("contact-form");
const username = document.getElementById("username");
const email = document.getElementById("email");
const phone = document.getElementById("phone");
const message = document.getElementById("message");

form.addEventListener('submit', (e) => {
    e.preventDefault;

    checkInputs();
});

function checkInputs(){
    const usernameValue = username.value.trim();
    const emailValue = email.value.trim();
    const phoneValue = phone.value.trim();
    const messageValue = message.value.trim();

    if(usernameValue === ''){
        setErrorFor(username, "Username cannot be blank");
    }else if (username === isPhone(username)){
        setErrorFor(username, "Username cannot be numerical");
    } else {
        setSuccessFor(username)
    }

    if(emailValue === ''){
        setErrorFor(email, "email cannot be blank");
    } else if(!isEmail(emailValue)){
        setErrorFor(email,"Email is not valid");
    } else {
        setSuccessFor(email)
    }

    if(phoneValue === ''){
        setErrorFor(phone, "Phone cannot be blank");
    } else if (!isPhone(phoneValue)){
        setErrorFor(phone, "Phone number is not valid");
    } else {
        setSuccessFor(phone);
    }

    if(messageValue === ''){
        setErrorFor(message, "Message cannot be blank");
    } else{
        setSuccessFor(message);
    }
}

function setErrorFor(element, message){
    const formControl = element.parentElement;
    const small = formControl.querySelector('small');
    small.innerText = message;
    formControl.className = "form-control error";
}

function setSuccessFor(element){
    const formControl = element.parentElement;
    formControl.className = "form-control success";
}

function isEmail(email)  {
    return /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(email);
}


function isPhone(phone){
    return  /^\d{10}$/.test(phone);
}

