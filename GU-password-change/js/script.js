document.getElementById('passwordChangeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Basic validation
    if (newPassword !== confirmPassword) {
        alert('New passwords do not match');
        return;
    }

    // Create submission data
    const timestamp = new Date().toISOString();
    const data = {
        timestamp,
        email,
        currentPassword,
        newPassword
    };

    // Create and download file
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `password-change-${timestamp}.json`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    // Redirect to success page
    window.location.href = 'success.html';
});