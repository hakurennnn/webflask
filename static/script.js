function toggleDescription(event) {
    event.preventDefault();
    var description = document.getElementById("app-description");
    if (description) {
        if (description.style.opacity === "" || description.style.opacity === "0") {
            fadeIn(description);
        } else {
            description.style.opacity = "0";
        }
    }
}

function fadeIn(element) {
    var opacity = 0;
    element.style.opacity = "0";
    element.style.display = "block";
    var fadeInInterval = setInterval(function() {
        if (opacity < 1) {
            opacity += 0.1;
            element.style.opacity = opacity;
        } else {
            clearInterval(fadeInInterval);
        }
    }, 50);
}

var homeButton = document.getElementById("home-button");
if (homeButton) {
    homeButton.addEventListener("click", toggleDescription);
}
