function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.querySelector(".openbtn").style.display = "block"; 
}

function toggleNav() {
    var sidebar = document.getElementById("mySidebar");
    var mainContent = document.getElementById("main");
    var button = document.querySelector(".openbtn");
    if (sidebar.style.width === "250px") {
        sidebar.style.width = "0";
        mainContent.style.marginLeft = "0";
    } else {
        sidebar.style.width = "250px";
        mainContent.style.marginLeft = "250px";
        button.style.display = "none";
    }
}
