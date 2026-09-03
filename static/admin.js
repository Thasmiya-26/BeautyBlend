// ==============================
// SHOW / HIDE PASSWORD
// ==============================

function togglePassword() {

    const password = document.getElementById("password");
    const eye = document.getElementById("eye");

    if (password.type === "password") {

        password.type = "text";
        eye.innerHTML = '<i class="fa-solid fa-eye"></i>';

    } else {

        password.type = "password";
        eye.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
    }
}


// ==============================
// ADMIN LOGIN
// ==============================

async function adminLogin() {

    const username =
        document.getElementById("username").value.trim();

    const password =
        document.getElementById("password").value;


    // Username validation
    if (username === "") {

        document.getElementById("message").style.color = "red";
        document.getElementById("message").innerText =
            "Please enter username.";

        return;
    }


    // Password validation
    if (password === "") {

        document.getElementById("message").style.color = "red";
        document.getElementById("message").innerText =
            "Please enter password.";

        return;
    }


    try {

        const response = await fetch("/api/admin-login/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })
        });


        const data = await response.json();


        if (data.success) {

            localStorage.setItem("adminLoggedIn", "true");
            localStorage.setItem("adminName", username);

            window.location.href = "/dashboard/";

        } else {

            document.getElementById("message").style.color = "red";

            document.getElementById("message").innerText =
                data.message;
        }


    } catch (error) {

        document.getElementById("message").style.color = "red";

        document.getElementById("message").innerText =
            "Unable to connect to the server.";

        console.error(error);
    }
}