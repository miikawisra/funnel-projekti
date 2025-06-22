const form = document.getElementById("newsletter-form");
const responseMsg = document.getElementById("response");

form.addEventListener("submit", function (event) {
  event.preventDefault();

  const email = document.getElementById("email").value;

  fetch("/subscribe", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email: email })
  })
    .then(res => res.text())
    .then(data => {
      responseMsg.textContent = data;
      form.reset();
    })
    .catch(() => {
      responseMsg.textContent = "Virhe palvelimessa.";
    });
});