// =====================================================
// BEAUTY BLEND - FORGOT PASSWORD
// Connected to Django Database
// =====================================================


// =====================================================
// SHOW / HIDE NEW PASSWORD
// =====================================================

function toggleNewPassword() {

    const password =
        document.getElementById("newPassword");

    const eye =
        document.getElementById("eye1");


    if (!password || !eye) {
        return;
    }


    if (password.type === "password") {

        password.type = "text";

        eye.classList.remove(
            "fa-eye-slash"
        );

        eye.classList.add(
            "fa-eye"
        );

    }

    else {

        password.type = "password";

        eye.classList.remove(
            "fa-eye"
        );

        eye.classList.add(
            "fa-eye-slash"
        );

    }

}


// =====================================================
// SHOW / HIDE CONFIRM PASSWORD
// =====================================================

function toggleConfirmPassword() {

    const password =
        document.getElementById("confirmPassword");

    const eye =
        document.getElementById("eye2");


    if (!password || !eye) {
        return;
    }


    if (password.type === "password") {

        password.type = "text";

        eye.classList.remove(
            "fa-eye-slash"
        );

        eye.classList.add(
            "fa-eye"
        );

    }

    else {

        password.type = "password";

        eye.classList.remove(
            "fa-eye"
        );

        eye.classList.add(
            "fa-eye-slash"
        );

    }

}


// =====================================================
// RESET PASSWORD
// =====================================================

async function resetPassword() {

    const emailElement =
        document.getElementById("email");

    const newPasswordElement =
        document.getElementById("newPassword");

    const confirmPasswordElement =
        document.getElementById("confirmPassword");


    // =================================================
    // CHECK FORM
    // =================================================

    if (
        !emailElement ||
        !newPasswordElement ||
        !confirmPasswordElement
    ) {

        alert(
            "Forgot Password form is not loaded correctly."
        );

        return;

    }


    const email =
        emailElement.value.trim();

    const newPassword =
        newPasswordElement.value;

    const confirmPassword =
        confirmPasswordElement.value;


    // =================================================
    // EMAIL VALIDATION
    // =================================================

    if (email === "") {

        alert(
            "Please enter your registered email."
        );

        emailElement.focus();

        return;

    }


    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (!emailPattern.test(email)) {

        alert(
            "Please enter a valid email address."
        );

        emailElement.focus();

        return;

    }


    // =================================================
    // PASSWORD VALIDATION
    // =================================================

    if (newPassword === "") {

        alert(
            "Please enter a new password."
        );

        newPasswordElement.focus();

        return;

    }


    if (newPassword.length < 8) {

        alert(
            "Password must contain at least 8 characters."
        );

        newPasswordElement.focus();

        return;

    }


    // =================================================
    // CONFIRM PASSWORD
    // =================================================

    if (confirmPassword === "") {

        alert(
            "Please confirm your new password."
        );

        confirmPasswordElement.focus();

        return;

    }


    if (newPassword !== confirmPassword) {

        alert(
            "Passwords do not match."
        );

        confirmPasswordElement.focus();

        return;

    }


    // =================================================
    // SEND DATA TO DJANGO
    // =================================================

    try {

        const response =
            await fetch(
                "/api/reset-password/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        email: email,

                        new_password:
                            newPassword

                    })

                }
            );


        const data =
            await response.json();


        // =================================================
        // SUCCESS
        // =================================================

        if (data.success) {

            alert(
                data.message
            );


            window.location.href =
                "/login/";

        }


        // =================================================
        // FAILED
        // =================================================

        else {

            alert(
                data.message ||
                "Unable to reset password."
            );

        }

    }


    // =================================================
    // CONNECTION ERROR
    // =================================================

    catch (error) {

        console.error(
            "Password reset error:",
            error
        );


        alert(
            "Unable to connect to the server."
        );

    }

}