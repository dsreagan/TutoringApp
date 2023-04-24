/*!
 * Start Bootstrap - Agency v7.0.11 (https://startbootstrap.com/theme/agency)
 * Copyright 2013-2022 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
 */
//
// Scripts
//

window.addEventListener("DOMContentLoaded", (event) => {
  // Navbar shrink function
  var navbarShrink = function () {
    const navbarCollapsible = document.body.querySelector("#mainNav");
    if (!navbarCollapsible) {
      return;
    }
    if (window.scrollY === 0) {
      navbarCollapsible.classList.remove("navbar-shrink");
    } else {
      navbarCollapsible.classList.add("navbar-shrink");
    }
  };

  // Shrink the navbar
  navbarShrink();

  // Shrink the navbar when page is scrolled
  document.addEventListener("scroll", navbarShrink);

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.body.querySelector("#mainNav");
  if (mainNav) {
    new bootstrap.ScrollSpy(document.body, {
      target: "#mainNav",
      offset: 74,
    });
  }

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector(".navbar-toggler");
  const responsiveNavItems = [].slice.call(document.querySelectorAll("#navbarResponsive .nav-link"));
  responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener("click", () => {
      if (window.getComputedStyle(navbarToggler).display !== "none") {
        navbarToggler.click();
      }
    });
  });
});

// Tutor registration disable display functions
var enableSunday = function () {
  var sundayCheck = document.getElementById("sundayCheck");
  var sundayBegin = document.getElementById("sundayBegin");
  var sundayEnd = document.getElementById("sundayEnd");
  if (sundayCheck.checked) {
    sundayBegin.removeAttribute("disabled");
    sundayEnd.removeAttribute("disabled");
  } else {
    sundayBegin.disabled = "true";
    sundayEnd.disabled = "true";
  }
};
var enableMonday = function () {
  var mondayCheck = document.getElementById("mondayCheck");
  var mondayBegin = document.getElementById("mondayBegin");
  var mondayEnd = document.getElementById("mondayEnd");
  if (mondayCheck.checked) {
    mondayBegin.removeAttribute("disabled");
    mondayEnd.removeAttribute("disabled");
  } else {
    mondayBegin.disabled = "true";
    mondayEnd.disabled = "true";
  }
};
var enableTuesday = function () {
  var tuesdayCheck = document.getElementById("tuesdayCheck");
  var tuesdayBegin = document.getElementById("tuesdayBegin");
  var tuesdayEnd = document.getElementById("tuesdayEnd");
  if (tuesdayCheck.checked) {
    tuesdayBegin.removeAttribute("disabled");
    tuesdayEnd.removeAttribute("disabled");
  } else {
    tuesdayBegin.disabled = "true";
    tuesdayEnd.disabled = "true";
  }
};
var enableWednesday = function () {
  var wednesdayCheck = document.getElementById("wednesdayCheck");
  var wednesdayBegin = document.getElementById("wednesdayBegin");
  var wednesdayEnd = document.getElementById("wednesdayEnd");
  if (wednesdayCheck.checked) {
    wednesdayBegin.removeAttribute("disabled");
    wednesdayEnd.removeAttribute("disabled");
  } else {
    wednesdayBegin.disabled = "true";
    wednesdayEnd.disabled = "true";
  }
};
var enableThursday = function () {
  var thursdayCheck = document.getElementById("thursdayCheck");
  var thursdayBegin = document.getElementById("thursdayBegin");
  var thursdayEnd = document.getElementById("thursdayEnd");
  if (thursdayCheck.checked) {
    thursdayBegin.removeAttribute("disabled");
    thursdayEnd.removeAttribute("disabled");
  } else {
    thursdayBegin.disabled = "true";
    thursdayEnd.disabled = "true";
  }
};
var enableFriday = function () {
  var fridayCheck = document.getElementById("fridayCheck");
  var fridayBegin = document.getElementById("fridayBegin");
  var fridayEnd = document.getElementById("fridayEnd");
  if (fridayCheck.checked) {
    fridayBegin.removeAttribute("disabled");
    fridayEnd.removeAttribute("disabled");
  } else {
    fridayBegin.disabled = "true";
    fridayEnd.disabled = "true";
  }
};
var enableSaturday = function () {
  var saturdayCheck = document.getElementById("saturdayCheck");
  var saturdayBegin = document.getElementById("saturdayBegin");
  var saturdayEnd = document.getElementById("saturdayEnd");
  if (saturdayCheck.checked) {
    saturdayBegin.removeAttribute("disabled");
    saturdayEnd.removeAttribute("disabled");
  } else {
    saturdayBegin.disabled = "true";
    saturdayEnd.disabled = "true";
  }
};

var validateStudent = function () {
  var password = document.getElementById("studentPassword");
  var upper = document.getElementById("upperCheckS");
  var number = document.getElementById("numberCheckS");
  var special = document.getElementById("specialCheckS");

  if (password.value.match(/[0-9]/)) {
    number.style.color = "green";
  } else {
    number.style.color = "red";
  }

  if (password.value.match(/[A-Z]/)) {
    upper.style.color = "green";
  } else {
    upper.style.color = "red";
  }

  if (password.value.match(/[!\@\#\$\%\^\&\*\(\)]/)) {
    special.style.color = "green";
  } else {
    special.style.color = "red";
  }
};

var validateTutor = function () {
  var password = document.getElementById("tutorPassword");
  var upper = document.getElementById("upperCheckT");
  var number = document.getElementById("numberCheckT");
  var special = document.getElementById("specialCheckT");

  if (password.value.match(/[0-9]/)) {
    number.style.color = "green";
  } else {
    number.style.color = "red";
  }

  if (password.value.match(/[A-Z]/)) {
    upper.style.color = "green";
  } else {
    upper.style.color = "red";
  }

  if (password.value.match(/[!\@\#\$\%\^\&\*\(\)]/)) {
    special.style.color = "green";
  } else {
    special.style.color = "red";
  }
};
