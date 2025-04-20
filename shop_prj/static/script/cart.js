function getCSRFToken(){
    let csrfToken = null;
    document.cookie.split(";").forEach(cookie=>{
        let [key, value] = cookie.trim().split("=");
        if (key === "csrftoken"){
            csrfToken = value;
        }
    });
    console.log("CSRF Token:", csrfToken);
    return csrfToken
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".update-cart-form").forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            let productId = this.dataset.productId;
            let amount = this.querySelector("input[name='amount']").value;
            let csrfToken = getCSRFToken();

            fetch(`/update_cart/${productId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrfToken
                },
                body: `amount=${amount}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        });
    });
});
