// ==============================
// BEAUTY BLEND - USER LOGIN
// ==============================


// ==============================
// SHOW / HIDE PASSWORD
// ==============================

const togglePassword =
    document.getElementById("togglePassword");

const password =
    document.getElementById("password");


if (togglePassword && password) {

    togglePassword.addEventListener(
        "click",
        function () {

            if (password.type === "password") {

                password.type = "text";

                togglePassword.classList.remove(
                    "fa-eye-slash"
                );

                togglePassword.classList.add(
                    "fa-eye"
                );

            } else {

                password.type = "password";

                togglePassword.classList.remove(
                    "fa-eye"
                );

                togglePassword.classList.add(
                    "fa-eye-slash"
                );

            }

        }
    );

}


// ==============================
// LOGIN FORM
// ==============================

const loginForm =
    document.getElementById("loginForm");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            // ==============================
            // GET EMAIL
            // ==============================

            const emailInput =
                document.getElementById("email");


            if (!emailInput) {

                alert(
                    "Email field not found."
                );

                return;
            }


            const email =
                emailInput.value.trim();


            // ==============================
            // GET PASSWORD
            // ==============================

            const passwordInput =
                document.getElementById("password");


            if (!passwordInput) {

                alert(
                    "Password field not found."
                );

                return;
            }


            const passwordValue =
                passwordInput.value;


            // ==============================
            // EMAIL VALIDATION
            // ==============================

            if (email === "") {

                alert(
                    "Please enter your email address."
                );

                emailInput.focus();

                return;
            }


            const emailPattern =
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


            if (!emailPattern.test(email)) {

                alert(
                    "Please enter a valid email address."
                );

                emailInput.focus();

                return;
            }


            // ==============================
            // PASSWORD VALIDATION
            // ==============================

            if (passwordValue === "") {

                alert(
                    "Please enter your password."
                );

                passwordInput.focus();

                return;
            }


            if (passwordValue.length < 8) {

                alert(
                    "Password must contain at least 8 characters."
                );

                passwordInput.focus();

                return;
            }


            // ==============================
            // SEND LOGIN DATA TO DJANGO
            // ==============================

            try {

                const response =
                    await fetch(
                        "/api/login/",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({

                                    email: email,

                                    password:
                                        passwordValue

                                })

                        }
                    );


                const data =
                    await response.json();


                // ==============================
                // LOGIN SUCCESS
                // ==============================

                if (data.success) {


                    // --------------------------------
                    // SAVE USER NAME
                    // --------------------------------

                    localStorage.setItem(
                        "BeautyBlendUserName",
                        data.name
                    );
                    console.log("LOGIN NAME:",data.name);


                    // --------------------------------
                    // SAVE USER EMAIL
                    // --------------------------------

                    localStorage.setItem(
                        "BeautyBlendUserEmail",
                        data.email
                    );


                    // --------------------------------
                    // SAVE USER PHONE
                    // --------------------------------

                    localStorage.setItem(
                        "BeautyBlendUserPhone",
                        data.phone
                    );


                    // --------------------------------
                    // SAVE COMPLETE USER DATA
                    // This is used by Book.js
                    // --------------------------------

                    const loggedInUser = {

                        name: data.name,

                        email: data.email,

                        phone: data.phone

                    };


                    localStorage.setItem(
                        "loggedInUser",
                        JSON.stringify(
                            loggedInUser
                        )
                    );


                    // --------------------------------
                    // LOGIN STATUS
                    // --------------------------------

                    localStorage.setItem(
                        "BeautyBlendLoggedIn",
                        "true"
                    );


                    localStorage.setItem(
                        "loggedIn",
                        "true"
                    );


                    // --------------------------------
                    // SUCCESS MESSAGE
                    // --------------------------------

                    alert(
                        data.message
                    );


                    // --------------------------------
                    // GO TO HOME PAGE
                    // --------------------------------

                    window.location.href = "/";

                }


                // ==============================
                // LOGIN FAILED
                // ==============================

                else {

                    alert(
                        data.message
                    );

                }

            }


            // ==============================
            // SERVER / CONNECTION ERROR
            // ==============================

            catch (error) {

                console.error(
                    "Login error:",
                    error
                );


                alert(
                    "Unable to connect to the server."
                );

            }

        }
    );

}