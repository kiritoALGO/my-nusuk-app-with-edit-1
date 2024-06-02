document.addEventListener("DOMContentLoaded", function() {
    // Select all card elements
    var cards = document.querySelectorAll(".card");

    // Add event listener to each card
    cards.forEach(function(card) {
        card.addEventListener("click", function() {
            // Retrieve the customer ID from the data attribute
            var customerId = this.getAttribute("data-customer-id");
            
            // Redirect to the customer detail page with the customer ID
            window.location.href = `/customer/get/${customerId}/`;
        });
    });
});
