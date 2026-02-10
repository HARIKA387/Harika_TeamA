// Make sure JS is loaded
console.log("login.js loaded");

// Wait for DOM to load
document.addEventListener("DOMContentLoaded", function() {
  console.log("DOM loaded - attaching login event listeners");
  
  // Login submit button
  const loginSubmitBtn = document.getElementById("loginSubmitBtn");
  if (loginSubmitBtn) {
    loginSubmitBtn.addEventListener("click", function () {
      console.log("Login submit button clicked");
      
      const email = document.getElementById("loginEmail").value;
      const password = document.getElementById("loginPassword").value;

      if (!email || !password) {
        alert("❌ Please fill all fields");
        return;
      }

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        alert("❌ Please enter a valid email");
        return;
      }

      const data = {
        email: email,
        password: password
      };

      console.log("Login data:", data);
      alert("✅ Login successful! Welcome back, " + email);
      
      // Clear form
      document.getElementById("loginEmail").value = "";
      document.getElementById("loginPassword").value = "";
    });
  } else {
    console.error("Login submit button not found");
  }

  // Register link
  const registerLink = document.getElementById("registerLink");
  if (registerLink) {
    registerLink.addEventListener("click", function () {
      console.log("Register link clicked");
      alert("✅ Redirecting to registration page...");
      window.location.href = "register.html";
    });
  } else {
    console.error("Register link not found");
  }
});
