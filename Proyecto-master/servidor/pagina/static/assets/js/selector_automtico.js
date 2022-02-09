var sidebar = document.getElementById('sidebar-item1')
var sidebar2 = document.getElementById('sidebar-item2')
if (window.location.pathname == '/pagina/index.html') {
    sidebar.className += ' active'
} else if(window.location.pathname == '/pagina/buscar') {
    sidebar2.className += ' active'
}