
// const mypage = document.getElementsByTagName("body"); 

window.onload = function () {
  
  var dropMenuTrigger = document.getElementById("dropdownNavbarLink");
  var dropMenuTarget = document.getElementById("dropdownNavbar");
  var mainMenuTrigger = document.getElementById("mainMenuTrigger");
  var mainMenuTarget = document.getElementById("navbar-dropdown");
  var hamburgerMenu = document.getElementById("hamburger");
  
  if (dropMenuTrigger!==null){
    dropMenuTrigger.onclick = function(event) {
    // console.log("Link clicked")
    dropMenuTarget.classList.toggle("hidden")
    }
  }
  
  mainMenuTrigger.onclick = function(event) {
    // console.log("Link clicked")
    mainMenuTarget.classList.toggle("hidden")
  }

  // Close the dropdown if the user clicks outside of it
  window.onclick = function(event) {
  if ((!(event.target.matches('#dropdownNavbarLink')||event.target.matches('#dropdownNavbarLinkArrow')))) 
    {
        // console.log("Clicked Elsewhere")
        if (dropMenuTarget!==null){
          if (!(dropMenuTarget.classList.contains('hidden'))) {
            // console.log("Clicked")  
            dropMenuTarget.classList.add('hidden');
          }
        }
      }
    if ((!(event.target.matches('#navbar-dropdown')
          ||event.target.matches('#mainMenuTrigger')
          ||event.target.matches('#hamburger')
          ||event.target.matches('#dropdownNavbarLink')
          ||event.target.matches('#dropdownNavbarLinkArrow'))))
      {
        if (!(mainMenuTarget.classList.contains('hidden'))) {
          mainMenuTarget.classList.add('hidden');
        }
      }
    // if (event.target.matches('#dropdownNavbarLink')){
    //   console.log("Navbar Clicked!")
    // }
  }
}




//  /* When the user clicks on the button,
//  toggle between hiding and showing the dropdown content */
// function myFunction() {
//   document.getElementById("myDropdown").classList.toggle("show");
// }

// //Close the dropdown menu if the user clicks outside of it
// window.onclick = function(event) {
//   if (!event.target.matches('.dropbtn')) {
//     var dropdowns = document.getElementsByClassName("dropdown-content");
//     var i;
//     for (i = 0; i < dropdowns.length; i++) {
//       var openDropdown = dropdowns[i];
//       if (openDropdown.classList.contains('show')) {
//         openDropdown.classList.remove('show');
//       }
//     }
//   }
// }