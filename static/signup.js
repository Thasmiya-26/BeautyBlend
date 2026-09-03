// ==============================
// SHOW / HIDE PASSWORD
// ==============================

function togglePassword() {

    const password =
        document.getElementById("password");

    const eye =
        document.getElementById("eye1");


    if (password.type === "password") {

        password.type = "text";

        eye.innerHTML =
            '<i class="fa-solid fa-eye"></i>';

    } else {

        password.type = "password";

        eye.innerHTML =
            '<i class="fa-solid fa-eye-slash"></i>';
    }
}


// ==============================
// SHOW / HIDE CONFIRM PASSWORD
// ==============================

function toggleConfirmPassword() {

    const confirmPassword =
        document.getElementById("confirmPassword");

    const eye =
        document.getElementById("eye2");


    if (confirmPassword.type === "password") {

        confirmPassword.type = "text";

        eye.innerHTML =
            '<i class="fa-solid fa-eye"></i>';

    } else {

        confirmPassword.type = "password";

        eye.innerHTML =
            '<i class="fa-solid fa-eye-slash"></i>';
    }
}


// ==============================
// REGISTER USER
// ==============================

async function register() {

    const fullname =
        document.getElementById("fullname").value.trim();


    const email =
        document.getElementById("email").value.trim();


    const phone =
        document.getElementById("phone").value.trim();


    const password =
        document.getElementById("password").value;


    const confirmPassword =
        document.getElementById("confirmPassword").value;


    // ==============================
    // NAME VALIDATION
    // ==============================

    if (fullname === "") {

        alert("Please enter your full name.");

        return;
    }


    if (!/^[a-zA-Z\s]+$/.test(fullname)) {

        alert(
            "Please enter alphabets only in the name."
        );

        return;
    }


    // ==============================
    // EMAIL VALIDATION
    // ==============================

    if (email === "") {

        alert(
            "Please enter your email address."
        );

        return;
    }


    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (!emailPattern.test(email)) {

        alert(
            "Please enter a valid email address."
        );

        return;
    }


    // ==============================
    // PHONE VALIDATION
    // ==============================

    if (phone === "") {

        alert(
            "Please enter your phone number."
        );

        return;
    }


    if (!/^\d+$/.test(phone)) {

        alert(
            "Phone number must contain digits only."
        );

        return;
    }


    if (phone.length !== 10) {

        alert(
            "Phone number must contain exactly 10 digits."
        );

        return;
    }


    // ==============================
    // PASSWORD VALIDATION
    // ==============================

    if (password === "") {

        alert(
            "Please enter your password."
        );

        return;
    }


    if (password.length < 8) {

        alert(
            "Password must contain at least 8 characters."
        );

        return;
    }


    // ==============================
    // CONFIRM PASSWORD
    // ==============================

    if (password !== confirmPassword) {

        alert(
            "Passwords do not match."
        );

        return;
    }


    // ==============================
    // SEND DATA TO DJANGO
    // ==============================

    try {

        const response =
            await fetch(
                "/api/register/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        name: fullname,

                        email: email,

                        phone: phone,

                        password: password

                    })
                }
            );


        const data =
            await response.json();


        // ==============================
        // REGISTRATION SUCCESS
        // ==============================

        if (data.success) {

            alert(data.message);

            window.location.href =
                "/login/";

        }


        // ==============================
        // REGISTRATION ERROR
        // ==============================

        else {

            alert(data.message);

        }


    }


    catch (error) {

        console.error(
            "Registration error:",
            error
        );

        alert(
            "Unable to connect to the server."
        );

    }

}