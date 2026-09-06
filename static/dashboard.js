// =====================================================
// BEAUTY BLEND - ADMIN DASHBOARD
// Connected to Django + SQLite
// =====================================================


// =====================================================
// FIXED BEAUTYBLEND SERVICE CATALOGUE
// These are the services shown on the Services page.
// They are NOT taken from customer appointments.
// =====================================================

const AVAILABLE_SERVICES = [

    {
        name: "Hair Cut",
        price: 300,
        description: "Salon service"
    },

    {
        name: "Hair Wash",
        price: 200,
        description: "Salon service"
    },

    {
        name: "Hair Spa",
        price: 1200,
        description: "Salon service"
    },

    {
        name: "Smoothening",
        price: 3500,
        description: "Salon service"
    },

    {
        name: "Keratin Treatment",
        price: 4500,
        description: "Salon service"
    },

    {
        name: "Cleanup",
        price: 500,
        description: "Salon service"
    },

    {
        name: "Basic Facial",
        price: 700,
        description: "Salon service"
    },

    {
        name: "Fruit Facial",
        price: 1000,
        description: "Salon service"
    },

    {
        name: "Gold Facial",
        price: 1500,
        description: "Salon service"
    },

    {
        name: "Party Makeup",
        price: 2500,
        description: "Salon service"
    },

    {
        name: "Engagement Makeup",
        price: 7000,
        description: "Salon service"
    },

    {
        name: "Bridal Makeup",
        price: 12000,
        description: "Salon service"
    },

    {
        name: "Manicure",
        price: 500,
        description: "Salon service"
    },

    {
        name: "Pedicure",
        price: 700,
        description: "Salon service"
    },

    {
        name: "Nail Art",
        price: 1200,
        description: "Salon service"
    },

    {
        name: "Eyebrow",
        price: 50,
        description: "Salon service"
    },

    {
        name: "Upper Lip",
        price: 40,
        description: "Salon service"
    },

    {
        name: "Full Arms Wax",
        price: 400,
        description: "Salon service"
    },

    {
        name: "Full Legs Wax",
        price: 600,
        description: "Salon service"
    }

];


// =====================================================
// PAGE LOAD
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadDashboard();

    }
);


// =====================================================
// LOAD DASHBOARD DATA
// =====================================================

async function loadDashboard() {

    try {

        const response =
            await fetch("/api/dashboard-data/");

        const data =
            await response.json();


        if (!data.success) {

            console.error(
                "Unable to load dashboard data."
            );

            return;

        }


        // =================================================
        // TOTAL USERS
        // =================================================

        const totalUsers =
            document.getElementById("totalUsers");

        if (totalUsers) {

            totalUsers.textContent =
                data.totalUsers || 0;

        }


        // =================================================
        // TOTAL SERVICES
        // Always show the actual BeautyBlend catalogue count.
        // =================================================

        const totalServices =
            document.getElementById("totalServices");

        if (totalServices) {

            totalServices.textContent =
                AVAILABLE_SERVICES.length;

        }


        // =================================================
        // TOTAL APPOINTMENTS
        // =================================================

        const totalAppointments =
            document.getElementById("totalAppointments");

        if (totalAppointments) {

            totalAppointments.textContent =
                data.totalAppointments || 0;

        }


        // =================================================
        // TOTAL FEEDBACK
        // =================================================

        const totalFeedback =
            document.getElementById("totalFeedback");

        if (totalFeedback) {

            totalFeedback.textContent =
                data.totalFeedback || 0;

        }


        // =================================================
        // TOTAL COMBOS
        // =================================================

        const totalCombos =
            document.getElementById("totalCombos");

        if (totalCombos) {

            totalCombos.textContent =
                data.totalCombos || 0;

        }


        // =================================================
        // TOTAL REVENUE
        // =================================================

        const totalRevenue =
            document.getElementById("totalRevenue");

        if (totalRevenue) {

            totalRevenue.textContent =
                "₹" + (data.totalRevenue || 0);

        }

    }

    catch (error) {

        console.error(
            "Dashboard connection error:",
            error
        );

    }

}


// =====================================================
// SHOW DATA
// =====================================================

function showData(type) {

    const modal =
        document.getElementById("dataModal");

    const title =
        document.getElementById("modalTitle");

    const description =
        document.getElementById("modalDescription");

    const content =
        document.getElementById("modalContent");


    if (
        !modal ||
        !title ||
        !description ||
        !content
    ) {

        console.error(
            "Dashboard modal elements not found."
        );

        return;

    }


    modal.style.display =
        "flex";


    // USERS
    if (type === "users") {

        showUsers(
            title,
            description,
            content
        );

    }


    // SERVICES
    else if (type === "services") {

        showServices(
            title,
            description,
            content
        );

    }


    // APPOINTMENTS
    else if (type === "appointments") {

        showAppointments(
            title,
            description,
            content
        );

    }


    // REVENUE
    else if (type === "revenue") {

        showRevenue(
            title,
            description,
            content
        );

    }


    // FEEDBACK
    else if (type === "feedback") {

        showFeedback(
            title,
            description,
            content
        );

    }


    // COMBOS
    else if (type === "combos") {

        showCombos(
            title,
            description,
            content
        );

    }

}


// =====================================================
// SHOW USERS
// =====================================================

async function showUsers(
    title,
    description,
    content
) {

    title.textContent =
        "Registered Users";

    description.textContent =
        "Customers registered in Beauty Blend.";

    content.innerHTML =
        loadingMessage("Loading Users...");


    try {

        const response =
            await fetch("/api/dashboard-data/");

        const data =
            await response.json();


        if (
            !data.success ||
            !data.users ||
            data.users.length === 0
        ) {

            content.innerHTML =
                emptyMessage(
                    "No Users Yet",
                    "Registered customers will appear here."
                );

            return;

        }


        let html = "";


        data.users.forEach(
            function (user) {

                const name =
                    user.name ||
                    "Customer";

                const email =
                    user.email ||
                    "Email not available";


                html += `

                    <div class="data-card">

                        <div class="data-left">

                            <div class="data-avatar">
                                ${getInitial(name)}
                            </div>

                            <div class="data-info">

                                <h3>
                                    ${escapeHTML(
                                        String(name)
                                    )}
                                </h3>

                                <p>
                                    <i class="fa-solid fa-envelope"></i>
                                    ${escapeHTML(
                                        String(email)
                                    )}
                                </p>

                            </div>

                        </div>

                    </div>

                `;

            }
        );


        content.innerHTML =
            html;

    }

    catch (error) {

        console.error(
            "Users loading error:",
            error
        );

        content.innerHTML =
            emptyMessage(
                "Error",
                "Unable to load users."
            );

    }

}


// =====================================================
// SHOW SERVICES
// =====================================================
// IMPORTANT:
// This uses AVAILABLE_SERVICES.
// It does NOT use appointment.service.
// Therefore customer selections cannot change this list.
// =====================================================

function showServices(
    title,
    description,
    content
) {

    title.textContent =
        "Beauty Services";

    description.textContent =
        "All services available at Beauty Blend.";

    content.innerHTML =
        loadingMessage("Loading Services...");


    if (
        !AVAILABLE_SERVICES ||
        AVAILABLE_SERVICES.length === 0
    ) {

        content.innerHTML =
            emptyMessage(
                "No Services Yet",
                "Services available at Beauty Blend will appear here."
            );

        return;

    }


    let html = "";


    AVAILABLE_SERVICES.forEach(
        function (service) {

            const name =
                service.name ||
                "Service";

            const serviceDescription =
                service.description ||
                "";

            const price =
                service.price ||
                0;


            html += `

                <div class="service-card">

                    <div>

                        <h3>
                            ${escapeHTML(
                                String(name)
                            )}
                        </h3>

                        <p>
                            ${escapeHTML(
                                String(serviceDescription)
                            )}
                        </p>

                    </div>

                    <div class="service-price">
                        ₹${escapeHTML(
                            String(price)
                        )}
                    </div>

                </div>

            `;

        }
    );


    content.innerHTML =
        html;

}


// =====================================================
// SHOW COMBOS
// =====================================================
// Combos remain completely separate from appointments.
// They are loaded from the Combo table.
// =====================================================

async function showCombos(
    title,
    description,
    content
) {

    title.textContent =
        "Combo Packages";

    description.textContent =
        "All combo packages available at Beauty Blend.";

    content.innerHTML =
        loadingMessage("Loading Combos...");


    try {

        const response =
            await fetch("/api/dashboard-data/");

        const data =
            await response.json();


        if (
            !data.success ||
            !data.combos ||
            data.combos.length === 0
        ) {

            content.innerHTML =
                emptyMessage(
                    "No Combos Yet",
                    "Combo packages available at Beauty Blend will appear here."
                );

            return;

        }


        let html = "";


        data.combos.forEach(
            function (combo) {

                const name =
                    combo.name ||
                    "Combo";

                const comboDescription =
                    combo.description ||
                    "";

                const price =
                    combo.price ||
                    0;


                html += `

                    <div class="service-card">

                        <div>

                            <h3>
                                ${escapeHTML(
                                    String(name)
                                )}
                            </h3>

                            <p>
                                ${escapeHTML(
                                    String(comboDescription)
                                )}
                            </p>

                        </div>

                        <div class="service-price">
                            ₹${escapeHTML(
                                String(price)
                            )}
                        </div>

                    </div>

                `;

            }
        );


        content.innerHTML =
            html;

    }

    catch (error) {

        console.error(
            "Combos loading error:",
            error
        );

        content.innerHTML =
            emptyMessage(
                "Error",
                "Unable to load combos."
            );

    }

}


// =====================================================
// SHOW APPOINTMENTS
// =====================================================
// DO NOT CHANGE THIS SECTION.
// Customer-selected services remain here.
// =====================================================

async function showAppointments(
    title,
    description,
    content
) {

    title.textContent =
        "Appointments";

    description.textContent =
        "Customer appointments and selected services.";

    content.innerHTML =
        loadingMessage("Loading Appointments...");


    try {

        const response =
            await fetch("/api/dashboard-data/");

        const data =
            await response.json();


        if (
            !data.success ||
            !data.appointments ||
            data.appointments.length === 0
        ) {

            content.innerHTML =
                emptyMessage(
                    "No Appointments Yet",
                    "Booked appointments will appear here."
                );

            return;

        }


        let html = "";


        data.appointments.forEach(
            function (appointment) {

                const customerName =
                    appointment.customer_name ||
                    "Customer";

                const phone =
                    appointment.phone ||
                    "Not available";

                const services =
                    appointment.service ||
                    "Not available";

                const date =
                    appointment.date ||
                    "Not available";

                const time =
                    appointment.time ||
                    "Not available";

                const amount =
                    appointment.amount ||
                    0;

                const status =
                    appointment.status ||
                    "Booked";

                const paymentStatus =
                    appointment.payment_status ||
                    "Pending";


                let paymentHTML = "";


                if (
                    String(
                        paymentStatus
                    ).toLowerCase() === "paid"
                ) {

                    paymentHTML = `

                        <span class="status-badge paid">
                            Paid
                        </span>

                    `;

                }

                else {

                    paymentHTML = `

                        <div class="payment-action">

                            <span class="status-badge pending">
                                Pending
                            </span>

                            <button
                                type="button"
                                class="mark-paid-btn"
                                onclick="markPaymentPaid(${appointment.id})"
                            >

                                <i class="fa-solid fa-check"></i>

                                Mark as Paid

                            </button>

                        </div>

                    `;

                }


                html += `

                    <div class="appointment-card">

                        <div class="appointment-header">

                            <div class="data-left">

                                <div class="data-avatar">
                                    ${getInitial(customerName)}
                                </div>

                                <div class="data-info">

                                    <h3>
                                        ${escapeHTML(
                                            String(customerName)
                                        )}
                                    </h3>

                                    <p>
                                        <i class="fa-solid fa-phone"></i>
                                        ${escapeHTML(
                                            String(phone)
                                        )}
                                    </p>

                                </div>

                            </div>

                        </div>


                        <div class="appointment-details">

                            <div class="appointment-detail">

                                <span class="detail-label">
                                    Services
                                </span>

                                <strong>
                                    ${escapeHTML(
                                        String(services)
                                    )}
                                </strong>

                            </div>


                            <div class="appointment-detail">

                                <span class="detail-label">
                                    Date
                                </span>

                                <strong>
                                    ${escapeHTML(
                                        String(date)
                                    )}
                                </strong>

                            </div>


                            <div class="appointment-detail">

                                <span class="detail-label">
                                    Time
                                </span>

                                <strong>
                                    ${escapeHTML(
                                        String(time)
                                    )}
                                </strong>

                            </div>


                            <div class="appointment-detail">

                                <span class="detail-label">
                                    Amount
                                </span>

                                <strong>
                                    ₹${escapeHTML(
                                        String(amount)
                                    )}
                                </strong>

                            </div>


                            <div class="appointment-detail">

                                <span class="detail-label">
                                    Status
                                </span>

                                <span class="status-badge">
                                    ${escapeHTML(
                                        String(status)
                                    )}
                                </span>

                            </div>


                            <div class="appointment-detail">

                                <span class="detail-label">
                                    Payment
                                </span>

                                ${paymentHTML}

                            </div>

                        </div>

                    </div>

                `;

            }
        );


        content.innerHTML =
            html;

    }

    catch (error) {

        console.error(
            "Appointments loading error:",
            error
        );

        content.innerHTML =
            emptyMessage(
                "Error",
                "Unable to load appointments."
            );

    }

}


// =====================================================
// SHOW REVENUE
// =====================================================

async function showRevenue(
    title,
    description,
    content
) {

    title.textContent =
        "Total Revenue";

    description.textContent =
        "Revenue generated from completed payments.";

    content.innerHTML =
        loadingMessage("Loading Revenue...");


    try {

        const response =
            await fetch("/api/dashboard-data/");

        const data =
            await response.json();


        if (!data.success) {

            content.innerHTML =
                emptyMessage(
                    "Error",
                    "Unable to load revenue data."
                );

            return;

        }


        const totalRevenue =
            parseFloat(
                data.totalRevenue
            ) || 0;


        const paidAppointments =
            (
                data.appointments ||
                []
            ).filter(
                function (appointment) {

                    return String(
                        appointment.payment_status
                    ).toLowerCase() === "paid";

                }
            );


        let html = `

            <div class="revenue-summary">

                <div class="data-card">

                    <div class="data-left">

                        <div class="data-avatar">
                            ₹
                        </div>

                        <div class="data-info">

                            <h3>
                                Total Revenue
                            </h3>

                            <p>
                                Revenue received from paid appointments.
                            </p>

                        </div>

                    </div>

                    <div class="service-price">
                        ₹${totalRevenue.toFixed(2)}
                    </div>

                </div>

            </div>

        `;


        if (
            paidAppointments.length === 0
        ) {

            html += `

                <div class="empty-message">

                    <i class="fa-solid fa-indian-rupee-sign"></i>

                    <h3>
                        No Paid Appointments Yet
                    </h3>

                    <p>
                        Revenue details will appear here
                        after payments are marked as paid.
                    </p>

                </div>

            `;

            content.innerHTML =
                html;

            return;

        }


        html += `

            <h3 class="revenue-heading">
                Paid Appointments
            </h3>

        `;


        paidAppointments.forEach(
            function (appointment) {

                const customerName =
                    appointment.customer_name ||
                    "Customer";

                const service =
                    appointment.service ||
                    "Service";

                const date =
                    appointment.date ||
                    "Not available";

                const time =
                    appointment.time ||
                    "Not available";

                const amount =
                    appointment.amount ||
                    0;


                html += `

                    <div class="data-card">

                        <div class="data-left">

                            <div class="data-avatar">
                                ${getInitial(customerName)}
                            </div>

                            <div class="data-info">

                                <h3>
                                    ${escapeHTML(
                                        String(customerName)
                                    )}
                                </h3>

                                <p>
                                    ${escapeHTML(
                                        String(service)
                                    )}
                                </p>

                                <p>

                                    <i class="fa-solid fa-calendar"></i>

                                    ${escapeHTML(
                                        String(date)
                                    )}

                                    &nbsp;&nbsp;

                                    <i class="fa-solid fa-clock"></i>

                                    ${escapeHTML(
                                        String(time)
                                    )}

                                </p>

                            </div>

                        </div>

                        <div class="service-price">
                            ₹${escapeHTML(
                                String(amount)
                            )}
                        </div>

                    </div>

                `;

            }
        );


        content.innerHTML =
            html;

    }

    catch (error) {

        console.error(
            "Revenue loading error:",
            error
        );

        content.innerHTML =
            emptyMessage(
                "Error",
                "Unable to load revenue."
            );

    }

}


// =====================================================
// MARK PAYMENT AS PAID
// =====================================================

async function markPaymentPaid(
    appointmentId
) {

    if (!appointmentId) {

        alert(
            "Appointment ID is missing."
        );

        return;

    }


    const confirmation =
        confirm(
            "Are you sure you want to mark this payment as PAID?"
        );


    if (!confirmation) {

        return;

    }


    try {

        const response =
            await fetch(
                "/api/mark-payment-paid/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        appointment_id:
                            appointmentId

                    })

                }
            );


        const data =
            await response.json();


        if (data.success) {

            alert(
                "Payment marked as PAID successfully!"
            );


            loadDashboard();


            const title =
                document.getElementById(
                    "modalTitle"
                );

            const description =
                document.getElementById(
                    "modalDescription"
                );

            const content =
                document.getElementById(
                    "modalContent"
                );


            if (
                title &&
                description &&
                content
            ) {

                showAppointments(
                    title,
                    description,
                    content
                );

            }

        }

        else {

            alert(
                data.message ||
                "Unable to mark payment as paid."
            );

        }

    }

    catch (error) {

        console.error(
            "Payment update error:",
            error
        );

        alert(
            "Unable to connect to the server."
        );

    }

}


// =====================================================
// SHOW FEEDBACK
// =====================================================

async function showFeedback(
    title,
    description,
    content
) {

    title.textContent =
        "Customer Feedback";

    description.textContent =
        "Feedback submitted by Beauty Blend customers.";

    content.innerHTML =
        loadingMessage("Loading Feedback...");


    try {

        const response =
            await fetch(
                "/api/dashboard-data/"
            );

        const data =
            await response.json();


        if (
            !data.success ||
            !data.feedback ||
            data.feedback.length === 0
        ) {

            content.innerHTML =
                emptyMessage(
                    "No Feedback Yet",
                    "Customer feedback will appear here."
                );

            return;

        }


        let html = "";


        data.feedback.forEach(
            function (item) {

                const customerName =
                    item.customer_name ||
                    "Customer";

                const message =
                    item.message ||
                    "No message";

                const rating =
                    parseInt(
                        item.rating
                    ) || 0;


                let stars = "";


                for (
                    let i = 1;
                    i <= 5;
                    i++
                ) {

                    stars +=
                        i <= rating
                            ? "★"
                            : "☆";

                }


                html += `

                    <div class="data-card">

                        <div class="data-left">

                            <div class="data-avatar">
                                ${getInitial(customerName)}
                            </div>

                            <div class="data-info">

                                <h3>
                                    ${escapeHTML(
                                        String(customerName)
                                    )}
                                </h3>

                                <p class="rating">
                                    ${stars}
                                </p>

                                <p>
                                    ${escapeHTML(
                                        String(message)
                                    )}
                                </p>

                            </div>

                        </div>

                    </div>

                `;

            }
        );


        content.innerHTML =
            html;

    }

    catch (error) {

        console.error(
            "Feedback loading error:",
            error
        );

        content.innerHTML =
            emptyMessage(
                "Error",
                "Unable to load feedback."
            );

    }

}


// =====================================================
// LOADING MESSAGE
// =====================================================

function loadingMessage(
    message
) {

    return `

        <div class="empty-message">

            <i class="fa-solid fa-spinner fa-spin"></i>

            <h3>
                ${escapeHTML(message)}
            </h3>

            <p>
                Please wait.
            </p>

        </div>

    `;

}


// =====================================================
// EMPTY MESSAGE
// =====================================================

function emptyMessage(
    title,
    message
) {

    return `

        <div class="empty-message">

            <i class="fa-solid fa-folder-open"></i>

            <h3>
                ${escapeHTML(title)}
            </h3>

            <p>
                ${escapeHTML(message)}
            </p>

        </div>

    `;

}


// =====================================================
// GET INITIAL
// =====================================================

function getInitial(
    name
) {

    if (!name) {

        return "C";

    }


    return String(name)
        .trim()
        .charAt(0)
        .toUpperCase();

}


// =====================================================
// ESCAPE HTML
// =====================================================

function escapeHTML(
    value
) {

    const div =
        document.createElement("div");

    div.textContent =
        value;

    return div.innerHTML;

}


// =====================================================
// CLOSE MODAL
// =====================================================

function closeModal() {

    const modal =
        document.getElementById(
            "dataModal"
        );

    if (modal) {

        modal.style.display =
            "none";

    }

}


// =====================================================
// CLOSE MODAL OUTSIDE CLICK
// =====================================================

window.addEventListener(
    "click",
    function (event) {

        const modal =
            document.getElementById(
                "dataModal"
            );

        if (
            modal &&
            event.target === modal
        ) {

            closeModal();

        }

    }
);