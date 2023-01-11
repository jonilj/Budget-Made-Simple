// Adds current year to the footer
function showYear() {
  const year = new Date().getFullYear()

  // If year is 2022, don't show anything additional
  if (year == "2022") {
    document.getElementById("showYear").innerHTML = "";
  }
  else {
    document.getElementById("showYear").innerHTML = year;
  }
}