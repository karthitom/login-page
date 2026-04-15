<script>
    function convertToRot3() {
        const password = document.getElementById('password').value;
        const output = document.getElementById('rot3-output');
        
        let rot3Result = "";

        for (let i = 0; i < password.length; i++) {
            let charCode = password.charCodeAt(i);

            // For Uppercase (A-Z)
            if (charCode >= 65 && charCode <= 90) {
                rot3Result += String.fromCharCode(((charCode - 65 + 3) % 26) + 65);
            }
            // For Lowercase (a-z)
            else if (charCode >= 97 && charCode <= 122) {
                rot3Result += String.fromCharCode(((charCode - 97 + 3) % 26) + 97);
            }
            // For Numbers or other characters (no change)
            else {
                rot3Result += password[i];
            }
        }

        output.innerText = rot3Result || "...";
    }
</script>
</body>
</html>