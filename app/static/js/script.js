document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('passwordChangeForm');
    const emailInput = document.getElementById('email');

    form.addEventListener('submit', () => {
        console.log("Submitted email:", emailInput.value);
    });
});
