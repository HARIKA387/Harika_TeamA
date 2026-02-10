// Make sure JS is loaded
console.log("register.js loaded");

// Wait for DOM to load
document.addEventListener("DOMContentLoaded", function() {
  console.log("DOM loaded - attaching event listeners");
  
  // Register button
  const registerBtn = document.getElementById("registerBtn");
  if (registerBtn) {
    registerBtn.addEventListener("click", function () {
      console.log("Register button clicked");
      
      const name = document.getElementById("name").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      const language = document.getElementById("language").value;

      if (!name || !email || !password || !language) {
        alert("❌ Please fill all fields");
        return;
      }

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        alert("❌ Please enter a valid email");
        return;
      }

      // Validate password length
      if (password.length < 6) {
        alert("❌ Password must be at least 6 characters");
        return;
      }

      const data = {
        name: name,
        email: email,
        password: password,
        language: language
      };

      console.log("Registration data:", data);
      alert("✅ Registration successful! Name: " + name);
      
      // Clear form
      document.getElementById("name").value = "";
      document.getElementById("email").value = "";
      document.getElementById("password").value = "";
      document.getElementById("language").value = "";
    });
  } else {
    console.error("Register button not found");
  }

  // Login link
  const loginBtn = document.getElementById("loginBtn");
  if (loginBtn) {
    loginBtn.addEventListener("click", function () {
      console.log("Login link clicked");
      alert("✅ Redirecting to login page...");
      window.location.href = "login.html";
    });
  } else {
    console.error("Login button not found");
  }
});
