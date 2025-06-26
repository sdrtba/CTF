document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;
  const error = document.querySelector("#error");

  if (path === "/login") {
    const form = document.querySelector("form");
    if (form) {
      form.addEventListener("submit", (e) => handleLogin(e, error));
    }
    checkToken();
  }

  if (path === "/register") {
    const form = document.querySelector("form");
    if (form) {
      form.addEventListener("submit", handleRegister);
    }
  }

  if (path === "/profile") {
    loadProfile();
    const logoutBtn = document.querySelector("#logout");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", logout);
    }
  }
});

function checkToken() {
  const token = localStorage.getItem("token");
  if (token) {
    window.location.href = "/profile";
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/";
}

async function handleLogin(e, error) {
  console.log(error);
  e.preventDefault();
  const username = document.querySelector("#username").value;
  const password = document.querySelector("#password").value;

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok && data.token) {
      localStorage.setItem("token", data.token);
      window.location.href = "/profile";
    } else {
      error.textContent = "Error: " + (data.error || "Unknown");
      error.style.display = "block";
    }
  } catch (err) {
      error.textContent = "Connection error";
      error.style.display = "block";
  }
}

async function handleRegister(e) {
  e.preventDefault();
  const username = document.querySelector("#username").value;
  const password = document.querySelector("#password").value;

  try {
    const res = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (data.error) {
      error.textContent = data.message || data.error;
      error.style.display = "block";
    }
    if (res.ok) {
      window.location.href = "/login";
    }
  } catch (err) {
    error.textContent = "Connection error";
    error.style.display = "block";
  }
}

async function loadProfile() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "/login";
    return;
  }

  try {
    const res = await fetch("/api/profile", {
      headers: { Authorization: "Bearer " + token }
    });

    const data = await res.json();

    if (res.ok) {
      const profile = document.querySelector("#profile");
      if (profile) {
        profile.innerText = data.note;
      }
    } else {
      alert("Access denied: " + data.error);
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
  } catch (err) {
    alert("Connection error");
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
}
