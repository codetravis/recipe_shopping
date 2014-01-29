

function addIngredient()
{
    var list = document.getElementById('ingredient_list');
    var current_html = list.innerHTML;
    list.innerHTML = current_html + "item<br/>";
}

window.onload = function() {
document.getElementById('add_ingredient').onclick = addIngredient;
}
