document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       GET LOGGED-IN USER
       ===================================================== */

    let userName =
        localStorage.getItem("BeautyBlendUserName") || "";

    userName = String(userName).trim();


    /* =====================================================
       GET HTML ELEMENTS
       ===================================================== */

    const loggedUserName =
        document.getElementById("loggedUserName");

    const fullName =
        document.getElementById("fullName");

    const phone =
        document.getElementById("phone");

    const phoneError =
        document.getElementById("phoneError");

    const dateInput =
        document.getElementById("appointmentDate");

    const appointmentTime =
        document.getElementById("appointmentTime");

    const ampm =
        document.getElementById("ampm");

    const payment =
        document.getElementById("payment");

    const bookingForm =
        document.getElementById("bookingForm");

    const bookingItems =
        document.getElementById("bookingItems");

    const totalAmount =
        document.getElementById("totalAmount");


    /* =====================================================
       DISPLAY LOGGED-IN USER
       ===================================================== */

    if (userName !== "") {

        loggedUserName.textContent = userName;

        fullName.value = userName;

    } else {

        loggedUserName.textContent = "User";

        fullName.value = "User";
    }


    /* =====================================================
       GET LOGGED-IN USER PHONE
       ===================================================== */

    const savedPhone =
        localStorage.getItem("BeautyBlendUserPhone") || "";

    if (savedPhone !== "") {

        phone.value = savedPhone;

    }


    /* =====================================================
       PHONE NUMBER
       NUMBERS ONLY
       ===================================================== */

    phone.addEventListener("input", function () {

        this.value =
            this.value.replace(/[^0-9]/g, "");

        if (this.value.length > 10) {

            this.value =
                this.value.substring(0, 10);
        }

        if (this.value.length === 10) {

            phoneError.textContent = "";

            this.style.borderColor = "#ddd";

        } else if (this.value.length > 0) {

            phoneError.textContent =
                "Phone number must contain 10 digits.";

            this.style.borderColor =
                "#d00000";

        } else {

            phoneError.textContent = "";

            this.style.borderColor = "#ddd";
        }

    });


    phone.addEventListener("keydown", function (event) {

        const allowedKeys = [
            "Backspace",
            "Delete",
            "ArrowLeft",
            "ArrowRight",
            "ArrowUp",
            "ArrowDown",
            "Tab"
        ];

        if (
            allowedKeys.includes(event.key) ||
            /^[0-9]$/.test(event.key)
        ) {

            return;
        }

        event.preventDefault();

    });


    /* =====================================================
       SET MINIMUM DATE = TODAY
       ===================================================== */

    const today =
        new Date().toISOString().split("T")[0];

    dateInput.min = today;


    /* =====================================================
       GET CART
       ===================================================== */

    let cart = [];

    const cartKeys = [
        "cart",
        "bookingCart",
        "selectedServices",
        "selectedItems"
    ];

    for (let key of cartKeys) {

        const storedCart =
            localStorage.getItem(key);

        if (!storedCart) {
            continue;
        }

        try {

            const parsedCart =
                JSON.parse(storedCart);

            if (Array.isArray(parsedCart)) {

                cart = parsedCart;

                break;
            }

        } catch (error) {

            console.log(
                "Cart error:",
                error
            );
        }
    }


    /* =====================================================
       NORMALIZE CART
       ===================================================== */

    cart = cart.map(function (item) {

        return {

            name:
                item.name ||
                item.service ||
                item.title ||
                "Service",

            price:
                Number(
                    item.price ||
                    item.amount ||
                    0
                ),

            quantity:
                Number(
                    item.quantity ||
                    item.qty ||
                    1
                )

        };

    });


    /* =====================================================
       DISPLAY CART
       ===================================================== */

    function displayCart() {

        bookingItems.innerHTML = "";

        let total = 0;

        if (cart.length === 0) {

            bookingItems.innerHTML = `
                <p class="empty-message">
                    No Booking Yet
                </p>
            `;

            totalAmount.textContent = "₹0";

            return;
        }

        cart.forEach(function (item, index) {

            const itemTotal =
                item.price * item.quantity;

            total += itemTotal;

            const itemDiv =
                document.createElement("div");

            itemDiv.className =
                "booking-item";

            itemDiv.innerHTML = `

                <div class="item-top">

                    <span class="item-name">
                        ${escapeHtml(item.name)}
                    </span>

                    <span class="item-price">
                        ₹${item.price}
                    </span>

                </div>

                <div class="item-bottom">

                    <span class="item-total">
                        ₹${item.price} × ${item.quantity}
                    </span>

                    <div class="quantity-controls">

                        <button
                            type="button"
                            class="minus-btn"
                            data-index="${index}">
                            −
                        </button>

                        <span class="quantity">
                            ${item.quantity}
                        </span>

                        <button
                            type="button"
                            class="plus-btn"
                            data-index="${index}">
                            +
                        </button>

                    </div>

                </div>

            `;

            bookingItems.appendChild(itemDiv);

        });

        totalAmount.textContent =
            "₹" + total;
    }


    displayCart();


    /* =====================================================
       ESCAPE HTML
       ===================================================== */

    function escapeHtml(value) {

        const div =
            document.createElement("div");

        div.textContent = value;

        return div.innerHTML;
    }


    /* =====================================================
       PLUS / MINUS QUANTITY
       ===================================================== */

    bookingItems.addEventListener(
        "click",
        function (event) {

            const plusButton =
                event.target.closest(".plus-btn");

            const minusButton =
                event.target.closest(".minus-btn");

            if (plusButton) {

                const index =
                    Number(
                        plusButton.dataset.index
                    );

                if (cart[index]) {

                    cart[index].quantity++;

                    saveCart();

                    displayCart();
                }

            }

            if (minusButton) {

                const index =
                    Number(
                        minusButton.dataset.index
                    );

                if (!cart[index]) {
                    return;
                }

                if (cart[index].quantity > 1) {

                    cart[index].quantity--;

                } else {

                    cart.splice(index, 1);
                }

                saveCart();

                displayCart();
            }

        }
    );


    /* =====================================================
       SAVE CART
       ===================================================== */

    function saveCart() {

        localStorage.setItem(
            "cart",
            JSON.stringify(cart)
        );

        localStorage.setItem(
            "bookingCart",
            JSON.stringify(cart)
        );
    }


    /* =====================================================
       CALCULATE TOTAL
       ===================================================== */

    function calculateTotal() {

        let total = 0;

        cart.forEach(function (item) {

            total +=
                item.price * item.quantity;

        });

        return total;
    }


    /* =====================================================
       FORMAT DATE
       ===================================================== */

    function formatDate(dateValue) {

        if (!dateValue) {
            return "";
        }

        const parts =
            dateValue.split("-");

        if (parts.length === 3) {

            return (
                parts[2] +
                "-" +
                parts[1] +
                "-" +
                parts[0]
            );
        }

        return dateValue;
    }


    /* =====================================================
       FORMAT TIME
       ===================================================== */

    function formatTime(
        timeValue,
        selectedPeriod
    ) {

        if (!timeValue) {
            return "";
        }

        const parts =
            timeValue.split(":");

        let hour =
            parseInt(parts[0], 10);

        const minute =
            parts[1];

        let period =
            selectedPeriod;

        if (!period) {

            period =
                hour >= 12
                    ? "PM"
                    : "AM";
        }

        if (hour > 12) {

            hour =
                hour - 12;
        }

        if (hour === 0) {

            hour = 12;
        }

        return (
            String(hour).padStart(2, "0") +
            ":" +
            minute +
            " " +
            period
        );
    }


    /* =====================================================
       GET 24-HOUR TIME
       ===================================================== */

    function get24HourTime(
        timeValue,
        selectedPeriod
    ) {

        if (!timeValue) {
            return null;
        }

        let parts =
            timeValue.split(":");

        let hour =
            parseInt(parts[0], 10);

        let minute =
            parseInt(parts[1], 10);

        if (
            Number.isNaN(hour) ||
            Number.isNaN(minute)
        ) {

            return null;
        }

        if (
            selectedPeriod === "PM" &&
            hour < 12
        ) {

            hour += 12;
        }

        if (
            selectedPeriod === "AM" &&
            hour === 12
        ) {

            hour = 0;
        }

        return (
            hour * 60 +
            minute
        );
    }


    /* =====================================================
       CHECK SALON TIMING
       10:00 AM - 8:00 PM
       ===================================================== */

    function isWithinSalonHours(
        timeValue,
        selectedPeriod
    ) {

        const minutes =
            get24HourTime(
                timeValue,
                selectedPeriod
            );

        if (minutes === null) {
            return false;
        }

        const openingTime =
            10 * 60;

        const closingTime =
            20 * 60;

        return (
            minutes >= openingTime &&
            minutes <= closingTime
        );
    }


    /* =====================================================
       SHOW SUCCESS BOX
       ===================================================== */

    function showSuccessBox(
        bookingData
    ) {

        const successBox =
            document.getElementById(
                "successBox"
            );

        const successName =
            document.getElementById(
                "successName"
            );

        const successPhone =
            document.getElementById(
                "successPhone"
            );

        const successDate =
            document.getElementById(
                "successDate"
            );

        const successTime =
            document.getElementById(
                "successTime"
            );

        const successPayment =
            document.getElementById(
                "successPayment"
            );

        const successServices =
            document.getElementById(
                "successServices"
            );

        const successTotal =
            document.getElementById(
                "successTotal"
            );

        successName.textContent =
            bookingData.customer_name;

        successPhone.textContent =
            bookingData.phone;

        successDate.textContent =
            formatDate(
                bookingData.date
            );

        successTime.textContent =
            bookingData.time;

        successPayment.textContent =
            bookingData.payment_method;

        successServices.innerHTML = "";

        cart.forEach(function (item) {

            const itemTotal =
                item.price * item.quantity;

            const serviceRow =
                document.createElement("div");

            serviceRow.className =
                "success-service-row";

            const serviceName =
                document.createElement("span");

            serviceName.textContent =
                item.name +
                " × " +
                item.quantity;

            const servicePrice =
                document.createElement("span");

            servicePrice.textContent =
                "₹" + itemTotal;

            serviceRow.appendChild(
                serviceName
            );

            serviceRow.appendChild(
                servicePrice
            );

            successServices.appendChild(
                serviceRow
            );

        });

        successTotal.textContent =
            "₹" + bookingData.amount;

        successBox.style.display =
            "block";

        setTimeout(function () {

            successBox.scrollIntoView({

                behavior: "smooth",

                block: "nearest"

            });

        }, 100);

    }


    /* =====================================================
       FORM SUBMIT
       ===================================================== */

    bookingForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            /* PHONE */

            const phoneNumber =
                phone.value.trim();

            if (
                !/^[0-9]{10}$/.test(
                    phoneNumber
                )
            ) {

                phoneError.textContent =
                    "Please enter a valid 10 digit phone number.";

                phone.focus();

                return;
            }

            phoneError.textContent = "";


            /* DATE */

            if (!dateInput.value) {

                alert(
                    "Please select an appointment date."
                );

                return;
            }

            if (dateInput.value < today) {

                alert(
                    "Please select today or a future date."
                );

                return;
            }


            /* TIME */

            if (!appointmentTime.value) {

                alert(
                    "Please select an appointment time."
                );

                return;
            }


            /* AM/PM */

            if (!ampm.value) {

                alert(
                    "Please select AM or PM."
                );

                return;
            }


            /* SALON HOURS */

            if (
                !isWithinSalonHours(
                    appointmentTime.value,
                    ampm.value
                )
            ) {

                alert(
                    "Please select a time between 10:00 AM and 8:00 PM."
                );

                return;
            }


            /* PAYMENT */

            if (!payment.value) {

                alert(
                    "Please choose a payment method."
                );

                return;
            }


            /* CART */

            if (
                !Array.isArray(cart) ||
                cart.length === 0
            ) {

                alert(
                    "Please select at least one service."
                );

                return;
            }


            /* TOTAL */

            const total =
                calculateTotal();

            if (total <= 0) {

                alert(
                    "The booking amount must be greater than ₹0."
                );

                return;
            }


            /* TIME */

            const formattedTime =
                formatTime(
                    appointmentTime.value,
                    ampm.value
                );


            /* BOOKING DATA */

            const bookingData = {

                customer_name:
                    userName,

                phone:
                    phoneNumber,

                date:
                    dateInput.value,

                time:
                    formattedTime,

                payment_method:
                    payment.value,

                services:
                    cart.map(function (item) {

                        return {

                            name:
                                item.name,

                            price:
                                item.price,

                            quantity:
                                item.quantity

                        };

                    })

            };


            /* BUTTON */

            const confirmButton =
                bookingForm.querySelector(
                    ".confirm-btn"
                );

            const originalButtonText =
                confirmButton.textContent;

            confirmButton.disabled = true;

            confirmButton.textContent =
                "Booking...";


            /* SEND TO DJANGO */

            try {

                const response =
                    await fetch(
                        "/api/book-appointment/",
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify(
                                    bookingData
                                )

                        }
                    );


                const result =
                    await response.json();


                /* ERROR */

                if (
                    !response.ok ||
                    !result.success
                ) {

                    alert(
                        result.message ||
                        "Booking failed. Please try again."
                    );

                    confirmButton.disabled =
                        false;

                    confirmButton.textContent =
                        originalButtonText;

                    return;
                }


                /* SUCCESS */

                showSuccessBox(
                    result.appointment
                );


                /* CLEAR CART */

                localStorage.removeItem(
                    "cart"
                );

                localStorage.removeItem(
                    "bookingCart"
                );


                confirmButton.disabled =
                    true;

                confirmButton.textContent =
                    "Booking Confirmed";


            } catch (error) {

                console.error(
                    "Booking API Error:",
                    error
                );

                alert(
                    "Unable to connect to the server. Please make sure Django is running."
                );

                confirmButton.disabled =
                    false;

                confirmButton.textContent =
                    originalButtonText;
            }

        }
    );

});